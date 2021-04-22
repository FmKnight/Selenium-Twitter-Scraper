from redis import Redis
from .dbconfig import Redis_config

class UserInfo:
    """[use redis to check whether tweet is scraped or not]
    """

    def __init__(self):
        self.db = None
        self.Table = ""

    def connect(self):
        """[connect to redis]
        """
        self.db = Redis(host=Redis_config["host"], password=Redis_config["pwd"], port=Redis_config["port"], 
                        db=Redis_config["schema"], decode_responses=True)
        self.Table = 'twitter'

    def addDigest(self, tweet_digest):
        """[add tweet digest to 'twitter']
        Args:
            tweet_digest ([str]): [sha256 digest of tweet]
        """
        self.db.sadd(self.Table, tweet_digest)

    def IsDuplicate(self, tweet_digest):
        """[check whether tweet has scraped or not]
        Args:
            tweet_digest ([str]): [sha256 digest of tweet]
        Returns:
            [Bool]: [return True if tweet digest in Redis set else False]
        """
        return self.db.sismember(self.Table, tweet_digest)


RedisDAL = UserInfo()

if __name__ == '__main__':
    usr = UserInfo()
    usrinfo = usr.IsDuplicate("hello,world")
    print(usrinfo)
