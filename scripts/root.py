import os,sys,random

from quixote.publish import *
from quixote.directory import Directory
from quixote.util import StaticFile,StaticDirectory
from jinja2 import Environment,FileSystemLoader

from statusIO import StatusIO

HTML_DIR = "../web"
JAVASCRIPT_DIR = "../web/js"
STATUS_FILE = "../status_file"

EXCEPTION_TYPE = "html"
HOST = "localhost"
PORT = 8080

class Root(Directory):
    _q_exports = ["","js","getstatus","writestatus"]

    js = StaticDirectory(os.path.join(os.getcwd(),JAVASCRIPT_DIR))

    def __init__(self):
        self.__status_file = StatusIO(STATUS_FILE)

    def _q_index(self):
        env = Environment(loader=FileSystemLoader(
            os.path.join(os.getcwd(),HTML_DIR)))
        return env.get_template("home.html").render()

    def getstatus(self):
        return self.__status_file.readBuff(get_response(),get_request().get_field("lastLine"))

    #for debug
    def writestatus(self):
        self.__status_file.write(get_request().get_field("write"))

#how can I sep into different directories????
#   need one master directory that controls/provides access to other
#   directories
def create_publisher():
    return Publisher(Root(),display_exceptions=EXCEPTION_TYPE)

if __name__ == "__main__":
    from quixote.server.simple_server import run
    port = 8080
    host = "localhost"
    print("current working directory: %s" % os.getcwd())
    print("listening on %s:%i" % (host,port))
    run(create_publisher,host=host,port=port)
