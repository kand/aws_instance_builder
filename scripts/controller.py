import thread,os

from serverio.statusIO import *

class _Controller(object):
    '''Manages program resources, threads.'''
    __cDir = os.path.abspath(__file__).replace("controller.pyc","") \
        .replace("controller.py","")
    
    __DIR_RESOURCES = os.path.join(__cDir,"../resources")
    __DIR_HTML = os.path.join(__cDir,"../web")
    __DIR_JS = os.path.join(__DIR_HTML,"js")
    __DIR_CSS = os.path.join(__DIR_HTML,"css")
    
    __DB_FILE = os.path.join(__DIR_RESOURCES,"db.sqlite")
    
    def __init__(self):
        self.__statusIO = StatusIO(self.__DB_FILE)
        self.__threads = []
        self.__signals = {}
        
    def startThreading(self,threadInstance):
        '''Starts thread class threadInstance (which must already be 
        instantiated)'''
        threadInstance.start()
        self.__threads.append(threadInstance)
    
    def getHtmlDir(self):
        return self.__DIR_HTML
    
    def getJsDir(self):
        return self.__DIR_JS
    
    def getCssDir(self):
        return self.__DIR_CSS
    
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
    
    def getStatusIO(self):
        return self.__statusIO
    
_controller = _Controller()
    
def Controller(): return _controller
