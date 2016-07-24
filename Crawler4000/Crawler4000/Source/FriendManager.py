import sys, re
from source.Profile import Profile
from bs4 import BeautifulSoup

class FriendManager(object):
    """manages all profiles scraped"""

    def __init__(self, id):
        self.id = id
        self.profiles = []

    def addProfile(self, profile):
        self.profiles.add(profile)

    def addProfile(self, id, name):
        profile = Profile(id, name)
        self.profiles.append(profile)

    def getFriends(self, browser):

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
            self.addProfile(fbid, name)

        print "scraped " + str(counter) + ", could not scrape " + str(locked) + " profiles"
        
    def save(self, db):
        db.setPersonScraped(self.id, True)

        print "saving " + str(len(self.profiles)) + " profiles"
        if len(self.profiles) == 0:
            return

        try:
            for profile in self.profiles:
                db.createConnection(self.id, profile.id)
                profile.save(db)
        except:
            print("Unexpected error:", sys.exc_info()[0])
        db.Commit()

