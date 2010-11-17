import os

class StatusIO(object):
    '''Provides methods to read/write to server status files. This file is
        then given to the server to be returned to client so client can see
        server activity'''
    def __init__(self,path):
        '''create/truncate file to write to'''
        self.__statusFileLocation = path    #path to file to be written to
        self.__writeBuffer = []             #stores all lines written since last read
                                            #   need separate one of these for each
                                            #   client connecting
        open(self.__statusFileLocation,"w+").close()

    def write(self,text):
        '''append text to end of status file'''
        f = open(self.__statusFileLocation,"a")
        f.write(text)
        f.close()
        self.__writeBuffer.append(text)

    def read(self):
        '''return entire status file contents'''
        f = open(self.__statusFileLocation,"r")
        ret = f.read()
        f.close()
        self.__writeBuffer = []
        return ret

    def readBuff(self):
        '''return all lines written since last read'''
        ret = ""
        for line in self.__writeBuffer:
            ret += line
        self.__writeBuffer = []
        return ret

    def getStatusFileLocation(self):
        return self.__statusFileLocation

if __name__ == "__main__":
    pass
