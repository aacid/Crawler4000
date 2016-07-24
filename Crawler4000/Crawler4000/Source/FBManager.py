import mechanize, re, sys
from bs4 import BeautifulSoup
from FriendManager import FriendManager
from Exceptions import CouldNotReadProfile
class FBManager(object):
    """Scrapping data from Facebook"""
    def __init__(self, db):
        self.db = db
        self.browser = mechanize.Browser()
        self.friends = FriendManager()

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

    def getFriendsFromProfile(self, id):

        counter = 0
        locked = 0
        
        profile_links = []
        while True:
            try:
                response = self.browser.open('https://m.facebook.com/' + id + "/friends?startindex=" + str(counter))
                data = response.read()
                link = None

                soup = BeautifulSoup(data, "html.parser")
                soup = soup.find(id='objects_container')
                tables = soup.find_all('tbody')

                if len(tables) == 0:
                    break
                for table in tables:
                    link = table.find('a')
                    if link.has_attr('href'):
                        profile_links.append((unicode(link.contents[0]), link['href']))
                    else:
                        locked += 1
                    counter += 1
                #for link in self.browser.links(url_regex=r".*hovercard.*"):
                #    profile_links.append(link.url)        
                #    counter += 1
            except:
                print("Unexpected error:", sys.exc_info()[0])
            
        for name, link in profile_links:
            if "profile.php" in link:
                match = re.search(r'\/(.*)\&', link)
            else:
                match = re.search(r'\/(.*)\?', link)
            if match:
                fbid = match.group(1)
            else:
                fbid = ''
            self.friends.addProfile(fbid, name)


        self.friends.save(self.db)


    def getIdFromHoverCard(self, card):
        soup = BeautifulSoup(card, "html.parser")
        #name = soup.h1.string
        link_tag = soup.find(string=re.compile("View.Profile"))
        match = re.search(r'\/(.*)\?', link_tag.parent.parent['href'])
        if match:
            return match.group(1)

    def addProfile(self, id):
        self.friends.addProfile(id)
        
