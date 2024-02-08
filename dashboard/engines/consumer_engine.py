import pandas as pd
import numpy as np
from datetime import  datetime, timedelta
from dashboard.engines import general_engine

def getNID(subject_info):
    keys = ['NID','NID (10 Digit)', 'NID no', 'NID (17 Digit) No', 'NID (10 Digit) No', 'NID (10 or 17 Digit)', 'NID (17 Digit)']
    for key in keys:
        if key in subject_info.keys():
            return subject_info[key]
        
def getFathersName(subject_info):
    keys = ["Title, Father's name"]
    for key in keys:
        if key in subject_info.keys():
            return subject_info[key]

def isBusiness(subject_info):
    keys = ['Trade Name']
    for key in keys:
        if key in subject_info.keys():
            if len(subject_info[key]) > 0:
                return "Yes"
    return "No"

def getFacilityStartDate(fac):
    for key in ['Starting date']:
        if key in fac['Ref'].keys():
            return str(fac['Ref'][key])

def getLoanExpiryDate(fac):
    for key in ['End date of contract']:
        if key in fac['Ref'].keys():
            return str(fac['Ref'][key])

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

def percentOfCreditCardLimitOutstanding(fac):
    return "Not Implemented"

def getWorstCLStatusInLast12Months(facility : dict):
    if not general_engine.isStayOrder(facility):
        return general_engine.getClassFromSet(set(facility["Contract History"].Status))
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

def getConsumerDataFrame(cib):
    df = pd.DataFrame(columns = ['Borrowers Name', 'Facility Type', 'Phase', 'Role', 'Business', 'Santioned Limit', 'Facility Start Date', 'Loan Expiry Date', 'Outstanding', 'EMI', 'Total EMI', 'Remaining EMI', 'Average Outstanding Last 12 Months', 'Overdue', 'Current CL Status', 'Percent of Credit Card Limit Outstanding', 'Worst CL Status in Last 12 Months', 'Current NPI', 'No of NPI Last 3 Months', 'No of NPI Last 6 Months', 'No of NPI Last 12 Months'])
    for fac_type in (cib.installment_facility, cib.noninstallment_facility, cib.credit_card_facility):
        response = []
        if fac_type is not None:
            for fac in fac_type:
                response.append({
                    "Borrowers Name": general_engine.getBorrowersName(cib.subject_info),
                    "Borrower Name": general_engine.getConditionalBorrowerName(fac),
                    "Facility Type": general_engine.getFacilityType(fac),
                    "Phase": general_engine.getPhase(fac),
                    "Role": general_engine.getRole(fac),
                    "Business": isBusiness(cib.subject_info),
                    "Santioned Limit": general_engine.getLimit(fac),
                    "Facility Start Date": getFacilityStartDate(fac),
                    "Loan Expiry Date": getLoanExpiryDate(fac),
                    "Outstanding": general_engine.getOutstanding(fac),
                    "EMI": getEMI(fac),
                    "Total EMI": getTotalEMI(fac),
                    "Remaining EMI": getRemainingEMI(fac),
                    "Average Outstanding Last 12 Months": getAvgOutstandingLast12Months(fac),
                    "Overdue": general_engine.getOverdue(fac),
                    "Current CL Status": general_engine.getCurrentCLStatus(fac),
                    'Percent of Credit Card Limit Outstanding': percentOfCreditCardLimitOutstanding(fac),
                    'Worst CL Status in Last 12 Months': getWorstCLStatusInLast12Months(fac),
                    'Current NPI': getCurrentNPI(fac),
                    'No of NPI Last 3 Months': getNoOfNPI(fac, 3),
                    'No of NPI Last 6 Months': getNoOfNPI(fac, 6),
                    'No of NPI Last 12 Months': getNoOfNPI(fac, 12),
                })
        df = pd.concat([df, pd.DataFrame(response)], ignore_index=True)
    return df
