import os,sys
from controller import Controller,SIG_KEY_INSTALLER
from components.webroot import WebRoot
from components.installer import Installer
from components.pipeline import Pipeline

def start(host,port,softwareList,piplineUrl):
    Controller().startThreading(WebRoot(host,port))
    
    i = Installer(softwareList)
    Controller().startThreading(i)
    
    #wait for installer to finish and start pipeline
    while not Controller().SIG_KEYS[SIG_KEY_INSTALLER]: pass
    Controller().startThreading(Pipeline(pipelineUrl))
        
    while Controller().isAlive(): pass
    
def pusage():
    print("\nstart_instance_builder.py")
    print("Starts an aws_instance_builder server that will" 
        + " install necessary software and provide a web interface that"
        + " informs the user of server activity. Built for use with Python2.7.")
    print("\nusage: start_instance_builder.py <host> <port> <softwareList> <pipelineUrl>")
    print("\t        host - host to start server on")
    print("\t        port - port number to start server on")
    print("\tsoftwareList - no spaces, enclosed in brackets,"
        + " comma separated list of software to install")
    
if __name__ == "__main__":
    if len(sys.argv) < 5:
        pusage()
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        softwareList = sys.argv[3].lstrip("[").rstrip("]").split(",")
        pipelineUrl = sys.argv[4]
        start(host,port,softwareList,pipelineUrl)
        
