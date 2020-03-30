import os
import csv
from LP_functions import * 

print('\n- Creating landing page for bios..\n')

# html starts here

html_output += f'<section class="ScrollSpyPageHeader">\n<div class="image-header image-header-awards">\n<div class="container">\n<h1 class="SpyMenuItem">{full_award} &ndash; {year} {fc}Judges</h1>\n<p><a href="/{prize}.prize" class="box-links blue">Back to the {awards_or_prize} page</a></p>\n</div>\n</div>\n</section>\n\n<!-- Chair of Judges -->\n<h4 id="chair">Chair of Judges</h4>\n<div class="judge group">'

with open(judges_details, 'r') as data_file:
	csv_data = list(csv.reader(data_file))
	Chair = (csv_data[1][0]) + ' ' + (csv_data[1][1])
	chair_name = Chair.replace(' ', '-')
	chair_name = chair_name.lower()
	chair_title = Chair + ' &ndash; ' + (csv_data[1][2]) + ', ' + (csv_data[1][3])

	# need to add bios to csv file
	chair_bio = csv_data[1][4]
	
	html_output += f'\n<h4 id="{chair_name}"><img src="/Images/WARCSiteContent/landing-pages/awards/{award}/judges/{chair_name}.jpg" alt="{Chair}">{chair_title}</h4>\n<div class="chair-bio">\n<p>{chair_bio}</p>\n</div>\n</div>\n'

html_output += '\n<!-- The Panel -->\n<h4 id="panel">The Panel</h4>\n'

with open(judges_details, 'r') as data_file:
	csv_data = csv.DictReader(data_file)	
	
	# skip chair
	next(csv_data) 

	for line in csv_data:
		Name = f"{line['Name']} {line['Surname']}"
		title = f"{Name} &ndash; {line['Title']}, {line['Company']}"
		name = Name.replace(' ', '-')
		name = name.lower()
		bio = line['Bio']
		
		# comment out judges with no pic / bio
		if len(bio) < 10:
			html_output += f'\n<!-- <div class="judge group">\n<h4 id="{name}"><img src="/Images/WARCSiteContent/landing-pages/awards/{award}/judges/{name}.jpg" alt="{Name}">{title}</h4>\n<p>{bio}</p>\n</div> -->\n'
		else:
			html_output += f'\n<div class="judge group">\n<h4 id="{name}"><img src="/Images/WARCSiteContent/landing-pages/awards/{award}/judges/{name}.jpg" alt="{Name}">{title}</h4>\n<p>{bio}</p>\n</div>\n'

html_output += f'\n<!-- Navigation -->\n<section class="navigate-between-pages">\n<div class="container">\n<div class="page-backwards">\n<a href="/{prize}.prize"><img src="/images-site/arrow.svg" alt="<" class="arrow" height="16" width="19"> Back to the {awards_or_prize} page</a>' 

html_output += '\n</div>\n</div>\n</section>'

if category == 'partnerships-sponsorships' or 'channel-integration':
	Category = Category.strip('-')
# output html filename #

new_dir = 'html pages'

if not os.path.exists(new_dir):
    os.makedirs(new_dir)

nf = rf'{new_dir}\\{Category} {year} bios LP - ({bio_page_code}).html'

with open(nf, 'w') as f:
	f.write(html_output)

	print(f'\n\tSuccessfully created\n\n\t{full_award} {year} {Category} landing page\n\n\tOUTPUT FILE: {nf}\n')