from typing import List, Callable, Tuple, Dict
from functools import wraps

def getParameterSet(name : str,parameterSet : Dict) -> Dict:
    if name in parameterSet:
        if isinstance(parameterSet[name], dict):
            return parameterSet[name]
    return {}

def MapPotitionnalArgument(paramNumber,objectName,ObjectParam):
    def MapArg(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            containerParams = getParameterSet(objectName,kwargs)
            containerParams[ObjectParam] = args[paramNumber]
            kwargs[objectName] = containerParams
            return method(*args,**kwargs)
        return wrapper
    return MapArg
def MapKeywordArg(functionParam,objectName,ObjectParam):
    def MapArg(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            containerParams = getParameterSet(objectName,kwargs)
            if (functionParam in kwargs) and kwargs[functionParam]:
                containerParams[ObjectParam] = kwargs[functionParam]
            kwargs[objectName] = containerParams
            return method(*args,**kwargs)
        return wrapper
    return MapArg


