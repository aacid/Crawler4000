from source.Profile import Profile

class FriendManager(object):
    """manages all profiles scrapped"""

    def __init__(self, scrapper):
        self.profiles = []
        self.scrapper = scrapper

    def addProfile(self, profile):
        self.profiles.add(profile)

    def addProfile(self, id):
        profile = Profile(id)
        profile.scrapeProfile(self.scrapper)
        self.profiles.append(profile)

