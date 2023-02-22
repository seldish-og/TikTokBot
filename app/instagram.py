import random
import time
import os
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import json


class InstagramParser:
    def __init__(self):
        with open("config.json", "r") as file:
            json_config = json.load(file)
        self.username = json_config["INSTAGRAM_LOGIN"]
        self.password = json_config["INSTAGRAM_PASSWORD"]
        # instagram's video src doesn't work on PC normally. Video has 'blob:https://...' link format
        # but using mobile emulator, link has normal form ('https://...')
        mobile_emulation = {
            "deviceName": "iPhone X"
        }  # choose device to emulate

        # define a variable to hold all the configurations we want
        chrome_options = webdriver.ChromeOptions()

        # add the mobile emulation to the chrome options variable
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        # create driver, pass it the path to the chromedriver file and the special configurations you want to run
        self.browser = webdriver.Chrome(
            executable_path='/home/mark/Desktop/TikTok-Project/TikTokBot/chromedriver',
            options=chrome_options)

        with open("inst_form.json", "r") as from_file:
            self.json_form = json.load(from_file)

    def close_browser(self):
        self.browser.close()
        self.browser.quit()  # (just in case)

    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def login(self):  # login to the account
        try:
            self.browser.get('https://www.instagram.com/accounts/login/?next=%2F&source=mobile_nav')
            time.sleep(random.randrange(2, 4))
            # find username input
            user_input = self.browser.find_element_by_name('username')
            # clear the field (just in case)
            user_input.clear()
            user_input.send_keys(self.username)

            time.sleep(random.randrange(2, 4))

            password_input = self.browser.find_element_by_name('password')
            password_input.clear()
            password_input.send_keys(self.password)

            time.sleep(random.randrange(2, 4))
            # send the complete authorization form
            password_input.send_keys(Keys.ENTER)
            time.sleep(5)
        except Exception as e:
            print(e)
            self.close_browser()

    # get hrefs from user page
    def get_list_of_hrefs(self, page_name):  # page_name = account name we need
        try:
            # open user page website
            self.browser.get(f'https://www.instagram.com/{page_name}/')
            time.sleep(5)
            # find all <a> on the page
            hrefs = self.browser.find_elements_by_tag_name('a')
            list_of_hrefs = []
            for i in hrefs:
                # extract links from the tag's attribute
                href = i.get_attribute('href')
                # all videos have /p/ in their href
                if '/p/' in href:
                    list_of_hrefs.append(href)
            return list_of_hrefs
        # if something went wrong, close the browser
        except Exception as exc:
            print(exc)
            print("something wrong with links")
            self.close_browser()

    def download_videos(self, page_name, video_number, hrefs, videos_quantity):
        try:
            for number in range(videos_quantity):
                video_number += 1
                self.browser.get(hrefs[number])
                time.sleep(4)
                video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"

                if self.xpath_exists(video_src):
                    video_src_url = self.browser.find_element_by_xpath(video_src).get_attribute("src")
                    # save video
                    video = requests.get(video_src_url, stream=True)
                    save_folder = "videos"
                    video_name = f"video_{page_name}_{video_number}.mp4"
                    complete_name = os.path.join(save_folder, video_name)
                    with open(complete_name, "wb") as video_file:
                        for chunk in video.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                video_file.write(chunk)
                    print(f"{hrefs[number]} successfully saved!")
                else:
                    print('error with video xpath')
                    break

        except Exception as exception:
            print(exception)
            print('error with downloading videos ')
            self.close_browser()

    def inst_main(self):
        self.login()
        pages_and_quantities = self.json_form["links_and_quantity"]
        video_number = 0
        try:
            for page in pages_and_quantities:
                hrefs = self.get_list_of_hrefs(page.split()[0])
                quantity = int(page.split()[1])
                self.download_videos(page, video_number, hrefs, quantity)
                video_number += quantity
            print("time break 1 hour")
            time.sleep(3600)
        except Exception as ex:
            print(ex)
