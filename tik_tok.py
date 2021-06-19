import random
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from tik_tok_auth import email, password


class TikTokBot:
    def __init__(self, email, password):
        self.username = email
        self.password = password
        self.browser = webdriver.Chrome("chromedriver.exe")

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def generate_discription(self):
        list_of_hashtags = ['#meme', '#tranding', '#trand', '#recommendations', '#tranding', '#trand',
                            '#recommendations', '#wow', '#batman', '#hightechnologies']
        random_quantity = random.randrange(2, 4)
        hashtags = random.sample(list_of_hashtags, random_quantity)  # return random unique hashtags from the list
        smiles = []
        text_description = []
        # return

    def login(self):
        try:
            self.browser.get('https://www.tiktok.com')
            time.sleep(1)
            # find and click log in button
            self.browser.find_element_by_class_name('login-button').click()
            time.sleep(20)
            # switch to iframe
            # iframe = self.browser.find_element_by_xpath('/html/body/div[2]/div[1]/iframe')
            # self.browser.switch_to.frame(iframe)
            # open auth by email
            self.browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[1]/div[2]/div[2]/div[2]').click()
            # find username input
            user_input = self.browser.find_element_by_name('email')
            # clear the field (just in case)
            user_input.clear()
            # write the username
            user_input.send_keys(email)
            time.sleep(random.randrange(2, 4))

            # find the field username
            password_input = self.browser.find_element_by_name('password')
            password_input.clear()
            # write the password
            password_input.send_keys(password)
            time.sleep(random.randrange(1, 4))
            # send the complete authorization form
            password_input.send_keys(Keys.ENTER)
            # time.sleep(100)

        except Exception as ex:
            print(ex)

    # /html/body/div[1]/div/div[1]/div/form/div/input

    def upload_new_post(self):
        # upload video
        self.browser.get('https://www.tiktok.com/upload')
        time.sleep(random.randrange(1, 3))
        video_input = self.browser.find_element_by_name('upload-btn')
        # ...
        video_input.send_keys()

        # add caption
        capton_input = self.browser.find_element_by_xpath(
            '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/div/div')
        capton_input.send_keys(self.generate_discription())

        capton_input.send_keys(Keys.ENTER)


tik_tok_parser = TikTokBot(email, password)
tik_tok_parser.login()
