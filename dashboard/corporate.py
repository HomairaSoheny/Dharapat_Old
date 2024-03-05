from dashboard.engines.corporate_engine import *
from dashboard.engines.general_engine import *
from utils.general_helper import *


def getSummaryTable(cibs):
    response = []
    for cib in cibs:
        df = getCorporateDataFrame([cib])
        funded = cib.summary_1A
        funded['total'] = funded[[i for i in funded.columns if 'Amount' in i]].sum(axis=1)
        non_funded = cib.summary_1B
        non_funded['total'] = non_funded[[i for i in non_funded.columns if 'Amount' in i]].sum(axis=1)
        response.append({
            "CIB Category": getCIBCategory(cib),
            "Name of Concern": getBorrowersName(cib.subject_info),
            "Funded Outstanding Installment": convertToMillion(funded.total.tolist()[0]),
            "Funded Outstanding Non Installment": convertToMillion(funded.total.tolist()[1]),
            "Funded Outstanding Total": convertToMillion(funded.total.tolist()[3]),
            "Non-Funded Outstanding": convertToMillion(non_funded.total.tolist()[3]),
            "Total Outstanding": convertToMillion(funded.total.tolist()[3]) + convertToMillion(non_funded.total.tolist()[3]),
            "Overdue": cib.summary_1['Total Overdue Amount'],
            "CL Status": "-" if df.empty else getClassFromSet(set(list(df['CL Status']))),
            "Default": "-" if df.empty else ("Yes" if "Yes" in list(df['Default']) else "No"),
            "CIB PDF View": PDF_LINK + cib.pdf_name,
            "Updated Overdue and CL Status": "-" if df.empty else (re.sub(r'[,\[\]]', '', str(list(df['Remarks']))).replace("'", '')),
        })
    df = pd.DataFrame(response)
    response = []
    for category in df['CIB Category'].unique():
        cat_df = df[df['CIB Category'] == category]
        for concern_name in df['Name of Concern'].unique():
            temp_df = cat_df[cat_df['Name of Concern'] == concern_name]
            response.append(getSummaryTableFields(category, concern_name, temp_df))
        sub_total_df = pd.DataFrame(response)
        sub_total_df = sub_total_df[sub_total_df['CIB Category'] == category]
        response.append(getSummaryTableFields(category, "Sub Total", sub_total_df))
    total_df = pd.DataFrame(response)
    total_df = total_df[total_df['Name of Concern'] == "Sub Total"]
    response.append(getSummaryTableFields(category, "Grand Total", total_df))
    return response

def getSummaryTableTwo(df):
    if df.empty:
        return []
    response = []
    for category in df['CIB Category'].unique():
        cat_df = df[df['CIB Category'] == category]
        for concern_name in df['Name'].unique():
            temp_df = cat_df[cat_df['Name'] == concern_name]
            response.append(getSummaryTableTwoFields(category, concern_name, temp_df))
        sub_total_df = pd.DataFrame(response)
        sub_total_df = sub_total_df[sub_total_df['CIB Category'] == category]
        response.append(getSummaryTableTwoSum(category, "Sub Total", sub_total_df))
    total_df = pd.DataFrame(response)
    total_df = total_df[total_df['Name of Concern'] == "Sub Total"]
    response.append(getSummaryTableTwoSum(category, "Grand Total", total_df))
    return response

def getSummaryTableThree(df):
    if df.empty:
        return []
    funded = []
    non_funded = []
    non_funded_loans = list(df[df['Is Funded'] == "No"]["Facility Type"].unique())
    for category in df['CIB Category'].unique():
        cat_df = df[df['CIB Category'] == category]
        for concern_name in df['Name'].unique():
            temp_df = cat_df[cat_df['Name'] == concern_name]
            funded.append(getSummaryTableThreeFundedFields(category, concern_name, temp_df[temp_df['Is Funded'] == "Yes"]))
            non_funded.append(getSummaryTableThreeNonFundedFields(category, concern_name, temp_df[temp_df['Is Funded'] == "No"], non_funded_loans))
        funded_sub_total_df = pd.DataFrame(funded)
        funded_sub_total_df = funded_sub_total_df[funded_sub_total_df['CIB Category'] == category]
        funded.append(getSummaryTableThreeFundedSum(category, "Sub Total", funded_sub_total_df))
        non_funded_sub_total_df = pd.DataFrame(non_funded)
        non_funded_sub_total_df = non_funded_sub_total_df[non_funded_sub_total_df['CIB Category'] == category]
        non_funded.append(getSummaryTableThreeNonFundedSum(category, "Sub Total", non_funded_sub_total_df, non_funded_loans))
    funded_total_df = pd.DataFrame(funded)
    funded_total_df = funded_total_df[funded_total_df['Borrowing Company - Person'] == "Sub Total"]
    funded.append(getSummaryTableThreeFundedSum(category, "Grand Total", funded_total_df))
    non_funded_total_df = pd.DataFrame(non_funded)
    non_funded_total_df = non_funded_total_df[non_funded_total_df['Borrowing Company - Person'] == "Sub Total"]
    non_funded.append(getSummaryTableThreeNonFundedSum(category, "Grand Total", non_funded_total_df, non_funded_loans))
        
    return {
        "funded": funded,
        "non_funded": non_funded
    }

