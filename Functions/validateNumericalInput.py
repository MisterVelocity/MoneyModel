import numpy as np

def validateInteger(x):
    try:
        x = int(x)
        return True
    except:
        return False

def validateFloat(x):
    try:
        x = float(x)
        return True
    except:
        return False


