# Selenium Twitter Scraper

This twitter scraper use selenium to crawl data from twitter without authentication.

## Feature

- Use `Redis` to deal with duplicate crawel
- Use `Mysql` to store data
- Use python database ORM `SQLalchemy`

## Install

If you want to use latest version, install from source. To install twitter-scraper from source, follow these steps:

Linux and macOS:

```
git clone git@github.com:FmKnight/Selenium-Twitter-Scraper.git
cd Selenium-Twitter-Scraperhttps://github.com/FmKnight/Selenium-Twitter-Scraper
pip3 install -r requirements.txt
```

## Run
### 1、crawel tweets

`tweet_craweler.py` : run this py file to get specific keywords tweets.Contain following fields:

- user_name
- user_id
- date
- content
- reply
- retweet
- like
![](https://krahets-1304820335.cos.ap-shanghai.myqcloud.com/Github_Repo/Selenium-Twitter-Scraper/crawel_tweet.png)

### 2、crawel user info
`user_info_craweler.py`: run this py file to get specific user's info.Contain following fields:

- following
- followers

![](https://krahets-1304820335.cos.ap-shanghai.myqcloud.com/Github_Repo/Selenium-Twitter-Scraper/crawel_user_info.png)


## Result 

![](https://krahets-1304820335.cos.ap-shanghai.myqcloud.com/Github_Repo/Selenium-Twitter-Scraper/result.png)

# Change Log

### v0.6.1(2021/04/20 21:50)

- Crawel tweets of specific keywords
- Crawel  specific user's info

  