import pandas as pd
import numpy as np
from datetime import  datetime, timedelta

def getBorrowersName(subject_info):
    keys = ['Title', 'Name', 'Title, Name', 'Trade Name']
    for key in keys:
        if key in subject_info.keys():
            if len(subject_info[key]) == 0:
                continue
            return subject_info[key]

def isBusiness(subject_info):
    keys = ['Trade Name']
    for key in keys:
        if key in subject_info.keys():
            if len(subject_info[key]) > 0:
                return True
    return False

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
            return str(fac['Ref'][key])

def getLoanExpiryDate(fac):
    for key in ['End date of contract']:
        if key in fac['Ref'].keys():
            return str(fac['Ref'][key])

def getOutstanding(fac):
    for key in ['Outstand', 'Outstanding']:
        if key in fac['Contract History'].keys():
            return fac['Contract History'].sort_values('Date', ascending=False)[key][0]

def getEMI(fac):
    for key in ['Monthly instalment amount', 'Installment Amount']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getTotalEMI(fac):
    EMI = getEMI(fac)
    for key in ['Total number of installments']:
        if key in fac['Ref'].keys():
            return int(fac['Ref'][key]) * int(EMI)

def getRemainingEMI(fac):
    for key in ['Remaining Amount', 'Remaining installments Amount']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getAvgOutstandingLast12Months(fac):
    for key in ['Outstanding', 'Outstand']:
        if key in fac['Contract History'].keys():
            df = (fac['Contract History']).sort_values('Date', ascending=False)[["Date", key]]
            return sum(df[df['Date'] > np.datetime64(datetime.utcnow().date() - timedelta(days=365))][key])/12

def getOverdue(fac):
    for key in ['Overdue']:
        if key in fac['Contract History'].keys():
            return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]

def getCurrentCLStatus(fac):
    for key in ['Status']:
        if key in fac['Contract History'].keys():
            return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]

def percentOfCreditCardLimitOutstanding(fac):
    return None

def isStayOrder(facility):
    if type(facility['Contract History']) == dict and 'Stay Order' in facility['Contract History'].keys():
        return True
    return False

def getClassFromSet(classes : set):
    for classification in ('BLW', 'BL', 'DF', 'SS', 'SMA', 'UC', "STD"):
        if classification in classes:
            return classification
    return "None"

def getWorstCLStatusInLast12Months(facility : dict):
    if not isStayOrder(facility):
        return getClassFromSet(set(facility["Contract History"].Status))
    return "None"

def getCurrentNPI(fac):
    for key in ['NPI']:
        if key in fac['Contract History'].keys():
            return (fac['Contract History']).sort_values('Date', ascending=False)[key][0]

def getNoOfNPI(fac, time_frame):
    for key in ['NPI']:
        if key in fac['Contract History'].keys():
            df = (fac['Contract History']).sort_values('Date', ascending=False)[["Date", key]]
            df = df[df[key] != 0]
            return df[df['Date'] > np.datetime64(datetime.utcnow().date() - timedelta(days=time_frame*30))][key].shape[0]

def getConsumerDataFrame(cibs):
    df = pd.DataFrame()
    for cib in cibs:
        for fac_type in (cib.installment_facility, cib.noninstallment_facility, cib.credit_card_facility):
            response = []
            if fac_type is not None:
                for fac in fac_type:
                    response.append({
                        "Borrowers Name": getBorrowersName(cib.subject_info),
                        "Facility Type": getFacilityType(fac),
                        "Phase": fac["Ref"]["Phase"],
                        "Role": fac["Ref"]["Role"],
                        "Business": isBusiness(cib.subject_info),
                        "Santioned Limit": getSanctionLimit(fac),
                        "Facility Start Date": getFacilityStartDate(fac),
                        "Loan Expiry Date": getLoanExpiryDate(fac),
                        "Outstanding": getOutstanding(fac),
                        "EMI": getEMI(fac),
                        "Total EMI": getTotalEMI(fac),
                        "Remaining EMI": getRemainingEMI(fac),
                        "Average Outstanding Last 12 Months": getAvgOutstandingLast12Months(fac),
                        "Overdue": getOverdue(fac),
                        "Current CL Status": getCurrentCLStatus(fac),
                        'Percent of Credit Card Limit Outstanding': percentOfCreditCardLimitOutstanding(fac),
                        'Worst CL Status in Last 12 Months': getWorstCLStatusInLast12Months(fac),
                        'Current NPI': getCurrentNPI(fac),
                        'No of NPI Last 3 Months': getNoOfNPI(fac, 3),
                        'No of NPI Last 6 Months': getNoOfNPI(fac, 6),
                        'No of NPI Last 12 Months': getNoOfNPI(fac, 12),
                    })
            df = pd.concat([df, pd.DataFrame(response)], ignore_index=True)
    return df