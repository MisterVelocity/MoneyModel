def createNullDictionary(d):
    if isinstance(d, dict):
        return {key: createNullDictionary(val) for key, val in d.items()}
    else:
        return None
    