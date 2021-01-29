import pandas as pd
import logging as log
from glob import glob
from pathlib import Path
from datetime import datetime as dtm

from dictionary import AWARDS


class Functions:

    def awd_elmt(award, category, page):
        '''To get launch page codes or cartridge code.'''
        replacements = [
            'preview-',
            '_bios',
            '_split',
            # '_headshots', # div within element
            'category_',
            'award_'
        ]
        for item in replacements:
            page = page.replace(item, '')
        try:
            category = AWARDS[award]['categories'][category]
            if page in [k for k in category.keys()]:
                code = category[page]
                return code
            else:
                code = AWARDS[award][page]
                return code
        except KeyError:
            log.error('page not found in awards dictionary keys:', page)
            return 0

    def process_date(date):
        '''To process input date and current year.'''
        raw_date = dtm.strptime(date, '%d/%m/%Y')
        full_date = raw_date.strftime('%d %B %Y')
        d = raw_date.strftime('%d %B')
        year = dtm.now().strftime('%Y')
        return full_date, d, year

    def get_chair(category):
        '''To get chair specifically from judges csv input.'''
        df = pd.read_csv(f'../data/csv/{category}-judges.csv', encoding="utf-8")  # change .. when moved
        chair = (df.iloc[0][0]) + ' ' + (df.iloc[0][1]) + \
            ', ' + (df.iloc[0][2]) + ', ' + (df.iloc[0][3])

        return chair

    def mknewdir(newdir):
        '''Creates relevant directory.'''
        if not Path(newdir).is_dir():
            log.info('made new directory:', newdir)
            Path(newdir).mkdir(parents=True)
        return newdir

    def save_name(page, awd, cat, year, code):
        '''Returns correct save name and directory.'''
        if awd == 'warc':
            award = AWARDS[awd]['full_award']  # WARC Awards
        elif awd == 'mena':
            award = AWARDS[awd]['award'].upper()  # MENA
        else:
            award = AWARDS[awd]['award'].title()  # Asia, Media
        newdir = f'../static/html/{year}'
        if cat == 'mena' or cat == 'asia':
            save_name = f'{Functions.mknewdir(newdir)}/{award} {page} ({code}).html'
        else:
            save_name = f'{Functions.mknewdir(newdir)}/{cat} {page} ({code}).html'

        return save_name.replace("_", " ")

    def judge_count(category):
        '''Counts the number of judges.'''
        df = pd.read_csv(f'../data/csv/{category}-judges.csv', encoding="utf-8")  # change .. when moved
        count = df['Name'].size
        return count

    def entry_count(file):
        '''Counts the number of entries.'''
        df = pd.read_csv(f'../data/csv/{file}.csv', encoding="utf-8")  # change .. when moved
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
