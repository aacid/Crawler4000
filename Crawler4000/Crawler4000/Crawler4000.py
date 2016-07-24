from source.ConfigManager import ConfigManager
from source.DBManager import DBManager
from source.FBManager import FBManager
from source.FriendManager import FriendManager

class Crawler4000(object):
    def __init__(self):
        self.config = ConfigManager()
        self.db = DBManager()
        self.initScrapper()

    def initScrapper(self):
        login = self.config.getFBLogin()
        password = self.config.getFBPassword()

        self.scrapper = FBManager(login, password)
        #self.scrapper.login()
        #self.scrapper.getFriends()
        self.friends = FriendManager(self.scrapper)
        self.friends.addProfile('martin.lukacka')

diplo = Crawler4000()
diplo.initScrapper()