def getSummaryOfTerminatedFacilityFunded(df):
    if df.empty:
        return []
    response = []
    df = df[df['Phase'] != 'Living']
    df = df[df['Is Funded'] == "Yes"]
    df = df[df['Installment Type'] == 'Installment']
    
    for i, row in df.iterrows():
        response.append({
            "Installment": row['Facility Type'],
            "Limit": convertToMillion(row["Limit"]),
            "Loan/Limit (days of adjustment before/after)": "Not Implemented",
            "Worse Classification Status": row["Worse Classification Status"],
            "Date of Classification": convertToString(row["Date of Classification"])
        })
    return response

def getSummaryOfTerminatedFacilityNonFunded(df):
    if df.empty:
        return []
    response = []
    df = df[df['Phase'] != 'Living']
    df = df[df['Is Funded'] == "No"]
    df = df[df['Installment Type'] == 'No Installment']
    
    for i, row in df.iterrows():
        response.append({
            "Non-Installment": row['Facility Type'],
            "Limit": convertToMillion(row["Limit"]),
            "Loan/Limit (days of adjustment before/after)": "Not Implemented",
            "Worse Classification Status": row["Worse Classification Status"],
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
    if df.empty:
        return {"Summary of funded facility": [],
                "Summary of non funded facility": []}
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
    if df.empty:
        return []
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
            temp_cib['Link'] = PDF_LINK + cib.pdf_name
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

def getSummaryOfStayOrder(df, role):
    if df.empty:
        return []
    df = df[df['Role'].isin(role) & (df['Is Stay Order'] == "Yes")]
    response = []
    for i, row in df.iterrows():
        response.append({
            "Name of account": row['Name'],
            "Nature of facility": row['Facility Type'],
            "Stayorder amount": row['Stay Order Amount'],
            "Writ no": row["Stay Order"],
            "Remarks": row['Remarks'],
            "Link": row['CIB Link']
        })
    return response

def getSummaryOfExpiredButShowingLiveFunded(df):
    if df.empty:
        return []
    response = []
    for i, row in df.iterrows():
        response.append({
            "Nature of Facility": "",
            "Limit": "",
            "Outstanding": "",
            "Overdue": "",
            "Start Date": "",
            "End Date of Contract": "",
            "Installment Amount": "",
            "Payment Period": "",
            "Total No of Installment": "",
            "No of Remaining Installment": "",
            "Date of Last Payment": "",
            "NPL": "",
            "Default": ""
        })

def getSummaryOfExpiredButShowingLiveNonFunded(df):
    if df.empty:
        return []
    response = []
    for i, row in df.iterrows():
        response.append({
            "Nature of Facility": "",
            "Limit": "",
            "Outstanding": "",
            "Start Date": "",
            "End Date of Contract": "",
            "Default": ""
        })

def getCorporateDashboard(cibs):
    response = {}
    df = getCorporateDataFrame(cibs)
    response['analysis type'] = "Corporate"
    response['Summary Table - 1'] = getSummaryTable(cibs)
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
    response['E - Summary of Stay Order'] = {
        "Borrower": getSummaryOfStayOrder(df, BORROWER),
        "Guarantor": getSummaryOfStayOrder(df, GUARANTOR)
        }
    response['F - Expired Loan But Showing Live'] = {
        "Summary of Funded Facility": getSummaryOfExpiredButShowingLiveFunded(df),
        "Summary of Non Funded Facility": getSummaryOfExpiredButShowingLiveNonFunded(df),
    }
    response['Summary Table - 2'] = getSummaryTableTwo(df)
    response['Summary Table - 3'] = getSummaryTableThree(df)
    
    return response