import subprocess,os,urllib

from threading import Thread
from controller import Controller,redirectExceptions

class Pipeline(Thread):
    '''Provides methods to run/use pipelines.'''
    
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
        try:
            pulr = urllib.urlopen(self.__pipelineUrl)
        except IOError:
            Controller().swrite("[ERROR] Pipeline not found at url.")
            return
            
        f = open(self.__PIPELINE_FILE_NAME,"w")
        f.write(pulr.read())
        f.close()
        pulr.close()
        
        if os.path.getsize(self.__PIPELINE_FILE_NAME) < 1:
            Controller().swrite("[ERROR] Pipeline script was not properly downloaded.")
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
            Controller().swrite("[PIPELINE] %s" % process.stdout.read())
            Controller().swrite("[PIPELINE] %s" % process.stderr.read())
        
        Controller().getSignals()[self.SIG_KEY] = True
    
if __name__ == "__main__":
    pass