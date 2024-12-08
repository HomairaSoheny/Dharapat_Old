from cProfile import label
from typing import final

from numpy.ma.extras import column_stack

from dashboard.engines.corporate_engine import *
from dashboard.engines.general_engine import *
from utils.general_helper import *


def alert_creation(cib, response):
    funded_total_outstanding = False
    funded_installment_outstanding = False
    funded_non_installment_outstanding = False
    nonfunded_total_outstanding = False

    warning_response = {}
    cdf = getCorporateDataFrame([cib])
    columns = cib.summary_1A.columns
    unique_prefixes = list({col.split('_')[0] for col in columns if '_' in col})
    unwanted_prefixes = ['Requested', 'Stay Order', 'Terminated']
    filtered_prefixes = list(set(unique_prefixes) - set(unwanted_prefixes))
    if not cdf.empty:
        #Funded Oustanding Installment Check
        out_installment = 0
        for status in filtered_prefixes:
            x = cdf[(cdf['Phase'] == "Living") & (cdf['CL Status'] == status) & (
                    cdf['Installment Type'] == 'Installment') & (cdf['Is Funded'] == 'Yes') & (
                            cdf['Role'] == 'Borrower')].Outstanding.sum()
            out_installment += x

        out_installment += cdf[cdf['Role'].isin(['Borrower']) & (cdf['Is Stay Order'] == "Yes") & (
                cdf['Installment Type'] == 'Installment') & (cdf['Is Funded'] == 'Yes')]['Stay Order Amount'].sum()
        if convertToMillion(out_installment) != response["Funded Outstanding Installment"]:
            funded_installment_outstanding = True

        #Funded Oustanding NonInstallment Check
        out_installment = 0
        for status in filtered_prefixes:
            x = cdf[(cdf['Phase'] == "Living") & (cdf['CL Status'] == status) & (
                cdf['Installment Type'].isin(['No Installment', 'Credit Card'])) & (cdf['Is Funded'] == 'Yes') & (
                            cdf['Role'] == 'Borrower')].Outstanding.sum()
            out_installment += x

        out_installment += cdf[cdf['Role'].isin(['Borrower']) & (cdf['Is Stay Order'] == "Yes") & (
            cdf['Installment Type'].isin(['No Installment', 'Credit Card'])) & (cdf['Is Funded'] == 'Yes')][
            'Stay Order Amount'].sum()
        if convertToMillion(out_installment) != response["Funded Outstanding Non Installment"]:
            funded_non_installment_outstanding = True

        #Funded Outstanding Total check
        out_total = 0
        for status in filtered_prefixes:
            x = cdf[(cdf['Phase'] == "Living") & (cdf['CL Status'] == status) & (cdf['Is Funded'] == 'Yes') & (
                    cdf['Role'] == 'Borrower')].Outstanding.sum()
            out_total += x
        out_total += \
            cdf[cdf['Role'].isin(['Borrower']) & (cdf['Is Stay Order'] == "Yes") & (cdf['Is Funded'] == 'Yes')][
                'Stay Order Amount'].sum()
        if convertToMillion(out_total) != response["Funded Outstanding Total"]:
            funded_total_outstanding = True

        #Non-Funded Outstanding Total check
        out_nonfunded = 0

        out_nonfunded += cdf[
            (cdf['Phase'] == "Living") & (cdf['Is Funded'] == 'No') & (cdf['Role'] == 'Borrower')].Outstanding.sum()
        out_nonfunded += \
            cdf[cdf['Role'].isin(['Borrower']) & (cdf['Is Stay Order'] == "Yes") & (cdf['Is Funded'] == 'No')][
                'Stay Order Amount'].sum()
        if convertToMillion(out_nonfunded) != response["Non-Funded Outstanding"]:
            nonfunded_total_outstanding = True

    cib_alert = {
        "Funded Outstanding Installment Alert": convertToString(funded_installment_outstanding),
        "Funded Outstanding Non Installment Alert": convertToString(funded_non_installment_outstanding),
        "Funded Outstanding Total Alert": convertToString(funded_total_outstanding),
        "Non-Funded Outstanding Alert": convertToString(nonfunded_total_outstanding)

    }
    return cib_alert


def StayOrderRemarks(cib):
    if cib.company_list is not None:
        company_list_df = cib.company_list

        # Extract unique stay order remarks from the company list DataFrame if it exists
        if company_list_df is not None and 'Stay Order' in company_list_df.columns:
            stay_order_remarks = set(company_list_df['Stay Order'])
            stay_order_comment = ", ".join(stay_order_remarks)
            return stay_order_comment  # Combine unique remarks into one comment
        else:
            stay_order_comment = ""
            return stay_order_comment
    return " "


def getInquiryDate(cib_header):
    if cib_header is not None:
        inquiry_timestamp = cib_header["Date of Inquiry"][0].timestamp()
        inquiry_date = datetime.fromtimestamp(inquiry_timestamp).strftime('%Y-%m-%d')
        return inquiry_date
    return ''


def return_empty_result(title):

    final_data = {
        "title": title,
        "columns": [],
        "data": []
    }
    return final_data


