import time
import logging as log  # urllib.request,
from pathlib import Path
from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
chrome_options = Options()
chrome_options.add_argument(
    r"user-data-dir=C:\Users\arondavidson\AppData\Local\Google\Chrome\User Data\Profile 1")
# chrome_options.add_argument('--headless')
# chrome_options.add_argument("--start-maximized")


class CMSBot:
    def __init__(self):
        self.bot = webdriver.Chrome(options=chrome_options,
                                    executable_path=r"C:\Users\arondavidson\AppData\Local\Programs\Python\Python37\chromedriver.exe")

    def edit_page(self, element):
        bot = self.bot
        url = f'http://newcms.warc.com/content/page-element/edit/{element}'
        bot.get(url)
        bot.implicitly_wait(10)

    def paste_content(self, content):
        bot = self.bot

        # def scroll_click(element):
        #     actions = ActionChains(bot)
        #     actions.move_to_element(element).perform()
        #     element.click()

        try:
            # wait = WebDriverWait(bot, 10)
            # grab open source code
            # body = bot.find_element_by_link_text('Content body (English)')
            source_code = bot.find_element_by_id(
                'HtmlContent-Editor-en-GB-Global-source-code')
            source_code.click()
            html = bot.find_element_by_id('source-code-textarea')
            html.click()
            html.clear()
            html.send_keys(content.replace('\t', '  '))  # do this in file
            # input('Happy to save changes? press any key.')
        except NoSuchElementException as e:
            log.error('Could not find element', e)

    def save_changes(self):
        '''clicks cms button to save changes'''
        try:
            bot = self.bot
            save = bot.find_element_by_id('source-code-modal-save').click()
            time.sleep(0.5)
            bot.find_element_by_xpath(
                '//span[@onclick="onSaveChangedClicked()"]').click()
            time.sleep(3)
            log.debug('saved changes')
        except NoSuchElementException as e:
            log.error('Could not find element', e)


# if __name__ == '__main__':
# 	try:
# 		cms = CMSBot()
# 		cms.edit_page(6746)

# 		content = 'test content Reprehenderit dolore mollit ea eiusmod pariatur sed in commodo reprehenderit culpa sunt irure eiusmod officia.'
# 		cms.paste_content(content)
# 	except Exception as e:
# 		raise e
# 	finally:
# 		cms.bot.quit() # don't quit here
