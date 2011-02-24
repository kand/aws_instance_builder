import os,sys,random

from threading import Thread
from quixote.publish import *
from quixote.directory import Directory
from quixote.util import StaticFile,StaticDirectory
from quixote.errors import TraversalError
from quixote.server.simple_server import run
from jinja2 import Environment,FileSystemLoader

from controller import Controller,DIR_JS,DIR_CSS,DIR_FILEOUTPUT,DIR_HTML,SIG_KEY_PIPELINE
from serverio.statusIO import StatusIO,redirectExceptions
from serverio.fileChecker import FileChecker
from pipeline import Pipeline

class Root(Directory):
    _q_exports = ["","css","js","output","getstatus","getfiles","console","files",
                  "results"]

    js = StaticDirectory(DIR_JS)
    css = StaticDirectory(DIR_CSS)
    output = StaticDirectory(DIR_FILEOUTPUT)
    __j2env = Environment(loader=FileSystemLoader(DIR_HTML))

    def __init__(self):
        pass

    def _q_index(self):
        return self.__j2env.get_template("login.html").render()
    
    def console(self):
        return self.__j2env.get_template("home.html").render(showResults=Controller().SIG_KEYS[SIG_KEY_PIPELINE],
                                                             console_active="active")
    
    def files(self):
        return self.__j2env.get_template("home.html").render(showResults=Controller().SIG_KEYS[SIG_KEY_PIPELINE],
                                                             outputFiles_active="active")
    
    def results(self):
        if Controller().SIG_KEYS[SIG_KEY_PIPELINE] == True:
            content = "pipeline finished"
            resultsOutput = self.__j2env.get_template("resultsOutput.html").render(content=content)
            return self.__j2env.get_template("home.html").render(showResults=True,
                                                                 results_active="active",
                                                                 results_output=resultsOutput)
        raise TraversalError()

    def getstatus(self):
        return StatusIO.read(get_response(),get_request().get_field("lastLine"))

    def getfiles(self):
        return FileChecker.getFiles(get_response(),get_request().get_field("lastFileId"))

class WebRoot(Thread):
    '''Provides methods to start web server.'''
    
    EXCEPTION_TYPE = "html"
    
    def __init__(self,host,port):
        Thread.__init__(self)
        self.__host = host
        self.__port = port
    
    @redirectExceptions
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
