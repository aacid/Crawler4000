from source.ConfigManager import ConfigManager
from source.DBManager import DBManager
from source.FBManager import FBManager

class Crawler4000(object):
    def __init__(self):
        self.config = ConfigManager()
        self.db = DBManager()
        self.initScrapper()

    def initScrapper(self):
        login = self.config.getFBLogin()
        password = self.config.getFBPassword()

        self.scrapper = FBManager(login, password)
        self.scrapper.login()
        self.scrapper.getFriends()

diplo = Crawler4000()