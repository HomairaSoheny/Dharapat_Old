def getBorrowersName(cib):
    keys = ['Title', 'Name', 'Title, Name', 'Trade Name']
    for key in keys:
        if key in cib.subject_info.keys():
            return cib.subject_info[key]

def getFacilityType(fac):
    for key in ['Facility']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

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

def getTotalEMI(fac):
    return None

def getRemainingEMI(fac):
    for key in ['Remaining Amount', 'Remaining installments Amount']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getAvgOutstandingLast12Months(fac):
    return None

def getOverdue(fac):
    for key in ['Overdue']:
        if key in fac['Contract History'].keys():
            return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]

def getCurrentCLStatus(fac):
    for key in ['Status']:
        if key in fac['Contract History'].keys():
            return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]

def percentOfCreditCardLimit12Outstanding(fac):
    return None

def getWorstCLStatusInLast12Months(fac):
    return None

def getCurrentNPI(fac):
    return None

def getNoOfNPI(fac, time_frame):
    return None