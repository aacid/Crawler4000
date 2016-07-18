class FriendManager(object):
    """manages all profiles scrapped"""

    def __init__(self):
        self.profiles = []

    def addProfile(self, profile):
        self.profiles.add(profile)

    def addProfile(self, id, name):
        profile = Profile(id, name)
        self.profiles.append(profile)


class Profile(object):
    """description of class"""

    def __init__(self, id, name):
        self.id = id
        self.name = name