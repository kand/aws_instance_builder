import thread,os

from serverio.statusIO import *

class _Controller(object):
    '''Manages program resources, threads.'''
    __cDir = os.path.abspath(__file__).replace("controller.pyc","") \
        .replace("controller.py","")
    __STATUS_FILE =  os.path.join(__cDir,"../server_status")
    __DIR_HTML = os.path.join(__cDir,"../web")
    __DIR_JS = os.path.join(__DIR_HTML,"js")
    __DIR_CSS = os.path.join(__DIR_HTML,"css")
    
    def __init__(self):
        self.__statusFile = StatusIO(self.__STATUS_FILE)
        self.__threads = []
        
    def startThreading(self,threadInstance):
        '''Starts thread class threadInstance (which must already be 
        instantiated)'''
        threadInstance.start()
        self.__threads.append(threadInstance)
        
    def getStatusFile(self):
        return self.__statusFile
    
    def getHtmlDir(self):
        return self.__DIR_HTML
    
    def getJsDir(self):
        return self.__DIR_JS
    
    def getCssDir(self):
        return self.__DIR_CSS
    
    def getThreads(self):
        return tuple(self.__threads)
    
    def isAlive(self):
        '''If this is false, none of the threads are running anymore.'''
        alive = True
        for t in self.__threads:
            alive = alive and t.isAlive()
        return alive
    
_controller = _Controller()
    
def Controller(): return _controller
