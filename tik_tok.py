import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from captcha import CaptchaSolver
from tik_tok_auth import email, password


class TikTokBot:
    def __init__(self, email, password):
        self.username = email
        self.password = password
        self.browser = webdriver.Chrome("chromedriver.exe")

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def open_browser(self):
        self.browser.get('https://www.tiktok.com')

    def generate_description(self):
        list_of_hashtags = ['#meme', '#tranding', '#trand', '#recommendations', '#tranding', '#trand',
                            '#recommendations', '#wow', '#batman', '#hightechnologies']
        random_quantity = random.randrange(2, 4)
        hashtags = random.sample(list_of_hashtags, random_quantity)  # return random unique hashtags from the list
        smiles = []
        text_description = []
        # return

    def captcha_exists(self, id):
        browser = self.browser
        try:
            browser.find_element_by_id(id)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def login(self):
        try:
            self.browser.get('https://www.tiktok.com')
            time.sleep(random.randrange(1, 3))

            # find captcha on the page
            while True:
                try:
                    captcha_id = "captcha-verify-image"
                    if self.captcha_exists(captcha_id):

                        # get captcha and captcha key
                        captcha_src = self.browser.find_element_by_id('captcha-verify-image').get_attribute("src")
                        # on the main page src ends at .image, to work with a pic I refactor link to .jpeg (it works)
                        captcha_src = f'{captcha_src[:-5]}jpg'
                        captcha_key_src = self.browser.find_element_by_class_name(
                            'captcha_verify_img_slide').get_attribute("src")
                        captcha_key_src = f'{captcha_key_src[:-5]}jpg'

                        # find the slider
                        slider = self.browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/div[2]/div[1]')
                        move = ActionChains(self.browser)
                        # get an offset value
                        captcha_coordinates = CaptchaSolver(captcha_src, captcha_key_src).find_coordinates()
                        # drive the slider
                        move.click_and_hold(slider).move_by_offset(captcha_coordinates, 0).release().perform()
                        if not self.captcha_exists(captcha_id):
                            break
                    else:
                        self.browser.refresh()
                        time.sleep(10)

                except Exception as ex:
                    print(ex)
                    break

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
        caption_input = self.browser.find_element_by_xpath(
            '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/div/div')
        caption_input.send_keys(self.generate_description())

        caption_input.send_keys(Keys.ENTER)


tik_tok_parser = TikTokBot(email, password)
tik_tok_parser.login()
