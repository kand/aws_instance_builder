import json

class JSONObject(object):
    '''Provides interface for making objects that can be serialized into json'''
    #def __init__(self):
    #    '''If inherited, will make getters/setters for each of the __json__ 
    #        variables in the object'''
    #    vdict = self.__getJSONdict();
    #    for v in vdict:
    #        self.__dict__["get" + v[0].upper() + v[1:]] = \
    #             lambda: self.__dict__[v]
    #        self.__dict__["set" + v[0].upper() + v[1:]] = \
    #             lambda val: self.__dict__[v] = val    #need to find a diff way to do this
    
    def serialize(self):
        '''Serializes any variables that are part of the class __dict__ (or 
            __dict__ of the particular instance) and prefixed with __json__ 
            into a json object'''
        ret = "{"
        vdict = self.__getJSONdict();
        for v in vdict:
            if isinstance(vdict[v],int) or isinstance(vdict[v],float):
                ret += '"%s":%s' % (v,str(vdict[v]))
            elif isinstance(vdict[v],str):
                ret += '"%s":%s' % (v,json.JSONEncoder() \
                    .encode(repr(vdict[v]).strip("'")))
            ret += ","
        return ret.rstrip(",") + "}"
        
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
        
