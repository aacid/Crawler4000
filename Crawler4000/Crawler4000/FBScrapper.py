import mechanize
from bs4 import BeautifulSoup

class FBScrapper(object):
    """description of class"""
    def __init__(self, fbLogin, fbPassword):
        self.login = fbLogin
        self.password = fbPassword

    def login(self):
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        cookies = mechanize.CookieJar()
        browser.set_cookiejar(cookies)
        browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
        browser.set_handle_refresh(False)

        url = "https://m.facebook.com/login.php"
        browser.open(url)
        browser.select_form(nr = 0)       #This is login-password form -> nr = number = 0
        browser.form['email'] = login
        browser.form['pass'] = password
        browser.submit()

        response = browser.open('https://m.facebook.com/friends/center/friends')
        #print response.read()

        soup = BeautifulSoup(response.read(), "html.parser")
        people = soup.find_all("h3", "_52jh")
        


