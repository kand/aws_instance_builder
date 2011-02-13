import subprocess,os,urllib,re

from threading import Thread
from controller import Controller,redirectExceptions

class Pipeline(Thread):
    '''Provides methods to run/use pipelines.'''
    
    __PIPELINE_FILE_NAME = "pipeline_script"
    __COMMAND_PATTERNS = {
        "addFileToDB":r"pComm\.addFileToDB\(\"(?P<name>.+)\",\"(?P<path>.+)\",\"(?P<desc>.+)\"\)"
    }
    
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
            #If a special 'pcomm.addFileToDB("<name>","<path>","<description>")' 
            #    command is echoed from a pipeline, a new file path entry will
            #    be added to the database so that the file can then be served
            #    to the client. This will only work for files placed in the
            #    web/output directory. The <path> variable must also be a path
            #    starting with 'output/'.
            
            #Note: pipelines are run from the scripts/ directory, so you must go up
            #    one level and down into web and output to put files in the correct
            #    place, eg '../web/output/'
            
            pOut = process.stdout.read()
            
            m = re.search(self.__COMMAND_PATTERNS["addFileToDB"],pOut)
            if m is not None:
                Controller().getFileChecker().addFile(m.group("name"),
                                                      m.group("path"),
                                                      m.group("desc"))
                Controller().swrite("Pipeline added file: %s,%s,%s" \
                                    % (m.group("name"),m.group("path"),m.group("desc")))
                pOut = pOut.replace(m.group(),"")
            
            if(len(pOut) > 0):
                Controller().swrite("[PIPELINE] %s" % pOut)
            Controller().swrite("[PIPELINE] %s" % process.stderr.read())
        
        Controller().getSignals()[self.SIG_KEY] = True
    
if __name__ == "__main__":
    pass