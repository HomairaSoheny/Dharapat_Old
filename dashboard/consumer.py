from dashboard.engines.consumer_engine import getConsumerDataFrame, getNID, getFathersName, getClassFromSet
from dashboard.engines.general_engine import getBorrowersName
from dashboard.engines.columns import *

def tableFilter(df, facility_type, phase, role, columns, exclude_facility_type = False, exclude_phase = False, check_business = False):
    df = df[~df['Business'] == False] if check_business else df[df['Business'] == False]
    df = df[~df['Facility Type'].isin(facility_type)] if exclude_facility_type else df[df['Facility Type'].isin(facility_type)]
    df = df[~df["Phase"].isin(phase)] if exclude_phase else df[df["Phase"].isin(phase)]
    df = df[df["Role"].isin(role)]
    return df[columns].to_dict()

def getConsumerDashboard(cibs):
    response = {}
    df = getConsumerDataFrame(cibs)
    
    response['CIB Report of'] = getBorrowersName(cibs[0].subject_info)
    response['NID Number'] = getNID(cibs[0].subject_info)
    response["Fathers Name"] = getFathersName(cibs[0].subject_info)
    response["No of Living Contracts"] = df[df['Phase'] == 'Living'].shape[0]
    response["Total Outstanding"] = sum(df[df['Phase'] == 'Living']['Outstanding'])
    response["Total Overdue"] = sum(df[df['Phase'] == 'Living']['Overdue'])
    response["Current Status"] = getClassFromSet(set(df[df['Phase'] == 'Living']['Current CL Status'].tolist()))
    response["Overall Worst Status"] = getClassFromSet(set(df[df['Phase'] == 'Living']['Worst CL Status in Last 12 Months'].tolist()))
    
    response["Credit Facilities as Applicant - Live (As Borrower)"] = {
        "Term Loan": tableFilter(df=df, facility_type=['Term Loan'], phase=['Living'], role=['Borrower', 'Co-Borrower', 'Co- Borrower'], columns=TERM_LOAN_COLUMNS),
        "Credit Card": tableFilter(df=df, facility_type=['Credit Card (Revolving)'], phase=['Living'], role=['Borrower', 'Co-Borrower', 'Co- Borrower'], columns=CREDIT_CARD_COLUMNS),
        "Others": tableFilter(df=df, facility_type=['Term Loan', 'Credit Card (Revolving)'], phase=['Living'], role=['Borrower', 'Co-Borrower', 'Co- Borrower'], columns=OTHER_COLUMNS, exclude_facility_type=True),
        }
    
    response["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"] = {
        "Term Loan": tableFilter(df=df, facility_type=['Term Loan'], phase=['Living'], role=['Borrower', 'Co-Borrower', 'Co- Borrower'], columns=TERM_LOAN_COLUMNS, exclude_phase=True),
        "Credit Card": tableFilter(df=df, facility_type=['Credit Card (Revolving)'], phase=['Living'], role=['Borrower', 'Co-Borrower', 'Co- Borrower'], columns=CREDIT_CARD_COLUMNS, exclude_phase=True),
        "Others": tableFilter(df=df, facility_type=['Term Loan', 'Credit Card (Revolving)'], phase=['Living'], role=['Borrower', 'Co-Borrower', 'Co- Borrower'], columns=OTHER_COLUMNS, exclude_facility_type=True, exclude_phase=True),
        }
    
    response["Credit Facilities as Guarantor - Live (As Guarantor)"] = {
        "Term Loan": tableFilter(df=df, facility_type=['Term Loan'], phase=['Living'], role=['Guarantor'], columns=TERM_LOAN_COLUMNS),
        "Credit Card": tableFilter(df=df, facility_type=['Credit Card (Revolving)'], phase=['Living'], role=['Guarantor'], columns=CREDIT_CARD_COLUMNS),
        "Others": tableFilter(df=df, facility_type=['Term Loan', 'Credit Card (Revolving)'], phase=['Living'], role=['Guarantor'], columns=OTHER_COLUMNS, exclude_facility_type=True),
        }
    
    response["Credit Facilities in the Name of Business - Live"] = {
        "Term Loan": tableFilter(df=df, facility_type=['Term Loan'], phase=['Living'], role=['Borrower', 'Co-Borrower', 'Co- Borrower'], columns=TERM_LOAN_COLUMNS, check_business=True),
        "Credit Card": tableFilter(df=df, facility_type=['Credit Card (Revolving)'], phase=['Living'], role=['Borrower', 'Co-Borrower', 'Co- Borrower'], columns=CREDIT_CARD_COLUMNS, check_business=True),
        "Others": tableFilter(df=df, facility_type=['Term Loan', 'Credit Card (Revolving)'], phase=['Living'], role=['Borrower', 'Co-Borrower', 'Co- Borrower'], columns=OTHER_COLUMNS, exclude_facility_type=True, check_business=True),
        }
    
    return response