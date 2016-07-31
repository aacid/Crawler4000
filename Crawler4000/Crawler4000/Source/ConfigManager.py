import ConfigParser
import os.path

class ConfigManager(object):
    """manages config file"""
    MAIN_FILE = 'main.cfg'
    FB_SECTION = 'FacebookLogin'
    FB_USERNAME = 'username'
    FB_PASSWORD = 'password'
    FB_FULLNAME = 'fullname'

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
        self.config.add_section(self.FB_SECTION)
        self.config.set(self.FB_SECTION, self.FB_USERNAME, '_DUMMY_USER_')
        self.config.set(self.FB_SECTION, self.FB_PASSWORD, '_DUMMY_PASS_')
        self.config.set(self.FB_SECTION, self.FB_FULLNAME, '_DUMMY_NAME_')
        
        with open(self.MAIN_FILE, 'wb') as configfile:
            self.config.write(configfile)

    def getFBLogin(self):
        if self.config.has_option(self.FB_SECTION, self.FB_USERNAME):
            return self.config.get(self.FB_SECTION, self.FB_USERNAME)

    def getFBPassword(self):
        if self.config.has_option(self.FB_SECTION, self.FB_PASSWORD):
            return self.config.get(self.FB_SECTION, self.FB_PASSWORD)
    def getFBFullname(self):
        if self.config.has_option(self.FB_SECTION, self.FB_FULLNAME):
            return self.config.get(self.FB_SECTION, self.FB_FULLNAME)