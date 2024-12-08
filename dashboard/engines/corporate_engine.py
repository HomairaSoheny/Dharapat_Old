import re
import pandas as pd
from datetime import datetime
from dashboard.engines import general_engine
from dashboard.engines.keywords import *
from utils.general_helper import *
from utils.env import PDF_LINK

def getCIBCategory(cib):
    return CATEGORY_MAPPING.get(cib.cib_category, None)
    
def extract_subject_code(prp_list):
    subject_code= []
    if prp_list is not None:
        for entry in prp_list:
            sub_code = entry['PROPRIETORSHIP CONCERN']['CIB subject code:']
            subject_code.append(sub_code)
        return subject_code
    return subject_code

def extract_trade_names_Code(prp_list):
    trade_names_dict = {}
    if prp_list is not None:
        for entry in prp_list:
            ref_number = entry['PROPRIETORSHIP CONCERN']['CIB subject code:']
            #first_digit = next((char for char in ref_number if char.isdigit()), None)
            # Check if the first digit is '2'
            #ey = ref_number.split('(')[0].strip()  # Extract the key
            trade_name = entry['PROPRIETORSHIP CONCERN']['Trade Name:']
            trade_names_dict[ref_number] = trade_name
        return trade_names_dict
    return trade_names_dict
                 

def getDateOfClassification(fac):
    for key in DATE_OF_CLASSIFICATION:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]
    return ""
def extract_trade_names(prp_list):
    trade_names_dict = {}
    if prp_list is not None:
        for entry in prp_list:
            ref_number = entry['PROPRIETORSHIP CONCERN']['Reference number (Ref.):']
            first_digit = next((char for char in ref_number if char.isdigit()), None)
            # Check if the first digit is '2'
            key = ref_number.split('(')[0].strip()  # Extract the key
            trade_name = entry['PROPRIETORSHIP CONCERN']['Trade Name:']
            trade_names_dict[key] = trade_name
        return trade_names_dict
    return trade_names_dict
                 

def getStartDate(fac):
    for key in STARTING_DATE:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]
    return ""

def getEndDateOfContract(fac):
    for key in END_DATE_OF_CONTRACT:
        if key in fac["Ref"].keys():
            try:
                return pd.Timestamp(fac["Ref"][key])
            except (pd.errors.OutOfBoundsDatetime, ValueError):
                return pd.NaT

    return None

def getRemarks(fac):
    for key in REMARKS:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]
    return ""


def getPaymentPeriod(fac):
    for key in PAYMENT_PERIOD:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]
    return ""


def getTotalNumberOfInstallment(fac):
    for key in TOTAL_NUMBER_OF_INSTALLMENT:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]
    return ""


def getNoOfRemainingInstallment(fac):
    for key in REMAINING_INSTALLMENT_NUMBER:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]
    return ""

def getNoOfInstallmentPaid(fac):
    total = getTotalNumberOfInstallment(fac)
    remaining = getNoOfRemainingInstallment(fac)
    try:
        return  total - remaining
    except:
        return ""


def getDateOfLastPayment(fac):
    for key in DATE_OF_LAST_PAYMENT:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]
    return ""


def getFacilityType(i):
    return FACILITY_CATEGORIES.get(i, "Unknown")


def getFundedOutstandingInstallment(df):
    df = df[df["Is Funded"] == "Yes"]
    df = df[df["Installment Type"] == "Installment"]
    return convertToFloat(df["Outstanding"].sum())


def getFundedOutstandingNonInstallment(df):
    df = df[df["Is Funded"] == "Yes"]
    df = df[df["Installment Type"] == "No Installment"]
    return convertToFloat(df["Outstanding"].sum())


def getFundedOutstandingTotal(df):
    return convertToFloat(getFundedOutstandingInstallment(df) + getFundedOutstandingNonInstallment(df))


def getNonFundedOutstanding(df):
    df = df[df["Is Funded"] == "No"]
    return convertToFloat(df["Outstanding"].sum())


def getTotalOutstanding(df):
    return convertToFloat(getFundedOutstandingTotal(df) + getNonFundedOutstanding(df))


def getOverdue(df):
    return convertToFloat(df["Overdue"].sum())

def getOutstandingZeroDate(fac):
    if 'Contract History' in fac and isinstance(fac['Contract History'], pd.DataFrame):
        for column_name in OUTSTANDING:
            if column_name in fac['Contract History']:
                sorted_contracts = fac['Contract History'].sort_values('Date', ascending=True)
                for index, row in sorted_contracts.iterrows():
                    if row[column_name] == 0:
                        return row['Date']

    return None

def getDaysOfAdjustmentOld(fac):
    try:
        if isStayOrder(fac) == "Yes":
            return ""
        start_date = datetime.strptime(str(getStartDate(fac)).replace(" 00:00:00", ""), "%Y-%M-%d")
        outstanding_start_date = datetime.strptime(str((fac['Contract History']).sort_values('Date', ascending=True)['Date'][0]).replace(" 00:00:00", ""), "%Y-%M-%d")
        return abs((outstanding_start_date - start_date).days)
    except:
        return 0
def getDaysOfAdjustment(fac):
    try:
        if isStayOrder(fac) == "Yes":
            return ""
        end_date = datetime.strptime(str(getEndDateOfContract(fac)).replace(" 00:00:00", ""), "%Y-%M-%d")
        outstanding_start_date = datetime.strptime(str((fac['Contract History']).sort_values('Date', ascending=True)['Date'][0]).replace(" 00:00:00", ""), "%Y-%M-%d")
        days_difference = ((outstanding_start_date - end_date).days)
        # Check if difference is negative and format accordingly
        if days_difference < 0:
            return f"({abs(days_difference)})"  # Return negative value within brackets
        else:
            return str(days_difference)  # Return positive value as string 
    except:
        return 0

def isStayOrder(fac):
    if general_engine.isStayOrder(fac):
        return "Yes"
    return "No"


