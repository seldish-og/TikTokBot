import random

from selenium import webdriver

from tik_tok_auth import username, password


class TikTokBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("chromedriver.exe")

    def add_discription(self):
        list_of_hashtags = ['#meme', '#tranding', '#trand', '#recommendations', '#tranding', '#trand', 
                            '#recommendations', '#wow', '#batman', '#hightechnologies']
        random_quantity = random.randrange(2, 4)
        hashtags = random.sample(list_of_hashtags, random_quantity) # return random unique hashtags from the list
        smiles = []
        text_description = []
        # return 


tik_tok_parser = TikTokBot(username, password)
tik_tok_parser.add_discription()
