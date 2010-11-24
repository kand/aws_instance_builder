import os,sys,json
import subprocess
from importlib import import_module

sys.path.append(os.path.join(os.getcwd(),"../scripts/serverio"))
sys.path.append(os.path.join(os.getcwd(),"../scripts"))
from statusIO import *

TEST_FILE = "test_file"

def make_subprocess():
    '''just to test the behavior of subprocess'''

    command = ['ls','-l']
    p = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

    while(p.poll() == None):
        print("'%s'" % p.stdout.read())
          
def test_statusIO_file_creation():
    if os.path.isfile(TEST_FILE):
        os.remove(TEST_FILE)
    status_file = StatusIO(TEST_FILE)
    assert os.path.isfile(TEST_FILE)
    
def test_statusIO_write():
    TEST_STRING = "abc123 bar \n foo arg "
    status_file = StatusIO(TEST_FILE)
    status_file.write(TEST_STRING)
    f = open(TEST_FILE,"r")
    f_contents = f.read()
    assert f_contents == TEST_STRING
    
def test_statusIO_read():
    TEST_STRINGS = ["this is the first line \n","this is the second line \n",
        "this is the third line \n"]
    TEST_CONTENTS = "".join(TEST_STRINGS)
    TEST_CONT_TYPE = "application/json"
    status_file = StatusIO(TEST_FILE)
    status_file.write(TEST_STRINGS[0])
    status_file.write(TEST_STRINGS[1])
    status_file.write(TEST_STRINGS[2])
    dresponse = dummy_response()
    j = json.JSONDecoder().decode(status_file.readBuff(dresponse,"a"))
    assert j["error"] == "lastLine must be int"
    j = json.JSONDecoder().decode(status_file.readBuff(dresponse,-1))
    assert j["lastLine"] == 2
    assert j["lines"].replace("\\n","\n") == TEST_CONTENTS
    assert dresponse.content_type == TEST_CONT_TYPE
    j = json.JSONDecoder().decode(status_file.readBuff(dresponse,0))
    assert j["lastLine"] == 2
    assert j["lines"].replace("\\n","\n") == (TEST_STRINGS[1] + TEST_STRINGS[2])
    assert dresponse.content_type == TEST_CONT_TYPE
    j = json.JSONDecoder().decode(status_file.readBuff(dresponse,1))
    assert j["lastLine"] == 2
    assert j["lines"].replace("\\n","\n") == TEST_STRINGS[2]
    assert dresponse.content_type == TEST_CONT_TYPE
    j = json.JSONDecoder().decode(status_file.readBuff(dresponse,2))
    assert j["lastLine"] == 2
    assert j["lines"].replace("\\n","\n") == ""
    assert dresponse.content_type == TEST_CONT_TYPE
    j = json.JSONDecoder().decode(status_file.readBuff(dresponse,3))
    assert j["error"] == "lastLine refers to a location beyond EoF"
    
class dummy_response():
    def __init__(self):
        self.content_type = ""

    def set_content_type(self,content_type):
        self.content_type = content_type
            
if __name__ == "__main__":
    #make_subprocess()
    test_statusIO_file_creation()
    test_statusIO_write()
    test_statusIO_read()
