def getBorrowersName(cib):
    keys = ['Title', 'Name', 'Title, Name', 'Trade Name']
    for key in keys:
        if key in cib.subject_info.keys():
            return cib.subject_info[key]

def getFacilityType(cib_data):
    return None

def getSanctionLimit(fac):
    for key in ['Sanction Limit', 'Credit limit']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getFacilityStartDate(fac):
    for key in ['Starting date']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getLoanExpiryDate(fac):
    for key in ['End date of contract']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getOutstanding(fac):
    for key in ['Outstand', 'Outstanding']:
        if key in fac['Contract History'].keys():
            return fac['Contract History'].sort_values('Date', ascending=False)[key][0]

def getEMI(fac):
    for key in ['Monthly instalment amount', 'Installment Amount']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getTotalEMI(cib_data):
    return None

def getRemainingEMI(cib_data):
    return None

def getAvgOutstandingLast12Months(cib_data):
    return None

def getOverdue(fac):
    for key in ['Overdue']:
        if key in fac['Contract History'].keys():
            return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]

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