import random
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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

    def xpath_exists(self, xpath):

        browser = self.browser
        try:
            browser.find_element_by_xpath(xpath)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def login(self):
        try:
            self.browser.get('https://www.tiktok.com')
            time.sleep(random.randrange(1, 3))

            # there must be captcha solution and a loop to solve it several times
            # or login manually and use cookies next times

            # find captcha on the page
            try:  # get captcha and captcha key to match them 
                captcha_xpath = "/html/body/div[6]/div"
                if self.xpath_exists(captcha_xpath):
                    captcha_src_url = self.browser.find_element_by_xpath(
                        '/html/body/div[6]/div/div[2]/img[1]').get_attribute("src")
                    captcha_key_src_url = self.browser.find_element_by_xpath(
                        '/html/body/div[6]/div/div[2]/img[2]').get_attribute("src")
                    captcha = requests.get(captcha_src_url, stream=True)
                    captcha_key = requests.get(captcha_key_src_url, stream=True)
            except Exception as ex:
                print(ex)

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
