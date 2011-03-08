import thread,os,subprocess

from util.dbAccess import *

CPATH = os.path.abspath(__file__).replace("controller.pyc","") \
    .replace("controller.py","")
    
DIR_RESOURCES = os.path.join(CPATH,"../resources")
DIR_HTML = os.path.join(CPATH,"../web")
DIR_JS = os.path.join(DIR_HTML,"js")
DIR_CSS = os.path.join(DIR_HTML,"css")
DIR_FILEOUTPUT = os.path.join(DIR_HTML,"output")
    
DB_FILE = os.path.join(DIR_RESOURCES,"db.sqlite")

PIPELINE_FILE_PATH = os.path.join(CPATH,"../pipeline_script")
PIPELINE_RESULTS_FILE = "resultsOutput.html"
PIPELINE_RESULTS_PATH = os.path.join(DIR_HTML,PIPELINE_RESULTS_FILE)

SIG_KEY_INSTALLER = "installer_complete"
SIG_KEY_PIPELINE = "pipeline_complete"

ERRORS_FILE = os.path.join(CPATH,"../error_trace")

class _Controller(object):
    '''Manages program resources, threads.'''
    
    SIG_KEYS = {SIG_KEY_INSTALLER:False,
           SIG_KEY_PIPELINE:False}
    
    def __init__(self):
        #clear database before use
        dba = DbAccess(DB_FILE)
        dba.executeFromFile(os.path.join(DIR_RESOURCES, "sql/clearDb.sql"))
        dba.closeConn()
        
        #make sure output folder exists
        if not os.path.isdir(DIR_FILEOUTPUT):
            print("Creating output directory...")
            os.mkdir(DIR_FILEOUTPUT)
        
        self.__threads = []
        self.__signals = {}
        
    def startThreading(self,threadInstance):
        '''Starts thread class threadInstance (which must already be 
        instantiated)'''
        threadInstance.start()
        self.__threads.append(threadInstance)
    
    def getThreads(self):
        return tuple(self.__threads)
    
    def getSignals(self):
        return self.__signals
    
    def isAlive(self):
        '''If this is false, none of the threads are running anymore.'''
        alive = True
        for t in self.__threads:
            alive = alive and t.isAlive()
        return alive
    
    def shutdown(self):
        '''Shuts down this instance.'''
        process = subprocess.Popen(["sudo","shutdown","-P","+0"])
        while(process.poll() is None): pass
    
_controller = _Controller()
    
def Controller(): return _controller

def cprint(text):
    '''For threads to print to top console.'''
    print(text)
    