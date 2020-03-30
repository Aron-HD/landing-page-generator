import os
import csv
from LP_functions import *

print('\n- Creating landing page for judges picture grid..\n')

# html starts here
html_output = ''
html_output += '''
<section class="container">
<div class="row">
<div class="col-xl-10">

<h3>Judges</h3>
<!-- Style -->
<style>'''

## CSS style section
with open(judges_details, 'r') as data_file:
	csv_data = csv.DictReader(data_file)

	for line in csv_data:
		Name = f"{line['Name']} {line['Surname']}"
		title = f"{Name} &ndash; {line['Title']}, {line['Company']}"
		bio = line['Bio']
		name = Name.replace(' ', '-')
		name = name.lower()

		# comment out judges who don't yet have a bio / pic
		if len(bio) < 10:
			html_output += f'\n\t/*.{name} {imgsrc}{award}/judges/{name}.jpg); {endbracket}*/'
		else:
			html_output += f'\n\t.{name} {imgsrc}{award}/judges/{name}.jpg); {endbracket}'

html_output += '\n</style>\n\n<!-- Picture Grid -->\n<div class="judges-grid">'

#	have to access csv as an array rather than a dictionary to get individual values
#	chair only needs to be printed once so can't be in the for loop

with open(judges_details, 'r') as data_file:
	csv_data = list(csv.reader(data_file))
	Chair = (csv_data[1][0]) + ' ' + (csv_data[1][1])
	chair_name = Chair.replace(' ', '-').lower()
	# chair_name = chair_name.lower()
	chair_title = Chair + ' &ndash; ' + (csv_data[1][2]) + ', ' + (csv_data[1][3])
	html_output += f'\n<a class="judge-image proportional-box ratio-1-1 {chair_name} chair" href="{category_href}.info#{chair_name}" onclick="TrackEvent(&#39;Warc_Awards&#39;, &#39;Judging_panel&#39;, &#39;Judge&#39;); return true;"><span class="proportional-box-content">{chair_title}</span></a>'

with open(judges_details, 'r') as data_file:
	csv_data = csv.DictReader(data_file)	
	# skip chair
	next(csv_data) 
	
	for line in csv_data:
		Name = f"{line['Name']} {line['Surname']}"
		title = f"{Name} &ndash; {line['Title']}, {line['Company']}"
		bio = line['Bio']
		name = Name.replace(' ', '-')
		name = name.lower()

		# comment out judges who don't yet have a bio / pic
		if len(bio) < 10:
			html_output += f'\n<!-- <a class="judge-image proportional-box ratio-1-1 {name}" href="{category_href}.info#{name}" onclick="TrackEvent(&#39;Warc_Awards&#39;, &#39;Judging_panel&#39;, &#39;Judge&#39;); return true;"><span class="proportional-box-content">{title}</span></a> -->'
		else:
			html_output += f'\n<a class="judge-image proportional-box ratio-1-1 {name}" href="{category_href}.info#{name}" onclick="TrackEvent(&#39;Warc_Awards&#39;, &#39;Judging_panel&#39;, &#39;Judge&#39;); return true;"><span class="proportional-box-content">{title}</span></a>'

html_output += "\n</div>\n</div>\n</div>\n</section>"

# output html filename #

new_dir = 'html pages'

if not os.path.exists(new_dir):
    os.makedirs(new_dir)

nf = rf'{new_dir}\\{Category} {year} pics LP - ({pic_page_code}).html'

with open(nf, 'w') as f:
	f.write(html_output)

	print(f'''
		Successfully created

		{full_award} {year} {Category} landing page

		OUTPUT FILE: {nf}
		''')

import LP_bios