def getSummaryTable(cibs):
    response = []
    for cib in cibs:
        df = getCorporateDataFrame([cib])

        # Initialize non_blank_dates to an empty series with datetime type
        non_blank_dates = pd.Series([], dtype='datetime64[ns]')

        if (cib.cib_category != 'Type j' and cib.cib_category != 'Type k') and not df.empty:
            df = df[df['Subject code'] == '1']

        if not df.empty:
            non_blank_dates = df.loc[df['Position Date'] != '', 'Position Date']

        funded = cib.summary_1A
        funded['total'] = funded[
            [i for i in funded.columns if 'Amount' in i and 'Requested' not in i and 'Terminated' not in i]].sum(axis=1)
        non_funded = cib.summary_1B
        non_funded['total'] = non_funded[
            [i for i in non_funded.columns if 'Amount' in i and 'Requested' not in i and 'Terminated' not in i]].sum(
            axis=1)

        funded_guarantor = cib.summary_2A
        funded_guarantor['total'] = funded_guarantor[[i for i in funded_guarantor.columns if
                                                      'Amount' in i and 'Requested' not in i and 'Terminated' not in i]].sum(
            axis=1)
        non_funded_guarantor = cib.summary_2B
        non_funded_guarantor['total'] = non_funded_guarantor[[i for i in non_funded_guarantor.columns if
                                                              'Amount' in i and 'Requested' not in i and 'Terminated' not in i]].sum(
            axis=1)

        temp_response = {
            "Funded Outstanding Installment": convertToMillion(
                funded[funded['Product'] == 'Installments'].total.tolist()[0]),
            "Funded Outstanding Non Installment": convertToMillion(
                funded[funded['Product'] == 'Non-Installments'].total.tolist()[0]),
            "Funded Outstanding Total": convertToMillion(funded[funded['Product'] == 'Total'].total.tolist()[0]),
            "Non-Funded Outstanding": convertToMillion(non_funded.total.tolist()[3]),
            "Total Outstanding": convertToMillion(
                convertToFloat(funded.total.tolist()[3]) + convertToFloat(non_funded.total.tolist()[3])),
        }

        cib_alert = alert_creation(cib, temp_response)

        response.append({
            "CIB Category": getCIBCategory(cib),
            "Date of inquiry": getInquiryDate(cib.cib_header),
            "Name of Concern": getBorrowersName(cib.subject_info),
            "Position Date": non_blank_dates.max() if not non_blank_dates.empty else '',
            "Funded Outstanding Installment": convertToMillion(
                funded[funded['Product'] == 'Installments'].total.tolist()[0]),
            "Funded Outstanding Installment Raw": funded[funded['Product'] == 'Installments'].total.tolist()[0],
            "Funded Outstanding Non Installment": convertToMillion(
                funded[funded['Product'] == 'Non-Installments'].total.tolist()[0]),
            "Funded Outstanding Non Installment Raw": funded[funded['Product'] == 'Non-Installments'].total.tolist()[0],
            "Funded Outstanding Total": convertToMillion(funded[funded['Product'] == 'Total'].total.tolist()[0]),
            "Funded Outstanding Total Raw": funded[funded['Product'] == 'Total'].total.tolist()[0],
            "Non-Funded Outstanding": convertToMillion(non_funded.total.tolist()[3]),
            "Non-Funded Outstanding Raw": non_funded.total.tolist()[3],
            "Total Outstanding": convertToMillion(
                convertToFloat(funded.total.tolist()[3]) + convertToFloat(non_funded.total.tolist()[3])),
            "Total Outstanding Raw": convertToFloat(
                funded.total.tolist()[3] + convertToFloat(non_funded.total.tolist()[3])),
            "Overdue": convertToMillion(cib.summary_1['Total Overdue Amount']),
            "Overdue Raw": cib.summary_1['Total Overdue Amount'],
            "STD": funded['STD_Amount'].sum(),
            "SMA": funded['SMA_Amount'].sum(),
            "SS(No)": funded['SS_No_Amount'].sum(),
            "SS(Yes)": funded['SS_Yes_Amount'].sum(),
            "DF": funded['DF_Amount'].sum(),
            "BLW": funded['BLW_Amount'].sum(),
            "Terminated": funded['Terminated_Amount'].sum(),
            "Requested": funded['Requested_Amount'].sum(),
            "Stay Order": funded['Stay_Order_Amount'].sum(),
            "Willful Default(WD)": funded['Willful_Default_WD_Amount'].sum(),
            "Willful Default(Appeal)": funded['Willful_Default_Appeal_Amount'].sum(),
            "CL Status": "-" if df.empty else general_engine.getClassFromSet(set(list(df['CL Status']))),
            # "Worst CL Status as Borrower": '' if df.empty else getClassFromSet(set(df[df['Role'] == 'Borrower']["Worse Classification Status"])),
            "Default": "-" if df.empty else ("Yes" if "Yes" in list(df['Default']) else "No"),
            "Stay Order Remarks": StayOrderRemarks(cib),
            "Outstanding Guarantor": funded_guarantor['total'].iloc[-1] + non_funded_guarantor['total'].iloc[-1],
            "Worst CL Status as Guarantor": '' if df.empty else getClassFromSet(
                set(df[df['Role'] == 'Guarantor']["Worse Classification Status"])),
            "Default Guarantor": "-" if df.empty else ("Yes" if "Yes" in list(df['Default']) else "No"),
            "Stay Order Remarks Guarantor": StayOrderRemarks(cib),
            "CIB PDF View": PDF_LINK + cib.pdf_name,
            "Updated Overdue and CL Status": "-" if df.empty else (
                re.sub(r'[,\[\]]', '', str(list(df['Remarks']))).replace("'", '')),
            "Funded Outstanding Installment Alert": cib_alert["Funded Outstanding Installment Alert"],
            "Funded Outstanding Non Installment Alert": cib_alert["Funded Outstanding Non Installment Alert"],
            "Funded Outstanding Total Alert": cib_alert["Funded Outstanding Total Alert"],
            "Non-Funded Outstanding Alert": cib_alert["Non-Funded Outstanding Alert"]
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

    columns = [
        {
            "label": "CIB Category",
            "key": "CIB Category"
        },
        {
            'label': 'Name of Concern',
            'key': 'Name of Concern'
        },
        {
            'label': 'Position Date',
            'key': 'Position Date'
        },
        {
            'label': 'Installment(In Million)',
            'key': 'Funded Outstanding Installment',
            'parentColumnName': 'Funded Outstanding'
        },
        {
            'label': 'Installment(Raw)',
            'key': 'Funded Outstanding Installment Raw',
            'parentColumnName': 'Funded Outstanding'
        },
        {
            'label': 'Non Installment(In Million)',
            'key': 'Funded Outstanding Non Installment',
            'parentColumnName': 'Funded Outstanding',
        },
        {
            'label': 'Funded Outstanding Non Installment(Raw)',
            'key': 'Funded Outstanding Non Installment Raw',
            'parentColumnName': 'Funded Outstanding',
        },
        {
            'label': 'Total(In Million)',
            'key': 'Funded Outstanding Total',
            'parentColumnName': 'Funded Outstanding',
        },
        {
            'label': 'Total(Raw)',
            'key': 'Funded Outstanding Total Raw',
            'parentColumnName': 'Funded Outstanding',
        },
        {
            'label': 'Non-Funded Outstanding(In Million)',
            'key': 'Non-Funded Outstanding'
        },
        {
            'label': 'Non-Funded Outstanding(Raw)',
            'key': 'Non-Funded Outstanding Raw'
        },
        {
            'label': 'Total Outstanding(In Million)',
            'key': 'Total Outstanding'
        },
        {
            'label': 'Total Outstanding(Raw)',
            'key': 'Total Outstanding Raw'
        },
        {
            'label': 'Overdue(In Million)',
            'key': 'Overdue'
        },
        {
            'label': 'Overdue(Raw)',
            'key': 'Overdue Raw'
        },
        {
            'label': 'STD',
            'key': 'STD'
        },
        {
            'label': 'SMA',
            'key': 'SMA'
        },
        {
            'label': 'SS(No)',
            'key': 'SS(No)'
        },
        {
            'label': 'SS(Yes)',
            'key': 'SS(Yes)'
        },
        {
            'label': 'DF',
            'key': 'DF'
        },
        {
            'label': 'BLW',
            'key': 'BLW'
        },
        {
            'label': 'Terminated',
            'key': 'Terminated'
        },
        {
            'label': 'Requested',
            'key': 'Requested'
        },
        {
            'label': 'Stay Order',
            'key': 'Stay Order'
        },
        {
            'label': 'Willful Default(WD)',
            'key': 'Willful Default(WD)'
        },
        {
            'label': 'Willful Default(Appeal)',
            'key': 'Willful Default(Appeal)'
        },
        {
            'label': 'CL Status',
            'key': 'CL Status'
        },
        {
            'label': 'Default/Willfull default',
            'key': 'Default'
        },
        {
            'label': 'Stay Order Remarks',
            'key': 'Stay Order Remarks'
        },
        {
            'label': 'Outstanding',
            'key': 'Outstanding Guarantor',
            'parentColumnName': 'Guarantor'
        },
        {
            'label': 'Worst CL Status as Guarantor',
            'key': 'Worst CL Status as Guarantor',
            'parentColumnName': 'Guarantor'
        },
        {
            'label': 'Default/Willful default as Guarantor',
            'key': 'Default Guarantor',
            'parentColumnName': 'Guarantor'
        },
        {
            'label': 'Stay Order Remarks',
            'key': 'Stay Order Remarks Guarantor',
            'parentColumnName': 'Guarantor'
        },
        {
            'label': 'CIB PDF View',
            'key': 'CIB PDF View'
        },
        {
            'label': 'Updated Overdue and CL Status',
            'key': 'Updated Overdue and CL Status'
        },
        {
            'label': 'Funded Outstanding Installment Alert',
            'key': 'Funded Outstanding Installment Alert'
        },
        {
            'label': 'Funded Outstanding Non Installment Alert',
            'key': 'Funded Outstanding Non Installment Alert'
        },
        {
            'label': 'Funded Outstanding Total Alert',
            'key': 'Funded Outstanding Total Alert'
        },
        {
            'label': 'Non-Funded Outstanding Alert',
            'key': 'Non-Funded Outstanding Alert'
        }
    ]

    final_data = {
        "title": "Summary Table - 1",
        "columns": columns,
        "data": response
    }


    # print("Summary Table -1 Format")
    # print(final_data)
    # print("Summary Table -1 ended")
    # return response
    return final_data


def getSummaryTableConcern(cibs):
    response = []
    for cib in cibs:
        df = getCorporateDataFrame([cib])
        if not df.empty:
            # Apply filtering to df
            df = df[(df['Subject code'] != '1') & (df['CIB Category'].str.contains('proprietorship concern'))]

            if not df.empty:
                df = df[(df['Phase'] == 'Living') & (df['Role'] == 'Borrower')]
                if not df.empty:
                    non_blank_dates = df.loc[df['Position Date'] != '', 'Position Date']
                    for category in df['CIB Category'].unique():
                        cat_df = df[df['CIB Category'] == category]
                        cib_holders_name = cat_df["Name"].iloc[0]
                        for concern_name in cat_df["Concerns Trade Name"].unique():
                            temp_df = cat_df[cat_df["Concerns Trade Name"] == concern_name]
                            response.append(
                                getSummaryTableConcernFields(cib, category, concern_name, cib_holders_name, temp_df))
                            temp_df = pd.DataFrame(response)
                            response.append(getSummaryTableConcernSum("", "Total for concern", temp_df))
                        sub_total_df = pd.DataFrame(response)
                        sub_total_df = sub_total_df[sub_total_df['CIB Category'] == category]
                        response.append(getSummaryTableConcernSum("", "Sub Total", sub_total_df))
                    total_df = pd.DataFrame(response)
                    total_df = total_df[total_df["Concerns Trade Name"] == "Sub Total"]
                    # total_df = total_df.query("Name of Concern == 'Sub Total'")

                    response.append(getSummaryTableConcernSum("", "Grand Total", total_df))
    columns = []

    if len(response)!=0:
        for key,val in response[0].items():
            temp_dict = {}
            temp_dict['label'] = key
            temp_dict['key'] = key
            columns.append(temp_dict)


    final_data = {
        "title": "Summary Table - 1 for Proprietorship Concern",
        "columns": columns,
        "data": response
    }
    return final_data


def getSummaryTableTwo(df):
    if df.empty:
        return return_empty_result("Summary Table - 2")
    response = []
    is_proprietorship = df['CIB Category'].str.contains('proprietorship', case=False)
    df = df[
        (is_proprietorship & (df['Subject code'] == '1')) |
        (~is_proprietorship)
        ]
    df = df[df['Phase'] == 'Living']
    if not df.empty:

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

        columns = [
            {
                'label': 'CIB Category',
                'key': 'CIB Category'
            },
            {
                'label': 'Name of Concern',
                'key': 'Name of Concern'
            },
            {
                'label': 'Installment(In Million)',
                'key': 'Funded Installment',
                'parentColumnName': 'Funded'
            },
            {
                'label': 'Installment(Raw)',
                'key': 'Funded Installment Raw',
                'parentColumnName': 'Funded'
            },
            {
                'label': 'Non Installment(In Million)',
                'key': 'Funded Non Installment',
                'parentColumnName': 'Funded'
            },
            {
                'label': 'Non Installment(Raw)',
                'key': 'Funded Non Installment Raw',
                'parentColumnName': 'Funded'
            },
            {
                'label': 'Total(In Million)',
                'key': 'Funded Total',
                'parentColumnName': 'Funded'
            },
            {
                'label': 'Total(Raw)',
                'key': 'Funded Total Raw',
                'parentColumnName': 'Funded'
            },
            {
                'label': 'Non-Funded(In Million)',
                'key': 'Non-Funded'
            },
            {
                'label': 'Non-Funded(Raw)',
                'key': 'Non-Funded Raw'
            },
            {
                'label': 'Total(In Million)',
                'key': 'Total'
            },
            {
                'label': 'Total(Raw)',
                'key': 'Total Raw'
            },
            {
                'label': 'Overdue(In Million)',
                'key': 'Overdue'
            },
            {
                'label': 'Overdue(Raw)',
                'key': 'Overdue Raw'
            },
            {
                'label': 'Worst CL Status',
                'key': 'Worst CL Status'
            },
            {
                'label': 'Rescheduled Loan',
                'key': 'Rescheduled Loan'
            },
            {
                'label': 'STD',
                'key': 'Loan STD',
                'parentColumnName': 'Loan Amount in Million'
            },
            {
                'label': 'SMA',
                'key': 'Loan SMA',
                'parentColumnName': 'Loan Amount in Million'
            },
            {
                'label': 'SS',
                'key': 'Loan SS',
                'parentColumnName': 'Loan Amount in Million'
            },
            {
                'label': 'DF',
                'key': 'Loan DF',
                'parentColumnName': 'Loan Amount in Million'
            },
            {
                'label': 'Loan',
                'key': 'Loan BL',
                'parentColumnName': 'Loan Amount in Million'
            },
            {
                'label': 'BLW',
                'key': 'Loan BLW',
                'parentColumnName': 'Loan Amount in Million'
            },
            {
                'label': 'Loan Stay Order',
                'key': 'Loan Stay Order',
                'parentColumnName': 'Loan Amount in Million'
            },
            {
                'label': 'Remarks(CIB) related to classified liability',
                'key': 'Remarks'
            }
        ]

        final_data = {
            "title": "Summary Table - 2",
            "columns": columns,
            "data": response
        }
        return final_data

    return return_empty_result("Summary Table - 2")


def getSummaryTableTwoConcern(df):
    if df.empty:
        return return_empty_result("Summary Table - 2 for Concern")
    response = []
    df = df[(df["Subject code"] != '1') & (df['CIB Category'].str.contains('proprietorship', case=False))]
    df = df[df['Phase'] == 'Living']
    if not df.empty:

        if not df.empty:
            for category in df['CIB Category'].unique():
                cat_df = df[df['CIB Category'] == category]
                cib_holders_name = cat_df["Name"].iloc[0]
                for concern_name in cat_df["Concerns Trade Name"].unique():
                    temp_df = cat_df[cat_df["Concerns Trade Name"] == concern_name]
                    response.append(getSummaryTableTwoConcernFields(category, concern_name, cib_holders_name, temp_df))
                    temp_df = pd.DataFrame(response)
                    response.append(getSummaryTableTwoConcernSum("", "Total for concern", temp_df))
                sub_total_df = pd.DataFrame(response)
                sub_total_df = sub_total_df[sub_total_df['CIB Category'] == category]
                response.append(getSummaryTableTwoConcernSum(category, "Sub Total", sub_total_df))
            total_df = pd.DataFrame(response)
            #total_df = total_df[total_df['Name of Concern'] == "Sub Total"]
            total_df = total_df.query("`Name of Concern` == 'Sub Total'")
            response.append(getSummaryTableTwoConcernSum("", "Grand Total", total_df))
    columns=[]
    if len(response)!=0:
        for key, val in response[0].items():
            temp_f = {}
            temp_f['label'] = key
            temp_f['key'] = key
            columns.append(temp_f)
    final_data = {
        "title": "Summary Table - 2 for Concern",
        "columns": columns,
        "data": response
    }

    return final_data


def getSummaryTableThree(df):
    if df.empty:
        final_data_funded = return_empty_result('Funded')
        final_data_nonfunded = return_empty_result('Non Funded')
        return {
            "funded": final_data_funded,
            "non_funded": final_data_nonfunded
        }
    funded = []
    non_funded = []
    is_proprietorship = df['CIB Category'].str.contains('proprietorship', case=False)
    df = df[
        (is_proprietorship & (df['Subject code'] == '1')) |
        (~is_proprietorship)
        ]
    df = df[df['Phase'] == 'Living']
    if not df.empty:

        non_funded_loans = list(df[df['Is Funded'] == "No"]["Facility Type"].unique())
        for category in df['CIB Category'].unique():
            cat_df = df[df['CIB Category'] == category]
            for concern_name in cat_df['Name'].unique():
                temp_df = cat_df[cat_df['Name'] == concern_name]
                funded.append(
                    getSummaryTableThreeFundedFields(category, concern_name, temp_df[temp_df['Is Funded'] == "Yes"]))
                non_funded.append(
                    getSummaryTableThreeNonFundedFields(category, concern_name, temp_df[temp_df['Is Funded'] == "No"],
                                                        non_funded_loans))
            funded_sub_total_df = pd.DataFrame(funded)
            funded_sub_total_df = funded_sub_total_df[funded_sub_total_df['CIB Category'] == category]
            funded.append(getSummaryTableThreeFundedSum(category, "Sub Total", funded_sub_total_df))
            non_funded_sub_total_df = pd.DataFrame(non_funded)
            non_funded_sub_total_df = non_funded_sub_total_df[non_funded_sub_total_df['CIB Category'] == category]
            non_funded.append(
                getSummaryTableThreeNonFundedSum(category, "Sub Total", non_funded_sub_total_df, non_funded_loans))
        funded_total_df = pd.DataFrame(funded)
        funded_total_df = funded_total_df[funded_total_df['Borrowing Company - Person'] == "Sub Total"]
        funded.append(getSummaryTableThreeFundedSum("", "Grand Total", funded_total_df))
        non_funded_total_df = pd.DataFrame(non_funded)
        non_funded_total_df = non_funded_total_df[non_funded_total_df['Borrowing Company - Person'] == "Sub Total"]
        non_funded.append(getSummaryTableThreeNonFundedSum("", "Grand Total", non_funded_total_df, non_funded_loans))

        columns_funded = [
            {
                'label': 'CIB Category',
                'key': 'CIB Category'
            },
            {
                'label': 'Borrowing Company - Person',
                'key': 'Borrowing Company - Person'
            },
            {
                'label': 'A - Overdraft - Cash Credit',
                'key': 'A - Overdraft - Cash Credit'
            },
            {
                'label': 'Overdue - EOL of A',
                'key': 'Overdue - EOL of A'
            },
            {
                'label': 'B - Time Loan',
                'key': 'B - Time Loan'
            },
            {
                'label': 'Overdue - EOL of B',
                'key': 'Overdue - EOL of B'
            },
            {
                'label': 'C - LTR',
                'key': 'C - LTR'
            },
            {
                'label': 'Overdue - EOL of C',
                'key': 'Overdue - EOL of C'
            },
            {
                'label': 'D - Other Non Installment',
                'key': 'D - Other Non Installment'
            },
            {
                'label': 'Overdue - EOL of D',
                'key': 'Overdue - EOL of D'
            },
            {
                'label': 'E - Term Loan',
                'key': 'E - Term Loan'
            },
            {
                'label': 'EMI of E',
                'key': 'EMI of E'
            },
            {
                'label': 'Overdue - EOL of E',
                'key': 'Overdue - EOL of E'
            },
            {
                'label': 'F - Other Installment Loan',
                'key': 'F - Other Installment Loan'
            },
            {
                'label': 'EMI of F',
                'key': 'EMI of F'
            },
            {
                'label': 'Overdue - EOL of F',
                'key': 'Overdue - EOL of F'
            }
        ]
        columns_nonfunded = [
            {
                'label': 'CIB Category',
                'key': 'CIB Category'
            },
            {
                'label': 'Borrowing Company - Person',
                'key': 'Borrowing Company - Person'
            },
            {
                'label': 'Guarantee (non funded)',
                'key': 'Guarantee (non funded)'
            },
            {
                'label': 'Letter of credit (non funded)',
                'key': 'Letter of credit (non funded)'
            }
        ]

        final_data_funded = {
            "title": "Funded",
            "columns": columns_funded,
            "data": funded
        }
        final_data_nonfunded = {
            "title": "Non Funded",
            "columns": columns_nonfunded,
            "data": non_funded
        }
        return {
            "funded": final_data_funded,
            "non_funded": final_data_nonfunded
        }
    final_data_funded = return_empty_result('Funded')
    final_data_nonfunded = return_empty_result('Non Funded')
    return {
        "funded": final_data_funded,
        "non_funded": final_data_nonfunded
    }


def getSummaryTableThreeConcern(df):
    if df.empty:
        final_data_funded = return_empty_result('Funded - Concern')
        final_data_nonfunded = return_empty_result('Non Funded Concern')
        return {
            "funded": final_data_funded,
            "non_funded": final_data_nonfunded
        }
    df = df[(df["Subject code"] != '1') & (df['CIB Category'].str.contains('proprietorship', case=False))]
    funded = []
    non_funded = []
    df = df[df['Phase'] == 'Living']
    if not df.empty:

        non_funded_loans = list(df[df['Is Funded'] == "No"]["Facility Type"].unique())
        for category in df['CIB Category'].unique():
            cat_df = df[df['CIB Category'] == category]

            for concern_name in cat_df["Concerns Trade Name"].unique():
                temp_df = cat_df[cat_df["Concerns Trade Name"] == concern_name]
                cib_holders_name = temp_df["Name"].iloc[0]
                funded.append(getSummaryTableThreeFundedFieldsConcern(category, concern_name, cib_holders_name,
                                                                      temp_df[temp_df['Is Funded'] == "Yes"]))

                non_funded.append(getSummaryTableThreeNonFundedFieldsConcern(category, concern_name, cib_holders_name,
                                                                             temp_df[temp_df['Is Funded'] == "No"],
                                                                             non_funded_loans))
            funded_sub_total_df = pd.DataFrame(funded)
            funded_sub_total_df = funded_sub_total_df[funded_sub_total_df['CIB Category'] == category]
            funded.append(getSummaryTableThreeFundedConcernSum("Sub Total", funded_sub_total_df))
            non_funded_sub_total_df = pd.DataFrame(non_funded)
            non_funded_sub_total_df = non_funded_sub_total_df[non_funded_sub_total_df['CIB Category'] == category]
            non_funded.append(getSummaryTableThreeNonFundedConcernSum(category, "Sub Total", non_funded_sub_total_df,
                                                                      non_funded_loans))
        funded_total_df = pd.DataFrame(funded)
        funded_total_df = funded_total_df[funded_total_df['Borrowing Company - Person'] == "Sub Total"]
        funded.append(getSummaryTableThreeFundedConcernSum("Grand Total", funded_total_df))
        non_funded_total_df = pd.DataFrame(non_funded)
        non_funded_total_df = non_funded_total_df[non_funded_total_df['Borrowing Company - Person'] == "Sub Total"]
        non_funded.append(
            getSummaryTableThreeNonFundedConcernSum("", "Grand Total", non_funded_total_df, non_funded_loans))

        columns_funded = []
        columns_nonfunded = []
        for key, val in funded[0].items():
            temp_f = {}
            temp_f['label']=key
            temp_f['key'] = key
            columns_funded.append(temp_f)
        for key, val in non_funded[0].items():
            temp_f = {}
            temp_f['label']=key
            temp_f['key'] = key
            columns_nonfunded.append(temp_f)
        final_data_funded = {
            "title": "Funded",
            "columns": columns_funded,
            "data": funded
        }
        final_data_nonfunded = {
            "title": "Funded",
            "columns": columns_nonfunded,
            "data": non_funded
        }
        return {
            "funded": final_data_funded,
            "non_funded": final_data_nonfunded
        }
    final_data_funded = return_empty_result('Funded - Concern')
    final_data_nonfunded = return_empty_result('Non Funded Concern')
    return {
        "funded": final_data_funded,
        "non_funded": final_data_nonfunded
    }


def getSummaryOfTerminatedFacilityFunded(df):
    if df.empty:
        return return_empty_result('A - Summary of Terminated Facilities : Funded')
    response = []
    df = df[df['Phase'] != 'Living']
    df = df[df['Is Funded'] == "Yes"]
    df = df[df['Installment Type'] == 'Installment']
    is_proprietorship = df['CIB Category'].str.contains('proprietorship', case=False)
    df = df[
        (is_proprietorship & (df['Subject code'] == '1')) |
        (~is_proprietorship)
        ]
    total_limit = 0
    total_days = 0
    for i, row in df.iterrows():
        response.append({
            "Category": row['CIB Category'],
            "Name of the Concern": row['Name'],
            "Installment": row['Facility Type'],
            "Limit": convertToMillion(row["Limit"]),
            "Loan/Limit (days of adjustment before/after)": (row['Loan/Limit (days of adjustment before/after)']),
            "Worse Classification Status": row["Worse Classification Status"],
            "Date of Classification": convertToString(row["Date of Classification"]).replace(" 00:00:00", "")
        })
    result_json = []
    if len(response) > 0:
        response_df = pd.DataFrame(response)
        CIBCategorySet = list(set(response_df.Category))
        result_df = pd.DataFrame()
        for cat in CIBCategorySet:
            temp_df = response_df[response_df['Category'] == cat]
            limit_sum = temp_df['Limit'].sum()
            new_row = [{
                'Category': cat,
                "Name of the Concern": 'Sub Total',
                'Installment': '-',
                'Limit': limit_sum,
                'Loan/Limit (days of adjustment before/after)': "-",
                'Worse Classification Status': '-',
                'Date of Classification': '-'
            }]
            new_row_df = pd.DataFrame(new_row)
            # Append the new row to the DataFrame
            temp_df = pd.concat([temp_df, new_row_df])
            result_df = pd.concat([result_df, temp_df])

        result_json = result_df.to_dict('records')

        result_json.append({
            "Category": '',
            "Name of the Concern": 'Grand Total',
            'Installment': "-",
            "Limit": convertToMillion(df['Limit'].sum()),
            "Loan/Limit (days of adjustment before/after)": "-",
            'Worse Classification Status': '-',
            'Date of Classification': '-'
        })

    columns = []
    if len(result_json) != 0:
        for key, val in result_json[0].items():
            temp_dict = {}
            temp_dict['label'] = key
            temp_dict['key'] = key
            columns.append(temp_dict)

    final_data = {
        "title": "A - Summary of Terminated Facilities : Funded",
        "columns": columns,
        "data": response
    }
    return final_data


def getSummaryOfTerminatedFacilityFundedConcern(df):
    if df.empty:
        return return_empty_result('A1 - Summary of Terminated Facilities for Concerns : Funded')
    response = []
    df = df[(df["Subject code"] != '1') & (df['CIB Category'].str.contains('proprietorship', case=False))]
    total_limit = 0
    total_days = 0
    if not df.empty:
        total_limit = 0
        total_days = 0
        df = df[df['Phase'] != 'Living']
        df = df[df['Is Funded'] == "Yes"]
        df = df[df['Installment Type'] == 'Installment']
        if not df.empty:
            for i, row in df.iterrows():
                response.append({
                    "Category": row['CIB Category'],
                    "Name of the Concern": row['Name'],
                    "Concerns Trade Name": row["Concerns Trade Name"],
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
                temp_df = response_df[response_df['Category'] == cat]
                limit_sum = temp_df['Limit'].sum()
                new_row = [{
                    'Category': cat,
                    "Name of the Concern": '-',
                    "Concerns Trade Name": 'Sub Total',
                    'Installment': '-',
                    'Limit': limit_sum,
                    'Loan/Limit (days of adjustment before/after)': "--",
                    'Worse Classification Status': '-',
                    'Date of Classification': '-'
                }]
                new_row_df = pd.DataFrame(new_row)
                # Append the new row to the DataFrame
                temp_df = pd.concat([temp_df, new_row_df])
                result_df = pd.concat([result_df, temp_df])

            result_json = result_df.to_dict('records')

            if len(response) > 0:
                result_json.append({
                    "Category": '',
                    "Name of the Concern": '-',
                    "Concerns Trade Name": 'Grand Total',
                    'Installment': "-",
                    "Limit": convertToMillion(df['Limit'].sum()),
                    "Loan/Limit (days of adjustment before/after)": "--",
                    'Worse Classification Status': '-',
                    'Date of Classification': '-'
                })

            columns = []
            if len(result_json) != 0:
                for key, val in result_json[0].items():
                    temp_dict = {}
                    temp_dict['label'] = key
                    temp_dict['key'] = key
                    columns.append(temp_dict)

            final_data = {
                "title": "A1 - Summary of Terminated Facilities for Concerns : Funded",
                "columns": columns,
                "data": result_json
            }

            return final_data
    columns = []

    final_data = {
        "title": "A1 - Summary of Terminated Facilities for Concerns : Funded",
        "columns": columns,
        "data": response
    }

    # response.append({
    #     "Category": '',
    #     "Name of the Concern": '-',
    #     "Concerns Trade Name": 'No Concerns Found',
    #     "Installment": '-',
    #     "Limit": total_limit,
    #     "Loan/Limit (days of adjustment before/after)": '',
    #     "Worse Classification Status": '',
    #     "Date of Classification": ''
    # })
    return final_data


def getSummaryOfTerminatedFacilityNonFunded(df):
    if df.empty:
        return return_empty_result('A - Summary of Terminated Facilities : Non-Funded')
    response = []
    df = df[df['Phase'] != 'Living']
    df = df[df['Is Funded'] == "No"]
    df = df[df['Installment Type'] == 'No Installment']
    is_proprietorship = df['CIB Category'].str.contains('proprietorship', case=False)
    df = df[
        (is_proprietorship & (df['Subject code'] == '1')) |
        (~is_proprietorship)
        ]
    total_limit = 0
    total_days = 0
    for i, row in df.iterrows():
        response.append({
            "Category": row['CIB Category'],
            "Name of the Concern": row['Name'],
            "Non-Installment": row['Facility Type'],
            "Limit": convertToMillion(row["Limit"]),
            "Loan/Limit (days of adjustment before/after)": row['Loan/Limit (days of adjustment before/after)'],
            "Worse Classification Status": row["Worse Classification Status"],
            "Date of Classification": convertToString(row["Date of Classification"]).replace(" 00:00:00", "")
        })

    result_json = []
    if len(response) > 0:
        response_df = pd.DataFrame(response)
        CIBCategorySet = list(set(response_df.Category))
        result_df = pd.DataFrame()
        for cat in CIBCategorySet:
            temp_df = response_df[response_df['Category'] == cat]
            limit_sum = temp_df['Limit'].sum()

            new_row = [{
                'Category': cat,
                "Name of the Concern": '-',
                'Non-Installment': 'Sub Total',
                'Limit': limit_sum,
                'Loan/Limit (days of adjustment before/after)': '-',
                'Worse Classification Status': '-',
                'Date of Classification': '-'
            }]
            new_row_df = pd.DataFrame(new_row)
            # Append the new row to the DataFrame
            temp_df = pd.concat([temp_df, new_row_df])
            result_df = pd.concat([result_df, temp_df])

        result_json = result_df.to_dict('records')

        result_json.append({
            "Category": '',
            "Name of the Concern": '-',
            'Non-Installment': "Grand Total",
            "Limit": convertToMillion(df['Limit'].sum()),
            "Loan/Limit (days of adjustment before/after)": '-',
            'Worse Classification Status': '-',
            'Date of Classification': '-'
        })
    columns = []
    if len(response) != 0:
        for key, val in result_json[0].items():
            temp_dict = {}
            temp_dict['label'] = key
            temp_dict['key'] = key
            columns.append(temp_dict)

    final_data = {
        "title": "A - Summary of Terminated Facilities : Non-Funded",
        "columns": columns,
        "data": response
    }
    return final_data


def getSummaryOfTerminatedFacilityNonFundedConcern(df):
    if df.empty:
        return return_empty_result('A1 - Summary of Terminated Facilities for Concerns : Non-Funded')
    response = []
    df = df[(df["Subject code"] != '1') & (df['CIB Category'].str.contains('proprietorship', case=False))]
    total_limit = 0
    total_days = 0
    if not df.empty:
        df = df[df['Phase'] != 'Living']
        df = df[df['Is Funded'] == "No"]
        df = df[df['Installment Type'] == 'No Installment']
        total_limit = 0
        total_days = 0
        if not df.empty:
            for i, row in df.iterrows():
                response.append({
                    "Category": row['CIB Category'],
                    "Name of the Concern": row['Name'],
                    "Concerns Trade Name": row["Concerns Trade Name"],
                    "Non-Installment": row['Facility Type'],
                    "Limit": convertToMillion(row["Limit"]),
                    "Loan/Limit (days of adjustment before/after)": row['Loan/Limit (days of adjustment before/after)'],
                    "Worse Classification Status": row["Worse Classification Status"],
                    "Date of Classification": convertToString(row["Date of Classification"]).replace(" 00:00:00", "")
                })

            response_df = pd.DataFrame(response)
            CIBCategorySet = list(set(response_df.Category))
            result_df = pd.DataFrame()
            for cat in CIBCategorySet:
                temp_df = response_df[response_df['Category'] == cat]
                limit_sum = temp_df['Limit'].sum()
                new_row = [{
                    'Category': cat,
                    "Name of the Concern": '-',
                    "Concerns Trade Name": '-',
                    'Non-Installment': 'Sub Total',
                    'Limit': limit_sum,
                    'Loan/Limit (days of adjustment before/after)': '-',
                    'Worse Classification Status': '-',
                    'Date of Classification': '-'
                }]
                new_row_df = pd.DataFrame(new_row)
                # Append the new row to the DataFrame
                temp_df = pd.concat([temp_df, new_row_df])
                result_df = pd.concat([result_df, temp_df])

            result_json = result_df.to_dict('records')

            if len(result_json) > 0:
                result_json.append({
                    "Category": '',
                    "Name of the Concern": '-',
                    "Concerns Trade Name": '-',
                    'Non-Installment': "Grand Total",
                    "Limit": convertToMillion(df['Limit'].sum()),
                    "Loan/Limit (days of adjustment before/after)": '-',
                    'Worse Classification Status': '-',
                    'Date of Classification': '-'
                })

            columns = []
            if len(result_json) != 0:
                for key, val in result_json[0].items():
                    temp_dict = {}
                    temp_dict['label'] = key
                    temp_dict['key'] = key
                    columns.append(temp_dict)

            final_data = {
                "title": "A1 - Summary of Terminated Facilities for Concerns : Non-Funded",
                "columns": columns,
                "data": result_json
            }
            return final_data
        # response.append({
        #     "Category": '',
        #     "Name of the Concern": '-',
        #     "Concerns Trade Name": '-',
        #     "Non-Installment": 'Sub Total',
        #     "Limit": total_limit,
        #     "Loan/Limit (days of adjustment before/after)": '',
        #     "Worse Classification Status": '',
        #     "Date of Classification": ''
        # })
        # return response
    # response.append({
    #     "Category": '',
    #     "Name of the Concern": '-',
    #     "Concerns Trade Name": '-',
    #     "Non-Installment": 'No Concern Found',
    #     "Limit": total_limit,
    #     "Loan/Limit (days of adjustment before/after)": '',
    #     "Worse Classification Status": '',
    #     "Date of Classification": ''
    # })
    return return_empty_result('A1 - Summary of Terminated Facilities for Concerns : Non-Funded')


def getSummaryOfFundedFacility(df):
    response = []
    df = df[df['Phase'] == 'Living']
    df = df[df['Is Funded'] == 'Yes']
    is_proprietorship = df['CIB Category'].str.contains('proprietorship', case=False)
    df = df[
        (is_proprietorship & (df['Subject code'] == '1')) |
        (~is_proprietorship)
        ]
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
    df = df[(df["Subject code"] != '1') & (df['CIB Category'].str.contains('proprietorship', case=False))]

    if not df.empty:
        df = df[df['Phase'] == 'Living']
        df = df[df['Is Funded'] == 'Yes']
        installment = df[df['Installment Type'] == 'Installment']
        non_installment = df[df['Installment Type'] == 'No Installment']

        for i, row in installment.iterrows():
            response.append(getSummaryOfFundedFacilityFieldsConcern(row, i, True))
        if installment.shape[0] > 0:
            response.append(getSummaryOfFundedFacilitySumConcern(installment, "Sub Total", "Installment"))

        for i, row in non_installment.iterrows():
            response.append(getSummaryOfFundedFacilityFieldsConcern(row, i, False))
        if non_installment.shape[0] > 0:
            response.append(getSummaryOfFundedFacilitySumConcern(non_installment, "Sub Total", "No Installment"))

    return response


def getSummaryOfNonFundedFacility(df):
    response = []
    df = df[df['Phase'] == 'Living']
    df = df[df['Is Funded'] == 'No']
    is_proprietorship = df['CIB Category'].str.contains('proprietorship', case=False)
    df = df[
        (is_proprietorship & (df['Subject code'] == '1')) |
        (~is_proprietorship)
        ]
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
    df = df[(df["Subject code"] != '1') & (df['CIB Category'].str.contains('proprietorship', case=False))]

    total_limit = 0
    total_outstanding = 0
    if not df.empty:
        df = df[df['Phase'] == 'Living']
        df = df[df['Is Funded'] == 'No']
        for i, row in df.iterrows():
            response.append({
                "Nature of Facility": row['Facility Type'],
                "Name of The Concern": row["Name"],
                "Concerns Trade Name": row["Concerns Trade Name"],
                "Limit": convertToMillion(row["Limit"]),
                "Outstanding": convertToMillion(row["Outstanding"]),
                "Start Date": convertToString(row["Start Date"]).replace(" 00:00:00", ""),
                "End Date of Contract": convertToString(row["End Date of Contract"]).replace(" 00:00:00", ""),
                "Default": row["Default"]
            })
            total_limit += convertToMillion(row["Limit"])
            total_outstanding += convertToMillion(row["Outstanding"])

        response.append({
            "Name of The Concern": 'Sub Total',
            "Nature of Facility": '',
            "Concerns Trade Name": '',
            "Limit": total_limit,
            "Outstanding": total_outstanding,
            "Start Date": '',
            "End Date of Contract": '',
            "Default": ''
        })
    return response


def getSummaryOfFacilities(df):
    if df.empty:
        funded = return_empty_result('B - Summary of Facilities : Funded')
        non_funded = return_empty_result('B - Summary of Facilities : Non Funded')
        return {"Summary of funded facility": funded,
                "Summary of non funded facility": non_funded}
    response = {}
    summary_of_funded_facility = {}
    summary_of_non_funded_facility = {}
    summary_funded_facility = []
    summary_non_funded_facility = []
    for cib_type in df['CIB Category'].unique():
        temp_df = df[df['CIB Category'] == cib_type]
        # summary_of_funded_facility[cib_type] = getSummaryOfFundedFacility(temp_df)
        summary_funded_facility = getSummaryOfFundedFacility(temp_df)
        summary_non_funded_facility = getSummaryOfNonFundedFacility(temp_df)
        for each in summary_funded_facility:
            each['CIB Type'] = cib_type
        # summary_of_non_funded_facility[cib_type] = getSummaryOfNonFundedFacility(temp_df)
        for each in summary_non_funded_facility:
            each['CIB Type'] = cib_type


    # a = []
    # b = []
    # for key, val in summary_of_funded_facility['Concerns of primary borrower with PBL'][0].items():
    #     fun = {}
    #     fun['label'] = key
    #     fun['key'] = key
    #     a.append(fun)
    # for key, val in summary_of_non_funded_facility['Concerns of primary borrower with PBL'][0].items():
    #     fun = {}
    #     fun['label'] = key
    #     fun['key'] = key
    #     b.append(fun)
    columns_funded = [
        {
            'label': 'CIB Type',
            'key': 'CIB Type'
        },
        {
            'label': 'SL',
            'key': 'SL'
        },
        {
            'label': 'Nature of Facility',
            'key': 'Nature of Facility'
        },
        {
            'label': 'Name of the Concern',
            'key': 'Name of the Concern'
        },
        {
            'label': 'Installment Type',
            'key': 'Installment Type'
        },
        {
            'label': 'Limit',
            'key': 'Limit'
        },
        {
            'label': 'Outstanding',
            'key': 'Outstanding'
        },
        {
            'label': 'Overdue',
            'key': 'Overdue'
        },
        {
            'label': 'Start Date',
            'key': 'Start Date'
        },
        {
            'label': 'End Date of Contract',
            'key': 'End Date of Contract'
        },
        {
            'label': 'Installment Amount',
            'key': 'Installment Amount'
        },
        {
            'label': 'Payment Period',
            'key': 'Payment Period'
        },
        {
            'label': 'Total No. of Installment',
            'key': 'Total No. of Installment'
        },
        {
            'label': 'Total no. of Installment paid',
            'key': 'Total no. of Installment paid'
        },
        {
            'label': 'No. of Remaining Installment',
            'key': 'No. of Remaining Installment'
        },
        {
            'label': 'Date of Last Payment',
            'key': 'Date of Last Payment'
        },
        {
            'label': 'NPI',
            'key': 'NPI'
        },
        {
            'label': 'Default',
            'key': 'Default'
        }
    ]
    columns_nonfunded = [
        {
            'label': 'CIB Type',
            'key': 'CIB Type'
        },
        {
            'label': 'Nature of Facility',
            'key': 'Nature of Facility'
        },
        {
            'label': 'Limit',
            'key': 'Limit'
        },
        {
            'label': 'Outstanding',
            'key': 'Outstanding'
        },
        {
            'label': 'Start Date',
            'key': 'Start Date'
        },
        {
            'label': 'End Date of Contract',
            'key': 'End Date of Contract'
        },
        {
            'label': 'Default',
            'key': 'Default'
        }
    ]
    final_data_funded = {
        "title": "B - Summary of Facilities : Funded",
        "columns": columns_funded,
        "data": summary_funded_facility
    }
    final_data_non_funded = {
        "title": "B - Summary of Facilities : Non Funded",
        "columns": columns_nonfunded,
        "data": summary_non_funded_facility
    }

    response['Summary of funded facility'] = final_data_funded
    response['Summary of non funded facility'] = final_data_non_funded
    return response


def getSummaryOfFacilitiesConcern(df):
    if df.empty:
        funded = return_empty_result('B1 - Summary of Facilities for Concerns : Funded')
        non_funded = return_empty_result('B1 - Summary of Facilities for Concerns : Non Funded')
        return {"Summary of funded facility": funded,
                "Summary of non funded facility": non_funded}
    response = {}
    summary_of_funded_facility_concern = {}
    summary_of_non_funded_facility_concern = {}
    summary_funded_facility = []
    summary_non_funded_facility = []
    for cib_type in df['CIB Category'].unique():
        temp_df = df[df['CIB Category'] == cib_type]
        # summary_of_funded_facility_concern[cib_type] = getSummaryOfFundedFacilityConcern(temp_df)
        # summary_of_non_funded_facility_concern[cib_type] = getSummaryOfNonFundedFacilityConcern(temp_df)
        summary_funded_facility = getSummaryOfFundedFacilityConcern(temp_df)
        summary_non_funded_facility = getSummaryOfNonFundedFacilityConcern(temp_df)
        for each in summary_funded_facility:
            each['CIB Type'] = cib_type
        # summary_of_non_funded_facility[cib_type] = getSummaryOfNonFundedFacility(temp_df)
        for each in summary_non_funded_facility:
            each['CIB Type'] = cib_type
    columns_funded=[]
    columns_nonfunded = []

    #
    if len(summary_funded_facility)!=0:
        for key, val in summary_funded_facility[0].items():
            fun = {}
            fun['label'] = key
            fun['key'] = key
            columns_nonfunded.append(fun)
    if len(summary_non_funded_facility)!=0:
        for key, val in summary_non_funded_facility[0].items():
            fun = {}
            fun['label'] = key
            fun['key'] = key
            columns_nonfunded.append(fun)
    #
    #
    final_data_funded = {
        "title": "B1 - Summary of Facilities for Concerns : Funded",
        "columns": columns_funded,
        "data": summary_funded_facility
    }
    final_data_non_funded = {
        "title": "B1 - Summary of Facilities for Concerns : Non Funded",
        "columns": columns_nonfunded,
        "data": summary_non_funded_facility
    }

    response['Summary of funded facility'] = final_data_funded
    response['Summary of non funded facility'] = final_data_non_funded
    return response


def getSummaryOfRescheduleLoan(df, role):
    if df.empty:
        return return_empty_result("C - Summary of Reschedule Loan : "+role[0])
    response = []
    df = df[(df['Reschedule Type'] != "Not Rescheduled") & df['Role'].isin(role)]
    is_proprietorship = df['CIB Category'].str.contains('proprietorship', case=False)
    df = df[
        (is_proprietorship & (df['Subject code'] == '1')) |
        (~is_proprietorship)
        ]
    if not df.empty:
        for i, row in df.iterrows():
            response.append({
                "Category": row['CIB Category'],
                "Name of Account": row["Name"],
                "Nature of Facility": row['Facility Type'],
                "Type of Reschedule": convertToString(row['Reschedule Type']),
                "Expiry of Reschedule Loan": convertToString(row['End Date of Contract']).replace(" 00:00:00", ""),
                "Amount": convertToFloat(row['Total Disbursement Amount']),
                "Overdue": convertToFloat(row['Overdue']),
                "Outstanding": convertToFloat(row['Outstanding']),
                "Latest CL Status": convertToFloat(row["CL Status"]),
                "Date of Last Rescheduling": convertToString(row['Last Date of Reschedule']).replace(" 00:00:00", ""),
                "Link": row['CIB Link']
            })
        response_df = pd.DataFrame(response)
        CIBCategorySet = list(set(response_df.Category))
        result_df = pd.DataFrame()
        for cat in CIBCategorySet:
            temp_df = response_df[response_df['Category'] == cat]
            temp_df = temp_df.fillna(0)
            amount_sum = temp_df['Amount'].sum()
            overdue_sum = temp_df["Overdue"].sum()
            outstanding_sum = temp_df['Outstanding'].sum()
            new_row = [{
                'Category': 'Sub Total',
                'Name of Account': '-',
                'Nature of Facility': '-',
                'Type of Reschedule': '-',
                'Expiry of Reschedule Loan': '-',
                'Amount': convertToFloat(amount_sum),
                "Overdue": convertToFloat(overdue_sum),
                'Outstanding': convertToFloat(outstanding_sum),
                'Latest CL Status': '-',
                'Date of Last Rescheduling': '-',
                'Link': '-'
            }]
            new_row_df = pd.DataFrame(new_row)
            # Append the new row to the DataFrame
            temp_df = pd.concat([temp_df, new_row_df])
            result_df = pd.concat([result_df, temp_df])

        result_json = result_df.to_dict('records')

        if len(response) > 0:
            result_json.append({
                "Category": "Grand Total",
                "Name of Account": '',
                "Nature of Facility": '',
                "Type of Reschedule": "-",
                "Expiry of Reschedule Loan": "-",
                "Amount": convertToFloat(df['Total Disbursement Amount'].sum()),
                "Overdue": convertToFloat(df['Overdue']),
                "Outstanding": convertToFloat(df['Outstanding'].sum()),
                'Latest CL Status': '-',
                "Date of Last Rescheduling": "-",
                "Link": "-"
            })
        columns = []
        if len(result_json) != 0:
            for key, val in result_json[0].items():
                temp_dict = {}
                temp_dict['label'] = key
                temp_dict['key'] = key
                columns.append(temp_dict)

        final_data = {
            "title": "C - Summary of Reschedule Loan : "+role[0],
            "columns": columns,
            "data": result_json
        }
        return final_data

    return return_empty_result("C - Summary of Reschedule Loan : "+role[0])


def getSummaryOfRescheduleLoanConcern(df, role):
    if df.empty:
        return return_empty_result("C1 - Summary of Reschedule Loan for Concerns : "+role[0])
    response = []
    df = df[(df["Subject code"] != '1') & (df['CIB Category'].str.contains('proprietorship', case=False))]

    if not df.empty:
        df = df[(df['Reschedule Type'] != "Not Rescheduled") & df['Role'].isin(role)]
        if not df.empty:
            for i, row in df.iterrows():
                response.append({
                    "Category": row['CIB Category'],
                    "Name of Account": row["Name"],
                    "Concerns Trade Name": row["Concerns Trade Name"],
                    "Nature of Facility": row['Facility Type'],
                    "Type of Reschedule": row['Reschedule Type'],
                    "Expiry of Reschedule Loan": convertToString(row['End Date of Contract']).replace(" 00:00:00", ""),
                    "Amount": convertToFloat(row['Total Disbursement Amount']),
                    "Overdue": convertToFloat(row['Overdue']),
                    "Outstanding": convertToFloat(row['Outstanding']),
                    "Latest CL Status": convertToFloat(row["CL Status"]),
                    "Date of Last Rescheduling": convertToString(row['Last Date of Reschedule']).replace(" 00:00:00",
                                                                                                         ""),
                    "Link": row['CIB Link']
                })
            response_df = pd.DataFrame(response)
            CIBCategorySet = list(set(response_df.Category))
            result_df = pd.DataFrame()
            for cat in CIBCategorySet:
                temp_df = response_df[response_df['Category'] == cat]
                amount_sum = temp_df['Amount'].sum()
                overdue_sum = temp_df["Overdue"].sum()
                outstanding_sum = temp_df['Outstanding'].sum()
                new_row = [{
                    'Category': 'Sub Total',
                    'Name of Account': '-',
                    'Concerns Trade Name': '-',
                    'Nature of Facility': '-',
                    'Type of Reschedule': '-',
                    'Expiry of Reschedule Loan': '-',
                    'Amount': convertToFloat(amount_sum),
                    "Overdue": convertToFloat(overdue_sum),
                    'Outstanding': convertToFloat(outstanding_sum),
                    "Latest CL Status": '-',
                    'Date of Last Rescheduling': '-',
                    'Link': '-'
                }]
                new_row_df = pd.DataFrame(new_row)
                # Append the new row to the DataFrame
                temp_df = pd.concat([temp_df, new_row_df])
                result_df = pd.concat([result_df, temp_df])

            result_json = result_df.to_dict('records')

            if len(response) > 0:
                result_json.append({
                    "Category": 'Grand Total',
                    "Name of Account": '',
                    "Concerns Trade Name": '-',
                    "Nature of Facility": '-',
                    "Type of Reschedule": "-",
                    "Expiry of Reschedule Loan": "-",
                    "Amount": convertToFloat(df['Total Disbursement Amount'].sum()),
                    "Overdue": convertToFloat(df["Overdue"].sum()),
                    "Outstanding": convertToFloat(df['Outstanding'].sum()),
                    "Latest CL Status": '-',
                    "Date of Last Rescheduling": "-",
                    "Link": "-"
                })
                columns = []
                if len(result_json) != 0:
                    for key, val in result_json[0].items():
                        temp_dict = {}
                        temp_dict['label'] = key
                        temp_dict['key'] = key
                        columns.append(temp_dict)

                final_data = {
                    "title": "C1 - Summary of Reschedule Loan for Concerns : "+role[0],
                    "columns": columns,
                    "data": result_json
                }
                return final_data
        final_data = {
            "title": "C1 - Summary of Reschedule Loan for Concerns : "+role[0],
            "columns": [],
            "data": []
        }
        return final_data

    return return_empty_result("C1 - Summary of Reschedule Loan for Concerns : "+role[0])


def getSummaryOfRequestedLoan(cibs):
    response = []
    df = pd.DataFrame()
    for cib in cibs:
        if cib.req_contracts is not None:
            temp_cib = cib.req_contracts
            temp_cib['Role'] = cib.req_contracts["Role"]
            temp_cib['Link'] = PDF_LINK + cib.pdf_name
            temp_cib['CIB Category'] = getCIBCategory(cib)
            is_proprietorship = temp_cib['CIB Category'].str.contains('proprietorship', case=False)
            temp_cib = temp_cib[
                (is_proprietorship & (temp_cib['CIB subject code'] == cib.subject_info['CIB subject code'])) |
                (~is_proprietorship)
                ]
            df = pd.concat([df, temp_cib])
    Flag = False
    for i, row in df.iterrows():
        response.append({
            "Category": convertToString(row['CIB Category']).replace(" 00:00:00", ""),
            "Type of Loan": convertToString(row['Type of Contract']).replace(" 00:00:00", ""),
            "Facility": convertToString(row['Facility']).replace(" 00:00:00", ""),
            "Role": convertToString(row['Role']).replace(" 00:00:00", ""),
            "Requested Amount": convertToMillion(row['Total Requested Amount']),
            "Date of Request": convertToString(row['Request date']).replace(" 00:00:00", ""),
            "Link": convertToString(row['Link'])
        })

        Flag = True
    if len(response) != 0:
        response.append({
            "Category": '',
            "Type of Loan": '',
            "Facility": 'Sub Total',
            "Role": '',
            "Requested Amount": convertToMillion(df['Total Requested Amount'].sum() if Flag == True else " "),
            "Date of Request": '',
            "Link": ''
        })
    columns = []
    if len(response) != 0:
        for key, val in response[0].items():
            temp_dict = {}
            temp_dict['label'] = key
            temp_dict['key'] = key
            columns.append(temp_dict)

    final_data = {
        "title": "D - Summary of Requested Loan",
        "columns": columns,
        "data": response
    }
    return final_data


def getSummaryOfRequestedLoanConcern(cibs):
    response = []
    df = pd.DataFrame()
    for cib in cibs:
        if (cib.linked_prop_list and cib.req_contracts is not None) and (cib.cib_category in ['Type j', 'Type k']):
            temp_cib = cib.req_contracts.copy()  # Make a copy of the DataFrame
            temp_cib['Role'] = cib.req_contracts["Role"]
            temp_cib['Link'] = PDF_LINK + cib.pdf_name
            temp_cib['CIB Category'] = getCIBCategory(cib)
            subject_codes = extract_subject_code(cib.linked_prop_list)
            trade_names_dict = extract_trade_names_Code(cib.linked_prop_list)

            for subject_code in subject_codes:
                trade_name = trade_names_dict.get(subject_code, None)
                if trade_name is not None:
                    # Filter rows based on subject code
                    temp_cib.loc[temp_cib['CIB subject code'] == subject_code, 'Concerns Trade Name'] = trade_name

            df = pd.concat([df, temp_cib])
    flag = False
    if not df.empty:
        for i, row in df.iterrows():
            response.append({
                "Category": convertToString(row['CIB Category']).replace(" 00:00:00", ""),
                "Concerns Trade Name": convertToString(row["Concerns Trade Name"]),
                "Type of Loan": convertToString(row['Type of Contract']).replace(" 00:00:00", ""),
                "Facility": convertToString(row['Facility']).replace(" 00:00:00", ""),
                "Role": convertToString(row['Role']).replace(" 00:00:00", ""),
                "Requested Amount": convertToMillion(row['Total Requested Amount']),
                "Date of Request": convertToString(row['Request date']).replace(" 00:00:00", ""),
                "Link": convertToString(row['Link'])
            })
        flag = True
    if len(response) != 0:
        response.append({
            "Category": '',
            "Concerns Trade Name": '',
            "Type of Loan": '',
            "Facility": 'Sub Total',
            "Role": '',
            "Requested Amount": convertToMillion(df['Total Requested Amount'].sum() if flag == True else ""),
            "Date of Request": '',
            "Link": ''
        })
    columns = []
    if len(response) != 0:
        for key, val in response[0].items():
            temp_dict = {}
            temp_dict['label'] = key
            temp_dict['key'] = key
            columns.append(temp_dict)

    final_data = {
        "title": "D1 - Summary of Requested Loan for Concern",
        "columns": columns,
        "data": response
    }
    return final_data


def getSummaryOfStayOrder(df, role):
    if df.empty:
        return return_empty_result("E - Summary of Stay Order : "+role[0])
    df = df[df['Role'].isin(role) & (df['Is Stay Order'] == "Yes")]
    is_proprietorship = df['CIB Category'].str.contains('proprietorship', case=False)
    df = df[
        (is_proprietorship & (df['Subject code'] == '1')) |
        (~is_proprietorship)
        ]
    response = []
    for i, row in df.iterrows():
        response.append({
            "Name of account": row['Name'],
            "Nature of facility": row['Facility Type'],
            "Stayorder amount": convertToMillion(row['Stay Order Amount']),
            "Writ no": row["Stay Order"],
            "Remarks": row['Remarks'],
            "Link": row['CIB Link']
        })

    if len(response)!=0:
        response.append({
            "Name of account": '',
            "Nature of facility": 'Grand Total',
            "Stayorder amount": convertToMillion(df['Stay Order Amount'].sum()),
            "Writ no": '',
            "Remarks": '',
            "Link": ''
        })
    columns = []
    if len(response) != 0:
        for key, val in response[0].items():
            temp_dict = {}
            temp_dict['label'] = key
            temp_dict['key'] = key
            columns.append(temp_dict)

    final_data = {
        "title": "E - Summary of Stay Order : "+role[0],
        "columns": columns,
        "data": response
    }
    return final_data


def getSummaryOfStayOrderConcern(df, role):
    if df.empty:
        return return_empty_result("E1 - Summary of Stay Order for Concern : "+role[0])
    df = df[(df["Subject code"] != '1') & (df['CIB Category'].str.contains('proprietorship', case=False))]
    response = []
    if not df.empty:
        df = df[df['Role'].isin(role) & (df['Is Stay Order'] == "Yes")]
        for i, row in df.iterrows():
            response.append({
                "Name of account": row['Name'],
                "Concerns Trade Name": convertToString(row["Concerns Trade Name"]),
                "Nature of facility": row['Facility Type'],
                "Stayorder amount": convertToFloat(row['Stay Order Amount']),
                "Writ no": row["Stay Order"],
                "Remarks": row['Remarks'],
                "Link": row['CIB Link']
            })
        response.append({
            "Name of account": '',
            "Concerns Trade Name": '',
            "Nature of facility": 'Grand Total',
            "Stayorder amount": convertToFloat(df['Stay Order Amount'].sum()),
            "Writ no": '',
            "Remarks": '',
            "Link": ''
        })
        columns = []
        if len(response) != 0:
            for key, val in response[0].items():
                temp_dict = {}
                temp_dict['label'] = key
                temp_dict['key'] = key
                columns.append(temp_dict)

        final_data = {
            "title": "E1 - Summary of Stay Order for Concern : "+role[0],
            "columns": columns,
            "data": response
        }
        return final_data
    if len(response)!=0:
        response.append({
            "Name of account": '',
            "Concerns Trade Name": '',
            "Nature of facility": 'Grand Total',
            "Stayorder amount": convertToFloat(df['Stay Order Amount'].sum()),
            "Writ no": '',
            "Remarks": '',
            "Link": ''
        })

    return return_empty_result("E1 - Summary of Stay Order for Concern : "+role[0])


def getSummaryOfExpiredButShowingLiveFunded(df):
    if df.empty:
        return return_empty_result("F - Expired Loan But Showing Live : Funded")
    try:
        df = df[df['Is Funded'] == "Yes"]
        df = df[df['Phase'] == 'Living']
        df = df[(pd.to_datetime(df['Outstanding Zero Date'], errors='coerce') < pd.to_datetime(
            df['End Date of Contract'], errors='coerce')) | (
                        pd.to_datetime(df["Outstanding Date"], errors='coerce') > pd.to_datetime(
                    df['End Date of Contract'], errors='coerce'))]
    except pd.errors.OutOfBoundsDatetime:
        # Handle OutOfBoundsDatetime error
        print("Error: OutOfBoundsDatetime encountered during datetime conversion.")
        return []

    is_proprietorship = df['CIB Category'].str.contains('proprietorship', case=False)
    df = df[(is_proprietorship & (df['Subject code'] == '1')) | (~is_proprietorship)]

    installment = df[df['Installment Type'] == 'Installment']
    non_installment = df[df['Installment Type'] == 'No Installment']
    response = []

    for i, row in installment.iterrows():
        response.append(getSummaryOfExpiredButShowingLiveFields(row, i, True))

    if installment.shape[0] > 0:
        response.append(getSummaryOfExpiredButShowingLiveFundedSum(installment, 'Sub Total', "Installment"))

    for i, row in non_installment.iterrows():
        response.append(getSummaryOfExpiredButShowingLiveFields(row, i, False))

    if non_installment.shape[0] > 0:
        response.append(getSummaryOfExpiredButShowingLiveFundedSum(non_installment, 'Sub Total', "Non-Installment"))

    total_df = pd.DataFrame(response)

    if not total_df.empty:
        total_df = total_df[total_df["Nature of Facility"] == 'Sub Total']
        response.append(getSummaryOfExpiredButShowingLiveFundedTotalSum("Grand Total", total_df))

    columns = [
        {
            'label': 'Nature of Facility',
            'key': 'Nature of Facility'
        },
        {
            'label': 'Limit',
            'key': 'Limit'
        },
        {
            'label': 'Outstanding',
            'key': 'Outstanding'
        },
        {
            'label': 'Overdue',
            'key': 'Overdue'
        },
        {
            'label': 'Start Date',
            'key': 'Start Date'
        },
        {
            'label': 'End Date of Contract',
            'key': 'End Date of Contract'
        },
        {
            'label': 'Installment Amount',
            'key': 'Installment Amount'
        },
        {
            'label': 'Payment Period',
            'key': 'Payment Period'
        },
        {
            'label': 'Total No of Installment',
            'key': 'Total No of Installment'
        },
        {
            'label': 'Total No of Installment paid',
            'key': 'Total No of Installment paid'
        },
        {
            'label': 'No of Remaining Installment',
            'key': 'No of Remaining Installment'
        },
        {
            'label': 'Date of Last Payment',
            'key': 'Date of Last Payment'
        },
        {
            'label': 'NPI',
            'key': 'NPI'
        },
        {
            'label': 'Default',
            'key': 'Default'
        }
    ]
    final_data = {
        "title": "F - Expired Loan But Showing Live : Funded",
        "columns": columns,
        "data": response
    }
    return final_data


def getSummaryOfExpiredButShowingLiveFundedConcern(df):
    if df.empty:
        return return_empty_result("F1 - Expired Loan But Showing Live for Concern : Funded")

    # Filter out rows with 'Subject code' as '1' and containing 'proprietorship' in 'CIB Category'
    df = df[(df["Subject code"] != '1') & (df['CIB Category'].str.contains('proprietorship', case=False))]
    response = []

    if not df.empty:
        try:
            # Filter rows for funded, living, and expired contracts
            df = df[df['Is Funded'] == "Yes"]
            df = df[df['Phase'] == 'Living']
            df = df[(pd.to_datetime(df['Outstanding Zero Date'], errors='coerce') < pd.to_datetime(
                df['End Date of Contract'], errors='coerce')) | (
                            pd.to_datetime(df["Outstanding Date"], errors='coerce') > pd.to_datetime(
                        df['End Date of Contract'], errors='coerce'))]
        except pd.errors.OutOfBoundsDatetime:
            # Handle OutOfBoundsDatetime error
            print("Error: OutOfBoundsDatetime encountered during datetime conversion.")
            return []

        installment = df[df['Installment Type'] == 'Installment']
        non_installment = df[df['Installment Type'] == 'No Installment']

        for i, row in installment.iterrows():
            response.append(getSummaryOfExpiredButShowingLiveFieldsConcern(row, i, True))

        if installment.shape[0] > 0:
            response.append(getSummaryOfExpiredButShowingLiveFundedConcernSum(installment, 'Sub Total', "Installment"))

        for i, row in non_installment.iterrows():
            response.append(getSummaryOfExpiredButShowingLiveFieldsConcern(row, i, False))

        if non_installment.shape[0] > 0:
            response.append(
                getSummaryOfExpiredButShowingLiveFundedConcernSum(non_installment, 'Sub Total', "Non-Installment"))

        total_df = pd.DataFrame(response)

        if not total_df.empty:
            total_df = total_df[total_df["Nature of Facility"] == 'Sub Total']
            response.append(getSummaryOfExpiredButShowingLiveFundedConcernTotalSum("Grand Total", total_df))

    columns= []
    if len(response)!=0:
        for key, val in response[0].items():
            fun = {}
            fun['label'] = key
            fun['key'] = key
            columns.append(fun)

    final_data = {
        "title": "F1 - Expired Loan But Showing Live for Concern : Funded",
        "columns": columns,
        "data": response
    }
    return final_data


def getSummaryOfExpiredButShowingLiveNonFunded(df):
    if df.empty:
        return return_empty_result("F - Expired Loan But Showing Live : Non Funded")
    try:
        df = df[df['Is Funded'] != "Yes"]
        df = df[df['Phase'] == 'Living']
        df = df[(pd.to_datetime(df['Outstanding Zero Date'], errors='coerce') < pd.to_datetime(
            df['End Date of Contract'], errors='coerce')) | (
                        pd.to_datetime(df["Outstanding Date"], errors='coerce') > pd.to_datetime(
                    df['End Date of Contract'], errors='coerce'))]
    except pd.errors.OutOfBoundsDatetime:
        # Handle OutOfBoundsDatetime error
        print("Error: OutOfBoundsDatetime encountered during datetime conversion.")
        return []

    is_proprietorship = df['CIB Category'].str.contains('proprietorship', case=False)
    df = df[(is_proprietorship & (df['Subject code'] == '1')) | (~is_proprietorship)]

    response = []
    total_limit = 0
    total_outstanding = 0
    total_overdue = 0

    for i, row in df.iterrows():
        response.append({
            "Nature of Facility": row['Facility Type'],
            "Limit": convertToMillion(row['Limit']),
            "Outstanding": convertToMillion(row['Outstanding']),
            "Overdue": convertToMillion(row['Overdue']),
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
    # a = []
    # for key, val in response[0].items():
    #     fun = {}
    #     fun['label'] = key
    #     fun['key'] = key
    #     a.append(fun)
    columns = [
        {
            'label': 'Nature of Facility',
            'key': 'Nature of Facility'
        },
        {
            'label': 'Limit',
            'key': 'Limit'
        },
        {
            'label': 'Outstanding',
            'key': 'Outstanding'
        },
        {
            'label': 'Overdue',
            'key': 'Overdue'
        },
        {
            'label': 'Start Date',
            'key': 'Start Date'
        },
        {
            'label': 'End Date of Contract',
            'key': 'End Date of Contract'
        },
        {
            'label': 'Default',
            'key': 'Default'
        }
    ]
    final_data = {
        "title": "F - Expired Loan But Showing Live : Non Funded",
        "columns": columns,
        "data": response
    }
    return final_data


def getSummaryOfExpiredButShowingLiveNonFundedConcern(df):
    if df.empty:
        return return_empty_result("F1 - Expired Loan But Showing Live for Concern : Non Funded")

    # Filter out rows with 'Subject code' as '1' and containing 'proprietorship' in 'CIB Category'
    df = df[(df["Subject code"] != '1') & (df['CIB Category'].str.contains('proprietorship', case=False))]

    if df.empty:
        return return_empty_result("F1 - Expired Loan But Showing Live for Concern : Non Funded")

    try:
        # Filter rows for non-funded, living, and expired contracts
        df = df[df['Is Funded'] != "Yes"]
        df = df[df['Phase'] == 'Living']
        df = df[(pd.to_datetime(df['Outstanding Zero Date'], errors='coerce') < pd.to_datetime(
            df['End Date of Contract'], errors='coerce')) | (
                        pd.to_datetime(df["Outstanding Date"], errors='coerce') > pd.to_datetime(
                    df['End Date of Contract'], errors='coerce'))]
    except pd.errors.OutOfBoundsDatetime:
        # Handle OutOfBoundsDatetime error
        print("Error: OutOfBoundsDatetime encountered during datetime conversion.")
        return return_empty_result("F1 - Expired Loan But Showing Live for Concern : Non Funded")

    response = []
    total_limit = 0
    total_outstanding = 0
    total_overdue = 0

    for i, row in df.iterrows():
        response.append({
            "Concerns Trade Name": row["Concern's Trade Name"],
            "Nature of Facility": row['Facility Type'],
            "Limit": convertToMillion(row['Limit']),
            "Outstanding": convertToMillion(row['Outstanding']),
            "Overdue": convertToMillion(row['Overdue']),
            "Start Date": convertToString(row['Start Date']).replace(" 00:00:00", ""),
            "End Date of Contract": convertToString(row['End Date of Contract']).replace(" 00:00:00", ""),
            "Default": row['Default']
        })
        total_limit += convertToMillion(row["Limit"])
        total_outstanding += convertToMillion(row["Outstanding"])
        total_overdue += convertToMillion(row['Overdue'])
    if len(response)!=0:
        response.append({
            "Concerns Trade Name": "Sub Total",
            "Nature of Facility": " ",
            "Limit": total_limit,
            "Outstanding": total_outstanding,
            "Overdue": total_overdue,
            "Start Date": ' ',
            "End Date of Contract": ' ',
            "Default": "Yes" if "Yes" in set(df['Default'].tolist()) else "No"
        })
    columns = []
    if len(response) != 0:
        for key, val in response[0].items():
            temp_dict = {}
            temp_dict['label'] = key
            temp_dict['key'] = key
            columns.append(temp_dict)

    final_data = {
        "title": "F1 - Expired Loan But Showing Live for Concern : Non Funded",
        "columns": columns,
        "data": response
    }

    return final_data


def getCorporateDashboard(cibs):
    response = {}
    df = getCorporateDataFrame(cibs)

    response['analysis type'] = "Corporate"
    summary_table_1 = {
        'tabName': 'Summary Table - 1',
        'tables': [getSummaryTable(cibs),getSummaryTableConcern(cibs)]
    }
    terminated_facility = {
        'tabName': 'Summary of Terminated Facilities',
        'tables': [getSummaryOfTerminatedFacilityFunded(df),getSummaryOfTerminatedFacilityNonFunded(df),
                   getSummaryOfTerminatedFacilityFundedConcern(df),getSummaryOfTerminatedFacilityNonFundedConcern(df)]
    }
    summary_facilities = {
        'tabName': 'Summary of Facilities',
        'tables': [getSummaryOfFacilities(df)['Summary of funded facility'],getSummaryOfFacilities(df)['Summary of non funded facility'],
                   getSummaryOfFacilitiesConcern(df)['Summary of funded facility'],getSummaryOfFacilitiesConcern(df)['Summary of non funded facility']]

    }
    rescheduled_loan = {
        'tabName': 'Summary of Reschedule Loan',
        'tables': [getSummaryOfRescheduleLoan(df, BORROWER),getSummaryOfRescheduleLoan(df, GUARANTOR),
                   getSummaryOfRescheduleLoanConcern(df, BORROWER),getSummaryOfRescheduleLoanConcern(df, GUARANTOR)]
    }
    requested_loan = {
        'tabName': 'Summary of Requested Loan',
        'tables': [getSummaryOfRequestedLoan(cibs),getSummaryOfRequestedLoanConcern(cibs)]
    }
    summary_stay_order = {
        'tabName': 'Summary of Stay Order',
        'tables' : [getSummaryOfStayOrder(df, BORROWER),getSummaryOfStayOrder(df, GUARANTOR),
                    getSummaryOfStayOrderConcern(df, BORROWER),getSummaryOfStayOrderConcern(df, GUARANTOR)]
    }
    expired_loan = {
        'tabName': 'Expired Loan But Showing Live',
        'tables': [getSummaryOfExpiredButShowingLiveFunded(df),getSummaryOfExpiredButShowingLiveNonFunded(df),
                   getSummaryOfExpiredButShowingLiveFundedConcern(df),getSummaryOfExpiredButShowingLiveNonFundedConcern(df)]
    }

    summary_table_2 = {
        'tabName': 'Summary Table - 2',
        'tables': [getSummaryTableTwo(df),getSummaryTableTwoConcern(df)]
    }
    summary_table_3 = {
        'tabName': 'Summary Table - 3',
        'tables': [getSummaryTableThree(df)['funded'],getSummaryTableThree(df)['non_funded'],
                   getSummaryTableThreeConcern(df)['funded'],getSummaryTableThreeConcern(df)['non_funded']]
    }

    final = []
    final.append(summary_table_1)
    final.append(terminated_facility)
    final.append(summary_facilities)
    final.append(rescheduled_loan)
    final.append(requested_loan)
    final.append(summary_stay_order)
    final.append(expired_loan)
    final.append(summary_table_2)
    final.append(summary_table_3)

    response['dashboardData'] = final
    # response['Summary Table - 1 for Proprietorship Concern'] = getSummaryTableConcern(cibs)
    # response['A - Summary of Terminated Facilities'] = {
    #     "Funded": getSummaryOfTerminatedFacilityFunded(df),
    #     "Non Funded": getSummaryOfTerminatedFacilityNonFunded(df)
    # }
    # response['A1 - Summary of Terminated Facilities for Concerns'] = {
    #     "Funded": getSummaryOfTerminatedFacilityFundedConcern(df),
    #     "Non Funded": getSummaryOfTerminatedFacilityNonFundedConcern(df)
    # }
    # response['B - Summary of Facilities'] = getSummaryOfFacilities(df)
    # response['B1 - Summary of Facilities for Concerns'] = getSummaryOfFacilitiesConcern(df)
    # response['C - Summary of Reschedule Loan'] = {
    #     "Borrower": getSummaryOfRescheduleLoan(df, BORROWER),
    #     "Guarantor": getSummaryOfRescheduleLoan(df, GUARANTOR)
    # }
    # response['C1 - Summary of Reschedule Loan for Concerns'] = {
    #     "Borrower": getSummaryOfRescheduleLoanConcern(df, BORROWER),
    #     "Guarantor": getSummaryOfRescheduleLoanConcern(df, GUARANTOR)
    # }
    # response['D - Summary of Requested Loan'] = getSummaryOfRequestedLoan(cibs)
    # response['D1 - Summary of Requested Loan for Concern'] = getSummaryOfRequestedLoanConcern(cibs)

    # response['E - Summary of Stay Order'] = {
    #     "Borrower": getSummaryOfStayOrder(df, BORROWER),
    #     "Guarantor": getSummaryOfStayOrder(df, GUARANTOR)
    # }
    # response['E1 - Summary of Stay Order for Concern'] = {
    #     "Borrower": getSummaryOfStayOrderConcern(df, BORROWER),
    #     "Guarantor": getSummaryOfStayOrderConcern(df, GUARANTOR)
    # }
    # response['F - Expired Loan But Showing Live'] = {
    #     "Summary of Funded Facility": getSummaryOfExpiredButShowingLiveFunded(df),
    #     "Summary of Non Funded Facility": getSummaryOfExpiredButShowingLiveNonFunded(df),
    # }
    #
    # response['F1 - Expired Loan But Showing Live for Concern'] = {
    #     "Summary of Funded Facility": getSummaryOfExpiredButShowingLiveFundedConcern(df),
    #     "Summary of Non Funded Facility": getSummaryOfExpiredButShowingLiveNonFundedConcern(df),
    # }
    # response['Summary Table - 2'] = getSummaryTableTwo(df)
    # response['Summary Table - 2 for Concern'] = getSummaryTableTwoConcern(df)
    # response['Summary Table - 3'] = getSummaryTableThree(df)
    # response['Summary Table - 3 for Concern'] = getSummaryTableThreeConcern(df)

    return response
