import subprocess
    
class Installer(object):
    '''Provides methods to install software on server'''

    NODEJS_PATH = '/etc/chef/node.js'
    CHEF_REPO_LOCATION = 'http://lyorn.idyll.org/~nolleyal/chef/' \
        'chef-solo.tar.gz'
        
    @staticmethod
    def install(softwareList,statusIOobj):
        '''Used to install software on the server. Reports to statusIOobj to
            inform user of status.'''
        #write software to node.js
        nodejs = open(NODEJS_PATH,"w")
        nodejs.write('{ "run_list": [ %s ] }' 
            % ', '.join(['"recipe[%s]"' % s for s in softwareList]))
        nodejs.close()
        
        #execute chef-solo to install
        command = 'chef-solo -j %s -r %s' % (NODEJS_PATH, CHEF_REPO_LOCATION)
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
            
        #send output to statusIOobj
        while(process.poll() == None):
            statusIOobj.write(process.stdin.read())
            statusIOobj.write(process.stderr.read())

if __name__ == "__main__":
    pass
