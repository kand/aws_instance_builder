import os,sys,random

from quixote.publish import *
from quixote.directory import Directory
from quixote.util import StaticFile,StaticDirectory
from jinja2 import Environment,FileSystemLoader

from controller import Controller

HTML_DIR = "../web"
JAVASCRIPT_DIR = "../web/js"
OUTPUT_FILE = "../server_output"

EXCEPTION_TYPE = "html"

class Root(Directory):
    _q_exports = ["","js","getstatus","writestatus"]

    js = StaticDirectory(os.path.join(os.getcwd(),JAVASCRIPT_DIR))

    def __init__(self):
        pass

    def _q_index(self):
        env = Environment(loader=FileSystemLoader(
            os.path.join(os.getcwd(),HTML_DIR)))
        return env.get_template("home.html").render()

    def getstatus(self):
        return Controller().getStatusFile().readBuff(get_response(),get_request().get_field("lastLine"))

    #for debug
    def writestatus(self):
        Controller().getStatusFile().write(get_request().get_field("write"))

#how can I sep into different directories????
#   need one master directory that controls/provides access to other
#   directories
def create_publisher():
    return Publisher(Root(),display_exceptions=EXCEPTION_TYPE)

if __name__ == "__main__":
    pass
