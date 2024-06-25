from typing import List, Callable, Tuple, Dict

def getParameterSet(name : str,parameterSet : Dict) -> Dict:
    if name in parameterSet:
        if isinstance(parameterSet[name], dict):
            return parameterSet[name]
    return {}