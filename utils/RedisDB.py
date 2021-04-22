from redis import Redis
from .db_config import Redis_config

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

    def addUser(self, userinfo):
        """[add user_info(userid,tweet time) to 'twitter']
        Args:
            userinfo ([str]): [contain userid and tweet time]
        """
        self.db.sadd(self.Table, userinfo)

    def IsDuplicate(self,userinfo):
        """[check whether tweet has scraped or not]
        Args:
            userinfo ([str]): [contain userid and tweet time]
        Returns:
            [Bool]: [return bool value]
        """
        return self.db.sismember(self.Table,userinfo)


RedisDAL = UserInfo()

if __name__ == '__main__':
    usr = UserInfo()
    usrinfo = usr.IsDuplicate("hello,world")
    print(usrinfo)
