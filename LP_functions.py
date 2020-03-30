"""If i were to make this again I'd do it entirely differently,
but it does the job and rewriting it wouldn't be worth the time invested."""

print('\n\t\t\tLanding Page Generator\n')

html_output = ''

# specify input csv file with judges info (direct from google sheets)

				#	FUNCTIONS 	#

year = input('\t- type year: ')
award = input("\t- type 'warc', 'mena', 'asia' or 'media': ")

if award == 'warc': # these could all be dictionaries

	category = input("\t- type 'innovation', 'purpose', 'content' or 'social': ")

	prize = 'WarcAwards'
	category_href = f'/WARCAwards/{category}-judges'
	full_award = 'WARC Awards'
	awards_or_prize = 'Awards'
	cartridge = 5790

	if category == 'innovation':
		bio_page_code = 5901
		pic_page_code = 5900
	elif category == 'purpose':
		bio_page_code = 5668
		pic_page_code = 5648
	elif category == 'content':
		bio_page_code = 5666
		pic_page_code = 5646
	elif category == 'social':
		bio_page_code = 5667
		pic_page_code = 5647 

elif award == 'mena':
	category = f'{award}'
	prize = f'{category}prize'
	category_href = f'/{prize}/{year}judges'
	full_award = 'WARC Prize for MENA Strategy'
	bio_page_code = 5642 
	pic_page_code = 5640
	awards_or_prize = 'Prize'
	fc = ''
	cartridge = 5822

elif award == 'asia':
	category = f'{award}'
	prize = f'{category}prize'
	category_href = f'/{prize}/{year}judges'
	full_award = 'WARC Prize for Asian Strategy'
	bio_page_code = 5711 
	pic_page_code = 5708
	awards_or_prize = 'Prize'
	fc = ''
	cartridge = 5676

elif award == 'media':

	category = input("\t- type 'channel-integration', 'data', 'tech' or 'partnerships-sponsorships': ") 

	prize = 'MediaAwards'
	category_href = f'/WARCAwards/{category}-judges'
	full_award = 'WARC Media Awards'
	awards_or_prize = 'Awards'
	cartridge = 5758
	
	if category == 'data':
		bio_page_code = 5750
		pic_page_code = 5741
	elif category == 'channel-integration':
		bio_page_code = 5748
		pic_page_code = 5739
	elif category == 'tech':
		bio_page_code = 5749
		pic_page_code = 5740
	elif category == 'partnerships-sponsorships':
		bio_page_code = 5751
		pic_page_code = 5742
	
Award = award.upper()
tCategory = category.split("-")[0]
Category = tCategory.title()

# Full category titles, could also be a dictionary

if category == 'data':
	fc = f'Use of {Category} '
elif category == 'tech':
	fc = f'Use of {Category} '
elif category == 'partnerships-sponsorships':
	fc = 'Partnerships & Sponsorships '
elif category == 'social':
	fc = f'Effective {Category} Strategy '
elif category == 'content':
	fc = f'Effective {Category} Strategy '
elif category == 'purpose':
	fc = 'Effective Use of Brand Purpose '
elif category == 'innovation':
	fc = 'Effective Innovation '
elif category == 'channel-integration':
	fc = 'Channel Integration '

imgsrc = '{ background-image: url(/Images/WARCSiteContent/landing-pages/awards/'
endbracket = '}'

if category == 'partnerships-sponsorships' or 'channel-integration':
	judges_details = f'csv\\{tCategory}-judges.csv'
else:
	judges_details = f'csv\\{category}-judges.csv'

print(f'''
	- csv input file = '{judges_details}'

	- ensure the csv files are named
	  correctly in the following format:
	  [category]-judges.csv
''')

# import LP_pics