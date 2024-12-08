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
            "Total Outstanding": convertToMillion(convertToFloat(funded.total.tolist()[3]) + convertToFloat(non_funded.total.tolist()[3])),
            "Overdue": convertToMillion(cib.summary_1['Total Overdue Amount']),
            "CL Status": "-" if df.empty else getClassFromSet(set(list(df['CL Status']))),
            "Default": "-" if df.empty else ("Yes" if "Yes" in list(df['Default']) else "No"),
            "CIB PDF View": PDF_LINK + cib.pdf_name,
            "Updated Overdue and CL Status": "-" if df.empty else (re.sub(r'[,\[\]]', '', str(list(df['Remarks']))).replace("'", '')),
        })
    df = pd.DataFrame(response)
    response = []
    for category in df['CIB Category'].unique():
        cat_df = df[df['CIB Category'] == category]
        for concern_name in cat_df['Name of Concern'].unique():
            temp_df = cat_df[cat_df['Name of Concern'] == concern_name]
            response.append(getSummaryTableFields(category, concern_name, temp_df))
        sub_total_df = pd.DataFrame(response)
        sub_total_df = sub_total_df[sub_total_df['CIB Category'] == category]
        response.append(getSummaryTableFields(category, "Sub Total", sub_total_df))
    total_df = pd.DataFrame(response)
    total_df = total_df[total_df['Name of Concern'] == "Sub Total"]
    response.append(getSummaryTableFields("", "Grand Total", total_df))
    return response

def getSummaryTableConcern(cibs):
    response = []
    for cib in cibs:
        df = getCorporateDataFrame([cib])
        if not df.empty:
            # Apply filtering to df
            df_filtered = df[df["Subject code"] != '1']
            if not df_filtered.empty:
                funded = cib.summary_1A
                funded['total'] = funded[[i for i in funded.columns if 'Amount' in i]].sum(axis=1)
                non_funded = cib.summary_1B
                non_funded['total'] = non_funded[[i for i in non_funded.columns if 'Amount' in i]].sum(axis=1)

                # Calculate summary statistics using filtered DataFrame
                response.append({
                    "CIB Category": getCIBCategory(cib),
                    "Name of Concern": getBorrowersName(cib.subject_info),
                    "Funded Outstanding Installment": convertToMillion(funded.total.iloc[0]),
                    "Funded Outstanding Non Installment": convertToMillion(funded.total.iloc[1]),
                    "Funded Outstanding Total": convertToMillion(funded.total.iloc[3]),
                    "Non-Funded Outstanding": convertToMillion(non_funded.total.iloc[3]),
                    "Total Outstanding": convertToMillion(funded.total.iloc[3] + non_funded.total.iloc[3]),
                    "Overdue": convertToMillion(cib.summary_1['Total Overdue Amount']),
                    "CL Status": getClassFromSet(set(df_filtered['CL Status'])),
                    "Default": "Yes" if "Yes" in df_filtered['Default'].values else "No",
                    "CIB PDF View": PDF_LINK + cib.pdf_name,
                    "Updated Overdue and CL Status": re.sub(r'[,\[\]]', '', str(list(df_filtered['Remarks']))).replace("'", ''),
                })

    df = pd.DataFrame(response)

    response = []
    for category in df['CIB Category'].unique():
        cat_df = df[df['CIB Category'] == category]
        for concern_name in cat_df['Name of Concern'].unique():
            temp_df = cat_df[cat_df['Name of Concern'] == concern_name]
            response.append(getSummaryTableFields(category, concern_name, temp_df))
        sub_total_df = pd.DataFrame(response)
        sub_total_df = sub_total_df[sub_total_df['CIB Category'] == category]
        response.append(getSummaryTableFields(category, "Sub Total", sub_total_df))
    total_df = pd.DataFrame(response)
    total_df = total_df[total_df['Name of Concern'] == "Sub Total"]
    response.append(getSummaryTableFields("", "Grand Total", total_df))
    
    return pd.DataFrame(response)



def getSummaryTableTwo(df):
    if df.empty:
        return []
    response = []
    df = df[df['Phase'] == 'Living']
    for category in df['CIB Category'].unique():
        cat_df = df[df['CIB Category'] == category]
        for concern_name in cat_df['Name'].unique():
            temp_df = cat_df[cat_df['Name'] == concern_name]
            response.append(getSummaryTableTwoFields(category, concern_name, temp_df))
        sub_total_df = pd.DataFrame(response)
        sub_total_df = sub_total_df[sub_total_df['CIB Category'] == category]
        response.append(getSummaryTableTwoSum(category, "Sub Total", sub_total_df))
    total_df = pd.DataFrame(response)
    total_df = total_df[total_df['Name of Concern'] == "Sub Total"]
    response.append(getSummaryTableTwoSum("", "Grand Total", total_df))
    return response

