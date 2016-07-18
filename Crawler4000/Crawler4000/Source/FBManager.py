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

    def login(self):
        
        self.browser.set_handle_robots(False)
        cookies = mechanize.CookieJar()
        self.browser.set_cookiejar(cookies)
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
        self.browser.set_handle_refresh(False)

        url = "https://m.facebook.com/login.php"
        self.browser.open(url)
        self.browser.select_form(nr = 0)       #This is login-password form -> nr = number = 0
        self.browser.form['email'] = self.username
        self.browser.form['pass'] = self.password
        self.browser.submit()

    def getFriends(self):

        counter = 0   
        friends = FriendManager()

        while True:
            response = self.browser.open('https://m.facebook.com/friends/center/friends/?ppk=' + str(counter))

            data = response.read()
            soup = BeautifulSoup(data, "html.parser")
            people = soup.find(id="friends_center_main")
        

            if people.h3.string != 'Friends':
                raise CouldNotReadProfile
            if len(people.contents) < 3:
                break
            for friend in people.contents[2]:
                url = friend.a['href']
                match = re.search(r'\?uid=(\d*)', url)
                if match:
                    url = match.group(1)
                name = friend.a.text
                friends.addProfile(url, name)

            counter += 1

        #friends.save()



        
