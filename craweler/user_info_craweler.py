import sys
sys.path.append("/Users/knight/Docs/Program/Selenium-Twitter-Scraper")

import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs

from db_settings.MysqlDB import MysqlDAL
from utils.content_filter import count
from  utils.logger_generator import logger

class UserInfoCraweler:

    def __init__(self) -> None:
        self.MysqlDAL = MysqlDAL   # MysqlDB Access Layer
        self.MysqlDAL.connect()    # connect to MysqlDB
        self.browser = None


    def Chrome_activate(self):
        """[activate chrome web driver]
        """
        options = webdriver.ChromeOptions()
        options.add_argument('blink-settings=imagesEnabled=false') # dont load image to make it more fast
        self.browser = webdriver.Chrome(options=options)

    def parse(self):
        """[summary]

        Returns:
            [int, int]: [user's following and followers]
        """
        content = bs(self.browser.page_source, 'html.parser')
        follow_data = content.find_all(
                    'span', {'class': 'css-901oao css-16my406 r-1fmj7o5 r-poiln3 r-b88u0q r-bcqeeo r-qvutc0'})
        if follow_data:
            following = count(follow_data[0].text)   # the num of user's following
            followers = count(follow_data[1].text)   # the num of user's followers
            #print(following, followers)
            return following, followers
        else:
            print("fail to get follow data, may be this user not exists")

    def update(self):
        """[update follow data to MysqlDB]
        """
        users_data = self.MysqlDAL.query()
        for user_data in users_data:
            try:
                if user_data.modify_tag == False:                             # check whether modified or not
                    user_id = user_data.user_id                               # get user_id from MysqlDB
                    user_id = user_id.replace("@","")
                    url = f"https://twitter.com/{user_id}"
                    self.browser.get(url)
                    time.sleep(3)
                    user_data.following, user_data.followers = self.parse()    # update value
                    user_data.modify_tag = True
                    self.MysqlDAL.session.commit()
                    print("save user's follow data to MysqlDB successfully")
                    time.sleep(1)
                else:
                    print("this user's follow data has been got")
                    continue
            except:
                continue

    def launcher(self):
        """[launch scraper]
        """
        for i in range(5):
            try:
                self.Chrome_activate()
                self.update()
                time.sleep(1000)
            except Exception as e:
                logger.exception(e)
                self.browser.close()
                continue
if __name__ == "__main__":
    tweeter = UserInfoCraweler()
    tweeter.launcher()