def getSummaryTableTwoConcern(df):
    if df.empty:
        return []
    response = []
    df_filtered = df[df["Subject code"] != '1']

    if not df_filtered.empty:
        df = df_filtered[df_filtered['Phase'] == 'Living']
        for category in df['CIB Category'].unique():
            cat_df = df[df['CIB Category'] == category]
            for concern_name in cat_df['Name'].unique():
                temp_df = cat_df[cat_df['Name'] == concern_name]
                response.append(getSummaryTableTwoFields(category, concern_name, temp_df))
            sub_total_df = pd.DataFrame(response)
            sub_total_df = sub_total_df[sub_total_df['CIB Category'] == category]
            response.append(getSummaryTableTwoSum(category, "Sub Total", sub_total_df))
        total_df = pd.DataFrame(response)
        total_df = total_df[total_df['Name of Concern'] == "Sub Total"]
        response.append(getSummaryTableTwoSum("", "Grand Total", total_df))
    return response

def getSummaryTableThree(df):
    if df.empty:
        return []
    df = df[df['Phase'] == 'Living']
    funded = []
    non_funded = []
    non_funded_loans = list(df[df['Is Funded'] == "No"]["Facility Type"].unique())
    for category in df['CIB Category'].unique():
        cat_df = df[df['CIB Category'] == category]
        for concern_name in cat_df['Name'].unique():
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
    funded.append(getSummaryTableThreeFundedSum("", "Grand Total", funded_total_df))
    non_funded_total_df = pd.DataFrame(non_funded)
    non_funded_total_df = non_funded_total_df[non_funded_total_df['Borrowing Company - Person'] == "Sub Total"]
    non_funded.append(getSummaryTableThreeNonFundedSum("", "Grand Total", non_funded_total_df, non_funded_loans))
        
    return {
        "funded": funded,
        "non_funded": non_funded
    }
def getSummaryTableThreeConcern(df):
    if df.empty:
        return []
    df = df[df["Subject code"] != '1']
    funded = []
    non_funded = []
    if not df.empty:
        df = df[df['Phase'] == 'Living']
        non_funded_loans = list(df[df['Is Funded'] == "No"]["Facility Type"].unique())
        for category in df['CIB Category'].unique():
            cat_df = df[df['CIB Category'] == category]
            for concern_name in cat_df['Name'].unique():
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
        funded.append(getSummaryTableThreeFundedSum("", "Grand Total", funded_total_df))
        non_funded_total_df = pd.DataFrame(non_funded)
        non_funded_total_df = non_funded_total_df[non_funded_total_df['Borrowing Company - Person'] == "Sub Total"]
        non_funded.append(getSummaryTableThreeNonFundedSum("", "Grand Total", non_funded_total_df, non_funded_loans))
        
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
    total_limit = 0
    total_days = 0
    for i, row in df.iterrows():
        response.append({
            "Category": row['CIB Category'],
            "Installment": row['Facility Type'],
            "Limit": convertToMillion(row["Limit"]),
            "Loan/Limit (days of adjustment before/after)": row['Loan/Limit (days of adjustment before/after)'],
            "Worse Classification Status": row["Worse Classification Status"],
            "Date of Classification": convertToString(row["Date of Classification"]).replace(" 00:00:00", "")
        })
    response_df = pd.DataFrame(response)
    CIBCategorySet = list(set(response_df.Category))
    result_df = pd.DataFrame()
    for cat in CIBCategorySet:
        temp_df = response_df[response_df['Category']==cat]
        limit_sum = temp_df['Limit'].sum()
        loan_limit_sum = temp_df['Loan/Limit (days of adjustment before/after)'].sum()
        new_row = [{
            'Category': cat,
            'Installment': 'Sub Total',
            'Limit': limit_sum,
            'Loan/Limit (days of adjustment before/after)': loan_limit_sum,
            'Worse Classification Status': '-',
            'Date of Classification': '-'
        }]
        new_row_df = pd.DataFrame(new_row)
        # Append the new row to the DataFrame
        temp_df = pd.concat([temp_df,new_row_df])
        result_df = pd.concat([result_df,temp_df])
    
    result_json = result_df.to_dict('records')

    if len(response) > 0:
        result_json.append({
            "Category": '',
            'Installment': "Grand Total",
            "Limit": convertToMillion(df['Limit'].sum()),
            "Loan/Limit (days of adjustment before/after)": df['Loan/Limit (days of adjustment before/after)'].sum(),
            'Worse Classification Status': '-',
            'Date of Classification': '-'
        })
    
    return result_json


