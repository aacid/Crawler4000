from source.ConfigManager import ConfigManager
from source.DBManager import DBManager
from source.FBManager import FBManager
from source.FriendManager import FriendManager

class Crawler4000(object):
    def __init__(self):
        print 'Initializing Facebook scraper.'
        self.config = ConfigManager()
        self.db = DBManager()
        if self.db.isConnected():
            self.scraper = FBManager(self.db)
            self.initScraper()

    def initScraper(self):
        if self.config.isLoaded():
            login = self.config.getFBLogin()
            password = self.config.getFBPassword()
        else:
            return

        if self.scraper.login(login, password):
            #self.scraper.scrapeFriendsRecursively(1000)
            self.scraper.scrapeProfiles()
                
diplo = Crawler4000()