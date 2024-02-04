def getPhase(fac):
    return fac["Ref"]["Phase"]

def getRole(fac):
    return fac["Ref"]["Role"]

def getBorrowersName(subject_info):
    keys = ['Title', 'Name', 'Title, Name', 'Trade Name']
    for key in keys:
        if key in subject_info.keys():
            if len(subject_info[key]) == 0:
                continue
            return subject_info[key]

def isNonFunded(fac):
    keywords = ['non funded', 'letter of credit', 'gurantee', 'other indirect facility']
    for key in keywords:
        if key in fac["Ref"]["Facility"].lower():
            return True
    return False

def getOutstanding(fac):
    for key in ['Outstand', 'Outstanding']:
        if key in fac['Contract History'].keys():
            return fac['Contract History'].sort_values('Date', ascending=False)[key][0]

def getOverdue(fac):
    for key in ['Overdue']:
        if key in fac['Contract History'].keys():
            return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]

def getCurrentCLStatus(fac):
    for key in ['Status']:
        if key in fac['Contract History'].keys():
            return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]

def getLimit(fac):
    for key in ['Sanction Limit', 'Credit limit']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]