def getSummaryOfTerminatedFacilityFunded(df):
    if df.empty:
        return []
    response = []
    df = df[df['Phase'] != 'Living']
    df = df[df['Is Funded'] == "Yes"]
    df = df[df['Installment Type'] == 'Installment']
    total_limit = 0
    total_days = 0
    for i, row in df.iterrows():
        response.append({
            "Category": row['CIB Category'],
            "Installment": row['Facility Type'],
            "Limit": convertToMillion(row["Limit"]),
            "Loan/Limit (days of adjustment before/after)": row['Loan/Limit (days of adjustment before/after)'],
            "Worse Classification Status": row["Worse Classification Status"],
            "Date of Classification": convertToString(row["Date of Classification"]).replace(" 00:00:00", "")
        })
        total_limit += convertToMillion(row["Limit"])
        total_days += row['Loan/Limit (days of adjustment before/after)']

    response.append({
            "Category": '',
            "Installment": 'Sub Total',
            "Limit": total_limit,
            "Loan/Limit (days of adjustment before/after)": total_days,
            "Worse Classification Status": '',
            "Date of Classification": ''
        })
    
    return response
def getSummaryOfTerminatedFacilityFundedConcern(df):
    if df.empty:
        return []
    response = []
    df = df[df["Subject code"] != '1']
    total_limit = 0
    total_days = 0
    if not df.empty:
        df = df[df['Phase'] != 'Living']
        df = df[df['Is Funded'] == "Yes"]
        df = df[df['Installment Type'] == 'Installment']
        for i, row in df.iterrows():
            response.append({
                "Category": row['CIB Category'],
                "Installment": row['Facility Type'],
                "Limit": convertToMillion(row["Limit"]),
                "Loan/Limit (days of adjustment before/after)": row['Loan/Limit (days of adjustment before/after)'],
                "Worse Classification Status": row["Worse Classification Status"],
                "Date of Classification": convertToString(row["Date of Classification"]).replace(" 00:00:00", "")
            })
            total_limit += convertToMillion(row["Limit"])
            total_days += row['Loan/Limit (days of adjustment before/after)']

    response.append({
            "Category": '',
            "Installment": 'Sub Total',
            "Limit": total_limit,
            "Loan/Limit (days of adjustment before/after)": total_days,
            "Worse Classification Status": '',
            "Date of Classification": ''
        })
    
    return response

def getSummaryOfTerminatedFacilityNonFunded(df):
    if df.empty:
        return []
    response = []
    df = df[df['Phase'] != 'Living']
    df = df[df['Is Funded'] == "No"]
    df = df[df['Installment Type'] == 'No Installment']
    total_limit = 0
    total_days = 0
    for i, row in df.iterrows():
        response.append({
            "Category": row['CIB Category'],
            "Non-Installment": row['Facility Type'],
            "Limit": str(convertToMillion(row["Limit"])),
            "Loan/Limit (days of adjustment before/after)": row['Loan/Limit (days of adjustment before/after)'],
            "Worse Classification Status": row["Worse Classification Status"],
            "Date of Classification": convertToString(row["Date of Classification"]).replace(" 00:00:00", "")
        })
        total_limit += convertToMillion(row["Limit"])
        total_days += row['Loan/Limit (days of adjustment before/after)']
    
    response.append({
            "Category": '',
            "Non-Installment": 'Sub Total',
            "Limit": total_limit,
            "Loan/Limit (days of adjustment before/after)": total_days,
            "Worse Classification Status": '',
            "Date of Classification": ''
        })
    return response
    
def getSummaryOfTerminatedFacilityNonFundedConcern(df):
    if df.empty:
        return []
    response = []
    df = df[df["Subject code"] != '1']
    total_limit = 0
    total_days = 0
    if not df.empty:
        df = df[df['Phase'] != 'Living']
        df = df[df['Is Funded'] == "No"]
        df = df[df['Installment Type'] == 'No Installment']
        for i, row in df.iterrows():
            response.append({
                "Category": row['CIB Category'],
                "Non-Installment": row['Facility Type'],
                "Limit": str(convertToMillion(row["Limit"])),
                "Loan/Limit (days of adjustment before/after)": row['Loan/Limit (days of adjustment before/after)'],
                "Worse Classification Status": row["Worse Classification Status"],
                "Date of Classification": convertToString(row["Date of Classification"]).replace(" 00:00:00", "")
            })
            total_limit += convertToMillion(row["Limit"])
            total_days += row['Loan/Limit (days of adjustment before/after)']
        
    response.append({
            "Category": '',
            "Non-Installment": 'Sub Total',
            "Limit": total_limit,
            "Loan/Limit (days of adjustment before/after)": total_days,
            "Worse Classification Status": '',
            "Date of Classification": ''
        })
    return response