def getStayOrder(fac):
    if type(fac['Contract History']) == dict:
        return fac['Contract History']['Stay Order']
    return ""
    
    
def getStayOrderAmount(fac):
    for key in STAY_ORDER_AMOUNT:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
    return 0


def getDefault(fac):
    if type(fac['Contract History']) != dict:
        if 'Default' in fac['Contract History'].columns:
            return "Yes" if "Yes" in fac["Contract History"]["Default"].tolist() else "No"
        return "Yes" if "Yes" in fac["Contract History"]["Default & Willful Default"].tolist() else "No"
    return ""

def getTypeOfReschedule(fac):
    for key in RESCHEDULE_LOAN:
        if key in fac['Ref'].keys():
            if fac['Ref'][key] not in [0, "", " ", "-"]:
                return fac['Ref'][key]
    return "Not Rescheduled"

def getRescheduleAmount(fac):
    if getTypeOfReschedule(fac) != "Not Rescheduled":
        return general_engine.getOutstanding(fac)
    return 0

def getDateOfLastReschedule(fac):
    for key in LAST_RESCHEDULING_DATE:
        if key in fac['Ref'].keys():
            return convertToString(fac['Ref'][key]).replace(" 00:00:00", "")
    return "Not Rescheduled"

def getTotalDisbursementAmount(fac):
    for key in TOTAL_DISBURSEMENT_AMOUNT:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]



def calculate_eol(df):
    Overdue = 0 
    for i, row in df.iterrows():
        if row['Overdue'] != 0 :
            Overdue += (row['Overdue'])
        else:
            eol = (df["Limit"] - df["Outstanding"]).sum()
            if eol < 0:
                eol = -eol
                Overdue += eol
    return convertToMillion(Overdue)



def getClassFromSet(classes):
    # Remove empty strings from the set of classes
    non_empty_classes = {c for c in classes if c.strip()}
    
    # If there are no non-empty classes, return an empty string
    if not non_empty_classes:
        return ""
    
    # Iterate through CL_STATUS to find the worst classification
    for classification in CL_STATUS:
        if classification in non_empty_classes:
            return classification
    
    # If no classification matches, return an empty string
    return ""

def getSummaryTableFields(category, concern_name, df):
    stay_order_remarks = ''
    if "Stay Order Remarks" in df.columns:
        unique_remarks = df["Stay Order Remarks"].dropna().unique()
        stay_order_remarks = ', '.join(unique_remarks) if unique_remarks.size > 0 else ' '
    
    worst_cl_status_as_guarantor = ""
    if "Worst CL Status as Guarantor" in df.columns:
        worst_cl_status_as_guarantor = getClassFromSet(set(df["Worst CL Status as Guarantor"]))
    
    return {
        "CIB Category": category,
        "Name of Concern": concern_name,
        "Position Date": df.loc[df['Position Date'] != '', 'Position Date'].max() if not df.loc[df['Position Date'] != '', 'Position Date'].empty else '',
        "Funded Outstanding Installment": convertToFloat(df["Funded Outstanding Installment"].sum()),
        "Funded Outstanding Installment Raw": df["Funded Outstanding Installment"].sum(),
        "Funded Outstanding Non Installment": convertToFloat(df["Funded Outstanding Non Installment"].sum()),
        "Funded Outstanding Non Installment Raw": df["Funded Outstanding Non Installment"].sum(),
        "Funded Outstanding Total": convertToFloat(df["Funded Outstanding Total"].sum()),
        "Funded Outstanding Total Raw": df["Funded Outstanding Total"].sum(),
        "Non-Funded Outstanding": convertToFloat(df["Non-Funded Outstanding"].sum()),
        "Non-Funded Outstanding Raw": df["Non-Funded Outstanding"].sum(),
        "Total Outstanding": convertToFloat(df["Total Outstanding"].sum()),
        "Total Outstanding Raw": df["Total Outstanding"].sum(),
        "Overdue": convertToFloat(df["Overdue"].sum()),
        "Overdue Raw": df["Overdue"].sum(),
        "STD": convertToFloat(df["STD"].sum()),
        "SMA": convertToFloat(df["SMA"].sum()),
        "SS(No)": convertToFloat(df["SS(No)"].sum()),
        "SS(Yes)": convertToFloat(df["SS(Yes)"].sum()),
        "DF": convertToFloat(df["DF"].sum()),
        "BLW": convertToFloat(df["BLW"].sum()),
        "Terminated": convertToFloat(df["Terminated"].sum()),
        "Requested": convertToFloat(df["Requested"].sum()),
        "Stay Order": convertToFloat(df["Stay Order"].sum()),
        "Willful Default(WD)": convertToFloat(df["Willful Default(WD)"].sum()),
        "Willful Default(Appeal)": convertToFloat(df["Willful Default(Appeal)"].sum()),
        "CL Status": general_engine.getClassFromSet(set(df["CL Status"].tolist())),
        "Worst CL Status as Borrower": worst_cl_status_as_guarantor,
        "Default": "Yes" if "Yes" in set(df["Default"].tolist()) else "No",
        "Stay Order Remarks": stay_order_remarks,
        "Outstanding Guarantor": df['Outstanding Guarantor'].sum(),
        "Worst CL Status as Guarantor": worst_cl_status_as_guarantor,
        "Default Guarantor": "-" if df.empty else ("Yes" if "Yes" in list(df['Default']) else "No"),
        "Stay Order Remarks Guarantor": stay_order_remarks,
        "CIB PDF View": " ".join(list(set(list(df["CIB PDF View"])))) if "Total" not in concern_name else "",
        "Updated Overdue and CL Status": " ".join(list(set(list(df["Updated Overdue and CL Status"])))) if "Total" not in concern_name else "",
        "Funded Outstanding Installment Alert": convertToString('True' if 'True' in set(df['Funded Outstanding Installment Alert']) else 'False'),
        "Funded Outstanding Non Installment Alert": convertToString('True' if 'True' in set(df['Funded Outstanding Non Installment Alert']) else 'False'),
        "Funded Outstanding Total Alert": convertToString('True' if 'True' in set(df['Funded Outstanding Total Alert']) else 'False'),
        "Non-Funded Outstanding Alert": convertToString('True' if 'True' in set(df['Non-Funded Outstanding Alert']) else 'False')
    }

