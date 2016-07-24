from bs4 import BeautifulSoup
import re
class Profile(object):
    """description of class"""

    def __init__(self, id):
        self.id = id
        self.scrapped = False
        self.workplaces = []
        self.education = []
        self.living = []
        self.contacts = []
        self.basicinfo = []

    def isScrapped(self):
        return self.scrapped

    def scrapeProfile(self, scrapper):        
        url = 'https://m.facebook.com/' + self.id + '/about'
        data = scrapper.getPage(url)
        #debug to load profile offline
        #f = open('D:\Dropbox\Projekty\Crawler4000\Crawler4000\Crawler4000\profile.html', 'r')
        data = f.read()
        self.scrapeAbout(data)

    def scrapeAbout(self, data):        
        soup = BeautifulSoup(data, "html.parser")

        #work
        div = soup.find(id='work')
        spans = div.find_all("span")

        for span in spans:
            self.workplaces.append(unicode(span.a.contents))

        #education
        div = soup.find(id='education')
        spans = div.find_all('a')

        for span in spans:
            if span.has_attr('class'):
                continue
            self.education.append(unicode(span.contents))

        #living
        div = soup.find(id='living')
        spans = div.find_all("a")

        for span in spans:
            self.living.append(unicode(span.contents))

        #contact-info
        div = soup.find(id='contact-info')
        spans = div.find_all('span')
        for span in spans:
            content = unicode(span.contents)
            if "Ask" in content or "requested" in content:
                continue
            for sibling in span.parent.parent.next_siblings:
                ty = type(sibling)
                if sibling == '\n':
                    continue
                val = sibling.stripped_strings.next()
                self.contacts.append((content, val))
                break
        
        #basic-info
        div = soup.find(id='basic-info')
        spans = div.find_all('span')
        for span in spans:
            content = unicode(span.contents)
            if "Ask" in content or "requested" in content:
                continue
            for sibling in span.parent.parent.next_siblings:
                if sibling == '\n':
                    continue
                val = sibling.stripped_strings.next()
                self.basicinfo.append((content, val))
                break