def getSummaryOfFundedFacility(df):
    response = []
    df = df[df['Phase'] == 'Living']
    df = df[df['Is Funded'] == 'Yes']
    installment = df[df['Installment Type'] == 'Installment']
    non_installment = df[df['Installment Type'] == 'No Installment']

    for i, row in installment.iterrows():
        response.append(getSummaryOfFundedFacilityFields(row, i, True))
    if installment.shape[0] > 0:
        response.append(getSummaryOfFundedFacilitySum(installment, "Sub Total", "Installment"))

    for i, row in non_installment.iterrows():
        response.append(getSummaryOfFundedFacilityFields(row, i, False))
    if non_installment.shape[0] > 0:
        response.append(getSummaryOfFundedFacilitySum(non_installment, "Sub Total", "No Installment"))
    
    return response

def getSummaryOfFundedFacilityConcern(df):
    response = []
    df = df[df["Subject code"] != '1']
    if not df.empty:
        df = df[df['Phase'] == 'Living']
        df = df[df['Is Funded'] == 'Yes']
        installment = df[df['Installment Type'] == 'Installment']
        non_installment = df[df['Installment Type'] == 'No Installment']

        for i, row in installment.iterrows():
            response.append(getSummaryOfFundedFacilityFields(row, i, True))
        if installment.shape[0] > 0:
            response.append(getSummaryOfFundedFacilitySum(installment, "Sub Total", "Installment"))

        for i, row in non_installment.iterrows():
            response.append(getSummaryOfFundedFacilityFields(row, i, False))
        if non_installment.shape[0] > 0:
            response.append(getSummaryOfFundedFacilitySum(non_installment, "Sub Total", "No Installment"))
    
    return response


def getSummaryOfNonFundedFacility(df):
    response = []
    df = df[df['Phase'] == 'Living']
    df = df[df['Is Funded'] == 'No']
    total_limit = 0
    total_outstanding = 0
    for i, row in df.iterrows():
        response.append({
            "Nature of Facility": row['Facility Type'],
            "Limit": convertToMillion(row["Limit"]),
            "Outstanding": convertToMillion(row["Outstanding"]),
            "Start Date": convertToString(row["Start Date"]).replace(" 00:00:00", ""),
            "End Date of Contract": convertToString(row["End Date of Contract"]).replace(" 00:00:00", ""),
            "Default": row["Default"]
        })
        total_limit += convertToMillion(row["Limit"])
        total_outstanding += convertToMillion(row["Outstanding"])

    response.append({
            "Nature of Facility": 'Sub Total',
            "Limit": total_limit,
            "Outstanding": total_outstanding,
            "Start Date": '',
            "End Date of Contract": '',
            "Default": ''
        })
    return response


def getSummaryOfNonFundedFacilityConcern(df):
    response = []
    df = df[df["Subject code"] != '1']
    total_limit = 0
    total_outstanding = 0
    if not df.empty:
        df = df[df['Phase'] == 'Living']
        df = df[df['Is Funded'] == 'No']
        for i, row in df.iterrows():
            response.append({
                "Nature of Facility": row['Facility Type'],
                "Limit": convertToMillion(row["Limit"]),
                "Outstanding": convertToMillion(row["Outstanding"]),
                "Start Date": convertToString(row["Start Date"]).replace(" 00:00:00", ""),
                "End Date of Contract": convertToString(row["End Date of Contract"]).replace(" 00:00:00", ""),
                "Default": row["Default"]
            })
            total_limit += convertToMillion(row["Limit"])
            total_outstanding += convertToMillion(row["Outstanding"])

    response.append({
            "Nature of Facility": 'Sub Total',
            "Limit": total_limit,
            "Outstanding": total_outstanding,
            "Start Date": '',
            "End Date of Contract": '',
            "Default": ''
        })
    return response