def getSummaryTableConcernFields(cib, category, concern_name,cib_holders_name, df):
    return {
        "CIB Category": category,
        "Name of Concern": cib_holders_name,
        "Concerns Trade Name": concern_name,
        "Position Date": convertToString(df.loc[df['Position Date'] != '', 'Position Date'].max() if not df.loc[df['Position Date'] != '', 'Position Date'].empty else '').replace(" 00:00:00", ""),
        "Funded Outstanding Installment": convertToMillion(getFundedOutstandingInstallment(df)),
        "Funded Outstanding Non Installment": convertToMillion(getFundedOutstandingNonInstallment(df)),
        "Funded Outstanding Total": convertToMillion(getFundedOutstandingTotal(df)),
        "Non-Funded Outstanding": convertToMillion(getNonFundedOutstanding(df)),
        "Total Outstanding": convertToMillion(getTotalOutstanding(df)),
        "Overdue": convertToMillion(getOverdue(df)),
        "CL Status": general_engine.getClassFromSet(set(df["CL Status"].tolist())),
        "Default": "Yes" if "Yes" in set(df["Default"].tolist()) else "No",
        "CIB PDF View": " ".join(list(set(list(df["CIB Link"])))) if "Total" not in concern_name else "",
        "Funded Outstanding Installment Alert": convertToString('False'),
        "Funded Outstanding Non Installment Alert": convertToString('False'),
        "Funded Outstanding Total Alert": convertToString('False'),
        "Non-Funded Outstanding Alert": convertToString('False')
    }
def getSummaryTableConcernSum(category, concern_name, df):
    return {
        "CIB Category": category,
        "Name of Concern": "",
        "Concerns Trade Name": concern_name,
        "Position Date": convertToString(df.loc[df['Position Date'] != '', 'Position Date'].max() if not df.loc[df['Position Date'] != '', 'Position Date'].empty else '').replace(" 00:00:00", ""),
        "Funded Outstanding Installment": convertToFloat(df["Funded Outstanding Installment"].sum()),
        "Funded Outstanding Non Installment": convertToFloat(df["Funded Outstanding Non Installment"].sum()),
        "Funded Outstanding Total": convertToFloat(df["Funded Outstanding Total"].sum()),
        "Non-Funded Outstanding": convertToFloat(df["Non-Funded Outstanding"].sum()),
        "Total Outstanding": convertToFloat(df["Total Outstanding"].sum()),
        "Overdue": convertToFloat(df["Overdue"].sum()),
        "CL Status": general_engine.getClassFromSet(set(df["CL Status"].tolist())),
        "Default": "Yes" if "Yes" in set(df["Default"].tolist()) else "No",
        "CIB PDF View": " ",
        "Funded Outstanding Installment Alert": convertToString('False'),
        "Funded Outstanding Non Installment Alert": convertToString('False'),
        "Funded Outstanding Total Alert": convertToString('False'),
        "Non-Funded Outstanding Alert": convertToString('False')
    }
def getSummaryTableTwoFields(category, concern_name, df):
    return {
        "CIB Category": category,
        "Name of Concern": concern_name,
        "Funded Installment": convertToMillion(getFundedOutstandingInstallment(df)),
        "Funded Installment Raw": getFundedOutstandingInstallment(df),
        "Funded Non Installment": convertToMillion(getFundedOutstandingNonInstallment(df)),
        "Funded Non Installment Raw": getFundedOutstandingNonInstallment(df),
        "Funded Total": convertToMillion(getFundedOutstandingTotal(df)),
        "Funded Total Raw": getFundedOutstandingTotal(df),
        "Non-Funded": convertToMillion(getNonFundedOutstanding(df)),
        "Non-Funded Raw": getNonFundedOutstanding(df),
        "Total": convertToMillion(getTotalOutstanding(df)),
        "Total Raw": getTotalOutstanding(df),
        "Overdue": convertToMillion(getOverdue(df)),
        "Overdue Raw": getOverdue(df),
        "Worst CL Status": general_engine.getClassFromSet(set(df["CL Status"].tolist())),
        # "Default": "Yes" if "Yes" in set(df["Default"].tolist()) else "No",
        "Rescheduled Loan": convertToMillion(df['Reschedule Amount'].sum()),
        "Loan STD": convertToMillion(df[df['CL Status'] == 'STD']['Outstanding'].sum()),
        "Loan SMA": convertToMillion(df[df['CL Status'] == 'SMA']['Outstanding'].sum()),
        "Loan SS": convertToMillion(df[df['CL Status'] == 'SS']['Outstanding'].sum()),
        "Loan DF": convertToMillion(df[df['CL Status'] == 'DF']['Outstanding'].sum()),
        "Loan BL": convertToMillion(df[df['CL Status'] == 'BL']['Outstanding'].sum()),
        "Loan BLW": convertToMillion(df[df['CL Status'] == 'BLW']['Outstanding'].sum()),
        "Loan Stay Order": convertToMillion(df['Stay Order Amount'].sum()),
        "Remarks": re.sub(r'[,\[\]]', '', str(list(df['Remarks']))).replace("'", ''),
    }

