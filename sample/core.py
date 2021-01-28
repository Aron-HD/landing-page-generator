import pandas as pd
import logging as log  # time # comment this once get_csv moved?
from glob import glob
from pathlib import Path

import dictionary as AWARDS
from helpers import Functions as func

# Jinja Imports
from jinja2 import Environment, FileSystemLoader
env = Environment(
    loader=FileSystemLoader('../templates'))

# CLI / GUI Inputs
values = {}
try:
    values['date'] = '01/01/2021'
    values['page'] = list(
        input("enter page ('special' 'body' 'category_hero'): ").strip().split(' '))
    values['open'] = True # effects whether to display registration, deadline, entry links
    values['award'] = input('award: ')
    # make this able to pass in a list of cats too
    values['cat'] = list(input("enter category: ").strip().split(' '))
    values['entry_kit'] = "MENAPrize2021-entrykit.pdf"
    values['report_link'] = "/content/article/2020-mena-strategy-report-insights-from-the-warc-prize-for-mena-strategy/133904"
    values['report_image'] = '../winner-2020.jpg'
except KeyError as e:
    print('invalid key input lists separated by spaces', e)
    raise SystemExit

# init as class
data = {}


def get_csv(cat, page):  # swap page for path
    '''Reads in csv data for shortlist, winners or judges.'''
    log.debug('reading csv')
    try:
        pg = page.replace('preview-', '').replace('_bios', '') # strip other tags
        path = {  # pass in path object in respective functions when class
            'shortlist': f'../data/csv/shortlists/{cat}_shortlist.csv',
            'winners': f'../data/csv/{cat}_winners.csv',
            'judges': f'../data/csv/{cat}-judges.csv'
        }
        df = pd.read_csv(path[pg])
        return df.to_dict('records')
    except UnicodeError:
        df = pd.read_csv(path[pg], encoding='cp1252')
        return df.to_dict('records')
    except KeyError:
        log.debug('no csv read')
        return False


def get_data(date, page, award, category):

    # init as class common ones have rest as functions
    # date = values['date']
    award = values['award']
    # category = values['cat']
    # page = values['page']
    
    data.update({	                               # get each elmt using awd_elmt() from AWARDS dictionary
        "award":       award,                      # and take input from gui window / cli and feed into temporary
        "cat":         category,                   # data dictionary for rendering template
        # should shrink this to just get date from now
        "year":        func.process_date(date)[2],
        page:         func.awd_elmt(award, category, page),
        "code":        AWARDS[award]['code'],
        "cartridge":   AWARDS[award]['cartridge'],
        "entry_kit":   values['entry_kit'],
        "report":      AWARDS[award]['categories'][category]['report'],
        "report_link": values['report_link'],
        "full_award":  AWARDS[award]['full_award'],
        "special_awards": AWARDS[award]['categories'][category]['special_awards'],
    })

    placeholder = "Pariatur exercitation qui aute eu veniam cillum ea excepteur sint. Sint tempor ea irure veniam proident ut pariatur consequat duis voluptate incididunt amet laborum reprehenderit aute dolore tempor nostrud anim magna adipisicing in ut et reprehenderit exercitation mollit in."
    # function only for when needed (category hero)
    data.update({
        "full_category": AWARDS[award]['categories'][category]['full_category'],
        "category_description": AWARDS[award]['categories'][category]['body_copy'].split(".")[0],
        "report_image": values['report_image']
    })

    # function for (body copy)
    # data.update({"body_copy": placeholder})
    data.update({"body_copy": AWARDS[award]
                 ['categories'][category]['body_copy']})
    # {papers / judges / winners / shortlist}
    # have each as individual function on GUI /
    # if radio input is true then get_csv that thing
    # get_csv(cat, page) if value for value in values True else pass
    # so that only necessary info is added to dict
    data.update({"papers": get_csv(category, page)})
    
    if 'judges' in page:
        data.update({"judges": get_csv(category, page)})
        print('Panel chair:\n', data['judges'][0]['Name'], data['judges'][0]['Surname'])

    if 'entry' in page:
        entry_form = AWARDS[award]['prize'] + data['year'] + '-entryform.docx'
        data.update({"entry_form": entry_form, "open": values['open']})
    
    if 'entry' or 'about' in page:
        deadline = input('Deadline for entries?: ')
        data.update({"deadline": deadline})

    return data


def write_html(filename, output):
    with open(filename, "w") as f:
        f.write(output)
    print("Wrote -->", filename)


# make this a class LandingPage: that imports from package /template_data with helpers in too
def get_html(date, page, award, category):
    '''Returns a filename, its output content and its page element code.'''
    try:
        d = get_data(date, page, award, category)
        yr = d['year']
        elmt = func.awd_elmt(
            page=page,
            award=award,
            category=category
        )
        # bring these functions into class
        fn = func.save_name(page, award, category, yr, elmt)

        # tpl.render
        out = env.get_template(f'{page}.html').render(d=d, page=page)
        return fn, out, elmt
    except Exception as e:
        raise e


def update_page(assets):
    log.info('\nselected write files to CMS...')
    from cmsbot.cmsbot import CMSBot  # import here so only if selected?
    try:
        cms = CMSBot()
        for name, page_element, content in assets:
            log.info("- updating ->", name)
            cms.edit_page(page_element)
            cms.paste_content(content)
            cms.save_changes()
        log.info('# updates complete')

    except Exception as e:
        raise e
    finally:
        cms.bot.quit()

# have this as runner file with classes and GUI/frontend as packages


def main():

    date = values['date']
    award = values['award']
    written_assets = []

    for page in values['page']:
        for category in values['cat']:
            file, output, element = get_html(date, page, award, category)
            write_html(file, output)
            fname = Path(file).name
            written_assets.append((fname, element, output))

    # log.info("\nfiles written:\n")
    # [log.info(f) for f, e, o in written_assets]
    string = f"\nupdate CMS articles with each file's content?\n\t- select 'Y' or 'N': "
    select = input(string).casefold()

    if select != 'y':
        return False
    else:
        update_page(written_assets)

# def main1():

# 	for f in glob(r"../templates/*.html"):
# 		log.info(f)
# 		for line in f:
# 			tag = line.find(r'{{')
# 			log.info(tag)


if __name__ == '__main__':
    main()