def getSummaryOfRescheduleLoan(df, role):
    if df.empty:
        return []
    response = []
    df = df[(df['Reschedule Type'] != "Not Rescheduled") & df['Role'].isin(role)]
    if not df.empty:
        for i, row in df.iterrows():
            response.append({
                "Category": row['CIB Category'],
                "Name of Account" : row["Name"],
                "Nature of Facility": row['Facility Type'],
                "Type of Reschedule": row['Reschedule Type'],
                "Expiry of Reschedule Loan": convertToString(row['End Date of Contract']).replace(" 00:00:00", ""),
                "Amount": row['Total Disbursement Amount'],
                "Outstanding": row['Outstanding'],
                "Date of Last Rescheduling": convertToString(row['Last Date of Reschedule']).replace(" 00:00:00", ""),
                "Link": row['CIB Link']
            })
        response_df = pd.DataFrame(response)
        CIBCategorySet = list(set(response_df.Category))
        result_df = pd.DataFrame()
        for cat in CIBCategorySet:
            temp_df = response_df[response_df['Category']==cat]
            amount_sum = temp_df['Amount'].sum()
            outstanding_sum = temp_df['Outstanding'].sum()
            new_row = [{
                'Category': cat,
                'Name of Account': '-',
                'Nature of Facility': 'Sub Total',
                'Type of Reschedule': '-',
                'Expiry of Reschedule Loan': '-',
                'Amount': amount_sum,
                'Outstanding': outstanding_sum,
                'Date of Last Rescheduling': '-',
                'Link': '-'
            }]
            new_row_df = pd.DataFrame(new_row)
            # Append the new row to the DataFrame
            temp_df = pd.concat([temp_df,new_row_df])
            result_df = pd.concat([result_df,temp_df])
        
        result_json = result_df.to_dict('records')

        if len(response) > 0:
            result_json.append({
                "Category": '',
                "Name of Account": '',
                "Nature of Facility": "Grand Total",
                "Type of Reschedule": "-",
                "Expiry of Reschedule Loan": "-",
                "Amount": convertToInteger(df['Total Disbursement Amount'].sum()),
                "Outstanding": convertToInteger(df['Outstanding'].sum()),
                "Date of Last Rescheduling": "-",
                "Link": "-"
            })
        return result_json
    return response

def getSummaryOfRescheduleLoanConcern(df, role):
    if df.empty:
        return []
    response = []
    df = df[df["Subject code"] != '1']
    if not df.empty:
        df = df[(df['Reschedule Type'] != "Not Rescheduled") & df['Role'].isin(role)]
        if not df.empty:
            for i, row in df.iterrows():
                response.append({
                    "Category": row['CIB Category'],
                    "Name of Account" : row["Name"],
                    "Nature of Facility": row['Facility Type'],
                    "Type of Reschedule": row['Reschedule Type'],
                    "Expiry of Reschedule Loan": convertToString(row['End Date of Contract']).replace(" 00:00:00", ""),
                    "Amount": row['Total Disbursement Amount'],
                    "Outstanding": row['Outstanding'],
                    "Date of Last Rescheduling": convertToString(row['Last Date of Reschedule']).replace(" 00:00:00", ""),
                    "Link": row['CIB Link']
                })
            response_df = pd.DataFrame(response)
            CIBCategorySet = list(set(response_df.Category))
            result_df = pd.DataFrame()
            for cat in CIBCategorySet:
                temp_df = response_df[response_df['Category']==cat]
                amount_sum = temp_df['Amount'].sum()
                outstanding_sum = temp_df['Outstanding'].sum()
                new_row = [{
                    'Category': cat,
                    'Name of Account': '-',
                    'Nature of Facility': 'Sub Total',
                    'Type of Reschedule': '-',
                    'Expiry of Reschedule Loan': '-',
                    'Amount': amount_sum,
                    'Outstanding': outstanding_sum,
                    'Date of Last Rescheduling': '-',
                    'Link': '-'
                }]
                new_row_df = pd.DataFrame(new_row)
                # Append the new row to the DataFrame
                temp_df = pd.concat([temp_df,new_row_df])
                result_df = pd.concat([result_df,temp_df])
            
            result_json = result_df.to_dict('records')

            if len(response) > 0:
                result_json.append({
                    "Category": '',
                    "Name of Account": '',
                    "Nature of Facility": "Grand Total",
                    "Type of Reschedule": "-",
                    "Expiry of Reschedule Loan": "-",
                    "Amount": convertToInteger(df['Total Disbursement Amount'].sum()),
                    "Outstanding": convertToInteger(df['Outstanding'].sum()),
                    "Date of Last Rescheduling": "-",
                    "Link": "-"
                })
            return result_json
        return response
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


