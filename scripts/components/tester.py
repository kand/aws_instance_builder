import time,random

from threading import Thread
from controller import Controller

class Tester(Thread):
    '''Spits out text to test gui'''
    
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        print("running tester...")
        
        random_text = ["some random string of information\n"]
        
        while 1:            
            Controller().getStatusFile() \
                .write(random_text[random.randint(0,len(random_text)-1)])
            time.sleep(random.randint(1,10))
            
if __name__ == "__main__":
    pass