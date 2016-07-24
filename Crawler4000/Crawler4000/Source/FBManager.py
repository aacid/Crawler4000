import mechanize, re, sys
from bs4 import BeautifulSoup
from FriendManager import FriendManager
from Exceptions import CouldNotReadProfile
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
        self.browser.submit()

    def getPage(self, page):
        response = self.browser.open(page)
        return response.read()
        
    def crawl(self):
        counter = 0
        while counter < 1000:
            person_id = self.db.getPersonWithNoFriends()
            if person_id == None:
                return
            counter += 1
            self.scrapeFriends(person_id[0])

    def scrapeFriends(self, id):
        person = FriendManager(id)
        person.getFriends(self.browser)
        person.save(self.db)

    def scrapeProfiles(self):
        counter = 0
        while counter < 1000:
            person_id = self.db.getPersonWithNoFriends()
            if person_id == None:
                return
            counter += 1
            self.scrapeFriends(person_id[0])

    def addProfile(self, id, name):
        self.db.addPerson(id, name)
        
