import pandas as pd
import numpy as np
from datetime import  datetime, timedelta
from dashboard.engines import general_engine
from dashboard.engines.keywords import *

def getNID(subject_info, inquired):    
    for key in NID:
        if key in subject_info.keys():
            return subject_info[key]
        if key in inquired.keys():
            return inquired[key]
        
def getFathersName(subject_info):
    for key in FATHER_NAME:
        if key in subject_info.keys():
            return subject_info[key] 

def isBusiness(fac):
    if fac['Ref']['Ref'][0] != "1":
        return "Yes"
    return "No"

def getFacilityStartDate(fac):
    for key in STARTING_DATE:
        if key in fac['Ref'].keys():
            return str(fac['Ref'][key])

def getLoanExpiryDate(fac):
    for key in END_DATE_OF_CONTRACT:
        if key in fac['Ref'].keys():
            return str(fac['Ref'][key])

def getTotalEMI(fac):
    EMI = general_engine.getEMI(fac)
    for key in TOTAL_NUMBER_OF_INSTALLMENT:
        if key in fac['Ref'].keys():
            return int(fac['Ref'][key]) * int(EMI)

def getRemainingEMI(fac):
    for key in REMAINING_INSTALLMENT_AMOUNT:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getAvgOutstandingLast12Months(fac):
    for key in OUTSTANDING:
        if key in fac['Contract History'].keys():
            df = (fac['Contract History']).sort_values('Date', ascending=False)[["Date", key]]
            return format(sum(df[df['Date'] > np.datetime64(datetime.utcnow().date() - timedelta(days=365))][key])/12, ".2f")

def percentOfCreditCardLimitOutstanding(fac):
    for key in CREDIT_LIMIT:
        if key in fac['Ref'].keys():
            credit = (fac['Ref']['Credit limit'])  
            outstand = (fac['Contract History'].sort_values('Date', ascending=False).Outstanding[0])
            if round(credit*(.6)) >= outstand :
                return (round(credit*.02))
            else:
                return (outstand*(.05))

def getWorstCLStatusInLast12Months(facility : dict):
    if not general_engine.isStayOrder(facility):
        return general_engine.getClassFromSet(set(facility["Contract History"].Status))
    return "None"

def getNoOfNPI(fac, time_frame):
    for key in NPI:
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
                    "Borrower Name": general_engine.getBorrowersName(cib.subject_info, fac),
                    "Facility Type": general_engine.getFacilityType(fac),
                    "Phase": general_engine.getPhase(fac),
                    "Role": general_engine.getRole(fac),
                    "Business": isBusiness(fac),
                    "Santioned Limit": general_engine.getLimit(fac),
                    "Facility Start Date": getFacilityStartDate(fac),
                    "Loan Expiry Date": getLoanExpiryDate(fac),
                    "Outstanding": general_engine.getOutstanding(fac),
                    "EMI": general_engine.getEMI(fac),
                    "Total EMI": getTotalEMI(fac),
                    "Remaining EMI": getRemainingEMI(fac),
                    "Average Outstanding Last 12 Months": getAvgOutstandingLast12Months(fac),
                    "Overdue": general_engine.getOverdue(fac),
                    "Current CL Status": general_engine.getCurrentCLStatus(fac),
                    'Percent of Credit Card Limit Outstanding': percentOfCreditCardLimitOutstanding(fac),
                    'Worst CL Status in Last 12 Months': getWorstCLStatusInLast12Months(fac),
                    'Current NPI': general_engine.getCurrentNPI(fac),
                    'No of NPI Last 3 Months': getNoOfNPI(fac, 3),
                    'No of NPI Last 6 Months': getNoOfNPI(fac, 6),
                    'No of NPI Last 12 Months': getNoOfNPI(fac, 12),
                })
        df = pd.concat([df, pd.DataFrame(response)], ignore_index=True)
    return df
