from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from inst_auth import username, password
import time
import random
import requests


class Parser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome('chromedriver.exe')

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):
        try:
            self.browser.get('https://www.instagram.com/')
            time.sleep(random.randrange(1, 3))
            user_input = self.browser.find_element_by_name('username')
            user_input.clear()
            user_input.send_keys(username)

            time.sleep(random.randrange(2, 4))

            password_input = self.browser.find_element_by_name('password')
            password_input.clear()
            password_input.send_keys(password)

            password_input.send_keys(Keys.ENTER)

            time.sleep(10)
            self.close_browser()
        except Exception as ex:
            print(ex)
            self.close_browser()


parser = Parser(username, password)
parser.login()
parser.close_browser()




# file_manager = FileManager()
# class FileManager:
#     def __init__(self):
#         pass
#
#     def y(self):
#         return 10