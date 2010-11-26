import thread

from serverio.statusIO import *
from quixote.server.simple_server import run

class _Controller(object):
    '''Manages program resources, threads.'''
    __STATUS_FILE = "../server_status"
    
    def __init__(self):
        self.__alive = True
        self.__statusFile = StatusIO(self.__STATUS_FILE)
        self.__serverThread = None
        self.__installThread = None
            
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
        
    def getStatusFile(self):
        return self.__statusFile
    
    def isAlive(self):
        '''If this is false, none of the threads are running anymore.'''
        return self.__alive
    
_controller = _Controller()
    
def Controller(): return _controller
