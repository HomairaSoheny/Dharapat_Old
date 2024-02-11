from dashboard.engines.corporate_engine import *
from dashboard.engines import general_engine

def getSummaryTable(df):
    response = []
    for category in df['CIB Category'].unique():
        cat_df = df[df['CIB Category'] == category]
        for concern_name in df['Name'].unique():
            temp_df = cat_df[cat_df['Name'] == concern_name]
            response.append({
                "CIB Category": category,
                "Name of Concern": concern_name,
                "Funded Outstanding Installment": getFundedOutstandingInstallment(temp_df),
                "Funded Outstanding Non Installment": getFundedOutstandingNonInstallment(temp_df),
                "Funded Outstanding Total": getFundedOutstandingTotal(temp_df),
                "Non-Funded Outstanding": getNonFundedOutstanding(temp_df),
                "Total Outstanding": getTotalOutstanding(temp_df),
                "CL Status": general_engine.getClassFromSet(set(temp_df['CL Status'].tolist())),
                "Default": "Yes" if "Yes" in set(temp_df['Default'].tolist()) else "No",
                "Updated Overdue and CL Status": "Need More Clarification"
            })
        sub_total_df = pd.DataFrame(response)
        sub_total_df = sub_total_df[sub_total_df['CIB Category'] == category]
        response.append({
            "CIB Category": category,
            "Name of Concern": "Sub Total",
            "Funded Outstanding Installment": float(format(sub_total_df['Funded Outstanding Installment'].sum(), '.3f')),
            "Funded Outstanding Non Installment": float(format(sub_total_df['Funded Outstanding Non Installment'].sum(), '.3f')),
            "Funded Outstanding Total": float(format(sub_total_df['Funded Outstanding Total'].sum(), '.3f')),
            "Non-Funded Outstanding": float(format(sub_total_df['Non-Funded Outstanding'].sum(), '.3f')),
            "Total Outstanding": float(format(sub_total_df['Total Outstanding'].sum(), '.3f')),
            "CL Status": general_engine.getClassFromSet(set(sub_total_df['CL Status'].tolist())),
            "Default": "Yes" if "Yes" in set(sub_total_df['Default'].tolist()) else "No",
            "Updated Overdue and CL Status": "Need More Clarification"
        })
    total_df = pd.DataFrame(response)
    total_df = total_df[total_df['Name of Concern'] == "Sub Total"]
    response.append({
            "CIB Category": category,
            "Name of Concern": "Grand Total",
            "Funded Outstanding Installment": float(format(total_df['Funded Outstanding Installment'].sum(), '.3f')),
            "Funded Outstanding Non Installment": float(format(total_df['Funded Outstanding Non Installment'].sum(), '.3f')),
            "Funded Outstanding Total": float(format(total_df['Funded Outstanding Total'].sum(), '.3f')),
            "Non-Funded Outstanding": float(format(total_df['Non-Funded Outstanding'].sum(), '.3f')),
            "Total Outstanding": float(format(total_df['Total Outstanding'].sum(), '.3f')),
            "CL Status": general_engine.getClassFromSet(set(total_df['CL Status'].tolist())),
            "Default": "Yes" if "Yes" in set(total_df['Default'].tolist()) else "No",
            "Updated Overdue and CL Status": "Need More Clarification"
        })
    return response

def getSummaryOfTerminatedFacilityFunded(df):
    response = []
    return response

def getSummaryOfTerminatedFacilityNonFunded(df):
    response = []
    return response

def getSummaryOfFundedFacility(df):
    response = []
    df = df[df['Is Funded'] == 'Yes']
    installment = df[df['Installment Type'] == 'Installment']
    non_installment = df[df['Installment Type'] == 'No Installment']
    
    for i, row in installment.iterrows():
        response.append({
            "SL": "B1.1 - " + str(i+1),
            "Nature of Facility": row['Facility Type'],
            "Installment Type": row["Installment Type"],
            "Limit": row["Limit"],
            "Outstanding": row['Outstanding'],
            "Overdue": row["Overdue"],
            "Start Date": row['Start Date'],
            "End Date of Contract": row['End Date of Contract'],
            "Installment Amount": "Not Implemented",
            "Payment Period": row['Payment Period (Monthly/Quarterly)'],
            "Total No. of Installment": row['Total No of Installment'],
            "Total no. of Installment paid": "Not Implemented",
            "No. of Remaining Installment": row['No of Remaining Installment'],
            "Date of Last Payment": row['Date of Last Payment'],
            "NPI": row['NPI'],
            "Default": row['Default']
        })
    response.append({
        "SL": "-",
        "Nature of Facility": "Sub Total",
        "Installment Type": "Installment",
        "Limit": installment["Limit"].sum(),
        "Outstanding": installment['Outstanding'].sum(),
        "Overdue": installment["Overdue"].sum(),
        "Start Date": "-",
        "End Date of Contract": "-",
        "Installment Amount": "Not Implemented",
        "Payment Period": "-",
        "Total No. of Installment": installment['Total No of Installment'].sum(),
        "Total no. of Installment paid": "Not Implemented",
        "No. of Remaining Installment": installment['No of Remaining Installment'].sum(),
        "Date of Last Payment": "-",
        "NPI": installment['NPI'].sum(),
        "Default": "Yes" if "Yes" in set(installment['Default'].tolist()) else "No",
    })
    
    
    
    for i, row in non_installment.iterrows():
        response.append({
            "SL": str(i+1),
            "Nature of Facility": row['Facility Type'],
            "Installment Type": row["Installment Type"],
            "Limit": row["Limit"],
            "Outstanding": row['Outstanding'],
            "Overdue": row["Overdue"],
            "Start Date": row['Start Date'],
            "End Date of Contract": row['End Date of Contract'],
            "Installment Amount": "Not Applicable",
            "Payment Period": "Not Applicable",
            "Total No. of Installment": "Not Applicable",
            "Total no. of Installment paid": "Not Applicable",
            "No. of Remaining Installment": "Not Applicable",
            "Date of Last Payment": row['Date of Last Payment'],
            "NPI": "Not Applicable",
            "Default": row['Default']
        })
    
    response.append({
        "SL": "-",
        "Nature of Facility": "Sub Total",
        "Installment Type": "Installment",
        "Limit": installment["Limit"].sum(),
        "Outstanding": installment['Outstanding'].sum(),
        "Overdue": installment["Overdue"].sum(),
        "Start Date": "-",
        "End Date of Contract": "-",
        "Installment Amount": "Not Applicable",
        "Payment Period": "Not Applicable",
        "Total No. of Installment": "Not Applicable",
        "Total no. of Installment paid": "Not Applicable",
        "No. of Remaining Installment": "Not Applicable",
        "Date of Last Payment": "-",
        "NPI": "Not Applicable",
        "Default": "Yes" if "Yes" in set(installment['Default'].tolist()) else "No",
    })
    
    return response

def getCorporateDashboard(cibs):
    response = {}
    df = getCorporateDataFrame(cibs)
    response['Summary Table - 1'] = getSummaryTable(df)
    response['Summary of terminated facility (Funded)'] = getSummaryOfTerminatedFacilityFunded(df)
    response['Summary of terminated facility (Non Funded)'] = getSummaryOfTerminatedFacilityNonFunded(df)
    response['Summary of funded facility'] = getSummaryOfFundedFacility(df)
    return response