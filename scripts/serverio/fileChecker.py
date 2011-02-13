import os

from util.jsonObject import *
from util.dbAccess import *

class fileCheckResponse(JSONObject):
    def __init__(self,error="",files=[]):
        self.__json__error = error
        self.__json__files = files
        
    def getError(self):
        return self.__json__error
    def setError(self,val):
        self.__json__error = val
    def getFiles(self):
        return self.__json__files
    def setFiles(self,val):
        self.__json__files = val
        
class fileChecker(object):
    '''Provides methods to get any files currently in the output directory.
    Based on database. Pipelines can send special command to program to add
    file entries to database.'''
    
    __DB_TABLE_PIPELINEFILES = "pipelinefiles"
    
    def __init__(self,outputDir,dbPath):
        self.__outputDir = outputDir
        self.__dbPath = dbPath
    
    def getFiles(self,response,lastFileId):
        '''Return JSON with any files in the output directory.
        
            response   - the http response object pass in from quixote.
            lastFileId - id of the last file the client has
            
            JSON returned has the following values:
            
            error    - populated only if an error has occured.
            files - a dictionary of files the client should display. The
                dictionary key is the name of the file to display, the value is
                a tuple = (fileId,filePath,fileDescription)'''
        response.set_content_type("application/json")
        try:
            lastFileId = int(lastFileId)
        except ValueError:
            return fileCheckResponse(error="lastFileId must be int\n").serialize()
        
        dba = DbAccess(self.__dbPath)
        sql = "SELECT * FROM " + self.__DB_TABLE_PIPELINEFILES \
            + " WHERE id > :lastFileId"
        params = {"lastFileId":lastFileId}
        
        c = dba.execute(sql,False,params)
        
        files = []
        
        for r in c:
            files.append({"id":r["id"],"name":r["name"],"path":r["path"],"desc":r["description"]})
        
        dba.closeConn()
        return fileCheckResponse(files=files).serialize()
    
    def addFile(self,name,path,description):
        '''Called through a command called by pipeline scripts. This will add a file
        path to the database that can then be served to the client.'''
        dba = DbAccess(self.__dbPath)
        sql = "INSERT INTO " + self.__DB_TABLE_PIPELINEFILES \
            + "(name,path,description) VALUES (:name,:path,:description)"
        params = {"name":name,"path":path,"description":description}
        
        dba.execute(sql,True,params)
        
        dba.closeConn()
        