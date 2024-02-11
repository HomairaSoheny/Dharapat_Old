import pandas as pd
from dashboard.engines import general_engine

def getCIBCategory(cib):
    category_mapping = {
        "Type a": "Concerns of primary borrower with PBL",
        "Type b": "Other sister concerns of primary borrower",
        "Type c": "Other concerns due to common shareholdings/directorship",
        "Type d": "Directors CIB",
        "Type e": "20% plus shareholder other than director",
        "Type f": "Guarantors CIB (Personal)",
        "Type g": "Corporate Guarantor",
        "Type h": "Related party of Guarantor",
        "Type i": "Other concerns/persons not related to the company"
    }

    return category_mapping.get(cib.cib_category, None)

def getDateOfClassification(fac):
    for key in ['Date of classification']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
        
def getStartDate(fac):
    for key in ['Starting date']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
        
def getEndDateOfContract(fac):
    for key in ['End date of contract']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
        
def getRemarks(fac):
    for key in ['Remarks']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
        
def getPaymentPeriod(fac):
    for key in ['Payments Periodicity', 'Payments periodicity',]:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getTotalNumberOfInstallment(fac):
    for key in ['Total number of installments']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
        
def getNoOfRemainingInstallment(fac):
    for key in ['Remaining installments Number']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
        
def getDateOfLastPayment(fac):
    for key in ['Date of last payment']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getFacilityType(i):
    facility_types = {
        0: "Installment",
        1: "No Installment",
        2: "Credit Card"
    }
    return facility_types.get(i, "Unknown")

def getFundedOutstandingInstallment(df):
    df = df[df['Is Funded'] == 'Yes']
    df = df[df['Installment Type'] == 'Installment']
    return float(format(df['Outstanding'].sum()/1000000, ".3f"))

def getFundedOutstandingNonInstallment(df):
    df = df[df['Is Funded'] == 'Yes']
    df = df[df['Installment Type'] == 'No Installment']
    return float(format(df['Outstanding'].sum()/1000000, ".3f"))

def getFundedOutstandingTotal(df):
    return float(format(getFundedOutstandingInstallment(df) + getFundedOutstandingNonInstallment(df), '.3f'))

def getNonFundedOutstanding(df):
    df = df[df['Is Funded'] == 'No']
    return float(format(df['Outstanding'].sum()/1000000, ".3f"))

def getTotalOutstanding(df):
    return float(format(getFundedOutstandingTotal(df) + getNonFundedOutstanding(df), '.3f'))

def getOverdue(df):
    return float(format(df['Overdue'].sum()/1000000, ".3f"))

def getDefault(fac):
    return "Yes" if "Yes" in fac['Contract History']['Default'].tolist() else "No"

def getCorporateDataFrame(cibs):
    df = pd.DataFrame()
    for cib in cibs:
        for i, fac_type in enumerate((cib.installment_facility, cib.noninstallment_facility, cib.credit_card_facility)):
            response = []
            if fac_type is not None:
                for fac in fac_type:
                    response.append({
                        "CIB Category": getCIBCategory(cib),
                        "Name": general_engine.getBorrowersName(cib.subject_info),
                        "Facility Type": general_engine.getFacilityType(fac),
                        "Phase": general_engine.getPhase(fac),
                        "Role": general_engine.getRole(fac),
                        "Is Funded": general_engine.isFunded(fac),
                        "Installment Type": getFacilityType(i),
                        "Outstanding": general_engine.getOutstanding(fac),
                        "Overdue": general_engine.getOverdue(fac),
                        "CL Status": general_engine.getCurrentCLStatus(fac),
                        "Default": getDefault(fac),
                        "Limit": general_engine.getLimit(fac),
                        "Loan/Limit (days of adjustment before/after)": "Need elaboration",
                        "Worse Classification Status": general_engine.getWorstCLStatus(fac),
                        "Date of Classification": getDateOfClassification(fac),
                        "Start Date": getStartDate(fac),
                        "End Date of Contract": getEndDateOfContract(fac),
                        "Type of Reschedule": "Need Elaboration",
                        "Reschedule Amount": "Need Elaboration",
                        "Date of Last Rescheduling": "Need Elaboration",
                        "Requested Amount": "Need Elaboration",
                        "Date of Request": "Need Elaboration",
                        "Writ no": "Need Elaboration",
                        "Remarks": getRemarks(fac),
                        "Payment Period (Monthly/Quarterly)": getPaymentPeriod(fac),
                        "Total No of Installment": getTotalNumberOfInstallment(fac),
                        "No of Remaining Installment": getNoOfRemainingInstallment(fac),
                        "Date of Last Payment": getDateOfLastPayment(fac),
                        "NPI": general_engine.getCurrentNPI(fac)
                    })
            df = pd.concat([df, pd.DataFrame(response)], ignore_index=True)
    return df