import subprocess
from controller import Controller

class Installer(object):
    '''Provides methods to install software on server'''

    NODEJS_PATH = '/etc/chef/node.js'
    CHEF_REPO_LOCATION = 'http://lyorn.idyll.org/~nolleyal/chef/' \
        'chef-solo.tar.gz'
    
    @staticmethod
    def install(softwareList):
        '''Used to install software on the server. Reports to statusIOobj to
            inform user of status.'''
        #write software to node.js
        nodejs = open(NODEJS_PATH,"w")
        nodejs.write('{ "run_list": [ %s ] }' 
            % ', '.join(['"recipe[%s]"' % s for s in softwareList]))
        nodejs.close()
        
        #execute chef-solo to install
        command = ["chef-solo","-j",NODEJS_PATH,"-r",CHEF_REPO_LOCATION]
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
            
        #send output to status file
        while(process.poll() == None):
            Controller().getStatusFile().write(process.stdin.read())
            Controller().getStatusFile().write(process.stderr.read())

if __name__ == "__main__":
    pass
