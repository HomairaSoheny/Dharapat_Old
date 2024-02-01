from consumer.engine import getConsumerDataFrame

TERM_LOAN_COLUMNS = ["Borrowers Name", "Facility Type", "Santioned Limit", "Facility Start Date", "Loan Expiry Date", "Outstanding", "EMI", "Total EMI", "Remaining EMI", "Overdue", "Current CL Status", "Worst CL Status in Last 12 Months", 'Current NPI', 'No of NPI Last 3 Months', 'No of NPI Last 6 Months', 'No of NPI Last 12 Months']
CREDIT_CARD_COLUMNS = ["Borrowers Name", "Facility Type", "Santioned Limit", "Facility Start Date", "Loan Expiry Date", "Outstanding", "Average Outstanding Last 12 Months", "Overdue", "Current CL Status", "Percent of Credit Card Limit Outstanding" ,"Worst CL Status in Last 12 Months", 'Current NPI', 'No of NPI Last 3 Months', 'No of NPI Last 6 Months', 'No of NPI Last 12 Months']
OTHER_COLUMNS = ["Borrowers Name", "Facility Type", "Santioned Limit", "Facility Start Date", "Loan Expiry Date", "Outstanding", "Average Outstanding Last 12 Months", "Overdue", "Current CL Status", "Percent of Credit Card Limit Outstanding" ,"Worst CL Status in Last 12 Months", 'Current NPI', 'No of NPI Last 3 Months', 'No of NPI Last 6 Months', 'No of NPI Last 12 Months']

def tableFilter(df, facility_type, phase, role, columns, exclude_facility_type = False):
    if exclude_facility_type:
        df = df[~df['Facility Type'].isin(facility_type)]
    else:
        df = df[df['Facility Type'].isin(facility_type)]
    df = df[df["Phase"] == phase]
    df = df[df["Role"].isin(role)]
    return df[columns]

def getConsumerDashboard(cibs):
    response = {}
    df = getConsumerDataFrame(cibs)
    
    response["Credit Facilities as Applicant - Live (As Borrower)"] = {
        "Term Loan": tableFilter(df=df, facility_type=['Term Loan'], phase='Living', role=['Borrower', 'Co-Borrower', 'Co- Borrower'], columns=TERM_LOAN_COLUMNS),
        "Credit Card": tableFilter(df=df, facility_type=['Credit Card (Revolving)'], phase='Living', role=['Co-Borrower', 'Co- Borrower'], columns=CREDIT_CARD_COLUMNS),
        "Others": tableFilter(df=df, facility_type=['Term Loan', 'Credit Card (Revolving)'], phase='Living', role=['Co-Borrower', 'Co- Borrower'], columns=OTHER_COLUMNS, exclude_facility_type=True),
        }
    return response