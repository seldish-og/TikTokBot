import random

from selenium import webdriver

from tik_tok_auth import username, password

from selenium.webdriver.common.keys import Keys


class TikTokBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("chromedriver.exe")

    def close_browser(self):
        self.browser.close()
        self.browser.quite()

    def add_discription(self):
        list_of_hashtags = ['#meme', '#tranding', '#trand', '#recommendations', '#tranding', '#trand', 
                            '#recommendations', '#wow', '#batman', '#hightechnologies']
        random_quantity = random.randrange(2, 4)
        hashtags = random.sample(list_of_hashtags, random_quantity) # return random unique hashtags from the list
        smiles = []
        text_description = []
        # return 

    def login(self):
        try:
            self.browser.get('https://www.tiktok.com/login/phone-or-email/email')
            time.sleep(random.randrange(2, 4))
            # find the field username
            user_input = self.browser.find_element_by_name('email') 
            # clear the field (just in case)
            user_input.clear()
            # write the username
            user_input.send_keys(username)  

            time.sleep(random.randrange(2, 4))
            # find the field username
            password_input = self.browser.find_element_by_name('password')  
            password_input.clear()
            # write the password
            password_input.send_keys(password)  
            # send the complete authorization form
            password_input.send_keys(Keys.ENTER)  

        except Exeption as ex:
        print(ex)
        self.close_browser()

tik_tok_parser = TikTokBot(username, password)
tik_tok_parser.add_discription()