def getSummaryOfFacilitiesConcern(df):
    if df.empty:
        return {"Summary of funded facility for concerns": [],
                "Summary of non funded facility for concerns": []}
    response = {}
    summary_of_funded_facility_concern = {}
    summary_of_non_funded_facility_concern = {}
    
    for cib_type in df['CIB Category'].unique():
        temp_df = df[df['CIB Category'] == cib_type]
        summary_of_funded_facility_concern[cib_type] = getSummaryOfFundedFacilityConcern(temp_df)
        summary_of_non_funded_facility_concern[cib_type] = getSummaryOfNonFundedFacilityConcern(temp_df)

    response['Summary of funded facility for concerns'] = summary_of_funded_facility_concern
    response['Summary of non funded facility for concerns'] = summary_of_non_funded_facility_concern
    return response

def getSummaryOfFacilitiesConcern(df):
    if df.empty:
        return {"Summary of funded facility": [],
                "Summary of non funded facility": []}
    response = {}
    summary_of_funded_facility_concern = {}
    summary_of_non_funded_facility_concern = {}
    
    for cib_type in df['CIB Category'].unique():
        temp_df = df[df['CIB Category'] == cib_type]
        summary_of_funded_facility_concern[cib_type] = getSummaryOfFundedFacilityConcern(temp_df)
        summary_of_non_funded_facility_concern[cib_type] = getSummaryOfNonFundedFacilityConcern(temp_df)

    response['Summary of funded facility'] = summary_of_funded_facility_concern
    response['Summary of non funded facility'] = summary_of_non_funded_facility_concern
    return response

def getSummaryOfRequestedLoan(cibs):
    response = []
    df = pd.DataFrame()
    for cib in cibs:
        if cib.req_contracts is not None:
            temp_cib = cib.req_contracts
            temp_cib['Role'] = cib.req_contracts["Role"]
            temp_cib['Link'] = PDF_LINK + cib.pdf_name
            temp_cib['CIB Category']  = getCIBCategory(cib)
            df = pd.concat([df, temp_cib])
    Flag = False 
    for i, row in df.iterrows():
        response.append({
            "Category": convertToString(row['CIB Category']).replace(" 00:00:00", ""),
            "Type of Loan": convertToString(row['Type of Contract']).replace(" 00:00:00", ""),
            "Facility": convertToString(row['Facility']).replace(" 00:00:00", ""),
            "Role": convertToString(row['Role']).replace(" 00:00:00", ""),
            "Requested Amount": convertToString(row['Total Requested Amount']).replace(" 00:00:00", ""),
            "Date of Request": convertToString(row['Request date']).replace(" 00:00:00", ""),
            "Link": convertToString(row['Link'])
        })
        Flag = True 
    response.append({
        "Type of Loan": '',
        "Facility": 'Sub Total',
        "Role": '',
        "Requested Amount": (df['Total Requested Amount'].sum() if True else " "),
        "Date of Request": '',
        "Link": ''
    })
    return response

    
