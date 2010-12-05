import time,random
from controller import Controller

class Tester(object):
    '''Spits out text to test gui'''
    
    @staticmethod
    def test():
        random_text = ["some random string of information\n"]
        
        while 1:
            Controller().getStatusFile() \
                .write(random_text[random.randint(0,len(random_text)-1)])
            time.sleep(random.randint(1,10))
            
if __name__ == "__main__":
    pass