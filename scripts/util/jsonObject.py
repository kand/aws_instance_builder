import json

class JSONObject(object):
    '''Provides interface for making objects that can be serialized into json.
        
        Note: This class is currently incomplete and only provides enough
        functionality to be useful in a specific case.'''
    def serialize(self):
        '''Serializes any variables that are part of the class __dict__ (or 
            __dict__ of the particular instance) and prefixed with __json__ 
            into a json object'''
        ret = "{"
        vdict = self.__getJSONdict();
        for v in vdict:
            ret += self.__convert(v,vdict[v])
        return ret.rstrip(",") + "}"
    
    def __convert(self,key,value):
        '''Recursively convert python objects into JSON format'''
        ret = ""
        if key:
            ret = '"%s":' % key
        if isinstance(value,int) or isinstance(value,float):
            ret += str(value) + ","
        elif isinstance(value,basestring):
            ret += json.JSONEncoder().encode(repr(value).lstrip("u'").strip("'").strip('"')) + ","
        elif isinstance(value,list):
            ret += "["
            for i in value:
                ret += self.__convert(None,i)
            ret = ret.rstrip(",") + "],"
        elif isinstance(value,dict):
            ret += "{"
            for k in value:
                ret += self.__convert(k, value[k])
            ret = ret.rstrip(",") + "},"
        return ret
        
    def __getJSONdict(self):
        retdict = {}
        for v in self.__class__.__dict__:
            if v.find("__json__") != -1:
                retdict[v.replace("_" + self.__class__.__name__,"") \
                    .replace("__json__","")] = getattr(self,v)
        for v in self.__dict__:
            if v.find("__json__") != -1:
                retdict[v.replace("_" + self.__class__.__name__,"") \
                    .replace("__json__","")] = getattr(self,v)
        return retdict
        
