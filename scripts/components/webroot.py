import os,sys,random

from threading import Thread
from quixote.publish import *
from quixote.directory import Directory
from quixote.util import StaticFile,StaticDirectory
from quixote.server.simple_server import run
from jinja2 import Environment,FileSystemLoader

from controller import Controller

class Root(Directory):
    _q_exports = ["","css","js","getstatus","writestatus"]

    js = StaticDirectory(Controller().getJsDir())
    css = StaticDirectory(Controller().getCssDir())

    def __init__(self):
        pass

    def _q_index(self):
        env = Environment(loader=FileSystemLoader(Controller().getHtmlDir()))
        return env.get_template("home.html").render()

    def getstatus(self):
        return Controller().getStatusFile().readBuff(get_response(),get_request().get_field("lastLine"))

class WebRoot(Thread):
    '''Provides methods to start web server.'''
    
    EXCEPTION_TYPE = "html"
    
    def __init__(self,host,port):
        Thread.__init__(self)
        self.__host = host
        self.__port = port
    
    def run(self):
        print("server starting...\nlistening on %s:%i" % (self.__host,self.__port))
        run(self.__create_publisher,host=self.__host,port=self.__port)
        
    def __create_publisher(self):
        return Publisher(Root(),display_exceptions=self.EXCEPTION_TYPE)

if __name__ == "__main__":
    pass
