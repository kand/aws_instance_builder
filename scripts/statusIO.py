import os

class StatusIO(object):
    '''Provides methods to read/write to server status files. This file is
        then given to the server as json to be returned to client so client
        can see server activity'''
    def __init__(self,path):
        '''create/truncate file to write to'''
        self.__statusFileLocation = path    #path to file to be written to
        self.__lineBuff = []
        open(self.__statusFileLocation,"w+").close()
        
    def write(self,text):
        '''writes specified text to file and line buffer'''
        f = open(self.__statusFileLocation,"a")
        f.write(text)
        f.close()
        self.__lineBuff.append(text)
        
    def readBuff(self,response,lastLine):
        '''return all lines since lastLine'''
        response.set_content_type("application/json")
        try:
            lastLine = int(lastLine)
        except TypeError:
            return "{\"error\":\"lastLine must be int\"}"
        ret = "{\"lastLine\":" + str(len(self.__lineBuff)-1)
        ret += ",\"lines\":\""
        if lastLine < 0:
            f = open(self.__statusFileLocation,"r")
            ret += f.read()
            f.close()
        else:
            l = len(self.__lineBuff)
            if lastLine < l:
                for i in range(lastLine + 1,l):
                    ret += self.__lineBuff[i]
        return ret + "\"}"

    def getStatusFileLocation(self):
        return self.__statusFileLocation

if __name__ == "__main__":
    pass
