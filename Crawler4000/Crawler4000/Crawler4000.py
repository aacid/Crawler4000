from source.ConfigManager import ConfigManager
from source.DBManager import DBManager
from source.FBManager import FBManager
from source.FriendManager import FriendManager

class Crawler4000(object):
    def __init__(self):
        self.config = ConfigManager()
        self.db = DBManager()
        self.scraper = FBManager(self.db)
        self.initScraper()

    def initScraper(self):
        login = self.config.getFBLogin()
        password = self.config.getFBPassword()

        
        self.scraper.login(login, password)
        self.scraper.addProfile('ooliver', 'Oliver Cernansky')
        self.scraper.crawl()
        #self.scraper.scrapeProfiles()
diplo = Crawler4000()