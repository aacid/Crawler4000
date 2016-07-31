import sqlite3

class DBManager(object):
    """manages all interaction with DB"""
    DB_NAME = 'data.db'
    tables = ['Profiles', 'Friends', 'PersonalInfo']
    is_connected = False

    def __init__(self):
        print 'Connecting to database ' + self.DB_NAME + '.'
        try:
            self.conn = sqlite3.connect(self.DB_NAME)
            self.c = self.conn.cursor()
        except sqlite3.Error as er:
            print 'Error connecting to db: ' + er.message
            return

        self.is_connected = True

        self.checkConsistency()

    def __del__(self):
        self.conn.commit()
        self.c.close()

    def isConnected(self):
        return self.is_connected

    def createTable(self, name):
        if name == 'Profiles':
            self.c.execute("""CREATE TABLE `Profiles` (
                                `id`	TEXT NOT NULL UNIQUE,
                                `Name`	TEXT,
                                `ProfileScraped`	TEXT DEFAULT 'N',
                                `FriendsScraped`	TEXT DEFAULT 'N',
                                PRIMARY KEY(id)
                            );""")
        elif name == 'Friends':
            self.c.execute("""CREATE TABLE `Friends` (
                                `IdPerson`	TEXT NOT NULL,
                                `IdFriend`	TEXT NOT NULL,
                                PRIMARY KEY(IdPerson,IdFriend),
                                FOREIGN KEY(`IdPerson`) REFERENCES Profiles(id),
                                FOREIGN KEY(`IdFriend`) REFERENCES Profiles(id)
                            );""")
        elif name == 'PersonalInfo':
            self.c.execute("""CREATE TABLE `PersonalInfo` (
                                `IdPerson`	TEXT NOT NULL,
                                `Type`	TEXT NOT NULL,
                                `Name`	TEXT,
                                `Info`	TEXT NOT NULL,
                                PRIMARY KEY(IdPerson,Type,Info),
                                FOREIGN KEY(`IdPerson`) REFERENCES Profiles(id)
                            );""")

    def checkConsistency(self):
        for table in self.tables:
            self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if self.c.fetchone() == None:
                self.createTable(table)


    def Commit(self):
        counter = 3
        while counter > 0:
            try:
                self.conn.commit()
                break
            except sqlite3.Error as er:
                print 'DB Commit:', er.message
                counter -= 1
        if counter == 0:
            print "DB Error: could not commit."

    def addPerson(self, id, name):
        try:
            self.c.execute("INSERT OR IGNORE INTO Profiles (id, Name) VALUES (?, ?)", (id, name))
        except sqlite3.Error as er:
            print 'AddPerson:', er.message

    def addPersons(self, list):
        query =  "INSERT OR IGNORE INTO Profiles VALUES"
        for person in list:
            query += " (" + list[0] + ", " + list[1] + "),"
        query = query[:-1] + ";"

        try:
            self.c.execute(query)
        except sqlite3.Error as er:
            print 'AddPersons:', er.message

    def createConnection(self, id, friend):
        try:
            self.c.execute("INSERT OR IGNORE INTO Friends (IdPerson, IdFriend) VALUES (?, ?)", (id, friend))
        except sqlite3.Error as er:
            print 'CreateConnection:', er.message

    def setPersonProfileScraped(self, id):
        try:
            self.c.execute("UPDATE Profiles SET ProfileScraped = ? WHERE id = ?", ('Y', id))
        except sqlite3.Error as er:
            print 'SetProfileScraped:', er.message

    def setPersonFriendsScraped(self, id):
        try:
            self.c.execute("UPDATE Profiles SET FriendsScraped = ? WHERE id = ?", ('Y', id))
        except sqlite3.Error as er:
            print 'SetFriendsScraped:', er.message

    def getPerson(self, id):
        self.c.execute("SELECT Name, ProfileScraped, FriendsScraped FROM Profiles WHERE id = ?", (id,))
        result = self.c.fetchone()
        return result
    
    def getPersonInfo(self, id):
        self.c.execute("SELECT * FROM PersonalInfo WHERE IdPerson = ?", (id,))
        return self.c.fetchall()

    def getPersonWithNoProfile(self):
        self.c.execute("SELECT id FROM Profiles WHERE ProfileScraped = 'N' LIMIT 1")
        result = self.c.fetchone()
        return result[0]
    
    def getPersonWithNoFriends(self):
        self.c.execute("SELECT id FROM Profiles WHERE FriendsScraped = 'N' LIMIT 1")
        result = self.c.fetchone()
        return result[0]
        
    def addPersonalInfo(self, person_id, list):
        query =  "INSERT OR IGNORE INTO PersonalInfo (IdPerson, Type, Name, Info) VALUES (?, ?, ?, ?)"

        try:
            self.c.executemany(query, list)
        except sqlite3.Error as er:
            print 'AddPersonalInfo:', er.message