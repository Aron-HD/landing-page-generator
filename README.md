# Landing Pages

**This is one of the first scripts I made, and I would do it completely differently now. However this works fine and serves the functional purpose, so rescripting it isn't currently worth the time.**

Automated creation of formulaic HTML static pages for Judging panels across all 10 of our awards categories. Previously a copy and paste job.

Takes input from csv, panel chair must be at top.

Outputs two html files - one for the judging panel grid with headshots, another for the judging bios. (These are hidden for confidentiality).

**Examples:**
- [Grid](https://www.warc.com/WarcAwards.prize?tab=innovation)
- [Bios](https://www.warc.com/WARCAwards/innovation-judges.info#jane-wakely)

Recently added functionality to comment out judges who have not yet submitted their pics or bios, which was previously a bit tedious to either remove from the csv, or comment out manually.

### Improvements

- need to add in sorting alphabetically on last name so that this doesn't have to be filtered in google sheets before export.
- all of the imports from LP_functions.py should just be in a dictionary or a JSON file. When I do get around to revising this.
- I could also add functionality to CMS-Bot repo to automatically upload resized images into the file admin in CMS *before* the script runs, so that images are definitely uploaded.
- currently working on an easier way to take the bios from the All_judges.docx and place them directly into the csv. Might have to use pandas for this.
- eventually I want to connect to google sheets itself through the API, rather than using a csv to cut out another stage of the process.






