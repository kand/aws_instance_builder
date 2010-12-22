import os,sys,random

from threading import Thread
from quixote.publish import *
from quixote.directory import Directory
from quixote.util import StaticFile,StaticDirectory
from quixote.server.simple_server import run
from jinja2 import Environment,FileSystemLoader

from controller import Controller

class Root(Directory):
    _q_exports = ["","css","js","getstatus","monitor"]

    js = StaticDirectory(Controller().getJsDir())
    css = StaticDirectory(Controller().getCssDir())
    __j2env = Environment(loader=FileSystemLoader(Controller().getHtmlDir()))

    def __init__(self):
        pass

    def _q_index(self):
        return self.__j2env.get_template("login.html").render()
    
    def monitor(self):
        return self.__j2env.get_template("home.html").render()

    def getstatus(self):
        return Controller().getStatusIO().read(get_response(),get_request().get_field("lastLine"))

class WebRoot(Thread):
    '''Provides methods to start web server.'''
    
    EXCEPTION_TYPE = "html"
    
    def __init__(self,host,port):
        Thread.__init__(self)
        self.__host = host
        self.__port = port
    
    def run(self):
        print("server starting...")
        print("listening on %s:%i" % (self.__host,self.__port))
        #to provide https support? not sure if this is correct, doesn't seem to work,
        #    need proxy also...
        #run(self.__create_publisher,host=self.__host,port=self.__port,https=True)
        run(self.__create_publisher,host=self.__host,port=self.__port)
        
    def __create_publisher(self):
        return Publisher(Root(),display_exceptions=self.EXCEPTION_TYPE)

if __name__ == "__main__":
    pass
