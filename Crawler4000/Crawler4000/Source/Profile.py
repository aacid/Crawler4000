from bs4 import BeautifulSoup
import re
class Profile(object):
    """description of class"""

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.scraped = False
        self.friends_scraped = False
        self.workplaces = []
        self.education = []
        self.living = []
        self.contacts = []
        self.basic_info = []
        
    @staticmethod
    def loadProfile(id, db):
        name, profile_scraped, friends_scraped = db.getProfile(id)

        profile = Profile(id, name)
        profile.scraped = profile_scraped == 'Y'
        profile.friends_scraped = friends_scraped == 'Y'
        return profile
    
    def save(self, db):
        db.addProfile(self.id, self.name)
        
        if self.scraped:
            info_list = []

            for workplace in self.workplaces:
                info_list.append(('Workplace', '', workplace))

            for edu in self.education:
                info_list.append(('Education', '', edu))

            for name, value in self.living:
                info_list.append(('Living', name, value))

            for name, value in self.contacts:
                info_list.append(('Contact', name, value))

            for name, value in self.basic_info:
                info_list.append(('BasicInfo', name, value))

            list = [ (self.id,) + x for x in info_list ]
            db.addDetails(list)
            print "saved " + str(len(list)) + " details"

    def getFriends(self, browser, db):

        print "getting friends of " + self.id
        counter = 0
        locked = 0
        
        profile_links = []
        while True:
            try:
                response = browser.open('https://m.facebook.com/' + self.id + "/friends?startindex=" + str(counter))
                data = response.read()

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
            profile = Profile(fbid, name)            
            profile.save(db)
            profile.setFriendOf(db, self.id)

        db.setFriendsScraped(self.id)
        
        db.Commit()

        print "scraped " + str(counter) + ", could not scrape " + str(locked) + " profiles"

    def scrapeProfile(self, browser):    
        print "scraping profile " + self.id
        if 'profile' in self.id:
            url = 'https://m.facebook.com/' + self.id.replace('?', '?v=info&')
        else:
            url = 'https://m.facebook.com/' + self.id + '/about'  
        try:      
            response = browser.open(url)
            data = response.read()
            self.scrapeAbout(data)
        except:
            pass

        self.scraped = True

    def scrapeAbout(self, data):        
        soup = BeautifulSoup(data, "html.parser")

        #work
        div = soup.find(id='work')
        if div != None:
            spans = div.find_all("span")

            for span in spans:
                if len(span.contents) == 0:
                    continue
                content = span.contents[0]
                while content.name != None:
                    if len(content.contents) == 0:
                        break
                    content = content.contents[0]
                if "Ask" in content or "requested" in content:
                    continue
                self.workplaces.append(content)

        #education
        div = soup.find(id='education')
        if div != None:
            spans = div.find_all('a')

            for span in spans:
                if span.has_attr('class'):
                    continue
                self.education.append(span.contents[0])

        #living
        div = soup.find(id='living')
        if div != None:
            spans = div.find_all("a", href=re.compile(r'profile'))

            for span in spans:
                if "Ask" in span.text or "requested" in span.text:
                    continue
                name = span.parent.parent.parent.parent.parent['title']
                self.living.append((name, span.contents[0]))

        #contact-info
        div = soup.find(id='contact-info')
        if div != None:
            spans = div.find_all('span')
            for span in spans:
                content = span.contents[0]
                if "Ask" in content or "requested" in content:
                    continue
                for sibling in span.parent.parent.next_siblings:
                    if sibling == '\n':
                        continue
                    val = sibling.stripped_strings.next()
                    self.contacts.append((content, val))
                    break
        
        #basic-info
        div = soup.find(id='basic-info')
        if div != None:
            spans = div.find_all('span')
            for span in spans:
                content = span.contents[0]
                if "Ask" in content or "requested" in content:
                    continue
                for sibling in span.parent.parent.next_siblings:
                    if sibling == '\n':
                        continue
                    try:
                        val = sibling.stripped_strings.next()
                    except StopIteration:
                        continue
                    self.basic_info.append((content, val))
                    break

    def setFriendOf(self, db, friend_id):
        db.createConnection(friend_id, self.id)