def getSummaryTableTwoSum(category, concern_name, df):
    return {
        "CIB Category": category,
        "Name of Concern": concern_name,
        "Funded Installment": convertToFloat(df["Funded Installment"].sum()),
        "Funded Installment Raw": convertToFloat(df["Funded Installment Raw"].sum()),
        "Funded Non Installment": convertToFloat(df["Funded Non Installment"].sum()),
        "Funded Non Installment Raw": convertToFloat(df["Funded Non Installment Raw"].sum()),
        "Funded Total": convertToFloat(df["Funded Total"].sum()),
        "Funded Total Raw": convertToFloat(df["Funded Total Raw"].sum()),
        "Non-Funded": convertToFloat(df["Non-Funded"].sum()),
        "Non-Funded Raw": convertToFloat(df["Non-Funded Raw"].sum()),
        "Total": convertToFloat(df["Total"].sum()),
        "Total Raw": convertToFloat(df["Total Raw"].sum()),
        "Overdue": convertToFloat(df["Overdue"].sum()),
        "Overdue Raw": convertToFloat(df["Overdue Raw"].sum()),
        "Worst CL Status": general_engine.getClassFromSet(set(df["Worst CL Status"].tolist())),
        # "Default": "Yes" if "Yes" in set(df["Default"].tolist()) else "No",
        "Rescheduled Loan": convertToFloat(df['Rescheduled Loan'].sum()),
        "Loan STD": convertToFloat(df["Loan STD"].sum()),
        "Loan SMA": convertToFloat(df["Loan SMA"].sum()),
        "Loan SS": convertToFloat(df["Loan SS"].sum()),
        "Loan DF": convertToFloat(df["Loan DF"].sum()),
        "Loan BL": convertToFloat(df["Loan BL"].sum()),
        "Loan BLW": convertToFloat(df["Loan BLW"].sum()),
        "Loan Stay Order": convertToFloat(df['Loan Stay Order'].sum()),
        "Remarks": "-",
    }

def getSummaryTableTwoConcernFields(category, concern_name, cib_holders_name,df):
    return {
        "CIB Category": category,
        "Name of Concern": cib_holders_name,
        "Concerns Trade Name": concern_name,
        "Funded Installment": convertToMillion(getFundedOutstandingInstallment(df)),
        "Funded Non Installment": convertToMillion(getFundedOutstandingNonInstallment(df)),
        "Funded Total": convertToMillion(getFundedOutstandingTotal(df)),
        "Non-Funded": convertToMillion(getNonFundedOutstanding(df)),
        "Total": convertToMillion(getTotalOutstanding(df)),
        "Overdue": convertToMillion(getOverdue(df)),
        "Worst CL Status": general_engine.getClassFromSet(set(df["CL Status"].tolist())),
        "Default": "Yes" if "Yes" in set(df["Default"].tolist()) else "No",
        "Rescheduled Loan": convertToMillion(df['Reschedule Amount'].sum()),
        "Loan STD": convertToMillion(df[df['CL Status'] == 'STD']['Outstanding'].sum()),
        "Loan SMA": convertToMillion(df[df['CL Status'] == 'SMA']['Outstanding'].sum()),
        "Loan SS": convertToMillion(df[df['CL Status'] == 'SS']['Outstanding'].sum()),
        "Loan DF": convertToMillion(df[df['CL Status'] == 'DF']['Outstanding'].sum()),
        "Loan BL": convertToMillion(df[df['CL Status'] == 'BL']['Outstanding'].sum()),
        "Loan BLW": convertToMillion(df[df['CL Status'] == 'BLW']['Outstanding'].sum()),
        "Loan Stay Order": convertToMillion(df['Stay Order Amount'].sum()),
        "Remarks": re.sub(r'[,\[\]]', '', str(list(df['Remarks']))).replace("'", ''),
    }

def getSummaryTableTwoConcernSum(category, concern_name, df):
    return {
        "CIB Category": category,
        "Name of Concern": concern_name,
        "Concerns Trade Name": " ",
        "Funded Installment": convertToFloat(df["Funded Installment"].sum()),
        "Funded Non Installment": convertToFloat(df["Funded Non Installment"].sum()),
        "Funded Total": convertToFloat(df["Funded Total"].sum()),
        "Non-Funded": convertToFloat(df["Non-Funded"].sum()),
        "Total": convertToFloat(df["Total"].sum()),
        "Overdue": convertToFloat(df["Overdue"].sum()),
        "Worst CL Status": general_engine.getClassFromSet(set(df["Worst CL Status"].tolist())),
        "Default": "Yes" if "Yes" in set(df["Default"].tolist()) else "No",
        "Rescheduled Loan": convertToFloat(df['Rescheduled Loan'].sum()),
        "Loan STD": convertToFloat(df["Loan STD"].sum()),
        "Loan SMA": convertToFloat(df["Loan SMA"].sum()),
        "Loan SS": convertToFloat(df["Loan SS"].sum()),
        "Loan DF": convertToFloat(df["Loan DF"].sum()),
        "Loan BL": convertToFloat(df["Loan BL"].sum()),
        "Loan BLW": convertToFloat(df["Loan BLW"].sum()),
        "Loan Stay Order": convertToFloat(df['Loan Stay Order'].sum()),
        "Remarks": "-",
    }
