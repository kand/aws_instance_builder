import subprocess,os

from threading import Thread

from controller import Controller,SIG_KEY_INSTALLER
from serverio.statusIO import StatusIO,redirectExceptions

class Installer(Thread):
    '''Provides methods to install software on server'''

    NODEJS_DIR = '/etc/chef'
    NODEJS_PATH = NODEJS_DIR + '/node.js'
    CHEF_REPO_LOCATION = 'http://lyorn.idyll.org/~nolleyal/chef/' \
        'chef-solo.tar.gz'
        
    def __init__(self,softwareList):
        Thread.__init__(self)
        self.__softwareList = softwareList
    
    @redirectExceptions
    def run(self):
        '''Used to install software on the server. Reports to statusIOobj to
            inform user of status. Starts pipeline once install complete'''
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
            
        #redirect output to website
        while(process.poll() == None):
            StatusIO.write(process.stdout.read())
            StatusIO.write(process.stderr.read())
            
        Controller().SIG_KEYS[SIG_KEY_INSTALLER] = True
        
if __name__ == "__main__":
    pass
