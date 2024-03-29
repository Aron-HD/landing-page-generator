import pandas as pd
import logging as log  # time # comment this once get_csv moved?
from glob import glob
from pathlib import Path

from frontend.gui import return_values
from dictionary import AWARDS
from helpers import Functions as func

# Jinja Imports
from jinja2 import Environment, FileSystemLoader
env = Environment(
    loader=FileSystemLoader('../templates'))

log.basicConfig(filename='log.log', level=log.DEBUG)

# get values from gui
try:
    values = return_values()
except KeyError as e:
    log.warning('invalid key input lists separated by spaces', e)
    raise SystemExit

# init as class
data = {}


def get_csv(cat, page):  # swap page for path
    '''Reads in csv data for shortlist, winners or judges.'''
    replacements = [
        'preview-',
        '_bios',
        '_split',
        '_headshots'
    ]
    try:
        for item in replacements:
            page = page.replace(item, '')

        base = '../data/csv'
        path = {  # pass in path object in respective functions when class
            'shortlist': f'{base}/shortlists/{cat}_shortlist.csv',
            'winners': f'{base}/{cat}_winners.csv',
            'previous': f'{base}/{cat}_winners.csv',
            'judges': f'{base}/{cat}-judges.csv',
            'chairs': f'{base}/effectiveness-chairs.csv'
        }
        # fill empty rows to stop empty bios being floats
        log.debug(f'reading {path[page]}')
        df = pd.read_csv(path[page], encoding='utf-8').fillna('')
        return df.to_dict('records')
    # catch utf encoding errors and try windows
    except UnicodeError as e:
        log.debug(e)
        df = pd.read_csv(path[page], encoding='cp1252').fillna('')
        return df.to_dict('records')
    except KeyError as e:
        log.warning(e)
        log.debug('no csv read')
        return False


def get_data(date, page, award, category):
    '''Consolidates all data sources and returns single dict output for rendering templates.'''
    # init as class common ones have rest as functions
    # date = values['date']
    # award = values['award']
    # category = values['cat']
    # page = values['page']
    data.update({"open": values['open']})
    data.update({                                  # get each elmt using awd_elmt() from AWARDS dictionary
        # and take input from gui window / cli and feed into temporary
        "award":       award,
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

    if 'winners' in page:
        yr = data['year']

        in_dates = (f"{yr}-01-01", f"{yr}-12-31") if not 'media' in data['award'] else (f"{yr}-09-01", f"{int(yr)+1}-12-31")

        full_cat = data['full_award'] if not 'media' in award else 'WARC Media Awards'

        query = func.get_entrants_query(
            in_dates, data['full_category'], full_cat, data['cartridge'])

        data.update({"entrants_query": query})

    # function for (body copy)
    # data.update({"body_copy": placeholder})
    data.update({"body_copy": AWARDS[award]
                 ['categories'][category]['body_copy']})
    # {papers / judges / winners / shortlist}
    # have each as individual function on GUI /
    # if radio input is true then get_csv that thing
    # get_csv(cat, page) if value for value in values True else pass
    # so that only necessary info is added to dict
    if any(i in page for i in ['winners', 'shortlist', 'previous']):
        papers = get_csv(category, page)

        if not 'shortlist' in page:
            medals = ['grand', 'gold', 'silver', 'bronze']
            # could do this better with filter and ~filter
            winning_ids = ['A'+str(i['ID']) for i in papers if any(
                [x in i['Award'].lower() for x in medals]
            )]
            shortlisted_ids = ['A'+str(i['ID']) for i in papers if any(
                [x not in i['Award'].lower() for x in medals]
            )]
            data.update({"winners_ids": winning_ids})
        else:
            winning_ids = None
            shortlisted_ids = ['A'+str(i['ID']) for i in papers]

        data.update({
            "papers": papers,
            "shortlist_ids": shortlisted_ids,
            "img_content_code": AWARDS[award]['img_content_code']
        })

    if 'judges' in page or 'chairs' in page:
        data.update({
            "judges": get_csv(category, page),
            "url": AWARDS[award]['url'],
            "category": AWARDS[award]['categories'][category]['category'],
            "category_url": AWARDS[award]['categories'][category]['url'],
            "judges_url": AWARDS[award]['categories'][category]['judges_url']
            # "category_href": AWARDS[award]['categories'][category]['category_href']
        })
        print('\nPanel chair:', data['judges'][0]
              ['Name'], data['judges'][0]['Surname'])

    if 'judges_split' in page:
        data.update({"quote": input('Insert quote:\n')})

    if 'entry' in page:
        entry_form = AWARDS[award]['prize'] + data['year'] + '-entryform.docx'
        data.update({"entry_form": entry_form})

    if 'entry' in page or 'about' in page:
        deadline = input('Deadline for entries?: ')
        data.update({"deadline": deadline})

    return data


def write_html(filename, output):
    try:
        with open(filename, "w", encoding='utf-8') as f:
            f.write(output)
    except UnicodeEncodeError as e:
        log.debug(e)
        with open(filename, "w", encoding='cp1252') as f:
            f.write(output)


# make this a class LandingPage: that imports from package /template_data with helpers in too
def get_html(date, page, award, category):
    '''Returns a filename, its output content and its page element code.'''
    d = get_data(date, page, award, category)
    yr = d['year']
    elmt = func.awd_elmt(  # page element
        page=page,
        award=award,
        category=category
    )
    # bring these functions into class
    fn = func.save_name(page, award, category, yr, elmt)  # filename
    try:
        output = env.get_template(f'{page}.html').render(d=d, page=page)
    except TypeError as e:
        print('error while rendering template, check logs')
        log.error(e)
        output = False
    return fn, output, elmt


def update_page(assets):
    '''Updates cms page element with created html content using the cmsbot package.'''
    log.debug('\nselected write files to CMS...')
    from cmsbot.cmsbot import CMSBot  # import here so only if selected?
    try:
        cms = CMSBot()
        print("\nupdating pages in cms...\n")
        prompt_save = input("save all changes? 'y' or 'n' - ")
        for name, page_element, content in assets:
            print(name)
            cms.edit_page(page_element)
            # .replace('\n', '\\n'))
            cms.paste_content(content.replace('\t', '   '))
            if prompt_save == 'y':
                cms.save_changes()
                print('saved')
            else:
                print('did not save')

        print('\n# updates complete')

    except Exception as e:
        log.error(e)
        print('Error while running cmsbot, check logs')
        raise e
    finally:
        cms.bot.quit()

# have this as runner file with classes and GUI/frontend as packages


def main():
    '''Write an html page element for each input with option to upload this to cms.'''
    date = values['date']
    award = values['award']
    written_assets = []
    print("Writing files:\n")

    for page in values['page']:  # should update data once instead of every page
        for category in values['cat']:
            file, output, element = get_html(date, page, award, category)
            fname = Path(file).name
            if output:
                write_html(file, output)
                print(fname)
                written_assets.append((fname, element, output))
            else:
                print(f'# failed --> {fname}')

    # write a file containing all output from written_assets
    proof_html_content = '\n'.join([i[2] for i in written_assets])
    write_html('../static/html/proof-html.html', proof_html_content)
    print('\n# wrote proof html file in /static/html')

    # prompt user whether to upload content
    string = f"\nupdate CMS articles with file content?\n- select 'y' or 'n': "
    select = input(string).casefold()

    # upload to cms using cmsbot class if confirmed
    if select == 'y':
        update_page(written_assets)
    else:
        pass


if __name__ == '__main__':
    main()
