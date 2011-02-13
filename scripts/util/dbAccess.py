import sqlite3

class DbAccess(object):
    '''Provides methods for creating/accessing db.'''
    
    def __init__(self,dbPath):
        self.__db = dbPath
        self.__conn = None
        
    def openConn(self):
        '''Open db connection to db at dbPath.'''
        if self.__conn is None:
            self.__conn = sqlite3.connect(self.__db)
            self.__conn.row_factory = sqlite3.Row
            
    def closeConn(self):
        '''Commit changes, close current db connection and cursor.'''
        if self.__conn is not None:
            self.__conn.commit()
            self.__conn.close()
            self.__conn = None
        
    def execute(self,sql,nonQuery=False,params={}):
        '''Execute sql on database, nonQuery True will execute sql without
        returning any results, otherwise function returns rows.'''
        self.openConn()
        rows = self.__conn.execute(sql,params)
        if nonQuery:
            self.__conn.commit()
        else:
            return rows
        
    def executeFromFile(self,sqlPath,nonQuery=False,params={}):
        '''Run sql from a file at sqlPath with specified params.'''
        f = open(sqlPath,"r")
        sql = f.read()
        f.close()
        
        self.openConn()
        self.__conn.executescript(sql)
    
if __name__ == "__main__":
    pass