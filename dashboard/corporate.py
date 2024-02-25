from dashboard.engines.corporate_engine import *
from utils.general_helper import *

def getSummaryTable(df):
    response = []
    for category in df['CIB Category'].unique():
        cat_df = df[df['CIB Category'] == category]
        for concern_name in df['Name'].unique():
            temp_df = cat_df[cat_df['Name'] == concern_name]
            response.append(getSummaryTableFields(category, concern_name, temp_df))
        sub_total_df = pd.DataFrame(response)
        sub_total_df = sub_total_df[sub_total_df['CIB Category'] == category]
        response.append(getSummaryTableSum(category, "Sub Total", sub_total_df))
    total_df = pd.DataFrame(response)
    total_df = total_df[total_df['Name of Concern'] == "Sub Total"]
    response.append(getSummaryTableSum(category, "Grand Total", total_df))
    return response

def getSummaryOfTerminatedFacilityFunded(df):
    response = []
    df = df[df['Phase'] != 'Living']
    df = df[df['Is Funded'] == "Yes"]
    df = df[df['Installment Type'] == 'Installment']
    
    for i, row in df.iterrows():
        response.append({
            "Installment": row['Facility Type'],
            "Limit": convertToFloat(row["Limit"]),
            "Loan/Limit (days of adjustment before/after)": "Not Implemented",
            "Worse Classification Status": row["CL Status"],
            "Date of Classification": convertToString(row["Date of Classification"])
        })
    return response

def getSummaryOfTerminatedFacilityNonFunded(df):
    response = []
    df = df[df['Phase'] != 'Living']
    df = df[df['Is Funded'] == "No"]
    df = df[df['Installment Type'] == 'No Installment']
    
    for i, row in df.iterrows():
        response.append({
            "Non-Installment": row['Facility Type'],
            "Limit": convertToFloat(row["Limit"]),
            "Loan/Limit (days of adjustment before/after)": "Not Implemented",
            "Worse Classification Status": row["CL Status"],
            "Date of Classification": convertToString(row["Date of Classification"])
        })
    return response
    

def getSummaryOfFundedFacility(df):
    response = []
    df = df[df['Is Funded'] == 'Yes']
    installment = df[df['Installment Type'] == 'Installment']
    non_installment = df[df['Installment Type'] == 'No Installment']

    for i, row in installment.iterrows():
        response.append(getSummaryOfFundedFacilityFields(row, i, True))
    response.append(getSummaryOfFundedFacilitySum(installment, "Sub Total", "Installment"))

    for i, row in non_installment.iterrows():
        response.append(getSummaryOfFundedFacilityFields(row, i, False))
    response.append(getSummaryOfFundedFacilitySum(non_installment, "Sub Total", "No Installment"))
    
    return response

def getSummaryOfNonFundedFacility(df):
    response = []
    df = df[df['Is Funded'] == 'No']
    for i, row in df.iterrows():
        response.append({
            "Nature of Facility": row['Facility Type'],
            "Limit": convertToFloat(row["Limit"]),
            "Outstanding": convertToFloat(row["Outstanding"]),
            "Start Date": convertToString(row["Start Date"]),
            "End Date of Contract": convertToString(row["End Date of Contract"]),
            "Default": row["Default"]
        })
    return response

def getSummaryOfFacilities(df):
    response = {}
    summary_of_funded_facility = {}
    summary_of_non_funded_facility = {}
    
    for cib_type in df['CIB Category'].unique():
        temp_df = df[df['CIB Category'] == cib_type]
        summary_of_funded_facility[cib_type] = getSummaryOfFundedFacility(temp_df)
        summary_of_non_funded_facility[cib_type] = getSummaryOfNonFundedFacility(temp_df)

    response['Summary of funded facility'] = summary_of_funded_facility
    response['Summary of non funded facility'] = summary_of_non_funded_facility
    return response

def getSummaryOfRescheduleLoan(df, role):
    response = []
    df = df[(df['Reschedule Type'] != "Not Rescheduled") & df['Role'].isin(role)]
    for i, row in df.iterrows():
        response.append({
            "Name of Account": row['Facility Type'],
            "Type of Reschedule": row['Reschedule Type'],
            "Expiry of Reschedule Loan": convertToString(row['End Date of Contract']),
            "Amount": row['Total Disbursement Amount'],
            "Date of Last Rescheduling": row['Last Date of Reschedule'],
            "Link": row['CIB Link']
        })
    response.append({
        "Name of Account": "Sub Total",
        "Type of Reschedule": "-",
        "Expiry of Reschedule Loan": "-",
        "Amount": convertToInteger(df['Total Disbursement Amount'].sum),
        "Date of Last Rescheduling": "-",
        "Link": "-"
    })
    return response

def getSummaryOfRequestedLoan(cibs):
    response = []
    df = pd.DataFrame()
    for cib in cibs:
        if cib.req_contracts is not None:
            temp_cib = cib.req_contracts
            temp_cib['Role'] = getCIBCategory(cib)
            temp_cib['Link'] = LINK + cib.pdf_name
            df = pd.concat([df, temp_cib])
    for i, row in df.iterrows():
        response.append({
            "Type of Loan": convertToString(row['Type of Contract']),
            "Facility": convertToString(row['Facility']),
            "Role": convertToString(row['Role']),
            "Requested Amount": convertToString(row['Total Requested Amount']),
            "Date of Request": convertToString(row['Request date']).replace(" 00:00:00", ""),
            "Link": convertToString(row['Link'])
        })
    return response

def getCorporateDashboard(cibs):
    response = {}
    df = getCorporateDataFrame(cibs)
    response['analysis type'] = "Corporate"
    response['Summary Table - 1'] = getSummaryTable(df)
    response['A - Summary of Terminated Facilities'] = {
        "Funded": getSummaryOfTerminatedFacilityFunded(df),
        "Non Funded": getSummaryOfTerminatedFacilityNonFunded(df)
    }
    response['B - Summary of Facilities'] = getSummaryOfFacilities(df)
    response['C - Summary of Reschedule Loan'] = {
        "Borrower": getSummaryOfRescheduleLoan(df, BORROWER),
        "Guarantor": getSummaryOfRescheduleLoan(df, GUARANTOR) 
    }
    response['D - Summary of Requested Loan'] = getSummaryOfRequestedLoan(cibs)
    
    return response