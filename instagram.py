import random
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from inst_auth import username, password


class Parser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # instagram's video src doesn't work on PC normally. Video has 'blob:https://...' link format
        # but using mobile emulator, link has normal format ('https://...')
        mobile_emulation = {
            "deviceName": "iPhone X"
        }  # choose device to emulate

        # define a variable to hold all the configurations we want
        chrome_options = webdriver.ChromeOptions()

        # add the mobile emulation to the chrome options variable
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        # create driver, pass it the path to the chromedriver file and the special configurations you want to run
        self.browser = webdriver.Chrome(
            executable_path='chromedriver.exe',
            options=chrome_options)

    def close_browser(self):
        self.browser.close()  # close
        self.browser.quit()  # (just in case)

    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def login(self):
        try:
            # open website
            self.browser.get('https://www.instagram.com/accounts/login/?next=%2F&source=mobile_nav')
            time.sleep(random.randrange(2, 4))
            # find username input
            user_input = self.browser.find_element_by_name('username')
            # clear the field (just in case)
            user_input.clear()
            # write the username
            user_input.send_keys(username)

            time.sleep(random.randrange(2, 4))
            # find password input
            password_input = self.browser.find_element_by_name('password')
            password_input.clear()
            # write the password
            password_input.send_keys(password)
            time.sleep(random.randrange(2, 4))
            # send the complete authorization form
            password_input.send_keys(Keys.ENTER)
            time.sleep(5)
        # if smth went wrong, close the browser
        except Exception as ex:
            print(ex)
            self.close_browser()

    # get hrefs from userpage
    def get_list_of_hrefs(self, username):  # username = account name we need
        try:
            # open userpage website
            self.browser.get(f'https://www.instagram.com/{username}/')
            time.sleep(5)
            # find all <a> on the page
            hrefs = self.browser.find_elements_by_tag_name('a')
            list_of_hrefs = []
            for i in hrefs:
                # extract links from the tag's attribute
                href = i.get_attribute('href')
                if '/p/' in href:
                    list_of_hrefs.append(href)
            return list_of_hrefs
        # if smth went wrong, close the browser
        except Exception as ex:
            print(ex)

    def download_videos(self, username):
        try:
            hrefs = self.get_list_of_hrefs(username)
            for post_url in hrefs:
                self.browser.get(post_url)
                time.sleep(4)
                video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
                post_id = post_url.split("/")[-2]
                video_src_urls = []

                if self.xpath_exists(video_src):
                    video_src_url = self.browser.find_element_by_xpath(video_src).get_attribute("src")
                    video_src_urls.append(video_src_url)

                    # save video
                    video = requests.get(video_src_url, stream=True)
                    with open(f"{post_id}_video.mp4", "wb") as video_file:
                        for chunk in video.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                video_file.write(chunk)
                else:
                    video_src_urls.append(f"{post_url}, no link!")
                print(f"{post_url} successfully saved!")

                self.close_browser()
        except Exception as ex:
            print(ex)
            self.close_browser()


parser = Parser(username, password)
parser.login()
parser.download_videos('funnyvideos')
