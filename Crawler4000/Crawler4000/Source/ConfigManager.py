import ConfigParser
import os.path

class ConfigManager(object):
    """manages config file"""
    MAIN_FILE = 'main.cfg'
    FB_CONFIG = 'FacebookLogin'
    FB_USERNAME = 'username'
    FB_PASSWORD = 'password'
    MN_CONFIG = 'MainConfig'
    MN_SCRAPE_LIMIT = 'scrape_limit'

    config_read = False

    def __init__(self):        
        print 'Reading data from main.cfg.'
        try:       
            self.config = ConfigParser.ConfigParser()
            if os.path.isfile(self.MAIN_FILE):
                self.config.read(self.MAIN_FILE)
            else:
                self.createConfig()
        except:
            print 'Could not read data from main.cfg.'
            return

        self.config_read = True
    
    def isLoaded(self):
        return self.config_read
            
    def createConfig(self):
        self.config.add_section(self.FB_CONFIG)
        self.config.set(self.FB_CONFIG, self.FB_USERNAME, '_DUMMY_USER_')
        self.config.set(self.FB_CONFIG, self.FB_PASSWORD, '_DUMMY_PASS_')
        self.config.add_section(self.MN_CONFIG)
        self.config.set(self.MN_CONFIG, self.MN_SCRAPE_LIMIT, '1000')
        
        with open(self.MAIN_FILE, 'wb') as configfile:
            self.config.write(configfile)

    def getFBLogin(self):
        if self.config.has_option(self.FB_CONFIG, self.FB_USERNAME):
            return self.config.get(self.FB_CONFIG, self.FB_USERNAME)

    def getFBPassword(self):
        if self.config.has_option(self.FB_CONFIG, self.FB_PASSWORD):
            return self.config.get(self.FB_CONFIG, self.FB_PASSWORD)

    def getScrapeLimit(self):
        if self.config.has_option(self.MN_CONFIG, self.MN_SCRAPE_LIMIT):
            value = self.config.get(self.MN_CONFIG, self.MN_SCRAPE_LIMIT)
            try:
                return int(value)
            except:
                print 'Error reading scrape limit from config, not an number'