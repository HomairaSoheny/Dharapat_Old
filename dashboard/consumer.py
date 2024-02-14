import json
from dashboard.engines.consumer_engine import getConsumerDataFrame, getNID, getFathersName
from dashboard.engines.general_engine import getBorrowersName, getClassFromSet
from dashboard.engines.columns import *

def tableFilter(df, facility_type, phase, role, columns, exclude_facility_type = False, exclude_phase = False, check_business = False):
    response = []
    
    df = df[~df["Business"].isin(["No"])] if check_business else df[df["Business"].isin(["No"])]
    df = df[~df["Facility Type"].isin(facility_type)] if exclude_facility_type else df[df["Facility Type"].isin(facility_type)]
    df = df[~df["Phase"].isin(phase)] if exclude_phase else df[df["Phase"].isin(phase)]
    df = df[df["Role"].isin(role)]
    
    if df.shape[0] == 0:
        return []
    
    for i, row in df[columns].iterrows():
        response.append(row.to_dict())
        
    return response

def getConsumerDashboard(cibs):
    response = []
    for cib in cibs:
        analysis = {}
        df = getConsumerDataFrame(cib)
        
        analysis["pdf_name"] = cib.pdf_name
        analysis['analysis type'] = "Consumer"
        analysis["CIB Report of"] = getBorrowersName(cib.subject_info)
        analysis["NID Number"] = getNID(cib.subject_info)
        analysis["Fathers Name"] = getFathersName(cib.subject_info)
        analysis["No of Living Contracts"] = df[df["Phase"] == "Living"].shape[0]
        analysis["Total Outstanding"] = sum(df[df["Phase"] == "Living"]["Outstanding"])
        analysis["Total Overdue"] = sum(df[df["Phase"] == "Living"]["Overdue"])
        analysis["Current Status"] = getClassFromSet(set(df[df["Phase"] == "Living"]["Current CL Status"].tolist()))
        analysis["Overall Worst Status"] = getClassFromSet(set(df[df["Phase"] == "Living"]["Worst CL Status in Last 12 Months"].tolist()))
        
        analysis["Credit Facilities as Applicant - Live (As Borrower)"] = {
            "Term Loan": tableFilter(df=df, facility_type=["Term Loan"], phase=["Living"], role=["Borrower", "Co-Borrower", "Co- Borrower"], columns=TERM_LOAN_COLUMNS),
            "Credit Card": tableFilter(df=df, facility_type=["Credit Card (Revolving)"], phase=["Living"], role=["Borrower", "Co-Borrower", "Co- Borrower"], columns=CREDIT_CARD_COLUMNS),
            "Others": tableFilter(df=df, facility_type=["Term Loan", "Credit Card (Revolving)"], phase=["Living"], role=["Borrower", "Co-Borrower", "Co- Borrower"], columns=OTHER_COLUMNS, exclude_facility_type=True),
            }
        
        analysis["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"] = {
            "Term Loan": tableFilter(df=df, facility_type=["Term Loan"], phase=["Living"], role=["Borrower", "Co-Borrower", "Co- Borrower"], columns=TERM_LOAN_COLUMNS, exclude_phase=True),
            "Credit Card": tableFilter(df=df, facility_type=["Credit Card (Revolving)"], phase=["Living"], role=["Borrower", "Co-Borrower", "Co- Borrower"], columns=CREDIT_CARD_COLUMNS, exclude_phase=True),
            "Others": tableFilter(df=df, facility_type=["Term Loan", "Credit Card (Revolving)"], phase=["Living"], role=["Borrower", "Co-Borrower", "Co- Borrower"], columns=OTHER_COLUMNS, exclude_facility_type=True, exclude_phase=True),
            }
        
        analysis["Credit Facilities as Guarantor - Live (As Guarantor)"] = {
            "Term Loan": tableFilter(df=df, facility_type=["Term Loan"], phase=["Living"], role=["Guarantor"], columns=TERM_LOAN_COLUMNS_FOR_GURANTOR_ROLE),
            "Credit Card": tableFilter(df=df, facility_type=["Credit Card (Revolving)"], phase=["Living"], role=["Guarantor"], columns=CREDIT_CARD_COLUMNS),
            "Others": tableFilter(df=df, facility_type=["Term Loan", "Credit Card (Revolving)"], phase=["Living"], role=["Guarantor"], columns=OTHER_COLUMNS, exclude_facility_type=True),
            }
        
        analysis["Credit Facilities in the Name of Business - Live"] = {
            "Term Loan": tableFilter(df=df, facility_type=["Term Loan"], phase=["Living"], role=["Borrower", "Co-Borrower", "Co- Borrower"], columns=TERM_LOAN_COLUMNS, check_business=True),
            "Credit Card": tableFilter(df=df, facility_type=["Credit Card (Revolving)"], phase=["Living"], role=["Borrower", "Co-Borrower", "Co- Borrower"], columns=CREDIT_CARD_COLUMNS, check_business=True),
            "Others": tableFilter(df=df, facility_type=["Term Loan", "Credit Card (Revolving)"], phase=["Living"], role=["Borrower", "Co-Borrower", "Co- Borrower"], columns=OTHER_COLUMNS, exclude_facility_type=True, check_business=True),
            }
        response.append(analysis)
    
    return json.dumps(response)
