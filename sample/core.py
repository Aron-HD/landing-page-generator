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
values['date'] = '29/10/2020'
values['page'] = "winners"
values['cat'] = "data" # make this able to pass in a list of cats too
values['award'] = "media"
values['entry_kit'] = "MENAPrize2020-entrykit_v2.pdf"
values['report_link'] = "/content/article/2020-mena-strategy-report-insights-from-the-warc-prize-for-mena-strategy/133904"

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

# make this a class TemplateData: that imports from package /template_data with helpers in too
def get_data():
			
	# init as class common ones have rest as functions
	date = values['date']
	awd = values['award']
	cat = values['cat']
	page = values['page']

	data.update({	                               # get each elmt using awd_elmt() from AWARDS dictionary
		"award":       awd,                        # and take input from gui window / cli and feed into temporary 
		"cat":         cat,                        # data dictionary for rendering template
		"year":        func.process_date(date)[2], # should shrink this to just get date from now
		 page:         func.awd_elmt(awd, cat, page),
		"code":        AWARDS[awd]['code'],	      
		"cartridge":   AWARDS[awd]['cartridge'],
		"entry_kit":   values['entry_kit'].replace('.pdf',''),
		"report":      AWARDS[awd]['categories'][cat]['report'],
		"report_link": values['report_link'],
		"full_award":  AWARDS[awd]['full_award'],
	  	"special_awards": AWARDS[awd]['categories'][cat]['special_awards'],
	})

	# {papers / judges / winners / shortlist}
	# have each as individual function on GUI / 
	# if radio input is true then get_csv that thing
	# get_csv(cat, page) if value for value in values True else pass
	# so that only necessary info is added to dict
	data.update({"papers": get_csv(cat, page)})
	# def function(): 
	'''To sort judges bios.'''
	# chair? for testimonial
	# chair = get_chair(category=cat)

	# pics and bios should be covered in above
	# also need to read in csvs
	# data.update({"judges": ?})

	return data, page

def write_html(filename, output):
	with open(filename, "w") as f:
		f.write(output)
	# subprocess.run([filename], check=True)

def main():
	# for page in pages ticked on gui
	try:
		# run_tests()
		d, pg = get_data()
		awd = d['award']
		yr = d['year']
		cat = d['cat']
		elmt = func.awd_elmt(awd, cat, pg)

		# do all this string processing elsewhere 
		fn = func.save_name(pg, awd, cat, yr, elmt) #<<<-----------------

		output = env.get_template(f'{pg}.tpl').render(d=d, page=pg)#tpl.render
		write_html(fn, output)
		print("wrote:", fn)
	except Exception as e:
		raise e

def main1():
	
	for f in glob(r"../templates/*.tpl"):
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