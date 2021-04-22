from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql.functions import modifier
from sqlalchemy.sql.sqltypes import Boolean

from .db_config import Mysql_config


Base = declarative_base()


# 用户表模型
class Tweet(Base):
    """[define tweet data table]
    Args:
        Base ([class]): [base class]
    """

    __tablename__ = "tweet_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(64))
    user_id = Column(String(64))
    following = Column(Integer(), default=0)
    followers = Column(Integer(), default=0)
    date = Column(String(64))
    content = Column(Text)
    reply = Column(Integer(), default=0)
    retweet = Column(Integer(), default=0)
    like = Column(Integer(), default=0)
    modify_tag = Column(Boolean(),default=False)

    def __init__(self, user_name, user_id, date, content, reply=0, retweet=0, like=0, following=0, followers=0, modify_tag=False):
        self.user_name = user_name
        self.user_id = user_id
        self.following = following
        self.followers = followers
        self.date = date
        self.content = content
        self.reply = reply
        self.retweet = retweet
        self.like = like
        self.modify_tag = modify_tag

class DataAccess:
    """[access to MysqlDB to process data]
    """

    def __init__(self):
        self.engine = None
        self.Session = None
        self.session = None

    def connect(self):
        """[connect to MysqlDB]
        """
        self.engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset=utf8".format(Mysql_config["username"],Mysql_config["pwd"], Mysql_config["host"], Mysql_config["schema"]),
                       #echo=True,  #测试使用
                       pool_size=8,
                       pool_recycle=60*30)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_data(self, content):
        """[insert tweet data to MysqlDB]

        Args:
            content ([class]): [Object of Tweet class]
        """
        self.session.add(content)

    def query(self):
        """[query data from MysqlDB]

        Returns:
            [list]: [query data]
        """
        data = self.session.query(Tweet).all()
        return data
        

MysqlDAL = DataAccess()


if __name__ == '__main__':
    tweet = DataAccess()
    tweet.connect()
    #content = Tweet("3","5","3","4",1,2,3,4,5)
    #tweet.add_data(content)
    tweet.query()

    #tweet.session.commit()


