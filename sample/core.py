import pandas as pd
from glob import glob
from pathlib import Path

from dictionary import AWARDS
from helpers import Functions as func

### Jinja Imports
from jinja2 import Environment, FileSystemLoader
env = Environment(
	loader=FileSystemLoader('../templates'))

### GUI Inputs
values = {}
values['date'] = '29/10/2020'
values['page'] = "special"
values['cat'] = "growth" # make this able to pass in a list of cats too
values['award'] = "effectiveness"
values['entry_kit'] = "MENAPrize2020-entrykit_v2.pdf"
values['report_link'] = "/content/article/2020-mena-strategy-report-insights-from-the-warc-prize-for-mena-strategy/133904"

def get_winners(cat):
	try:
		print('reading winners csv')
		winners = pd.read_csv(f'../data/csv/{cat}_winners.csv').to_dict('records')
		return winners
	except UnicodeError as e:
		winners = pd.read_csv(f'../data/csv/{cat}_winners.csv', encoding='cp1252').to_dict('records')
		return winners
	except FileNotFoundError:
		print('no winners papers')
		return False
		# raise e

def get_data():
			
	data = {}

	date = values['date']
	awd = values['award']
	cat = values['cat']
	page = values['page']

	# init as class
	data.update({	                              # get each elmt using awd_elmt() from AWARDS dictionary
		"code":        AWARDS[awd]['code'],	      # and take inputs from gui window and feed into temporary 
		"cartridge":   AWARDS[awd]['cartridge'],  # data dictionary for rendering template
		"award":       awd,
		"entry_kit":   values['entry_kit'].replace('.pdf',''),
		"report_link": values['report_link'],
		"report":      AWARDS[awd]['categories'][cat]['report'],
		"full_award":  AWARDS[awd]['full_award'],
		"year":        func.process_date(date)[2], # should shrink this to just get date from now
		page:          func.awd_elmt(awd, cat, page),
		"papers":      get_winners(cat),
		"cat":         cat,
	  	"special_awards": AWARDS[awd]['categories'][cat]['special_awards'],
	  	# "special_awards": ?,
	})

	# chair? for testimonial
	# chair = func.get_chair(category=cat)

	# pics and bios should be covered in above
	# also need to read in csvs

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