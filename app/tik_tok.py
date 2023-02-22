import glob
import json
import os
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from app.captcha import CaptchaSolver
from fake_useragent import UserAgent


class TikTokBot:
    def __init__(self):
        with open("config.json", "r") as file_config:
            json_config = json.load(file_config)

        with open("tik-tok_forms.json", "r") as file_forms:
            self.json_tik_tok_form = json.load(file_forms)
        self.username = json_config["TIK-TOK_LOGIN"]
        self.password = json_config["TIK-TOK_PASSWORD"]
#         mobile_emulation = {
#             "deviceName": "iPhone X"
#         }
#         chrome_options = webdriver.ChromeOptions()
#         # add the mobile emulation to the chrome options variable
#         chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

#         self.browser = webdriver.Chrome(
#             executable_path='chromedriver.exe',
#             options=chrome_options)
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1400,1400")
        ua = UserAgent()
        user_agent = ua.random
        print(user_agent)
        options.add_argument(f'user-agent={user_agent}')
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.browser = webdriver.Chrome(
            executable_path="chromedriver.exe", options=options)

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def generate_caption(self):
        list_of_descriptions = self.json_tik_tok_form["Captions"]
        caption = random.choice(list_of_descriptions)
        return caption

    def captcha_exists(self, id):
        browser = self.browser
        try:
            browser.find_element_by_id(id)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def solve_captcha(self):
        while True:
            try:
                # send captcha id to method
                if self.captcha_exists("captcha-verify-image"):
                    captcha_image_src = self.browser.find_element_by_id(
                        'captcha-verify-image').get_attribute("src")

                    '''on the main page src ends at .image, to work with a pic I refactor link to .jpeg(it works)'''
                    captcha_image_src = f'{captcha_image_src[:-6]}.jpg'
                    captcha_key_src = self.browser.find_element_by_class_name(
                        'captcha_verify_img_slide').get_attribute("src")
                    captcha_key_src = f'{captcha_key_src[:-6]}.jpg'

                    slider = self.browser.find_element_by_xpath(
                        '/html/body/div[2]/div/div[3]/div[2]/div[1]')
                    move = ActionChains(self.browser)
                    # get an offset value
                    captcha_key_coordinates = CaptchaSolver(
                        captcha_image_src, captcha_key_src).find_coordinates()
                    # drive the slider
                    # move.drag_and_drop_by_offset(slider, captcha_key_coordinates, 0).perform()
                    move.click_and_hold(slider).move_by_offset(
                        captcha_key_coordinates / 3, 0)
                    move.click_and_hold(slider).move_by_offset(
                        captcha_key_coordinates / 3, 0)
                    move.click_and_hold(slider).move_by_offset(
                        captcha_key_coordinates / 3, 0).release().perform()
                    time.sleep(random.randrange(3, 5))
                    if not self.captcha_exists("captcha-verify-image"):
                        break
                else:
                    self.browser.refresh()
                    print("No captcha on the page. Refreshing and wait 10sec")
                    time.sleep(25)

            except Exception as ex:
                print(ex)
                print("smth wrong with captcha")
                break

    def login(self):
        try:
            self.browser.get('https://www.tiktok.com')
            time.sleep(random.randrange(1, 3))

            self.solve_captcha()
            time.sleep(10)

            self.browser.find_element_by_class_name('login-button').click()
            time.sleep(10)

            # switch to iframe
            iframe = self.browser.find_element_by_xpath(
                '/html/body/div[3]/div[1]/iframe')
            self.browser.switch_to.frame(iframe)

            # open auth by email
            time.sleep(random.randrange(3, 6))
            self.browser.find_element_by_xpath(
                '/html/body/div[1]/div/div[1]/div/div[1]/div[2]/div[2]/div[2]').click()
            time.sleep(random.randrange(3, 7))
            self.browser.find_element_by_xpath(
                '/html/body/div[1]/div/div[1]/form/div[1]/a').click()
            time.sleep(random.randrange(3, 8))
            user_input = self.browser.find_element_by_name('email')
            user_input.clear()
            user_input.send_keys(self.username)
            time.sleep(random.randrange(2, 5))

            password_input = self.browser.find_element_by_name('password')
            password_input.clear()
            password_input.send_keys(self.password)
            time.sleep(random.randrange(1, 4))
            password_input.send_keys(Keys.ENTER)
        except Exception as ex:
            print(ex)
            print("smth with login")

    def upload_new_post(self, video):
        self.browser.get('https://www.tiktok.com/upload')
        time.sleep(random.randrange(1, 3))

        video_input_field = self.browser.find_element_by_name(
            'upload-btn')  # <input type="file" name="upload-btn"...>
        video_input_field.send_keys(video)

        # add caption
        caption_input = self.browser.find_element_by_xpath(
            '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/div/div')
        caption_input.send_keys(self.generate_caption())

        caption_input.send_keys(Keys.ENTER)


def delete_video(video_path, video_index):
    x = glob.glob(video_path)
    try:
        os.remove(x[video_index])
    except IndexError:
        print("folder with videos is empty")


tik_tok_parser = TikTokBot()
tik_tok_parser.login()
time.sleep(10)
folder_path = tik_tok_parser.json_tik_tok_form["Folder with video path"]
try:
    videos = glob.glob(f"{folder_path}/*.mp4")  # return list with videos paths
    for video in videos:
        tik_tok_parser.upload_new_post(video)
        time.sleep(
            tik_tok_parser.json_tik_tok_form["time delay, before uploading videos"])
except IndexError:
    print("folder with videos is empty")
