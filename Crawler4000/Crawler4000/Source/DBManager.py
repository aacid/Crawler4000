import sqlite3
from source.Exceptions import NoMoreDataException

class DBManager(object):
    """manages all interaction with DB"""

    tables = ['People', 'Friends', 'PersonalInfo']

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
        elif name == 'PersonalInfo':
            self.c.execute("""CREATE TABLE `PersonalInfo` (
                                `IdPerson`	TEXT NOT NULL,
                                `Type`	TEXT NOT NULL,
                                `Name`	TEXT,
                                `Info`	TEXT NOT NULL,
                                PRIMARY KEY(IdPerson,Type,Info)
                            );""")

    def checkConsistency(self):
        for table in self.tables:
            self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if self.c.fetchone() == None:
                self.createTable(table)


    def Commit(self):
        self.conn.commit()

    def addPerson(self, id, name, scrapped = False):
        if scrapped:
            is_scrapped = 'Y'
        else:
            is_scrapped = 'N'
        try:
            self.c.execute("INSERT OR IGNORE INTO People (id, Name, ProfileScrapped) VALUES (?, ?, ?)", (id, name, is_scrapped))
        except sqlite3.Error as er:
            print 'er:', er.message

    def addPersons(self, list):
        query =  "INSERT OR IGNORE INTO People VALUES"
        for person in list:
            query += " (" + list[0] + ", " + list[1] + "),"
        query = query[:-1] + ";"

        try:
            self.c.execute(query)
        except sqlite3.Error as er:
            print 'er:', er.message

    def createConnection(self, id, friend):
        try:
            self.c.execute("INSERT OR IGNORE INTO Friends (Person, Friend) VALUES (?, ?)", (id, friend))
        except sqlite3.Error as er:
            print 'er:', er.message

    def setPersonFriendScrapped(self, id):
        try:
            self.c.execute("UPDATE People SET FriendsScrapped = 'Y' WHERE id = ?", (id,))
        except sqlite3.Error as er:
            print 'er:', er.message

    def getPersonWithNoProfile(self):
        self.c.execute("SELECT id FROM People WHERE ProfileScrapped = 'N' LIMIT 1")
        result = self.c.fetchone()
        return result
    
    def getPersonWithNoFriends(self):
        self.c.execute("SELECT id FROM People WHERE FriendsScrapped = 'N' LIMIT 1")
        result = self.c.fetchone()
        return result
        
    def addPersonalInfo(self, person_id, list):
        query =  "INSERT OR IGNORE INTO PersonalInfo (IdPerson, Type, Name, Info) VALUES"
        for person in list:
            query += " (" + person_id + ", " + list[0] + ", " + list[1] + ", " + list[2] + "),"
        query = query[:-1] + ";"

        try:
            self.c.execute(query)
        except sqlite3.Error as er:
            print 'er:', er.message