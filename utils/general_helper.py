def convertToInteger(value):
    try:
        return int(value)
    except:
        return 0

def convertToFloat(value):
    try:
        return float(format(value, '.3f'))
    except:
        return 0

def convertToString(value):
    try:
        return str(value)
    except:
        return "None"

def convertToMillion(value):
    try:
        return float(format(value/1000000, '.3f'))
    except:
        return 0