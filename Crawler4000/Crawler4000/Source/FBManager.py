import mechanize, re, sys
from bs4 import BeautifulSoup
from source.Profile import Profile

class FBManager(object):
    """Scraping data from Facebook"""
    def __init__(self, db):
        self.db = db
        self.browser = mechanize.Browser()
        #self.friends = FriendManager()

    def login(self, fb_username, fb_password):
        self.browser.set_handle_robots(False)
        cookies = mechanize.CookieJar()
        self.browser.set_cookiejar(cookies)
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'),
                                   ('Accept-language', 'en-US,en;q=0.8,sk;q=0.6')]
        self.browser.set_handle_refresh(False)

        url = "https://m.facebook.com/login.php"
        self.browser.open(url)
        self.browser.select_form(nr = 0)       #This is login-password form -> nr = number = 0
        self.browser.form['email'] = fb_username
        self.browser.form['pass'] = fb_password
        request = self.browser.submit()
        data = request.read()
        soup = BeautifulSoup(data, "html.parser")        
        root = soup.find(id='root')
        if u'The email or phone number you\u2019ve entered doesn\u2019t match any account. ' in root.strings:
            print 'Logging into Facebook with username ' + fb_username + ' failed. Change login information in main.cfg.'
            return False
        username_tag = soup.find('a', string=re.compile(r'Profile'))
        match = re.search(r'\/(.*)\?', username_tag['href'])
        if match:
            username = match.group(1)
        logout_tag = soup.find('a', href=re.compile(r'logout.php'))
        match = re.search(r'\((.*)\)', logout_tag.contents[0])
        if match:
            name = match.group(1)
        print 'Successfuly logged into Facebook as user ' + name + '.'

         
        self.db.addProfile(username, name)
        self.db.setProfileScraped(username)

        return True
                
    def scrapeFriendsRecursively(self, limit):
        counter = 0
        print 'Getting friends of first ' + str(limit) + ' profiles.'
        while counter < limit:
            profile_id = self.db.getProfileWithNoFriends()
            if profile_id == None:
                return
            counter += 1
            print 'Profile #' + str(counter) + ':'
            profile = Profile.loadProfile(profile_id, self.db)
            profile.getFriends(self.browser, self.db)
            
    def scrapeProfiles(self):
        counter = 0
        while True:
            profile_id = self.db.getProfileWithNoDetails()
            if profile_id == None:
                return
            counter += 1
            profile = Profile.loadProfile(profile_id, self.db)
            profile.scrapeProfile(self.browser)
            profile.save(self.db)
            self.db.setProfileScraped(profile_id)
            self.db.Commit()
        
