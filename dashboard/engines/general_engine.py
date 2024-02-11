def getPhase(fac):
    return fac["Ref"]["Phase"]

def getRole(fac):
    if fac is not None:
        return fac["Ref"]["Role"]

def getBorrowersName(subject_info, fac = None):
    keys = ['Title', 'Name', 'Title, Name', 'Trade Name']
    if getRole(fac) in ['Guarantor']:
        if fac['Other subjects linked to the same contract'] is not None:
            for ind, Role in enumerate(fac['Other subjects linked to the same contract']["Role"]):
                if Role == "Borrower":
                    return fac['Other subjects linked to the same contract']["Name"][ind]
        return ""
    for key in keys:
        if key in subject_info.keys():
            if len(subject_info[key]) == 0:
                continue
            return subject_info[key]

def isNonFunded(fac):
    keywords = ['non funded', 'letter of credit', 'gurantee', 'other indirect facility']
    for key in keywords:
        if key in fac["Ref"]["Facility"].lower():
            return "Yes"
    return "No"

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

def isStayOrder(facility):
    if type(facility['Contract History']) == dict and 'Stay Order' in facility['Contract History'].keys():
        return True
    return False

def getClassFromSet(classes : set):
    for classification in ('BLW', 'BL', 'DF', 'SS', 'SMA', 'UC', "STD"):
        if classification in classes:
            return classification
    return "None"

def getWorstCLStatus(facility : dict):
    if not isStayOrder(facility):
        return getClassFromSet(set(facility["Contract History"].Status))
    return "None"

def getFacilityType(fac):
    for key in ['Facility']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getCurrentNPI(fac):
    for key in ['NPI']:
        if key in fac['Contract History'].keys():
            return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]