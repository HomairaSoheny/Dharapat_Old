from dashboard.engines.keywords import *
import pandas as pd

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
    for key in OUTSTANDING:
        if key in fac['Contract History'].keys():
            return fac['Contract History'].sort_values('Date', ascending=False)[key][0]
    return 0
def getOutstandingDate(fac):
    if 'Contract History' in fac and isinstance(fac['Contract History'], pd.DataFrame):
        for column_name in OUTSTANDING:
            if column_name in fac['Contract History']:
                sorted_contracts = fac['Contract History'].sort_values('Date', ascending=True)
                if sorted_contracts[column_name].iloc[0] != 0:
                    return sorted_contracts['Date'].iloc[0]
    return None

def getOverdue(fac):
    for key in OVERDUE:
        if key in fac['Contract History'].keys():
            return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]
    return 0

def getCurrentCLStatus(fac):
    if not isStayOrder(fac):
        for key in STATUS:
            if key in fac['Contract History'].keys():
                return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]
    return ""
def getOutstandingDate(fac):
    if 'Contract History' in fac and isinstance(fac['Contract History'], pd.DataFrame):
        for column_name in OUTSTANDING:
            if column_name in fac['Contract History']:
                sorted_contracts = fac['Contract History'].sort_values('Date', ascending=True)
                if sorted_contracts[column_name].iloc[0] != 0:
                    return sorted_contracts['Date'].iloc[0]
    return pd.NaT

def getLimit(fac):
    for key in LIMIT:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def isStayOrder(facility):
    if type(facility['Contract History']) == dict and 'Stay Order' in facility['Contract History'].keys():
        return True
    return False

def getClassFromSet(classes : set):
    for classification in CL_STATUS:
        if classification in classes:
            return classification
    return ""

def getWorstCLStatus(facility : dict):
    if not isStayOrder(facility):
        return getClassFromSet(set(facility["Contract History"].Status))
    return ""

def getWorstCLDate(facility : dict):
    if not isStayOrder(facility):
        worst_CL_status = getWorstCLStatus(facility)
        df = facility["Contract History"].copy()
        worst_CL_date = df.loc[df['Status'] == worst_CL_status, 'Date'].min()
        return worst_CL_date
    return ""

def getFacilityType(fac):
    for key in FACILITY:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
    return ""

def getCurrentNPI(fac):
    for key in NPI:
        if key in fac['Contract History'].keys():
            return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]
    return 0


def getEMI(fac):
    for key in EMI:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
    return 0


def getSubjectCode(fac):
    account_name = fac['Ref']['Ref']
    first_character = account_name.strip()[0]  # Extract the first character
    if first_character.isdigit():  # Check if the first character is a digit
        return (first_character)
    else:
        return None  

