import mechanize, re
from bs4 import BeautifulSoup
from FriendManager import FriendManager
from Exceptions import CouldNotReadProfile
class FBManager(object):
    """Scrapping data from Facebook"""
    def __init__(self, fbUsername, fbPassword):
        self.username = fbUsername
        self.password = fbPassword
        self.browser = mechanize.Browser()
        self.friends = FriendManager(self)

    def login(self):
        
        self.browser.set_handle_robots(False)
        cookies = mechanize.CookieJar()
        self.browser.set_cookiejar(cookies)
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'),
                                   ('Accept-language', 'en-US,en;q=0.8,sk;q=0.6')]
        self.browser.set_handle_refresh(False)

        url = "https://m.facebook.com/login.php"
        self.browser.open(url)
        self.browser.select_form(nr = 0)       #This is login-password form -> nr = number = 0
        self.browser.form['email'] = self.username
        self.browser.form['pass'] = self.password
        self.browser.submit()

    def getPage(self, page):
        response = self.browser.open(page)
        return response.read()

    def getFriends(self):

        counter = 0   
        
        profile_links = []
        while True:
            response = self.browser.open('https://m.facebook.com/friends/center/friends/?ppk=' + str(counter))

            link = None
            for link in self.browser.links(url_regex=r".*hovercard.*"):
                profile_links.append(link.url)
            
            if link == None:
                break

            counter += 1

        for link in profile_links:
            response = self.browser.open(link)
            fbid = self.getIdFromHoverCard(response.read())
            self.friends.addProfile(fbid[0], fbid[1])


        #friends.save()


    def getIdFromHoverCard(self, card):
        soup = BeautifulSoup(card, "html.parser")
        name = soup.h1.string
        link_tag = soup.find(string=re.compile("View.Profile"))
        match = re.search(r'\/(.*)\?', link_tag.parent.parent['href'])
        if match:
            return ( match.group(1), name)

    def addProfile(self, id):
        self.friends.addProfile(id)
        
