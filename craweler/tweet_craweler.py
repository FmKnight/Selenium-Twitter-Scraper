import sys
sys.path.append("/Users/knight/Docs/Program/Selenium-Twitter-Scraper")

from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
import re

from db_settings.RedisDB import RedisDAL
from db_settings.MysqlDB import Tweet, MysqlDAL
from utils.content_filter import filter_emoji, count
from utils.date_generator import time_span_generator
from utils.hash_digest import msg_digest
from  utils.logger_generator import logger


class TwitterScraper:
    """[main program of Twitter Scraper]
    """
    def __init__(self):
        self.url_list = []
        self.scraped_url_list = []
        self.browser = None
        self.MysqlDAL = MysqlDAL   # MysqlDB Access Layer
        self.RedisDAL = RedisDAL   # RedisDB Access Layer
        self.MysqlDAL.connect()    # connect to MysqlDB
        self.RedisDAL.connect()    # connect to RedisDB


    def Chrome_activate(self):
        """[activate chrome web driver]
        """
        options = webdriver.ChromeOptions()
        options.add_argument('blink-settings=imagesEnabled=false')
        self.browser = webdriver.Chrome(options=options)

    def get_url_list(self,*args):
        """[add url to url_list]
        """
        self.url_list.extend(args)

    def scroll(self):
        """[simulate scroll down]
        """
        start_height = 0 # initial Height
        cur_height_js = 'return document.body.scrollHeight'                  # js of get current page height
        scroll_js = 'window.scrollTo(0, document.body.scrollHeight)'         # js of scroll page
        while (self.browser.execute_script(cur_height_js) > start_height):
            start_height = self.browser.execute_script(cur_height_js)
            self.browser.execute_script(scroll_js)
            self.parse()                                                     # get page source data
            time.sleep(8)                                                    # set time between two scrape procedure

    def parse(self):
        """[get page source data]
        """
        content = bs(self.browser.page_source, 'html.parser')
        passages = content.find_all('article',re.compile('css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg'))
        print("Got {} passages of tweet(maybe contain same tweet)".format(len(passages)))
        self.process(passages)


    def process(self, passages):
        """[process passages of data,and save it to mysqlDB]
        Args:
            passages ([bs Object]): [passages once got]
        """

        for passage in passages:
            raw_content = passage.find(
                'div', {'class': 'css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0'})
            # check whether there is content or not
            if raw_content:
                raw_content = raw_content.text
                sha256_digest = msg_digest(raw_content)
                # check whether tweet is duplicate
                if self.RedisDAL.IsDuplicate(sha256_digest):
                    print("this tweet has benn scraped,skip to next one")
                    continue
                else:
                    self.RedisDAL.addDigest(sha256_digest)
                    content = raw_content.rstrip()          # remove newline character
                    content = filter_emoji(content)         # filter emoji
                    user_id = passage.find(
                        'div', {'class': 'css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t'}).get_text()
                    date = passage.find('time')['datetime']
                    # change raw time format("2021-04-12 20:30:31") to exact format("2021-04-12 20:30:31")
                    date = date.replace('T',' ').replace('X','').replace('.000Z','')
                    user_name = passage.find(
                        'div', {'class': 'css-1dbjc4n r-1awozwy r-18u37iz r-dnmrzs'}).get_text()
                    user_name = filter_emoji(user_name)
                    #get heat data(reply, retweet, like) after clean
                    heat_data = passage.find_all(
                    'span', {'class': 'css-901oao css-16my406 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-1e081e0 r-d3hbe1 r-axxi2z r-qvutc0'})
                    reply = count(heat_data[0].text)
                    retweet = count(heat_data[1].text)
                    like = count(heat_data[2].text)
                    self.save_data(user_name, user_id, date, content, reply, retweet, like)
                    print("save data to MysqlDB successfully")
            else:
                print("fail to get tweet from page")
                continue


    def save_data(self, user_name, user_id, date, content, reply, retweet, like):
        """[save tweet data to MysqlDB]
        Args:
            user_name ([str])
            user_id ([str])
            date ([str])
            content ([str])
            reply ([int])
            retweet ([int])
            like ([int])
        """
        tweet = Tweet(user_name, user_id, date, content, reply, retweet, like)
        self.MysqlDAL.add_data(tweet)
        self.MysqlDAL.session.commit()

    def launcher(self):
        """[launch scraper,contain exception process]
        """
        while True:
            try:
                # traverse base urls
                for base_url in self.url_list:
                    # get tweet from specific time span
                    for time_span in time_span_generator:
                        start_date, end_date = time_span
                        url = base_url.format(end_date, start_date)     # make specific urls
                        if url not in self.scraped_url_list:            # judge whether this url is scraped or not
                            self.scraped_url_list.append(url)
                            self.browser.get(url)
                            self.scroll()
                            time.sleep(5)
                        else:
                            continue
            except Exception as e:
                #if there are exceptions, restart program
                logger.exception(e)
                self.Chrome_activate()
                continue



if __name__ == "__main__":
    base_url1 = r"https://twitter.com/search?q=(Facebook%20OR%20Google%20OR%20Amazon%20OR%20Twitter%20OR%20%22Big%20Tech%22%20OR%20%22Giant%20Tech%22)%20AND%20(politics%20OR%20power%20OR%20election%20OR%20influence)%20until%3A{}%20since%3A{}&src=typed_query"
    base_url2 = r"https://twitter.com/search?q=(Facebook%20OR%20Google%20OR%20Amazon%20OR%20Twitter%20OR%20%22Big%20Tech%22%20OR%20%22Giant%20Tech%22)%20AND%20(Pandemic%20OR%20COVID-19)%20until%3A{}%20since%3A{}&src=typed_query"
    tweeter = TwitterScraper()
    tweeter.get_url_list(base_url1,base_url2)
    tweeter.launcher()

