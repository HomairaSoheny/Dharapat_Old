from dashboard.engines.keywords import *

def getPhase(fac):
    return fac["Ref"]["Phase"]

def getRole(fac):
    if fac is not None:
        return fac["Ref"]["Role"]

def getBorrowersName(subject_info, fac = None):
    if getRole(fac) in GUARANTOR:
        if fac['Other subjects linked to the same contract'] is not None:
            for ind, Role in enumerate(fac['Other subjects linked to the same contract']["Role"]):
                if Role == "Borrower":
                    return fac['Other subjects linked to the same contract']["Name"][ind]
        return ""
    for key in BORROWER_NAME:
        if key in subject_info.keys():
            if len(subject_info[key]) == 0:
                continue
            return subject_info[key]

def isFunded(fac):
    for key in NON_FUNDED:
        if key in fac["Ref"]["Facility"].lower():
            return "No"
    return "Yes"

def getOutstanding(fac):
    if type(fac['Contract History']) == dict:
        for key in OUTSTANDING:
            if key in fac['Contract History'].keys():
                return fac['Contract History'].sort_values('Date', ascending=False)[key][0]
    return 0

def getOverdue(fac):
    if type(fac['Contract History']) == dict:
        for key in OVERDUE:
            if key in fac['Contract History'].keys():
                return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]
    return 0

def getCurrentCLStatus(fac):
    if type(fac['Contract History']) == dict:
        for key in STATUS:
            if key in fac['Contract History'].keys():
                return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]
    return ""

def getLimit(fac):
    for key in LIMIT:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def isStayOrder(facility):
    if type(facility['Contract History']) == dict:
        if type(facility['Contract History']) == dict and 'Stay Order' in facility['Contract History'].keys():
            return True
    return False

def getClassFromSet(classes : set):
    for classification in CL_STATUS:
        if classification in classes:
            return classification
    return "None"

def getWorstCLStatus(facility : dict):
    if type(facility['Contract History']) == dict:
        if not isStayOrder(facility):
            return getClassFromSet(set(facility["Contract History"].Status))
        return "None"

def getFacilityType(fac):
    for key in FACILITY:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getCurrentNPI(fac):
    if type(fac['Contract History']) == dict:
        for key in NPI:
            if key in fac['Contract History'].keys():
                return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]
    return 0


def getEMI(fac):
    for key in EMI:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]