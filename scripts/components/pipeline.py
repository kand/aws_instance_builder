import subprocess,os

from threading import Thread
from controller import Controller

class Pipeline(Thread):
    '''Provides methods to run/use pipelines.'''
    
    SIG_KEY = "pipeline_complete"
    
    def __init__(self,pipelineUrl):
        Thread.__init__(self)
        self.__pipelineUrl = pipelineUrl
    
    def run(self):
        '''Start a pipeline downloaded from pipelineUrl.'''
        Controller().getSignals()[SIG_KEY] = False
        Controller().getStatusIO().write("Pipeline located at '%s' started" \
                                         % self.__pipelineUrl)
        #copy pipeline into current directory
        command = ["wget","-O","pipeline_script",self.__pipelineUrl]
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        
        #redirect wget output to website
        while(process.poll() == None):
            Controller().getStatusIO().write(process.stdout.read())
            Controller().getStatusIO().write(process.stderr.read())
            
        #make pipeline executable
        command = ["chmod","400","pipeline_script"]
        process = subprocess.Popen(command)
        while(process.poll() == None): pass
        
        #execute pipeline script
        command = ["sudo ./pipeline_script"]
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        
        #redirect output to website
        while(process.poll() == None):
            Controller().getStatusIO().write(process.stdout.read())
            Controller().getStatusIO().write(process.stderr.read())
        
        Controller().getSignals()[SIG_KEY] = True
    
if __name__ == "__main__":
    pass