def getSummaryTableThreeFundedFields(category, concern_name, df):
    funded_fields = {
        "CIB Category": category,
        "Borrowing Company - Person": concern_name,
        "A - Overdraft - Cash Credit": convertToMillion(df[df['Facility Type'].isin(OVERDRAFT)]['Outstanding'].sum()),
        "Overdue - EOL of A": calculate_eol(df[df['Facility Type'].isin(OVERDRAFT)]),
        "B - Time Loan": convertToMillion(df[df['Facility Type'].isin(TIME_LOAN)]['Outstanding'].sum()),
        "Overdue - EOL of B": calculate_eol(df[df['Facility Type'].isin(TIME_LOAN)]),
        "C - LTR": convertToMillion(df[df['Facility Type'].isin(LTR)]['Outstanding'].sum()),
        "Overdue - EOL of C": calculate_eol(df[df['Facility Type'].isin(LTR)]),
        "D - Other Non Installment": convertToMillion(getOtherNonInstallmentST3(df)['Outstanding']),
        "Overdue - EOL of D": calculate_eol(pd.DataFrame(getOtherNonInstallmentST3(df), index = [0])),
        "E - Term Loan": convertToMillion(convertToFloat(df[df['Facility Type'].isin(TERM_LOAN)]['Outstanding'].sum())),
        "EMI of E": convertToMillion(df[df['Facility Type'].isin(TERM_LOAN)]['Installment Amount'].sum()),
        "Overdue - EOL of E": calculate_eol(df[df['Facility Type'].isin(TERM_LOAN)]),
        "F - Other Installment Loan": convertToMillion(getOtherInstallmentST3(df)['Outstanding']),
        "EMI of F": convertToMillion(getOtherInstallmentST3(df)['Overdue']),
        "Overdue - EOL of F": calculate_eol(pd.DataFrame(getOtherInstallmentST3(df),  index = [0])),
    }
    return funded_fields


def getOtherNonInstallmentST3(df):
    df = df[~df['Facility Type'].isin([OVERDRAFT+TIME_LOAN+LTR+TERM_LOAN])]
    df = df[df['Installment Type'] == "No Installment"]
    return {"Outstanding": convertToFloat(df['Outstanding'].sum()), "Overdue": convertToFloat(df['Overdue'].sum()),  "Limit": convertToFloat(df["Limit"].sum())}

def getOtherInstallmentST3(df):
    df = df[~df['Facility Type'].isin([OVERDRAFT+TIME_LOAN+LTR+TERM_LOAN])]
    df = df[df['Installment Type'] == "Installment"]
    return {"Outstanding": convertToFloat(df['Outstanding'].sum()), "Overdue": convertToFloat(df['Overdue'].sum()), "EMI": convertToFloat(df['Installment Amount']), "Limit": convertToFloat(df["Limit"].sum())}

def getSummaryTableThreeFundedSum(category, concern_name, df):
    return {
        "CIB Category": category,
        "Borrowing Company - Person": concern_name,
        "A - Overdraft - Cash Credit": convertToFloat(df["A - Overdraft - Cash Credit"].sum()),
        "Overdue - EOL of A": convertToFloat(df["Overdue - EOL of A"].sum()),
        "B - Time Loan": convertToFloat(df["B - Time Loan"].sum()),
        "Overdue - EOL of B": convertToFloat(df["Overdue - EOL of B"].sum()),
        "C - LTR": convertToFloat(df["C - LTR"].sum()),
        "Overdue - EOL of C": convertToFloat(df["Overdue - EOL of C"].sum()),
        "D - Other Non Installment": convertToFloat(df["D - Other Non Installment"].sum()),
        "Overdue - EOL of D": convertToFloat(df["Overdue - EOL of D"].sum()),
        "E - Term Loan": convertToFloat(df["E - Term Loan"].sum()),
        "EMI of E": convertToFloat(df["EMI of E"].sum()),
        "Overdue - EOL of E": convertToFloat(df["Overdue - EOL of E"].sum()),
        "F - Other Installment Loan": convertToFloat(df["F - Other Installment Loan"].sum()),
        "EMI of F": convertToFloat(df["EMI of F"].sum()),
        "Overdue - EOL of F": convertToFloat(df["Overdue - EOL of F"].sum()),
    }

def getSummaryTableThreeNonFundedFields(category, concern_name, df, non_funded_loans):
    response = {
        "CIB Category": category,
        "Borrowing Company - Person": concern_name,
    }
    for loan in non_funded_loans:
        response[loan] = convertToMillion(df[df['Facility Type'].isin([loan])]['Outstanding'].sum())
    return response

def getSummaryTableThreeNonFundedSum(category, concern_name, df, non_funded_loans):
    response = {
        "CIB Category": category,
        "Borrowing Company - Person": concern_name,
    }
    for loan in non_funded_loans:
        response[loan] = convertToFloat(df[loan].sum())
    return response
def getSummaryTableThreeFundedFieldsConcern(category, concern_name,cib_holders_name, df):
    funded_fields = {
        "CIB Category": category,
        "Borrowing Company - Person": cib_holders_name, 
        "Concerns Trade Name":  concern_name,
        "A - Overdraft - Cash Credit": convertToMillion(df[df['Facility Type'].isin(OVERDRAFT)]['Outstanding'].sum()),
        "Overdue - EOL of A": calculate_eol(df[df['Facility Type'].isin(OVERDRAFT)]),
        "B - Time Loan": convertToMillion(df[df['Facility Type'].isin(TIME_LOAN)]['Outstanding'].sum()),
        "Overdue - EOL of B": calculate_eol(df[df['Facility Type'].isin(TIME_LOAN)]),
        "C - LTR": convertToMillion(df[df['Facility Type'].isin(LTR)]['Outstanding'].sum()),
        "Overdue - EOL of C": calculate_eol(df[df['Facility Type'].isin(LTR)]),
        "D - Other Non Installment": convertToMillion(getOtherNonInstallmentST3(df)['Outstanding']),
        "Overdue - EOL of D": calculate_eol(pd.DataFrame(getOtherNonInstallmentST3(df), index = [0])),
        "E - Term Loan": convertToMillion(convertToFloat(df[df['Facility Type'].isin(TERM_LOAN)]['Outstanding'].sum())),
        "EMI of E": convertToMillion(df[df['Facility Type'].isin(TERM_LOAN)]['Installment Amount'].sum()),
        "Overdue - EOL of E": calculate_eol(df[df['Facility Type'].isin(TERM_LOAN)]),
        "F - Other Installment Loan": convertToMillion(getOtherInstallmentST3(df)['Outstanding']),
        "EMI of F": convertToMillion(getOtherInstallmentST3(df)['Overdue']),
        "Overdue - EOL of F": calculate_eol(pd.DataFrame(getOtherInstallmentST3(df),  index = [0])),
    }
    return funded_fields


