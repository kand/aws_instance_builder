import subprocess,os

from threading import Thread
from controller import Controller,redirectExceptions

class Pipeline(Thread):
    '''Provides methods to run/use pipelines.'''
    
    __PIPELINE_DL_ERROR_MSG = "[ERROR] Pipeline script was not properly downloaded."
    __PIPELINE_FILE_NAME = "pipeline_script"
    
    SIG_KEY = "pipeline_complete"
    
    def __init__(self,pipelineUrl):
        Thread.__init__(self)
        self.__pipelineUrl = pipelineUrl
    
    @redirectExceptions
    def run(self):
        '''Start a pipeline downloaded from pipelineUrl.'''
        Controller().getSignals()[self.SIG_KEY] = False
        Controller().swrite("Pipeline located at '%s', downloading..." \
                                         % self.__pipelineUrl)
        #copy pipeline into current directory
        command = ["wget","-O",self.__PIPELINE_FILE_NAME,self.__pipelineUrl]
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        
        #redirect wget output to website
        while(process.poll() == None):
            Controller().swrite(process.stdout.read())
            Controller().swrite(process.stderr.read())
        
        #make sure pipeline was properly downloaded
        try:
            open(self.__PIPELINE_FILE_NAME)
        except IOError:
            Controller().swrite(self.__PIPELINE_DL_ERROR_MSG)
            return
        
        if os.path.getsize(self.__PIPELINE_FILE_NAME) < 1:
            Controller().swrite(self.__PIPELINE_DL_ERROR_MSG)
            return
            
        #make pipeline executable
        command = ["chmod","+x",self.__PIPELINE_FILE_NAME]
        process = subprocess.Popen(command)
        while(process.poll() == None): pass
        
        Controller().swrite("Pipeline now executable. Executing...")
        
        #execute pipeline script
        command = ["sudo","./%s" % self.__PIPELINE_FILE_NAME]
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        
        #redirect output to website
        while(process.poll() == None):
            Controller().swrite(process.stdout.read())
            Controller().swrite(process.stderr.read())
        
        Controller().getSignals()[self.SIG_KEY] = True
    
if __name__ == "__main__":
    pass