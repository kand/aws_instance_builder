import os

from util.jsonObject import *

class fileCheckResponse(JSONObject):
    def __init__(self,error="",newFiles={}):
        self.__json__error = error
        self.__json__newFiles = newFiles
        
    def getError(self):
        return self.__json__error
    def setError(self,val):
        self.__json__error = val
    def getNewFiles(self):
        return self.__json__newFiles
    def setNewFiles(self,val):
        self.__json__newFiles = val
        
class newFileObj:
    def __init__(self,name,id,path,desc):
        self.name = name
        self.id = id
        self.path = path
        self.desc = desc
    def getTup(self):
        return [name,tuple([id,path,desc])]
        
class fileChecker(object):
    '''Provides methods to check output directory for new files to be served to
    the webpage for download.'''
    
    def __init__(self,outputDir):
        self.__outputDir = outputDir
    
    def checkFiles(self,response,lastFileId):
        '''Return JSON with any new files that have been put into the output
        directory since the last update.
        
            response   - the http response object pass in from quixote.
            lastFileId - the id of the last file given to the client.
            
            JSON returned has the following values:
            
            error    - populated only if an error has occured.
            newFiles - a dictionary of new files the client should display. The
                dictionary key is the name of the file to display, the value is
                a tuple = (fileId,filePath,fileDescription)'''
        response.set_content_type("application/json")
        fileDict = {}
        
        
        #get files in directory
        #compare to database
        #add any new files to database
        #return all files since lastFileId
        
        return fileCheckResponse(newFiles=fileDict).serialize()
        