from typing import List, Callable, Tuple, Dict
from functools import wraps

def getParameterSet(name : str,parameterSet : Dict) -> Dict:
    if name in parameterSet:
        if isinstance(parameterSet[name], dict):
            return parameterSet[name]
    return {}


def MapKeywordArg(functionParam,objectName,ObjectParam):
    def MapArg(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            containerParams = getParameterSet(objectName,kwargs)
            if (functionParam in kwargs) and not(kwargs[functionParam] is None):
                containerParams[ObjectParam] = kwargs[functionParam]
            kwargs[objectName] = containerParams
            return method(*args,**kwargs)
        return wrapper
    return MapArg


