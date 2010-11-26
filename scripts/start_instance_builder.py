import os,sys
from components.webroot import create_publisher
from components.installer import Installer
from controller import Controller

def start(host,port,softwareList):
    Controller().startServer(create_publisher,host,port)
    Controller().startInstaller(Installer.install,softwareList)
    
    while Controller().isAlive(): pass
    
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.stdout.write("\nstart_instance_builder.py\n")
        sys.stdout.write("Starts an aws_instance_builder server that will" 
            + " install necessary software and provide a web interface that"
            + " informs the user of server activity. Built for use with Python2.7.")
        sys.stdout.write("\n\tusage: start_instance_builder.py <host> <port> <softwareList>\n")
        sys.stdout.write("\t        host - host to start server on\n")
        sys.stdout.write("\t        port - port number to start server on\n")
        sys.stdout.write("\tsoftwareList - no spaces, enclosed in brackets,"
            + " comma separated list of software to install.")
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        softwareList = sys.argv[3].lstrip("[").rstrip("]").split(",")
        
        start(host,port,softwareList)
        
