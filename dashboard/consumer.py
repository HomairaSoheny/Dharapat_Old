from utils.general_helper import convertToString
from dashboard.engines.consumer_engine import getConsumerDataFrame, getNID, getFathersName
from dashboard.engines.general_engine import getBorrowersName, getClassFromSet
from dashboard.engines.columns import *
from dashboard.engines.keywords import *

def tableFilter(df, facility_type, phase, role, columns, exclude_facility_type = False, exclude_phase = False, check_business = False):
    response = []
    
    df = df[~df["Business"].isin(["No"])] if check_business else df[df["Business"].isin(["No"])]
    df = df[~df["Facility Type"].isin(facility_type)] if exclude_facility_type else df[df["Facility Type"].isin(facility_type)]
    df = df[~df["Phase"].isin(phase)] if exclude_phase else df[df["Phase"].isin(phase)]
    df = df[df["Role"].isin(role)]
    
    if df.shape[0] == 0:
        return []
    
    for i, row in df[columns].iterrows():
        analysis_dict = {}
        row_dict = row.to_dict()
        for key in row_dict:
            analysis_dict[key] = convertToString(row_dict[key])
        response.append(analysis_dict)
        
    return response

def getConsumerDashboard(cibs):
    response = []
    for cib in cibs:
        analysis = {}
        df = getConsumerDataFrame(cib)
        
        analysis["pdf_name"] = convertToString(cib.pdf_name)
        analysis['analysis type'] = "Consumer"
        analysis["CIB Report of"] = convertToString(getBorrowersName(cib.subject_info))
        analysis["NID Number"] = convertToString(getNID(cib.subject_info, cib.inquired))
        analysis["Fathers Name"] = convertToString(getFathersName(cib.subject_info))
        analysis["No of Living Contracts"] = convertToString(df[(df["Phase"] == "Living") & df['Role'].isin(BORROWER)].shape[0])
        analysis["Total Outstanding"] = convertToString(sum(df[(df["Phase"] == "Living") & df['Role'].isin(BORROWER)]["Outstanding"]))
        analysis["Total Overdue"] = convertToString(sum(df[(df["Phase"] == "Living") & df['Role'].isin(BORROWER)]["Overdue"]))
        analysis["Current Status"] = convertToString(getClassFromSet(set(df[(df["Phase"] == "Living") & df['Role'].isin(BORROWER)]["Current CL Status"].tolist())))
        analysis["Overall Worst Status"] = convertToString(getClassFromSet(set(df[(df["Phase"] == "Living") & df['Role'].isin(BORROWER)]["Worst CL Status in Last 12 Months"].tolist())))
        
        analysis["Credit Facilities as Applicant - Live (As Borrower)"] = {
            "Term Loan": tableFilter(df=df, facility_type=TERM_LOAN, phase=["Living"], role=BORROWER, columns=TERM_LOAN_COLUMNS),
            "Credit Card": tableFilter(df=df, facility_type=CREDIT_CARD, phase=["Living"], role=BORROWER, columns=CREDIT_CARD_COLUMNS),
            "Others": tableFilter(df=df, facility_type=["Term Loan", "Credit Card (Revolving)"], phase=["Living"], role=BORROWER, columns=OTHER_COLUMNS, exclude_facility_type=True),
            }
        
        analysis["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"] = {
            "Term Loan": tableFilter(df=df, facility_type=TERM_LOAN, phase=["Living"], role=BORROWER, columns=TERM_LOAN_COLUMNS, exclude_phase=True),
            "Credit Card": tableFilter(df=df, facility_type=CREDIT_CARD, phase=["Living"], role=BORROWER, columns=CREDIT_CARD_COLUMNS, exclude_phase=True),
            "Others": tableFilter(df=df, facility_type=["Term Loan", "Credit Card (Revolving)"], phase=["Living"], role=BORROWER, columns=OTHER_COLUMNS, exclude_facility_type=True, exclude_phase=True),
            }
        
        analysis["Credit Facilities as Guarantor - Live (As Guarantor)"] = {
            "Term Loan": tableFilter(df=df, facility_type=TERM_LOAN, phase=["Living"], role=["Guarantor"], columns=TERM_LOAN_COLUMNS_FOR_GURANTOR_ROLE),
            "Credit Card": tableFilter(df=df, facility_type=CREDIT_CARD, phase=["Living"], role=["Guarantor"], columns=CREDIT_CARD_COLUMNS),
            "Others": tableFilter(df=df, facility_type=["Term Loan", "Credit Card (Revolving)"], phase=["Living"], role=["Guarantor"], columns=OTHER_COLUMNS, exclude_facility_type=True),
            }
        
        analysis["Credit Facilities in the Name of Business - Live"] = {
            "Term Loan": tableFilter(df=df, facility_type=TERM_LOAN, phase=["Living"], role=BORROWER, columns=TERM_LOAN_COLUMNS, check_business=True),
            "Credit Card": tableFilter(df=df, facility_type=CREDIT_CARD, phase=["Living"], role=BORROWER, columns=CREDIT_CARD_COLUMNS, check_business=True),
            "Others": tableFilter(df=df, facility_type=["Term Loan", "Credit Card (Revolving)"], phase=["Living"], role=BORROWER, columns=OTHER_COLUMNS, exclude_facility_type=True, check_business=True),
            }
        response.append(analysis)
    
    return response
