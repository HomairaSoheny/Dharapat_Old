# from msilib.schema import tables


# from pandas.plotting import table

from utils.general_helper import convertToString
from dashboard.engines.consumer_engine import getConsumerDataFrame, getNID, getFathersName
from dashboard.engines.general_engine import getBorrowersName, getClassFromSet
from dashboard.engines.columns import *
from dashboard.engines.keywords import *

def tableFilter(df, facility_type, phase, role, columns, exclude_facility_type = False, exclude_phase = False, check_business = False, table_name=None):
    response = []
    
    df = df[~df["Business"].isin(["No"])] if check_business else df[df["Business"].isin(["No"])]
    df = df[~df["Facility Type"].isin(facility_type)] if exclude_facility_type else df[df["Facility Type"].isin(facility_type)]
    df = df[~df["Phase"].isin(phase)] if exclude_phase else df[df["Phase"].isin(phase)]
    df = df[df["Role"].isin(role)]
    
    if df.shape[0] == 0:
        final_data = {
            "title": table_name,
            "columns": [],
            "data": []
        }
        return final_data
    
    for i, row in df[columns].iterrows():
        analysis_dict = {}
        row_dict = row.to_dict()
        for key in row_dict:
            analysis_dict[key] = convertToString(row_dict[key])
        response.append(analysis_dict)
    columns = []
    if len(response) != 0:
        for key,val in response[0].items():
            temp_dict = {}
            temp_dict['label'] = key
            temp_dict['key'] = key
            columns.append(temp_dict)

    final_data = {
        "title": table_name,
        "columns": columns,
        "data": response
    }
        
    return final_data

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

        term_loan_borrower_living = tableFilter(df=df, facility_type=TERM_LOAN, phase=["Living"], role=BORROWER, columns=TERM_LOAN_COLUMNS, table_name="Term Loan"),

        # credit_facility_live_borrower = {
        #     'tabName': 'Summary of Consumer',
        #     'tables': [term_loan_borrower_living]
        # }
        #
        # analysis['dashboardData'] = credit_facility_live_borrower
        analysis["Credit Facilities as Applicant - Live (As Borrower)"] = {
            "Term Loan": tableFilter(df=df, facility_type=TERM_LOAN, phase=["Living"], role=BORROWER, columns=TERM_LOAN_COLUMNS, table_name="Credit Facilities as Applicant - Live (As Borrower) - Term Loan"),
            "Credit Card": tableFilter(df=df, facility_type=CREDIT_CARD, phase=["Living"], role=BORROWER, columns=CREDIT_CARD_COLUMNS, table_name="Credit Facilities as Applicant - Live (As Borrower) - Credit Card"),
            "Others": tableFilter(df=df, facility_type=["Term Loan", "Credit Card (Revolving)"], phase=["Living"], role=BORROWER, columns=OTHER_COLUMNS, exclude_facility_type=True,table_name="Credit Facilities as Applicant - Live (As Borrower) - Others"),
            }
        analysis["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"] = {
            "Term Loan": tableFilter(df=df, facility_type=TERM_LOAN, phase=["Living"], role=BORROWER, columns=TERM_LOAN_COLUMNS, exclude_phase=True, table_name="Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower) - Term Loan"),
            "Credit Card": tableFilter(df=df, facility_type=CREDIT_CARD, phase=["Living"], role=BORROWER, columns=CREDIT_CARD_COLUMNS, exclude_phase=True, table_name="Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower) - Credit Card"),
            "Others": tableFilter(df=df, facility_type=["Term Loan", "Credit Card (Revolving)"], phase=["Living"], role=BORROWER, columns=OTHER_COLUMNS, exclude_facility_type=True, exclude_phase=True, table_name="Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower) - Others"),
            }

        analysis["Credit Facilities as Guarantor - Live (As Guarantor)"] = {
            "Term Loan": tableFilter(df=df, facility_type=TERM_LOAN, phase=["Living"], role=["Guarantor"], columns=TERM_LOAN_COLUMNS_FOR_GURANTOR_ROLE, table_name="Credit Facilities as Guarantor - Live (As Guarantor) - Term Loan"),
            "Credit Card": tableFilter(df=df, facility_type=CREDIT_CARD, phase=["Living"], role=["Guarantor"], columns=CREDIT_CARD_COLUMNS, table_name="Credit Facilities as Guarantor - Live (As Guarantor) - Credit Card"),
            "Others": tableFilter(df=df, facility_type=["Term Loan", "Credit Card (Revolving)"], phase=["Living"], role=["Guarantor"], columns=OTHER_COLUMNS, exclude_facility_type=True, table_name="Credit Facilities as Guarantor - Live (As Guarantor) - Others"),
            }

        analysis["Credit Facilities in the Name of Business - Live"] = {
            "Term Loan": tableFilter(df=df, facility_type=TERM_LOAN, phase=["Living"], role=BORROWER, columns=TERM_LOAN_COLUMNS, check_business=True, table_name="Credit Facilities in the Name of Business - Live - Term Loan"),
            "Credit Card": tableFilter(df=df, facility_type=CREDIT_CARD, phase=["Living"], role=BORROWER, columns=CREDIT_CARD_COLUMNS, check_business=True, table_name="Credit Facilities in the Name of Business - Live - Credit Card"),
            "Others": tableFilter(df=df, facility_type=["Term Loan", "Credit Card (Revolving)"], phase=["Living"], role=BORROWER, columns=OTHER_COLUMNS, exclude_facility_type=True, check_business=True, table_name="Credit Facilities in the Name of Business - Live - Others"),
            }
        response.append(analysis)

    final = []
    for each in response:

        credit_facility_live_borrower = {
            'tabName': each["CIB Report of"],
            'tables': [each["Credit Facilities as Applicant - Live (As Borrower)"]['Term Loan'],
                       each["Credit Facilities as Applicant - Live (As Borrower)"]['Credit Card'],
                       each["Credit Facilities as Applicant - Live (As Borrower)"]['Others'],
                       each["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"]['Term Loan'],
                       each["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"]['Credit Card'],
                       each["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"]['Others'],
                       each["Credit Facilities as Guarantor - Live (As Guarantor)"]['Term Loan'],
                       each["Credit Facilities as Guarantor - Live (As Guarantor)"]['Credit Card'],
                       each["Credit Facilities as Guarantor - Live (As Guarantor)"]['Others'],
                       each["Credit Facilities in the Name of Business - Live"]['Term Loan'],
                       each["Credit Facilities in the Name of Business - Live"]['Credit Card'],
                       each["Credit Facilities in the Name of Business - Live"]['Others'],
                       ],
            'cards': [
                {
                    'title': "Basic Information",
                    'data': [
                        {
                            'label': "CIB Name",
                            'value': each['CIB Report of']
                        },
                        {
                            'label': "NID Number",
                            'value': each['NID Number']
                        },
                        {
                            'label': "Fathers Name",
                            'value': each['Fathers Name']
                        },
                        {
                            'label': "No of Living Contracts",
                            'value': each['No of Living Contracts']
                        },
                        {
                            'label': "Total Outstanding",
                            'value': each['Total Outstanding']
                        },
                        {
                            'label': "Total Overdue",
                            'value': each['Total Overdue']
                        },
                        {
                            'label': "Current Status",
                            'value': each['Current Status']
                        },
                        {
                            'label': "Overall Worst Status",
                            'value': each['Overall Worst Status']
                        },
                    ]
                }
            ]
        }
        final.append(credit_facility_live_borrower)
    final_data = {}
    final_data['dashboardData'] = final
    print("response starts ..")
    print(final_data)


    
    return final_data
