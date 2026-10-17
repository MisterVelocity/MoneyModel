from numpy import float64

def formatNumberAsString(x):
    if isinstance(x, str):
        if '.' in x:
            try:
                x = float(x)
            except:
                return None
        else:
            try:
                x = int(x)
            except:
                return None

    if isinstance(x, int):
        return f'{x:,}'
    elif isinstance(x, (float, float64)):
        return f'{x:,.2f}'

    return None