def getSummaryTableThreeFundedConcernSum(cib_holders_name, df):
    return {
        "CIB Category": '',
        "Borrowing Company - Person":  cib_holders_name, 
        "Concerns Trade Name":  '',
        "A - Overdraft - Cash Credit": convertToFloat(df["A - Overdraft - Cash Credit"].sum()),
        "Overdue - EOL of A": convertToFloat(df["Overdue - EOL of A"].sum()),
        "B - Time Loan": convertToFloat(df["B - Time Loan"].sum()),
        "Overdue - EOL of B": convertToFloat(df["Overdue - EOL of B"].sum()),
        "C - LTR": convertToFloat(df["C - LTR"].sum()),
        "Overdue - EOL of C": convertToFloat(df["Overdue - EOL of C"].sum()),
        "D - Other Non Installment": convertToFloat(df["D - Other Non Installment"].sum()),
        "Overdue - EOL of D": convertToFloat(df["Overdue - EOL of D"].sum()),
        "E - Term Loan": convertToFloat(df["E - Term Loan"].sum()),
        "EMI of E": convertToFloat(df["EMI of E"].sum()),
        "Overdue - EOL of E": convertToFloat(df["Overdue - EOL of E"].sum()),
        "F - Other Installment Loan": convertToFloat(df["F - Other Installment Loan"].sum()),
        "EMI of F": convertToFloat(df["EMI of F"].sum()),
        "Overdue - EOL of F": convertToFloat(df["Overdue - EOL of F"].sum()),
    }

def getSummaryTableThreeNonFundedFieldsConcern(category, concern_name,cib_holders_name, df, non_funded_loans):
    response = {
        "CIB Category": category,
        "Borrowing Company - Person": cib_holders_name,
        "Concerns Trade Name": concern_name
    }
    for loan in non_funded_loans:
        response[loan] = convertToMillion(df[df['Facility Type'].isin([loan])]['Outstanding'].sum())
    return response

def getSummaryTableThreeNonFundedConcernSum(category, cib_holders_name, df, non_funded_loans):
    response = {
        "CIB Category": category,
        "Borrowing Company - Person": cib_holders_name,
        "Concerns Trade Name": ""
    }
    
    for loan in non_funded_loans:
        response[loan] = convertToFloat(df[loan].sum())
    return response

def getSummaryOfFundedFacilityFields(row, i, installment):
    return {
        "SL": "B1.1 - " + convertToString(i + 1) if installment else "B2.1 - " + convertToString(i + 1),
        "Nature of Facility": row["Facility Type"],
        "Name of the Concern": row["Name"],
        "Installment Type": row["Installment Type"],
        "Limit": convertToMillion(row["Limit"]),
        "Outstanding": convertToMillion(row["Outstanding"]),
        "Overdue": convertToMillion(row["Overdue"]),
        "Start Date": convertToString(row["Start Date"]),
        "End Date of Contract": convertToString(row["End Date of Contract"]),
        "Installment Amount": (convertToMillion(row["Installment Amount"]) if installment else "Not Applicable"),
        "Payment Period": (row["Payment Period (Monthly/Quarterly)"] if installment else "Not Applicable"),
        "Total No. of Installment": (float(row["Total No of Installment"]) if installment else "Not Applicable"),
        "Total no. of Installment paid": (float(row["Total No of Installment Paid"]) if installment else "Not Applicable"),
        "No. of Remaining Installment": (float(row["No of Remaining Installment"]) if installment else "Not Applicable"),
        "Date of Last Payment": convertToString(row["Date of Last Payment"]),
        "NPI": float(row["NPI"]) if installment else "Not Applicable",
        "Default": row["Default"],
    }

def getSummaryOfFundedFacilitySum(df, total_type, installment_type):
    return {
        "SL": "-",
        "Nature of Facility": total_type,
        "Name of the Concern": '-',
        "Installment Type": installment_type,
        "Limit": convertToMillion(df["Limit"].sum()),
        "Outstanding": convertToMillion(df['Outstanding'].sum()),
        "Overdue": convertToMillion(df["Overdue"].sum()),
        "Start Date": "-",
        "End Date of Contract": "-",
        "Installment Amount": convertToMillion(df['Installment Amount'].sum()),
        "Payment Period": "-",
        "Total No. of Installment": convertToMillion(df['Total No of Installment'].sum()),
        "Total no. of Installment paid": convertToMillion(df['Total No of Installment Paid'].sum()),
        "No. of Remaining Installment": convertToMillion(df['No of Remaining Installment'].sum()),
        "Date of Last Payment": "-",
        "NPI": convertToFloat(df['NPI'].sum()),
        "Default": "Yes" if "Yes" in set(df['Default'].tolist()) else "No",
    }

def getSummaryOfFundedFacilityFieldsConcern(row, i, installment):
    return {
        "SL": "B1.1 - " + convertToString(i + 1) if installment else "B2.1 - " + convertToString(i + 1),
        "Name of the Concern": row["Name"],
        "Concerns Trade Name": row["Concerns Trade Name"], 
        "Nature of Facility": row["Facility Type"],
        "Installment Type": row["Installment Type"],
        "Limit": convertToMillion(row["Limit"]),
        "Outstanding": convertToMillion(row["Outstanding"]),
        "Overdue": convertToMillion(row["Overdue"]),
        "Start Date": convertToString(row["Start Date"]),
        "End Date of Contract": convertToString(row["End Date of Contract"]),
        "Installment Amount": (convertToMillion(row["Installment Amount"]) if installment else "Not Applicable"),
        "Payment Period": (row["Payment Period (Monthly/Quarterly)"] if installment else "Not Applicable"),
        "Total No. of Installment": (float(row["Total No of Installment"]) if installment else "Not Applicable"),
        "Total no. of Installment paid": (float(row["Total No of Installment Paid"]) if installment else "Not Applicable"),
        "No. of Remaining Installment": (float(row["No of Remaining Installment"]) if installment else "Not Applicable"),
        "Date of Last Payment": convertToString(row["Date of Last Payment"]),
        "NPI": float(row["NPI"]) if installment else "Not Applicable",
        "Default": row["Default"],
    }

