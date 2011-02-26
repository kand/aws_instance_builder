import subprocess,os,urllib,re

from sqlite3 import OperationalError
from threading import Thread

from controller import Controller,cprint,DIR_FILEOUTPUT, \
                                        SIG_KEY_PIPELINE,\
                                        PIPELINE_RESULTS_PATH
                                        
from serverio.statusIO import StatusIO,redirectExceptions
from serverio.fileChecker import FileChecker

class Pipeline(Thread):
    '''Provides methods to run/use pipelines.'''
    
    __PIPELINE_FILE_NAME = "pipeline_script"
    __COMMAND_PATTERNS = {
        "addFileToDB":r"pComm\.addFileToDB\([\"\'](?P<name>.+)[\"\'],[\"\'](?P<path>.+)[\"\'],[\"\'](?P<desc>.+)[\"\']\)\n?",
        "writeToResults":r"pComm\.writeToResults\([\"\'](?P<results>.+)[\"\']\)\n?"
    }
    
    SIG_KEY = "pipeline_complete"
    
    def __init__(self,pipelineUrl):
        Thread.__init__(self)
        self.__pipelineUrl = pipelineUrl
    
    @redirectExceptions
    def run(self):
        '''Start a pipeline downloaded from pipelineUrl.'''
        
        StatusIO.write("Pipeline located at '%s', downloading..." \
                       % self.__pipelineUrl)
        
        #copy pipeline into current directory
        try:
            purl = urllib.urlopen(self.__pipelineUrl)
        except IOError:
            StatusIO.write("[ERROR] Pipeline not found at url.")
            return
            
        f = open(Pipeline.__PIPELINE_FILE_NAME,"w")
        f.write(purl.read())
        f.close()
        purl.close()
        
        if os.path.getsize(Pipeline.__PIPELINE_FILE_NAME) < 1:
            StatusIO.write("[ERROR] Pipeline script was not properly downloaded.")
            return
            
        #make pipeline executable
        command = ["chmod","+x",Pipeline.__PIPELINE_FILE_NAME]
        process = subprocess.Popen(command)
        while(process.poll() is None): pass
        
        StatusIO.write("Pipeline now executable. Executing...")
        
        #execute pipeline script
        command = ["sudo","./%s" % Pipeline.__PIPELINE_FILE_NAME]
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        
        #redirect output to website
        while(process.poll() is None):
            #If a special 'pcomm.addFileToDB("<name>","<path>","<description>")' 
            #    command is echoed from a pipeline, a new file path entry will
            #    be added to the database so that the file can then be served
            #    to the client. This will only work for files placed in the
            #    web/output directory. The <path> variable must also be a path
            #    starting with 'output/'.
            
            #NEW ISSUE: too much output produces an extremely long string here
            #    so, need to check length of string, if too long, just pipe it
            #    straight away to file???
            pOut = process.stdout.read()
            pErr = process.stderr.read()
            
            #might be able to search for both patterns at the sime time here
            pOut = self.__addFileToDB(pOut)
            pOut = self.__writeToResults(pOut)

            if(len(pOut) > 0):
                StatusIO.write("[PIPELINE][COUT] {{ %s }}" % pOut)
            if(len(pErr) > 0):
                StatusIO.write("[PIPELINE][CERR] {{ %s }}" % pErr)
                
            StatusIO.write("Pipeline complete. Click here to view results: <a href='results'>results</a>")
        
        Controller().SIG_KEYS[SIG_KEY_PIPELINE] = True
        
    def __addFileToDB(self,pOut):
        '''Check for addFileToDB command from pipeline, add file to
        database so it can be served to website, remove command from
        output piped to website.'''
        if(len(pOut) < len(self.__COMMAND_PATTERNS["addFileToDB"])):
            return pOut
        
        matches = re.finditer(self.__COMMAND_PATTERNS["addFileToDB"],pOut)
        for m in matches:
            if m is not None:
                FileChecker.addFile(m.group("name"),
                                    m.group("path"),
                                    m.group("desc"))
                StatusIO.write("Pipeline added file: <a href='%s' target='_blank'>%s</a> - %s" \
                               % (m.group("path"),m.group("name"),m.group("desc")))
            pOut = pOut.replace(m.group(),"")
        return pOut
    
    def __writeToResults(self,pOut):
        '''Check for writeToResults command from pipeline, append text passed in
        the command to the file. This text will be viewable through the results
        tab of the website once the pipeline is finished. So, this could really
        be written to a little at a time, to create a complete file.'''
        if(len(pOut) < len(self.__COMMAND_PATTERNS["writeToResults"])):
            return pOut
        
        matches = re.finditer(self.__COMMAND_PATTERNS["writeToResults"],pOut)
        for m in matches:
            if m is not None:
                res = m.group("results")
                f = open(PIPELINE_RESULTS_PATH,"a")
                f.write(res)
                f.close()
                pOut = pOut.replace(m.group(),"")
        return pOut
    
if __name__ == "__main__":
    pass