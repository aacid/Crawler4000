from ConfigManager import ConfigManager
from DBManager import DBManager
from FBManager import FBManager

class Crawler4000(object):
    def __init__(self):
        self.config = ConfigManager()
        self.db = DBManager()
        initScrapper()

    def initScrapper(self):
        login = self.config.getFBLogin()
        password = self.config.getFBPassword()

        self.scrapper = FBManager(login, password)

diplo = Crawler4000()