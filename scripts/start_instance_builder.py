import os,sys
from components.webroot import create_publisher
from components.installer import Installer
from controller import Controller

def start(host,port,softwareList,test=False):
    Controller().startServer(create_publisher,host,port)
    if not test:
        Controller().startInstaller(Installer.install,softwareList)
    else:
        print("running in test mode...")
    
    while Controller().isAlive(): pass
    
def pusage():
    print("\nstart_instance_builder.py")
    print("Starts an aws_instance_builder server that will" 
        + " install necessary software and provide a web interface that"
        + " informs the user of server activity. Built for use with Python2.7.")
    print("\nusage: start_instance_builder.py <host> <port> <softwareList> [-test]")
    print("\t        host - host to start server on")
    print("\t        port - port number to start server on")
    print("\tsoftwareList - no spaces, enclosed in brackets,"
        + " comma separated list of software to install")
    print("\t       -test - runs server without installing anything\n")
    
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        pusage()
    else:
        try:
            host = sys.argv[1]
            port = int(sys.argv[2])
            softwareList = sys.argv[3].lstrip("[").rstrip("]").split(",")
            if len(sys.argv) == 5 and sys.argv[4].strip() == "-test":
                start(host,port,softwareList,True)
            else:
                start(host,port,softwareList)
        except:
            pusage()
        
