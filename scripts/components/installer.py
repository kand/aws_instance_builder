import subprocess,os

from threading import Thread
from controller import Controller
from pipeline import Pipeline

class Installer(Thread):
    '''Provides methods to install software on server'''

    NODEJS_DIR = '/etc/chef'
    NODEJS_PATH = NODEJS_DIR + '/node.js'
    CHEF_REPO_LOCATION = 'http://lyorn.idyll.org/~nolleyal/chef/' \
        'chef-solo.tar.gz'
        
    def __init__(self,softwareList,pipelineUrl):
        Thread.__init__(self)
        self.__softwareList = softwareList
        self.__pipelineUrl = pipelineUrl
    
    def run(self):
        '''Used to install software on the server. Reports to statusIOobj to
            inform user of status. Starts pipeline once install complete'''
        print("installer started...")
            
        #write software to node.js
        if not os.path.isdir(Installer.NODEJS_DIR):
            os.mkdir(Installer.NODEJS_DIR)
        nodejs = open(Installer.NODEJS_PATH,"w")
        nodejs.write('{ "run_list": [ %s ] }' 
            % ', '.join(['"recipe[%s]"' % s for s in self.__softwareList]))
        nodejs.close()
        
        #execute chef-solo to install
        command = ["chef-solo","-j",Installer.NODEJS_PATH,"-r",Installer.CHEF_REPO_LOCATION]
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
            
        #send output to status file
        while(process.poll() == None):
            Controller().getStatusIO().write(process.stdout.read())
            Controller().getStatusIO().write(process.stderr.read())
            
        Controller().startThreading(Pipeline(self.__pipelineUrl))

if __name__ == "__main__":
    pass
