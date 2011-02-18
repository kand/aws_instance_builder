import os,traceback

from sqlite3 import OperationalError

from util.jsonObject import *
from util.dbAccess import *
from controller import Controller,cprint,DB_FILE

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

class StatusIO():
    '''Provides methods to read/write to server status db table.'''
    
    __DB_TABLE_STATUS = "status"
    __MAX_LINE_OUTPUT = 100     #specifies the maximum number of lines that should
                                #    be sent to client. This will prevent issues
                                #    where a program has output more lines than
                                #    can be properly be sent across the network
        
    @staticmethod
    def write(text):
        '''Writes specified text to db.
            
            dbPath = path to database file
            text = text to write'''
        dba = DbAccess(DB_FILE)
        
        vals = text.split("\n")
        pcount = 0
        for s in vals:
            sql = "INSERT INTO " + StatusIO.__DB_TABLE_STATUS + "(value)"
            key = "line%i" % pcount
            sql += " VALUES (:%s)" % key
            
            try:
                dba.execute(sql,True,{key:"%s\n" % s})
            except OperationalError:
                cprint("[DB_WRITE] [ERROR] a process has the database locked.")
                dba.closeConn()
                return
        
        dba.closeConn()
        cprint("[DB_WRITE] {{ %s }}" % text)
        
    @staticmethod
    def read(response,lastLine):
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
        dba = DbAccess(DB_FILE)
        sql = "SELECT id,value FROM " + StatusIO.__DB_TABLE_STATUS \
            + " WHERE id > :lastLine LIMIT " + str(StatusIO.__MAX_LINE_OUTPUT)
        params = {"lastLine":lastLine}
            
        try:
            c = dba.execute(sql,False,params)
        except OperationalError:
            cprint("[DB_READ] [ERROR] a process has the database locked.")
            dba.closeConn()
            return StatusIOResponse(error="A process has the database locked.\n").serialize()
            
        for r in c:
            lastLine = r["id"]
            lines += r["value"]
    
        dba.closeConn()
        cprint("[DB_READ] {{ %s }}" % lines)
        
        return StatusIOResponse(lastLine=lastLine,lines=lines).serialize()

def redirectExceptions(f):
    '''Function decorator to catch thread exceptions and print to main output.
    This decorator should be put before all run() functions in threads that
    are to be threaded through Controller. This makes error catching a lot
    easier.'''
    def wrap(self,*args,**kwargs):
        try:
           return f(self,*args,**kwargs)
        except:
           cprint(traceback.print_exc())
           StatusIO.write(traceback.print_exc())
           return None
    return wrap

if __name__ == "__main__":
    pass
