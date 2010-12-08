import thread,os

from serverio.statusIO import *
from quixote.server.simple_server import run

class _Controller(object):
    '''Manages program resources, threads.'''
    __cDir = os.path.abspath(__file__).replace("controller.pyc","") \
        .replace("controller.py","")
    __STATUS_FILE =  os.path.join(__cDir,"../server_status")
    __DIR_HTML = os.path.join(__cDir,"../web")
    __DIR_JS = os.path.join(__DIR_HTML,"js")
    __DIR_CSS = os.path.join(__DIR_HTML,"css")
    
    def __init__(self):
        self.__alive = True
        self.__statusFile = StatusIO(self.__STATUS_FILE)
        self.__serverThread = None
        self.__installThread = None
        self.__testThread = None
            
    def startServer(self,publish_func,host,port):
        '''Starts a new thread containing the web server component.'''
        self.__serverThread = thread.start_new_thread(run,tuple([publish_func]),
            {"host":host,"port":port})
        print("server started...")
        print("current working directory: %s" % os.getcwd())
        print("listening on %s:%i" % (host,port))
        
    def startInstaller(self,install_func,softwareList):
        '''Starts a new thread containing installer component.'''
        self.__installThread = thread.start_new_thread(install_func,
            tuple([softwareList]))
        print("installer started...")
        print("software to be installed:" + str(softwareList))
        
    def startTester(self,tester_func):
        '''Starts a new thread containing a test function.'''
        self.__testThread = thread.start_new_thread(tester_func, tuple())
        print("tester started...")
        
    def getStatusFile(self):
        return self.__statusFile
    
    def getHtmlDir(self):
        return self.__DIR_HTML
    
    def getJsDir(self):
        return self.__DIR_JS
    
    def getCssDir(self):
        return self.__DIR_CSS
    
    def isAlive(self):
        '''If this is false, none of the threads are running anymore.'''
        return self.__alive
    
_controller = _Controller()
    
def Controller(): return _controller
