import os

from threading import Thread

class Pipeline(Thread):
    '''Provides methods to run/use pipelines.'''
    def __init__(self,pipelineUrl):
        Thread.__init__(self)
        self.__pipelineUrl = pipelineUrl
    
    def run(self):
        '''Start a pipeline downloaded from pipelineUrl.'''
        print("Pipeline located at '%s' started" % pipelineUrl)
        print("Current dir %s" % os.getcwd())
    
if __name__ == "__main__":
    pass