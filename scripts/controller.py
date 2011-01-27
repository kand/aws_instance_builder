import thread,os,traceback

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
    
    def __dbr(self):
        return self.__signals[self.__DB_R_SIG_KEY]
    
    def __dbw(self):
        return self.__signals[self.__DB_W_SIG_KEY]
    
    def swrite(self,text):
        '''Hand text to statusIO and write to console.'''
        print("[SUBPROCESS] %s" % text)
        self.__statusIO.write(str(text))
        
    def sread(self,response,lastLine):
        '''Read text from statusIO.'''
        return self.__statusIO.read(response,lastLine)
    
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
    