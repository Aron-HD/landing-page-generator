# LANDING PAGES

### About

**This is one of the first scripts I made, and I would do it completely differently now. However this works fine and serves the functional purpose, so rescripting it isn't currently worth the time.**

Automated creation of formulaic HTML static pages for Judging panels across all 10 of our awards categories. Previously a copy and paste job.

Takes input from csv, panel chair must be at top.

Outputs two html files: one for the judging panel grid with headshots, another for the judging bios. (These are hidden for confidentiality).

**Examples:**

- [Grid](https://www.warc.com/WarcAwards.prize?tab=innovation)
- [Bios](https://www.warc.com/WARCAwards/innovation-judges.info#jane-wakely)

Recently added functionality to comment out judges who have not yet submitted their pics or bios, which was previously a bit tedious to either remove from the csv, or comment out manually.

---

# Redesign

Updating this to use Jinja2 module for templating rather than concatenating strings.

### ToDo

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

### Templates

##### Launch

- insights and inspirations (others extend from this)

d.report_link - *the full article link (e.g. "/content/article/2020-asian-strategy-report-insights-from-the-warc-prize-for-asian-strategy/134538"), which needs taking as input and updating to dictionary that is fed into render.*

d.report - *the full report name (e.g. 'Asian Strategy Report'*

d.page - *the type of page being made, "about", "entry_details", "previous" - Not 100% sure this TrackEvent changes though*

d.award - *might need category for category reports in global awards*

d.year - *current year*

d.entry_kit - *just the file name of the pdf (maybe strip '.pdf' so it doesn't matter if ext is in name)*

d.full_award - *for item title and description*


- entry details

**Links:**

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

- about

Seperate extended templates for about will probably be needed.

Use num2words module to count award year from start date and convert to word.

2020 was:
fifth year of Media
tenth year of Asia

- previous

##### Panels

- judges pics
- judges bios

##### Winners

These will be taken out of the landing page tabs when not relevant to keep judges separate.

- winners
- shortist


### Landing page codes

##### WARC Awards

- 5645 - About (Intro)
- 5902 - Previous
- 5665 - Entry details
- **Innovation** 
    - 5901 - bios
    - 5900 - pics
- **Purpose**
    - 5668 - bios
    - 5648 - pics
- **Content**
    - 5646 - bios
    - 5666 - pics
- **Social**
    - 5647 - bios
    - 5667 - pics

##### MENA

- 5638 - About (Intro)
- 5641 - Previous
- 5639 - Entry details
- 5642 bios
- 5640 pics

##### Asia

- 5694 - About (Intro)
- 5710 - Previous
- 5707 - Entry Details
- 5711 bios
- 5708 pics

##### Media Awards

- 5743 - About (Intro)
- 5752 - Previous
- 5744 - Entry details
- **Data**
    - 5750 bios
    - 5741 pics
- **Channel Integration**
    - 5748 bios
    - 5739 pics
- **Tech**
    - 5749 bios
    - 5740 pics
- **Partnerships**
    - 5751 bios
    - 5742 pics

##### China Prize
- 6593 - header 

##### Awards cartridge codes
- WARC - 5790
- MENA - 5822
- Asia - 5676
- Media - 5758

##### Navigation
- 91 - Our awards

### Improvements

- need to add in sorting alphabetically on last name so that this doesn't have to be filtered in google sheets before export.
- all of the imports from LP_functions.py should just be in a dictionary or a JSON file. When I do get around to revising this.
- I could also add functionality to CMS-Bot repo to automatically upload resized images into the file admin in CMS *before* the script runs, so that images are definitely uploaded.
- currently working on an easier way to take the bios from the All_judges.docx and place them directly into the csv. Might have to use pandas for this.
- eventually I want to connect to google sheets itself through the API, rather than using a csv to cut out another stage of the process.

