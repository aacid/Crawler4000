from bs4 import BeautifulSoup
import re
from source.DBManager import DBManager
class Profile(object):
    """description of class"""

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.scrapped = False
        self.friends_scrapped = False
        self.workplaces = []
        self.education = []
        self.living = []
        self.contacts = []
        self.basic_info = []
    
    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def isScrapped(self):
        return self.scrapped

    def save(self, db):
        if not self.scrapped:
            db.addPerson(self.id, self.name)
        else:
            db.addPerson(self.id, self.name, True)

            info_list = []

            for workplace in self.workplaces:
                info_list.append(('Workplace', '', workplace))

            for edu in self.education:
                info_list.append(('Education', '', edu))

            for liv in self.living:
                info_list.append(('Living', '', liv))

            for contact in self.contacts:
                info_list.append(('Contact', contact[0], contact[1]))

            for basic in self.basic_info:
                info_list.append(('BasicInfo', basic[0], basic[1]))

            db.addPersonalInfo(self.id, info_list)


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
                self.basic_info.append((content, val))
                break