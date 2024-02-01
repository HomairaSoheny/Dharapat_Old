import pandas as pd

def getBorrowersName(cib):
    keys = ['Title', 'Name', 'Title, Name', 'Trade Name']
    for key in keys:
        if key in cib.subject_info.keys():
            if len(cib.subject_info[key]) == 0:
                continue
            return cib.subject_info[key]

def isBusiness(cib):
    keys = ['Trade Name']
    for key in keys:
        if key in cib.subject_info.keys():
            if len(cib.subject_info[key]) > 0:
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

def getConsumerDataFrame(cibs):
    df = pd.DataFrame()
    for cib in cibs:
        for fac_type in (cib.installment_facility, cib.noninstallment_facility, cib.credit_card_facility):
            response = []
            if fac_type is not None:
                for fac in fac_type:
                    response.append({
                        "Borrowers Name": getBorrowersName(cib),
                        "Facility Type": getFacilityType(fac),
                        "Phase": fac["Ref"]["Phase"],
                        "Role": fac["Ref"]["Role"],
                        "Business": isBusiness(cib),
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
                        'Percent of Credit Card Limit Outstanding': percentOfCreditCardLimit12Outstanding(fac),
                        'Worst CL Status in Last 12 Months': getWorstCLStatusInLast12Months(fac),
                        'Current NPI': getCurrentNPI(cib),
                        'No of NPI Last 3 Months': getNoOfNPI(cib, 3),
                        'No of NPI Last 6 Months': getNoOfNPI(cib, 6),
                        'No of NPI Last 12 Months': getNoOfNPI(cib, 12),
                    })
            df = pd.concat([df, pd.DataFrame(response)], ignore_index=True)
    return df