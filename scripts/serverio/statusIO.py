import os
from util.jsonObject import *

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
    '''Provides methods to read/write to server status files. This file is
        then given to the server as json to be returned to client so client
        can see server activity.'''
    def __init__(self,path):
        '''Create/truncate file to write to.'''
        self.__statusFileLocation = path    #path to file to be written to
        self.__lineBuff = []                #contains all lines written
        open(self.__statusFileLocation,"w+").close()
        
    def write(self,text):
        '''Writes specified text to file and line buffer.'''
        f = open(self.__statusFileLocation,"a")
        f.write(text)
        f.close()
        self.__lineBuff.append(text)
        
    def readBuff(self,response,lastLine):
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
        if not isinstance(lastLine,int):
            return StatusIOResponse(error="lastLine must be int").serialize()
        lb_len = len(self.__lineBuff)
        lines = ""
        if lastLine < 0:
            f = open(self.__statusFileLocation,"r")
            lines += f.read()
            f.close()
        else:
            if lastLine < lb_len:
                for i in range(lastLine + 1,lb_len):
                    lines += self.__lineBuff[i]
            else:
                return StatusIOResponse(error="lastLine refers to a location beyond EoF").serialize()
        return StatusIOResponse(lastLine=lb_len-1,lines=lines).serialize()

    def getStatusFileLocation(self):
        return self.__statusFileLocation

if __name__ == "__main__":
    pass
