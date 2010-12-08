import os,sys,random

from quixote.publish import *
from quixote.directory import Directory
from quixote.util import StaticFile,StaticDirectory
from jinja2 import Environment,FileSystemLoader

from controller import Controller

EXCEPTION_TYPE = "html"

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

#how can I sep into different directories????
#   need one master directory that controls/provides access to other
#   directories
def create_publisher():
    return Publisher(Root(),display_exceptions=EXCEPTION_TYPE)

if __name__ == "__main__":
    pass
