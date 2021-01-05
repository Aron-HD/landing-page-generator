import pandas as pd
from glob import glob
from pathlib import Path
from datetime import datetime as dtm

from dictionary import AWARDS


class Functions:

	def awd_elmt(award, category, page):
		'''To get launch page codes or cartridge code.'''
		try:
			if page == any(key for key in AWARDS[award]['categories'].keys()):  # or 'preview' in page // for alt preview pages?
				code = AWARDS[award]['categories'][category][page]
				return code
			elif page == any(key for key in AWARDS[award].keys()):
				code = AWARDS[award][page]
				return code
		except KeyError:
			print('page not found in awards dictionary keys')

	def process_date(date):
		'''To get launch page codes or cartridge code.'''
		raw_date = dtm.strptime(date, '%d/%m/%Y')
		full_date = raw_date.strftime('%d %B %Y')
		d = raw_date.strftime('%d %B')
		year = dtm.now().strftime('%Y')
		return full_date, d, year

	def get_chair(category):
		'''To get launch page codes or cartridge code.'''
		df = pd.read_csv(f'../data/csv/{category}-judges.csv', encoding="utf-8") # change .. when moved
		chair = (df.iloc[0][0]) + ' ' + (df.iloc[0][1]) + ', ' + (df.iloc[0][2]) + ', ' + (df.iloc[0][3])
		return chair

	def mknewdir(year):
		'''To get launch page codes or cartridge code.'''
		newdir = f'../static/html/{year}'
		if not Path(newdir).is_dir():
			print('made new directory:', newdir)
			Path(newdir).mkdir(parents=True)
		return newdir

	def save_name(page, awd, cat, year, code):
		'''To get launch page codes or cartridge code.'''
		if awd == 'warc':
			award = AWARDS[awd]['full_award'] # WARC Awards
		elif awd == 'mena':
			award = AWARDS[awd]['award'].upper() # MENA
		else:
			award = AWARDS[awd]['award'].title() # Asia, Media

		if cat == 'mena' or cat == 'asia':
			save_name = f'{Functions.mknewdir(year)}/{award} {page} ({code}).html'
		else:
			save_name = f'{Functions.mknewdir(year)}/{cat} {page} ({code}).html'

		return save_name.replace("_"," ").replace("judges","")    

	def judge_count(category):
		'''To get launch page codes or cartridge code.'''
		df = pd.read_csv(f'../csv/{category}-judges.csv', encoding="utf-8") # change .. when moved
		count = df['Name'].size
		return count

	def entry_count(file):
		'''To get launch page codes or cartridge code.'''
		df = pd.read_csv(f'../csv/{file}.csv', encoding="utf-8") # change .. when moved
		count = df.columns[0]
		return df[count].size

'''
# Links

- **Reports**
	- "social": "/content/article/2020-social-strategy-report-insights-from-the-warc-awards/133117",
	- "content": "/content/article/2020-content-strategy-report-insights-from-the-warc-awards/133641"
	- "mena": "/content/article/2020-mena-strategy-report-insights-from-the-warc-prize-for-mena-strategy/133904",
	- "asia": "/content/article/2020-asian-strategy-report-insights-from-the-warc-prize-for-asian-strategy/134538"
	- "media": "/content/article/2020-media-strategy-report-insights-from-the-warc-media-awards/132328",
	- "innovation": ?
	- "purpose": ?
- **Entry kits**
	- warc-awards-entrykit2020.pdf
	- MENAPrize2020-entrykit_v2.pdf
	- AsiaPrize-entrykit2020_v03.pdf
	- mediaawards-entrykit2020.pdf
- **Entry forms**
	- warc-awards-entryform2020.docx
	- MENAPrize2020-entryform_v2.docx
	- AsiaPrize-entryform2020.docx
	- mediaawards-entryform2020.docx

'''
