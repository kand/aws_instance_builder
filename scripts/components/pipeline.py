import subprocess,os,urllib,re

from sqlite3 import OperationalError
from threading import Thread

from controller import Controller,cprint,DIR_FILEOUTPUT, \
                                        SIG_KEY_PIPELINE,\
                                        PIPELINE_RESULTS_PATH
                                        
from serverio.statusIO import StatusIO,redirectExceptions
from serverio.fileChecker import FileChecker

class _pComm():
    '''Class that stores regexes for various commands a pipeline can issue, as well
    as the functions associated with them.'''
    
    __addFile = re.compile(r"pComm\.addFile\([\"\'](?P<name>.+)[\"\'],[\"\'](?P<fileName>.+)[\"\'],[\"\'](?P<desc>.+)[\"\']\)\n?")
    __writeToFile = re.compile(r"pComm\.writeToFile\([\"\'](?P<fileName>.+)[\"\'],[\"\'](?P<text>.+)[\"\']\)\n?")
    __writeToResults = re.compile(r"pComm\.writeToResults\([\"\'](?P<text>.+)[\"\']\)\n?")
    
    @staticmethod
    def addFile(pOut):
        '''Used to make a file that will be shown in output tab of website. If
        the file does not exist, it will make a new one that can be written to.'''
        matches = _pComm.__addFile.finditer(pOut)
        for m in matches:
            if m is not None:
                FileChecker.addFile(m.group("name"),
                                    m.group("fileName"),
                                    m.group("desc"))
                
                if not os.path.isfile("output/" + m.group("fileName")):
                    open(os.path.join(DIR_FILEOUTPUT,m.group("fileName")),"w").close()
                
                StatusIO.write("Pipeline added file: <a href='%s' target='_blank'>%s</a> - %s" \
                               % ("output/" + m.group("fileName"),
                                  m.group("name"),
                                  m.group("desc")))
            pOut = pOut.replace(m.group(),"")
        return pOut
        
    @staticmethod
    def writeToFile(pOut):
        '''Can either use this function to write to an output file, or use the
        pipeline to pipe to a file that was already created with addFile.
        This command should be used with caution, if a pipeline is going to
        produce a lot of output, it would be better for it to directly pipe
        into the file.'''
        matches = _pComm.__writeToFile.finditer(pOut)
        open_dict = {}
        for m in matches:
            if m is not None:
                abs_path = os.path.join(DIR_FILEOUTPUT,m.group("fileName")) 
                
                if not os.path.isfile(abs_path):
                    StatusIO.write("[ERROR] File being written to with pComm.writeToFile cannot be found, did you forget to use addFile first?")
                    continue
                
                if abs_path not in open_dict.keys():
                    open_dict[abs_path] = open(abs_path,"a")
                
                #newlines show up escaped, also need to test for large output
                open_dict[abs_path].write(m.group("text"))
            pOut = pOut.replace(m.group(),"")
        for f in open_dict:
            f.close()
        return pOut
    
    @staticmethod
    def writeToResults(pOut):
        '''Check for writeToResults command from pipeline, append text passed in
        the command to the file. This text will be viewable through the results
        tab of the website once the pipeline is finished. So, this could really
        be written to a little at a time, to create a complete file.'''
        matches = _pComm.__writeToResults.finditer(pOut)
        f = open(PIPELINE_RESULTS_PATH,"a")
        for m in matches:
            if m is not None:
                res = m.group("text")
                f.write(res)
                pOut = pOut.replace(m.group(),"")
        f.close()
        return pOut
    
    @staticmethod
    def checkComm(pOut):
        pOut = _pComm.addFile(pOut)
        pOut = _pComm.writeToFile(pOut)
        pOut = _pComm.writeToResults(pOut)
        return pOut

class Pipeline(Thread):
    '''Provides methods to run/use pipelines.'''
        
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
            pOut = process.stdout.read()
            pErr = process.stderr.read()
            
            #here, pipeline output is checked for commands from stdout
            pOut = _pComm.checkComm(pOut)

            if(len(pOut) > 0):
                StatusIO.write("[PIPELINE][COUT] {{ %s }}" % pOut)
            if(len(pErr) > 0):
                StatusIO.write("[PIPELINE][CERR] {{ %s }}" % pErr)
        
                
        StatusIO.write("Pipeline complete. Click here to view results: <a href='results'>results</a>")
        Controller().SIG_KEYS[SIG_KEY_PIPELINE] = True
    
if __name__ == "__main__":
    pass