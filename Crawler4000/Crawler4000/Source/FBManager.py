import mechanize
from bs4 import BeautifulSoup

class FBManager(object):
    """Scrapping data from Facebook"""
    def __init__(self, fbLogin, fbPassword):
        self.login = fbLogin
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
        self.browser.form['email'] = login
        self.browser.form['pass'] = password
        self.browser.submit()

    def getFriends(self):
        response = self.browser.open('https://m.facebook.com/friends/center/friends')
        #print response.read()

        soup = BeautifulSoup(response.read(), "html.parser")
        people = soup.find_all("h3", "_52jh")
        





