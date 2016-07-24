from source.Profile import Profile

class FriendManager(object):
    """manages all profiles scrapped"""

    def __init__(self):
        self.profiles = []

    def addProfile(self, profile):
        self.profiles.add(profile)

    def addProfile(self, id, name):
        profile = Profile(id, name)
        #profile.scrapeProfile(self.scrapper)
        self.profiles.append(profile)

    def save(self, db):
        if len(self.profiles) == 0:
            return

        for profile in self.profiles:
            profile.save(db)