def getSummaryOfRequestedLoanConcern(cibs):
    response = []
    df = pd.DataFrame()
    for cib in cibs:
        if cib.linked_prop_list and cib.req_contracts is not None:
            temp_cib = cib.req_contracts.copy()  # Make a copy of the DataFrame
            temp_cib['Role'] = cib.req_contracts["Role"]
            temp_cib['Link'] = PDF_LINK + cib.pdf_name
            temp_cib['CIB Category'] = getCIBCategory(cib)
            subject_codes = extract_subject_code(cib.linked_prop_list)
            
            # Filter rows based on subject codes
            temp_cib = temp_cib[temp_cib['CIB subject code'].isin(subject_codes)]
            
            df = pd.concat([df, temp_cib])
    flag = False
    if not df.empty:
        for i, row in df.iterrows():
            response.append({
                "Category": convertToString(row['CIB Category']).replace(" 00:00:00", ""),
                "Type of Loan": convertToString(row['Type of Contract']).replace(" 00:00:00", ""),
                "Facility": convertToString(row['Facility']).replace(" 00:00:00", ""),
                "Role": convertToString(row['Role']).replace(" 00:00:00", ""),
                "Requested Amount": convertToString(row['Total Requested Amount']).replace(" 00:00:00", ""),
                "Date of Request": convertToString(row['Request date']).replace(" 00:00:00", ""),
                "Link": convertToString(row['Link'])
            })
        flag = True 
    response.append({
        "Category": '',
        "Type of Loan": '',
        "Facility": 'Sub Total',
        "Role": '',
        "Requested Amount": (df['Total Requested Amount'].sum() if True else ""),
        "Date of Request": '',
        "Link": ''
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

def getSummaryOfStayOrderConcern(df, role):
    if df.empty:
        return []
    df =  df[df["Subject code"] != '1']
    if not df.empty:
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
    return response

def getSummaryOfExpiredButShowingLiveFunded(df):
    if df.empty:
        return []
    df = df[df['Is Funded'] == "Yes"]
    df = df[df['Phase'] == 'Living']
    df = df[(pd.to_datetime(df['Outstanding Zero Date']) < pd.to_datetime(df['End Date of Contract'])) | (pd.to_datetime(df["Outstanding Date"]) > pd.to_datetime(df['End Date of Contract']))]

    installment = df[df['Installment Type'] == 'Installment']
    non_installment = df[df['Installment Type'] == 'No Installment']
    response = []
    for i, row in installment.iterrows():
        response.append(getSummaryOfExpiredButShowingLiveFields(row, i, True))
    if installment.shape[0]>0:
        response.append(getSummaryOfExpiredButShowingLiveFundedSum(installment, 'Sub Total', "Installment"))
    for i, row in non_installment.iterrows():
        response.append(getSummaryOfExpiredButShowingLiveFields(row, i, False))
    if non_installment.shape[0]>0:
        response.append(getSummaryOfExpiredButShowingLiveFundedSum(non_installment, 'Sub Total', "Non-Installment"))
    total_df = pd.DataFrame(response)
    if not total_df.empty:
        total_df = total_df[total_df["Nature of Facility"] == 'Sub Total']
        response.append(getSummaryOfExpiredButShowingLiveFundedTotalSum("Grand Total", total_df))
    return response


def getSummaryOfExpiredButShowingLiveFundedConcern(df):
    if df.empty:
        return []
    df = df[df["Subject code"] != '1']
    if not df.empty:
        df = df[df['Is Funded'] == "Yes"]
        df = df[df['Phase'] == 'Living']
        df = df[(pd.to_datetime(df['Outstanding Zero Date']) < pd.to_datetime(df['End Date of Contract'])) | (pd.to_datetime(df["Outstanding Date"]) > pd.to_datetime(df['End Date of Contract']))]

        installment = df[df['Installment Type'] == 'Installment']
        non_installment = df[df['Installment Type'] == 'No Installment']
        response = []
        for i, row in installment.iterrows():
            response.append(getSummaryOfExpiredButShowingLiveFields(row, i, True))
        if installment.shape[0]>0:
            response.append(getSummaryOfExpiredButShowingLiveFundedSum(installment, 'Sub Total', "Installment"))
        for i, row in non_installment.iterrows():
            response.append(getSummaryOfExpiredButShowingLiveFields(row, i, False))
        if non_installment.shape[0]>0:
            response.append(getSummaryOfExpiredButShowingLiveFundedSum(non_installment, 'Sub Total', "Non-Installment"))
        total_df = pd.DataFrame(response)
        if not total_df.empty:
            total_df = total_df[total_df["Nature of Facility"] == 'Sub Total']
            response.append(getSummaryOfExpiredButShowingLiveFundedTotalSum("Grand Total", total_df))
        return response
    return response


def getSummaryOfExpiredButShowingLiveNonFunded(df):
    if df.empty:
        return []
    df = df[df['Is Funded'] != "Yes"]
    df = df[df['Phase'] == 'Living']
    df = df[(pd.to_datetime(df['Outstanding Zero Date']) < pd.to_datetime(df['End Date of Contract'])) | (pd.to_datetime(df["Outstanding Date"]) > pd.to_datetime(df['End Date of Contract']))]
    response = []
    total_limit = 0
    total_outstanding = 0
    total_overdue = 0 
    for i, row in df.iterrows():
        response.append({
            "Nature of Facility": row['Facility Type'],
            "Limit": convertToString(row['Limit']),
            "Outstanding": row['Outstanding'],
            "Overdue": row['Overdue'],
            "Start Date": convertToString(row['Start Date']).replace(" 00:00:00", ""),
            "End Date of Contract": convertToString(row['End Date of Contract']).replace(" 00:00:00", ""),
            "Default": row['Default']
        })
        total_limit += convertToMillion(row["Limit"])
        total_outstanding += convertToMillion(row["Outstanding"])
        total_overdue += convertToMillion(row['Overdue'])
    response.append({
        "Nature of Facility": "Sub Total",
        "Limit": total_limit,
        "Outstanding": total_outstanding,
        "Overdue": total_overdue,
        "Start Date": ' ',
        "End Date of Contract": ' ',
        "Default": "Yes" if "Yes" in set(df['Default'].tolist()) else "No"
        })
    return response

def getSummaryOfExpiredButShowingLiveNonFundedConcern(df):
    if df.empty:
        return []
    df = df[df["Subject code"] != '1']   
    if not df.empty:
        df = df[df['Is Funded'] != "Yes"]
        df = df[df['Phase'] == 'Living']
        df = df[(pd.to_datetime(df['Outstanding Zero Date']) < pd.to_datetime(df['End Date of Contract'])) | (pd.to_datetime(df["Outstanding Date"]) > pd.to_datetime(df['End Date of Contract']))]
        response = []
        total_limit = 0
        total_outstanding = 0
        total_overdue = 0 
        for i, row in df.iterrows():
            response.append({
                "Nature of Facility": row['Facility Type'],
                "Limit": convertToString(row['Limit']),
                "Outstanding": row['Outstanding'],
                "Overdue": row['Overdue'],
                "Start Date": convertToString(row['Start Date']).replace(" 00:00:00", ""),
                "End Date of Contract": convertToString(row['End Date of Contract']).replace(" 00:00:00", ""),
                "Default": row['Default']
            })
            total_limit += convertToMillion(row["Limit"])
            total_outstanding += convertToMillion(row["Outstanding"])
            total_overdue += convertToMillion(row['Overdue'])
        response.append({
            "Nature of Facility": "Sub Total",
            "Limit": total_limit,
            "Outstanding": total_outstanding,
            "Overdue": total_overdue,
            "Start Date": ' ',
            "End Date of Contract": ' ',
            "Default": "Yes" if "Yes" in set(df['Default'].tolist()) else "No"
            })
    return response
def getCorporateDashboard(cibs):
    response = {}
    df = getCorporateDataFrame(cibs)
    response['analysis type'] = "Corporate"
    response['Summary Table - 1'] = getSummaryTable(cibs)
    response['Summary Table - 1 for Proprietorship Concern'] = getSummaryTableConcern(cibs)
    response['A - Summary of Terminated Facilities'] = {
        "Funded": getSummaryOfTerminatedFacilityFunded(df),
        "Non Funded": getSummaryOfTerminatedFacilityNonFunded(df)
    }
    response['A1 - Summary of Terminated Facilities for Concerns'] = {
        "Funded": getSummaryOfTerminatedFacilityFundedConcern(df),
        "Non Funded": getSummaryOfTerminatedFacilityNonFundedConcern(df)
    }
    response['B - Summary of Facilities for Concerns'] = getSummaryOfFacilities(df)
    response['B1 - Summary of Facilities'] = getSummaryOfFacilitiesConcern(df)
    response['C - Summary of Reschedule Loan'] = {
        "Borrower": getSummaryOfRescheduleLoan(df, BORROWER),
        "Guarantor": getSummaryOfRescheduleLoan(df, GUARANTOR) 
    }
    response['C1 - Summary of Reschedule Loan for Concerns'] = {
        "Borrower": getSummaryOfRescheduleLoanConcern(df, BORROWER),
        "Guarantor": getSummaryOfRescheduleLoanConcern(df, GUARANTOR) 
    }
    response['D - Summary of Requested Loan'] = getSummaryOfRequestedLoan(cibs)
    response['D1 - Summary of Requested Loan for Concern'] = getSummaryOfRequestedLoanConcern(cibs)

    response['E - Summary of Stay Order'] = {
        "Borrower": getSummaryOfStayOrder(df, BORROWER),
        "Guarantor": getSummaryOfStayOrder(df, GUARANTOR)
        }
    response['E1 - Summary of Stay Order for Concern'] = {
        "Borrower": getSummaryOfStayOrder(df, BORROWER),
        "Guarantor": getSummaryOfStayOrder(df, GUARANTOR)
        }
    response['F - Expired Loan But Showing Live'] = {
        "Summary of Funded Facility": getSummaryOfExpiredButShowingLiveFunded(df),
        "Summary of Non Funded Facility": getSummaryOfExpiredButShowingLiveNonFunded(df),
    }

    response['F1 - Expired Loan But Showing Live for Concern'] = {
        "Summary of Funded Facility": getSummaryOfExpiredButShowingLiveFundedConcern(df),
        "Summary of Non Funded Facility": getSummaryOfExpiredButShowingLiveNonFundedConcern(df),
    }
    response['Summary Table - 2'] = getSummaryTableTwo(df)
    response['Summary Table - 2 for Concern'] = getSummaryTableTwoConcern(df)
    response['Summary Table - 3'] = getSummaryTableThree(df)
    response['Summary Table - 3 for Concern'] = getSummaryTableThreeConcern(df)
    
    return response