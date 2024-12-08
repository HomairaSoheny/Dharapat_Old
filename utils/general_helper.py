def convertToInteger(value):
    try:
        return int(value)
    except:
        return 0

def convertToFloat(value):
    try:
        return float(format(value, '.6f'))
    except:
        return 0

def convertToString(value):
    try:
        return str(value)
    except:
        return "None"

def convertToMillion(value):
    try:
        return float(format(value/1000000, '.6f'))
    except:
        return 0
    
def convertToRaw(value):
    try:
        return float(format(value*1000000, '.2f'))
    except:
        return 0
    
def convertnanToZero(value):
    try:
        return float(value)
    except:
        return 0