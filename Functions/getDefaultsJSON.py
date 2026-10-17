import json, os, sys

def getJSONPath():
    if getattr(sys, 'frozen', False):
        basePath = sys.MEIPASS
    else:
        basePath = os.path.dirname(
            os.path.dirname(
                os.path.abspath(
                    __file__
                )
            )
        )
    
    return os.path.join(basePath, 'Resources', 'defaults.json')

def getDefaultsJSON():
    jsonPath = getJSONPath()
    with open(jsonPath, 'r') as f:
        defaults = json.load(f)
    
    return defaults