def getSummaryOfFundedFacilitySumConcern(df, total_type, installment_type):
    return {
        "SL": "-",
        "Name of the Concern": "-",
        "Concerns Trade Name": "-", 
        "Nature of Facility": total_type,
        "Installment Type": installment_type,
        "Limit": convertToMillion(df["Limit"].sum()),
        "Outstanding": convertToMillion(df['Outstanding'].sum()),
        "Overdue": convertToMillion(df["Overdue"].sum()),
        "Start Date": "-",
        "End Date of Contract": "-",
        "Installment Amount": convertToMillion(df['Installment Amount'].sum()),
        "Payment Period": "-",
        "Total No. of Installment": convertToMillion(df['Total No of Installment'].sum()),
        "Total no. of Installment paid": convertToMillion(df['Total No of Installment Paid'].sum()),
        "No. of Remaining Installment": convertToMillion(df['No of Remaining Installment'].sum()),
        "Date of Last Payment": "-",
        "NPI": convertToFloat(df['NPI'].sum()),
        "Default": "Yes" if "Yes" in set(df['Default'].tolist()) else "No",
    }
def getSummaryOfExpiredButShowingLiveFundedTotalSum( total_type, total_df):
    return {
        "Nature of Facility": convertToString(total_type),
        "Limit": convertToMillion(total_df["Limit"].sum()),
        "Outstanding": convertToMillion(total_df['Outstanding'].sum()),
        "Overdue": convertToMillion(total_df["Overdue"].sum()),
        "Start Date": "-",
        "End Date of Contract": "-",
        "Installment Amount": "-",
        "Payment Period": "-",
        "Total No of Installment": "-",
        "Total No of Installment paid":"-",
        "No of Remaining Installment": "-",
        "Date of Last Payment": "-",
        "NPI": convertToFloat(total_df['NPI'].sum()),
        "Default": "Yes" if "Yes" in set(total_df['Default'].tolist()) else "No"}

def getSummaryOfExpiredButShowingLiveFields(row, i, installment):
    return {"Nature of Facility": row['Facility Type'],
            "Limit": convertToMillion(row['Limit']),
            "Outstanding": convertToMillion(row['Outstanding']),
            "Overdue": convertToMillion(row['Overdue']),
            "Start Date": convertToString(row['Start Date']).replace(" 00:00:00", ""),
            "End Date of Contract": convertToString(row['End Date of Contract']).replace(" 00:00:00", ""),
            "Installment Amount": (convertToMillion(row['Installment Amount']) if installment else "Not Applicable"),
            "Payment Period": (row['Payment Period (Monthly/Quarterly)'] if installment else "Not Applicable"),
            "Total No of Installment": (convertToFloat(row["Total No of Installment"]) if installment else "Not Applicable"),
            "Total No of Installment paid": (convertToFloat(row["Total No of Installment Paid"]) if installment else "Not Applicable"),
            "No of Remaining Installment": (convertToFloat(row["No of Remaining Installment"]) if installment else "Not Applicable"),
            "Date of Last Payment": convertToString(row['Date of Last Payment']).replace(" 00:00:00", ""),
            "NPI": convertToFloat(row["NPI"]) if installment else "Not Applicable",
            "Default": row['Default']
        }

def getSummaryOfExpiredButShowingLiveFundedSum(df, total_type, installment_type):
    return {
        "Nature of Facility": total_type,
        "Limit": convertToMillion(df["Limit"].sum()),
        "Outstanding": convertToMillion(df['Outstanding'].sum()),
        "Overdue": convertToMillion(df["Overdue"].sum()),
        "Start Date": "-",
        "End Date of Contract": "-",
        "Installment Amount": convertToMillion(df['Installment Amount'].sum()),
        "Payment Period": "-",
        "Total No of Installment": convertToFloat(df['Total No of Installment'].sum()),
        "Total No of Installment paid": convertToFloat(df['Total No of Installment Paid'].sum()),
        "No of Remaining Installment": convertToFloat(df['No of Remaining Installment'].sum()),
        "Date of Last Payment": "-",
        "NPI": convertToFloat(df['NPI'].sum()),
        "Default": "Yes" if "Yes" in set(df['Default'].tolist()) else "No"}

def getSummaryOfExpiredButShowingLiveFundedConcernTotalSum( total_type, total_df):
    return {
        "Concerns Trade Name":convertToString(total_type),
        "Nature of Facility": '',
        "Limit": convertToMillion(total_df["Limit"].sum()),
        "Outstanding": convertToMillion(total_df['Outstanding'].sum()),
        "Overdue": convertToMillion(total_df["Overdue"].sum()),
        "Start Date": "-",
        "End Date of Contract": "-",
        "Installment Amount": "-",
        "Payment Period": "-",
        "Total No of Installment": "-",
        "Total No of Installment paid":"-",
        "No of Remaining Installment": "-",
        "Date of Last Payment": "-",
        "NPI": convertToFloat(total_df['NPI'].sum()),
        "Default": "Yes" if "Yes" in set(total_df['Default'].tolist()) else "No"}


