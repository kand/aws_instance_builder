from util.jsonObject import *
from util.dbAccess import *

class StatusIOResponse(JSONObject):
    def __init__(self,error="",lastLine=-1,lines=""):
        self.__json__error = error
        self.__json__lastLine = lastLine
        self.__json__lines = lines
        
    def getError(self):
        return self.__json__error
    def setError(self,val):
        self.__json__error = val
    def getLastLine(self):
        return self.__json__lastLine
    def setLastLine(self, val):
        self.__json__lastLine = val
    def getLines(self):
        return self.__json__lines
    def setLines(self,val):
        self.__json__lines = val

class StatusIO(object):
    '''Provides methods to read/write to server status db table.'''
    
    __DB_TABLE_STATUS = "status"
    
    def __init__(self,dbPath):
        self.__dbPath = dbPath
        
    def write(self,text):
        '''Writes specified text to db.'''
        dba = DbAccess(self.__dbPath)
        sql = "INSERT INTO " + self.__DB_TABLE_STATUS + " (value) VALUES (:text)"
        params = {"text":text}
        
        dba.execute(sql,True,params)
        dba.closeConn()
        
    def read(self,response,lastLine):
        '''Return, as json, all lines since lastLine. 
        
            response - the http response object passed in from quixote. 
            lastLine - the last line the client has, a value of -1 means that 
                this is the first request and the entire file contents should 
                be sent.
                
            The json returned has the following variables:
            
            error: this will be present only if an error has occured, the json
                message will contain only this variable and it will have the
                error message
            lastLine: the number of the current last line
            lines: all of the requested lines'''
        response.set_content_type("application/json")
        try:
            lastLine = int(lastLine)
        except ValueError:
            return StatusIOResponse(error="lastLine must be int\n").serialize()
        
        lines = ""
        dba = DbAccess(self.__dbPath)
        sql = "SELECT id,value FROM " + self.__DB_TABLE_STATUS \
            + " WHERE id > :lastLine"
        params = {"lastLine":lastLine}
            
        c = dba.execute(sql,False,params)
            
        for r in c:
            lastLine = r[0]
            lines += r[1]
    
        dba.closeConn()
        return StatusIOResponse(lastLine=lastLine,lines=lines).serialize()

    def getStatusTableName(self):
        return self.__DB_TABLE_STATUS

if __name__ == "__main__":
    pass
