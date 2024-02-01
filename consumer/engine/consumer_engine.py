def getBorrowersName(cib):
    keys = ['Title', 'Name', 'Title, Name', 'Trade Name']
    for key in keys:
        if key in cib.subject_info.keys():
            return cib.subject_info[key]

def getFacilityType(cib_data):
    return None

def getSanctionedLimit(cib_data):
    return None

def getFacilityStartDate(cib_data):
    return None

def getLoanExpiryDate(cib_data):
    return None

def getOutstanding(cib_data):
    return None

def getEMI(cib_data):
    return None

def getTotalEMI(cib_data):
    return None

def getRemainingEMI(cib_data):
    return None

def getAvgOutstandingLast12Months(cib_data):
    return None

def getOverdue(cib_data):
    return None

def getCurrentCLStatus(cib_data):
    return None

def percentOfCreditCardLimit12Outstanding(cib_data):
    return None

def getWorstCLStatusInLast12Months(cib_data):
    return None

def getCurrentNPI(cib_data):
    return None

def getNoOfNPI(cib_data, time_frame):
    return None

def getNoOfNPI(cib_data, time_frame):
    return None