def getSummaryOfExpiredButShowingLiveFieldsConcern(row, i, installment):
    return {"Concerns Trade Name": row["Concerns Trade Name"],
            "Nature of Facility": row['Facility Type'],
            "Limit": convertToMillion(row['Limit']),
            "Outstanding": convertToMillion(row['Outstanding']),
            "Overdue": convertToMillion(row['Overdue']),
            "Start Date": convertToString(row['Start Date']).replace(" 00:00:00", ""),
            "End Date of Contract": convertToString(row['End Date of Contract']).replace(" 00:00:00", ""),
            "Installment Amount": (convertToMillion(row['Installment Amount']) if installment else "Not Applicable"),
            "Payment Period": (row['Payment Period (Monthly/Quarterly)'] if installment else "Not Applicable"),
            "Total No of Installment": (convertToFloat(row["Total No of Installment"]) if installment else "Not Applicable"),
            "Total No of Installment paid": (convertToFloat(row["Total No of Installment Paid"]) if installment else "Not Applicable"),
            "No of Remaining Installment": (convertToFloat(row["No of Remaining Installment"]) if installment else "Not Applicable"),
            "Date of Last Payment": convertToString(row['Date of Last Payment']).replace(" 00:00:00", ""),
            "NPI": convertToFloat(row["NPI"]) if installment else "Not Applicable",
            "Default": row['Default']
        }

def getSummaryOfExpiredButShowingLiveFundedConcernSum(df, total_type, installment_type):
    return {
        "Concerns Trade Name": total_type, 
        "Nature of Facility": '',
        "Limit": convertToMillion(df["Limit"].sum()),
        "Outstanding": convertToMillion(df['Outstanding'].sum()),
        "Overdue": convertToMillion(df["Overdue"].sum()),
        "Start Date": "-",
        "End Date of Contract": "-",
        "Installment Amount": convertToMillion(df['Installment Amount'].sum()),
        "Payment Period": "-",
        "Total No of Installment": convertToFloat(df['Total No of Installment'].sum()),
        "Total No of Installment paid": convertToFloat(df['Total No of Installment Paid'].sum()),
        "No of Remaining Installment": convertToFloat(df['No of Remaining Installment'].sum()),
        "Date of Last Payment": "-",
        "NPI": convertToFloat(df['NPI'].sum()),
        "Default": "Yes" if "Yes" in set(df['Default'].tolist()) else "No"}

def getPositionDate(fac):
    if type(fac['Contract History']) != dict:
        Position_date = ((fac["Contract History"]).sort_values('Date', ascending=False)['Date'][0]).timestamp()
        Position_date = datetime.fromtimestamp(Position_date).strftime('%Y-%m-%d')
        return Position_date
    return ""

def getCorporateDataFrame(cibs):
    df = pd.DataFrame()
    for cib in cibs:
        if getCIBCategory(cib) in ["Related party of Guarantor(with proprietorship concern)", "Directors CIB(with proprietorship concern)"]:
            if cib.linked_prop_list is not None:
                trade_names_dict = extract_trade_names(cib.linked_prop_list)
            else:
                trade_names_dict = {}  # Initialize an empty dictionary if linked_prop_list is None
        for i, fac_type in enumerate((cib.installment_facility, cib.noninstallment_facility, cib.credit_card_facility)):
            response = []
            if fac_type is not None:
                for fac in fac_type:
                    subject_code = general_engine.getSubjectCode(fac)
                    if getCIBCategory(cib) in ["Related party of Guarantor(with proprietorship concern)", "Directors CIB(with proprietorship concern)"]:
                        concern_trade_name = trade_names_dict.get(subject_code, None)
                    else:
                        concern_trade_name = None

                    response.append(
                        {
                            "CIB Category": getCIBCategory(cib),
                            "Name": general_engine.getBorrowersName(cib.subject_info),
                            "Facility Type": general_engine.getFacilityType(fac),
                            "Phase": general_engine.getPhase(fac),
                            "Role": general_engine.getRole(fac),
                            "Subject code": subject_code,
                            "Concerns Trade Name": concern_trade_name,
                            "Is Funded": general_engine.isFunded(fac),
                            "Installment Type": getFacilityType(i),
                            "Outstanding": general_engine.getOutstanding(fac),
                            "Outstanding Date": general_engine.getOutstandingDate(fac),
                            "Outstanding Zero Date": getOutstandingZeroDate(fac),
                            "Position Date": getPositionDate(fac),
                            "Overdue": general_engine.getOverdue(fac),
                            "CL Status": general_engine.getCurrentCLStatus(fac),
                            "Default": getDefault(fac),
                            "Limit": general_engine.getLimit(fac),
                            "Loan/Limit (days of adjustment before/after)": getDaysOfAdjustment(fac),
                            "Installment Amount": general_engine.getEMI(fac),
                            "Worse Classification Status": general_engine.getWorstCLStatus(fac),
                            "Date of Classification": general_engine.getWorstCLDate(fac),
                            "Start Date": getStartDate(fac),
                            "End Date of Contract": getEndDateOfContract(fac),
                            "Is Stay Order": isStayOrder(fac),
                            "Stay Order": getStayOrder(fac),
                            "Stay Order Amount": getStayOrderAmount(fac),
                            "Writ no": getStayOrder(fac),
                            "Remarks": getRemarks(fac),
                            "Payment Period (Monthly/Quarterly)": getPaymentPeriod(fac),
                            "Total No of Installment": getTotalNumberOfInstallment(fac),
                            "Total No of Installment Paid": getNoOfInstallmentPaid(fac),
                            "No of Remaining Installment": getNoOfRemainingInstallment(fac),
                            "Date of Last Payment": getDateOfLastPayment(fac),
                            "NPI": general_engine.getCurrentNPI(fac),
                            "Reschedule Type": getTypeOfReschedule(fac),
                            "Last Date of Reschedule": getDateOfLastReschedule(fac),
                            "Reschedule Amount": getRescheduleAmount(fac),
                            "Total Disbursement Amount": getTotalDisbursementAmount(fac),
                            "CIB Link": PDF_LINK + cib.pdf_name
                        }
                    
                    )
                    
            df = pd.concat([df, pd.DataFrame(response)], ignore_index=True)
    return df


