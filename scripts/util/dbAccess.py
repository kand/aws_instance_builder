import sqlite3

class DbAccess(object):
    '''Provides methods for creating/accessing db.'''
    
    def __init__(self,dbPath):
        self.__db = dbPath
        self.__conn = None
        self.__cursor = None
        
    def openConn(self):
        '''Open db connection to db at dbPath.'''
        if self.__conn is None:
            self.__conn = sqlite3.connect(self.__db)
            
    def closeConn(self):
        '''Commit changes, close current db connection and cursor.'''
        self.closeCursor()
        if self.__conn is not None:
            self.__conn.commit()
            self.__conn.close()
            self.__conn = None
            
    def closeCursor(self):
        '''Close cursor if open.'''
        if self.__cursor is not None:
            self.__cursor.close()
            self.__cursor = None
        
    def execute(self,sql,nonQuery=False,params={}):
        '''Execute sql on database, nonQuery True will execute sql without
        returning any results, otherwise function returns cursor.'''
        self.openConn()
        
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute(sql,params)
        
        if nonQuery:
            self.closeCursor()
        else:
            return self.__cursor
        
    def executeFromFile(self,sqlPath,nonQuery=False,params={}):
        '''Run sql from a file at sqlPath with specified params.'''
        f = open(sqlPath,"r")
        sql = f.read()
        f.close()
        
        self.execute(sql,nonQuery,params)
    
if __name__ == "__main__":
    pass