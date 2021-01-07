import pandas as pd # comment this once get_csv moved?
from glob import glob
from pathlib import Path

from dictionary import AWARDS
from helpers import Functions as func

### Jinja Imports
from jinja2 import Environment, FileSystemLoader
env = Environment(
	loader=FileSystemLoader('../templates'))

### CLI / GUI Inputs
values = {}
try:
	values['date'] = '01/01/2021'
	values['page'] = list(input("enter page ('special' 'body' 'category_hero'): ").strip().split(' '))
	values['award'] = 'effectiveness'# input("enter award ('effectiveness'): ")
	values['cat'] = list(input("enter category: ").strip().split(' ')) # make this able to pass in a list of cats too
	values['entry_kit'] = "effectiveness2021-entrykit.pdf"
	values['report_link'] = "/content/article/2020-mena-strategy-report-insights-from-the-warc-prize-for-mena-strategy/133904"
	print(values['page'], values['cat'])
except KeyError as e:
	print('invalid key input lists separated by spaces', e)
	raise SystemExit

# init as class
data = {}

def get_csv(cat, page): # swap page for path 
	'''Reads in csv data for shortlist, winners or judges.'''
	print('reading csv')
	try: 
		path = { # pass in path object in respective functions when class
			'shortlist': f'../data/csv/shortlists/{cat}_shortlist.csv',
			'winners': f'../data/csv/{cat}_winners.csv',
			'judges': f'../data/csv/{cat}-judges.csv'
		}
		df = pd.read_csv(path[page])
		return df.to_dict('records')
	except UnicodeError:
		df = pd.read_csv(path[page], encoding='cp1252')
		return df.to_dict('records')
	except KeyError:
		print('no csv read')
		return False

def get_data(date, page, award, category):
			
	# init as class common ones have rest as functions
	# date = values['date']
	# award = values['award']
	# category = values['cat']
	# page = values['page']

	data.update({	                               # get each elmt using awd_elmt() from AWARDS dictionary
		# "award":       award,                      # and take input from gui window / cli and feed into temporary 
		"cat":         category,                   # data dictionary for rendering template
		"year":        func.process_date(date)[2], # should shrink this to just get date from now
		 page:         func.awd_elmt(award, category, page),
		"code":        AWARDS[award]['code'],	      
		"cartridge":   AWARDS[award]['cartridge'],
		"entry_kit":   values['entry_kit'].replace('.pdf',''),
		"report":      AWARDS[award]['categories'][category]['report'],
		"report_link": values['report_link'],
		"full_award":  AWARDS[award]['full_award'],
	  	"special_awards": AWARDS[award]['categories'][category]['special_awards'],
	})

	placeholder = "Pariatur exercitation qui aute eu veniam cillum ea excepteur sint. Sint tempor ea irure veniam proident ut pariatur consequat duis voluptate incididunt amet laborum reprehenderit aute dolore tempor nostrud anim magna adipisicing in ut et reprehenderit exercitation mollit in."
	# function only for when needed (category hero)
	data.update({
			"full_category": AWARDS[award]['categories'][category]['full_category'], 
			"category_description": placeholder
			# "category_description": AWARDS[award]['categories'][category]['category_description']
		})

	# function for (body copy)
	data.update({"body_copy": placeholder})
	# {papers / judges / winners / shortlist}
	# have each as individual function on GUI / 
	# if radio input is true then get_csv that thing
	# get_csv(cat, page) if value for value in values True else pass
	# so that only necessary info is added to dict
	data.update({"papers": get_csv(category, page)})
	# def function(): 
	'''To sort judges bios.'''
	# chair? for testimonial
	# chair = get_chair(category=cat)

	# pics and bios should be covered in above
	# also need to read in csvs
	# data.update({"judges": ?})

	return data

def write_html(filename, output):
	with open(filename, "w") as f:
		f.write(output)
	print("wrote:", filename)
	# subprocess.run([filename], check=True)

# make this a class LandingPage: that imports from package /template_data with helpers in too
def build_page(date, page, award, category):
	try:
		# run_tests()
		d = get_data(date, page, award, category)
		# awd = d['award']
		yr = d['year']
		# cat = d['cat']
		elmt = func.awd_elmt(
			page=page.replace('category_', '').replace('award_', '').replace('preview-', ''),
			award=award, 
			category=category
		)

		# bring these functions into class
		fn = func.save_name(page, award, category, yr, elmt)

		output = env.get_template(f'{page}.html').render(d=d, page=page)#tpl.render
		write_html(fn, output)
	except Exception as e:
		raise e

# have this as runner file with classes and GUI/frontend as packages
def main():
	
	date = values['date']
	award = values['award']

	for page in values['page']:
		for category in values['cat']:
			build_page(date, page, award, category) # make this class

def main1():
	
	for f in glob(r"../templates/*.html"):
		print(f)
		for line in f:
			tag = line.find(r'{{')
			print(tag)


# {{ year }}
# {{ report_link }}
# {{ report }}
# {{ full_award }}
# {{ award }}
# {{ entry_kit }}


if __name__ == '__main__':
	main()