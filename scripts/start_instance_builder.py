import os,sys
from controller import Controller
from components.webroot import WebRoot
from components.installer import Installer
from components.tester import Tester
from components.pipeline import Pipeline

def start(host,port,softwareList,piplineUrl,test=False):
    Controller().startThreading(WebRoot(host,port))
    if not test:
        i = Installer(softwareList)
        Controller().startThreading(i)
    
        #wait for installer to finish and start pipeline
        while i.isAlive(): Controller().getStatusIO().write("still alive")
        Controller().startThreading(Pipeline(self.__pipelineUrl))
    else:
        Controller().startThreading(Tester())
        
    while Controller().isAlive(): pass
    
def pusage():
    print("\nstart_instance_builder.py")
    print("Starts an aws_instance_builder server that will" 
        + " install necessary software and provide a web interface that"
        + " informs the user of server activity. Built for use with Python2.7.")
    print("\nusage: start_instance_builder.py <host> <port> <softwareList> <pipelineUrl> [-test]")
    print("\t        host - host to start server on")
    print("\t        port - port number to start server on")
    print("\tsoftwareList - no spaces, enclosed in brackets,"
        + " comma separated list of software to install")
    print("\t       -test - runs server without installing anything\n")
    
if __name__ == "__main__":
    if len(sys.argv) < 5:
        pusage()
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        softwareList = sys.argv[3].lstrip("[").rstrip("]").split(",")
        pipelineUrl = sys.argv[4]
        if len(sys.argv) == 6 and sys.argv[5].strip() == "-test":
            start(host,port,softwareList,pipelineUrl,True)
        else:
            start(host,port,softwareList,pipelineUrl)
        
