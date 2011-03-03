import os

from sqlite3 import OperationalError
from util.jsonObject import *
from util.dbAccess import *
from controller import cprint,DIR_FILEOUTPUT,DB_FILE

class FileCheckResponse(JSONObject):
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
        
class FileChecker(object):
    '''Provides methods to get any files currently in the output directory.
    Based on database. Pipelines can send special command to program to add
    file entries to database.'''
    
    __DB_TABLE_PIPELINEFILES = "pipelinefiles"
    
    @staticmethod
    def addFile(name,fileName,description):
        '''Called through a command called by pipeline scripts. This will add a file
        path to the database that can then be served to the client.'''
        dba = DbAccess(DB_FILE)
        sql = "INSERT INTO " + FileChecker.__DB_TABLE_PIPELINEFILES \
            + "(name,path,description) VALUES (:name,:fileName,:description)"
        params = {"name":name,"fileName":"output/" + fileName,"description":description}
        
        try:
            dba.execute(sql,True,params)
        except OperationalError:
            cprint("[ERROR] A process has the database locked.")
        
        dba.closeConn()
    
    @staticmethod
    def getFiles(response,lastFileId):
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
        
        dba = DbAccess(DB_FILE)
        sql = "SELECT * FROM " + FileChecker.__DB_TABLE_PIPELINEFILES \
            + " WHERE id > :lastFileId"
        params = {"lastFileId":lastFileId}
        
        try:
            c = dba.execute(sql,False,params)
        except OperationalError:
            cprint("[ERROR] A process has the database locked.")
        
        files = []
        
        for r in c:
            files.append({"id":r["id"],"name":r["name"],"path":r["path"],"desc":r["description"]})
        
        dba.closeConn()
        return FileCheckResponse(files=files).serialize()

        