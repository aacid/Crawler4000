from ConfigManager import ConfigManager
from DBManager import DBManager
class Crawler4000(object):
    def __init__(self):
        config = ConfigManager()
        db = DBManager()

diplo = Crawler4000()