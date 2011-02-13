import thread,os,traceback

from serverio.statusIO import *
from serverio.fileChecker import *

from util.dbAccess import *

class _Controller(object):
    '''Manages program resources, threads.'''
    __cDir = os.path.abspath(__file__).replace("controller.pyc","") \
        .replace("controller.py","")
    
    __DIR_RESOURCES = os.path.join(__cDir,"../resources")
    __DIR_HTML = os.path.join(__cDir,"../web")
    __DIR_JS = os.path.join(__DIR_HTML,"js")
    __DIR_CSS = os.path.join(__DIR_HTML,"css")
    __DIR_FILEOUTPUT = os.path.join(__DIR_HTML,"output")
    
    __DB_FILE = os.path.join(__DIR_RESOURCES,"db.sqlite")
    
    def __init__(self):
        #clear database before use
        dba = DbAccess(self.__DB_FILE)
        dba.executeFromFile(os.path.join(self.__DIR_RESOURCES, "sql/clearDb.sql"))
        dba.closeConn()
        
        #make sure output folder exists
        if not os.path.isdir(self.__DIR_FILEOUTPUT):
            print("Creating output directory...")
            os.mkdir(self.__DIR_FILEOUTPUT)
        
        self.__statusIO = StatusIO(self.__DB_FILE,self.__DIR_RESOURCES)
        self.__fileCheck = fileChecker(self.__DIR_FILEOUTPUT,self.__DB_FILE)
        self.__threads = []
        self.__signals = {}
        
    def startThreading(self,threadInstance):
        '''Starts thread class threadInstance (which must already be 
        instantiated)'''
        threadInstance.start()
        self.__threads.append(threadInstance)
        
    def getResDir(self):
        return self.__DIR_RESOURCES
    
    def getHtmlDir(self):
        return self.__DIR_HTML
    
    def getJsDir(self):
        return self.__DIR_JS
    
    def getCssDir(self):
        return self.__DIR_CSS
    
    def getFileOutDir(self):
        return self.__DIR_FILEOUTPUT
    
    def getThreads(self):
        return tuple(self.__threads)
    
    def getSignals(self):
        return self.__signals
    
    def getFileChecker(self):
        return self.__fileCheck
    
    def isAlive(self):
        '''If this is false, none of the threads are running anymore.'''
        alive = True
        for t in self.__threads:
            alive = alive and t.isAlive()
        return alive
    
    def swrite(self,text):
        '''Hand text to statusIO and write to console.'''
        print("[SUBPROCESS] %s" % text)
        self.__statusIO.write(str(text))
        
    def sread(self,response,lastLine):
        '''Read text from statusIO.'''
        return self.__statusIO.read(response,lastLine)
    
    def getFiles(self,response,lastFileId):
        '''Check output directory for new files.'''
        return self.__fileCheck.getFiles(response,lastFileId)
    
_controller = _Controller()
    
def Controller(): return _controller

def redirectExceptions(f):
    '''Function decorator to catch thread exceptions and print to main output.
    This decorator should be put before all run() functions in threads that
    are to be threaded through Controller. This makes error catching a lot
    easier.'''
    def wrap(self,*args,**kwargs):
        try:
           return f(self,*args,**kwargs)
        except:
           Controller().swrite(traceback.print_exc())
           return None
    return wrap
    