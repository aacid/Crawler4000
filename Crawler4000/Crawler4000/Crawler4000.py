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

        self.scrapper = FBManager(self.db)
        self.scrapper.login(login, password)

        self.scrapper.addProfile('ooliver', 'Oliver Cernansky')
        self.scrapper.crawl()

diplo = Crawler4000()