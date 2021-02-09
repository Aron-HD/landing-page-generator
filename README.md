# Landing page generator

Automated creation of formulaic HTML static pages for internal Awards landing pages of [WARC.com](https://www.warc.com/), judging panels across all 12 of our awards categories throughout the year.

Currently uses pulls data from python dictionary (or json) in `/data` in combination with additional data pulled from csv files for judging panels and winning campaigns. This is then collated and rendered through templates using Jinja2 templatig engine.

Outputs html files for each page and for each category specified. You can see examples of these in the [Examples](#2-examples) section.

# Contents

1. [Redesign](#1-redesign) 
2. [Examples](#2-examples) 
3. [Templates](#3-templates) 
4. [GUI Imports](#4-gui-Imports) 
5. [Improvements](#5-improvements) 

# 1. Redesign

Updated this to use Jinja2 module for templating rather than concatenating strings.

### ToDo

- add copy elements in data folder either as txt files or as csv values / columns
- rewrite README
- write tests
- add License
- add logging
- move data function to class in separate package with helpers and dict
- refactor core.py as Class
- add dependencies / requirements
- add GUI to core.py 
- finish templates
- format file when writing json
- fix unecessary and duplicate dictionary / json entries
- create docs in docs folder and add docstrings
- add database instead of csv

---

### 2. Examples

##### [Grid](https://www.warc.com/awards/warc-prize-for-mena-strategy)

![Judges Pics & Testimonial Split](./static/img/judges-pics-split.png "Judges Pics & Testimonial Split")

##### [Bios](https://www.warc.com/effectivenessawards/sustained-growth-judges)

![Judges Bios](./static/img/judges-bios.png "Judges Bios")

### 3. Templates

##### Data inputs

Data| Explanation
--- | ---
d.open | `True` or `False` to indicate whether the award is open for entries or not
d.award | indicates which award we are working in 'effectiveness', 'mena', 'asia', 'media'
d.cat | which category within each award - can input multiple by separating with spaces
d.year | current year
d.page | the type of page being made to correspond to template, 'about', 'entry_details', 'previous' - can input multiple by separating with spaces
d.code | lower case of shortened award for urls
d.cartridge | a 4 digit number used in search terms to filter articles tagged to the repective award
d.entry_kit | just the file name of the entry kit uploaded to CMS
d.report | the full report name (e.g. 'Asian Strategy Report'
d.report_link | the full article link on warc.com (e.g. '/content/article/2020-asian-strategy-report-insights-from-the-warc-prize-for-asian-strategy/134538').
d.full_award | for item title and description
d.special_awards | the special awards for that award or category (usually 3 - 5)
d.full_category | the correct full title of the category or award
d.category_description | description of the category or award
d.report_image | the image used for the report hosted in the CMS (usually same as that year's Grand Prix winner)
d.body_copy | main body text of the category section (could be a list split on lines so can have p tags for each, or have in separate txt files to edit easily)
d.winners_ids | the 6 digit article id numbers for each winning case study of that award or category from winners csv
d.papers | a nested dictionary containing the metadata for the winning / shortlisted papers for that award or category from respective csv, includes: award won, title, brand, brand owner, lead agency(ies), contributing agency(ies), budget, campaign duration, markets, industries and media channels
d.shortlist_ids | the 6 digit article id numbers for each shortlisted case study of that award or category from shortlist csv
d.img_content_code | the code for content in the award content folders of our CMS
d.judges | a nested dictionary containing metadata from judges csv, including judges name, surname, title and company
d.url | the url for the main award or category landing page
d.category | category or award code 
d.category_href | the url for the judges bios landing page for that award
d.quote | quote for the testimonial section, usually for judges-split section or about-split section
d.entry_form | the entry form document uploaded to the CMS
d.deadline | the deadline for entries format (d/ Month)

### 4. GUI Inputs

##### Links

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

### 5. Improvements

- need to add in sorting alphabetically on last name so that this doesn't have to be filtered in google sheets before export.
- I could also add functionality to CMS-Bot repo to automatically upload resized images into the file admin in CMS *before* the script runs, so that images are definitely uploaded.
- currently working on an easier way to take the bios from the All_judges.docx and place them directly into the csv. Might have to use pandas for this.
- eventually I want to connect to google sheets itself through the API, rather than using a csv to cut out another stage of the process.

##### about template

Use num2words module to count award year from start date and convert to word.

2020 was:
fifth year of Media
tenth year of Asia
