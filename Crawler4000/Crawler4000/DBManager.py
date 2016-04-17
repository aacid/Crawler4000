import sqlite3

class DBManager(object):
    """manages all interaction with DB"""
    tables = ['People',]
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
    def checkConsistency(self):
        for table in self.tables:
            self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if self.c.fetchone() == None:
                self.createTable(table)