import sqlite3
from Exceptions import NoMoreDataException

class DBManager(object):
    """manages all interaction with DB"""

    tables = ['People', 'Friends']

    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.c = self.conn.cursor()

        self.checkConsistency()

    def __del__(self):
        self.conn.commit()
        self.c.close()

    def createTable(self, name):
        if name == 'People':
            self.c.execute("""CREATE TABLE `People` (
                                `id`	TEXT NOT NULL UNIQUE,
                                `Name`	TEXT,
                                `ProfileScrapped`	TEXT DEFAULT 'N',
                                `FriendsScrapped`	TEXT DEFAULT 'N',
                                PRIMARY KEY(id)
                            );""")
        elif name == 'Friends':
            self.c.execute("""CREATE TABLE `Friends` (
                                `Person`	TEXT NOT NULL,
                                `Friend`	TEXT NOT NULL,
                                PRIMARY KEY(Person,Friend)
                            );""")

    def checkConsistency(self):
        for table in self.tables:
            self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if self.c.fetchone() == None:
                self.createTable(table)


    def addPerson(self, id, name):
        try:
            self.c.execute("INSERT INTO People VALUES (?, ?)", (id, name))
        except sqlite3.IntegrityError:
            pass

    def getPersonWithNoProfile():
        self.c.execute("SELECT id FROM People WHERE ProfileScrapped = 'N' LIMIT 1")
        result = self.c.fetchone()
        if result == None:
            raise NoMoreDataException
        return result
    
    def getPersonWithNoFriends():
        self.c.execute("SELECT id FROM People WHERE FriendsScrapped = 'N' LIMIT 1")
        result = self.c.fetchone()
        if result == None:
            raise NoMoreDataException
        return result
        