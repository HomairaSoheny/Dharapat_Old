import re
import pandas as pd
from dashboard.engines import general_engine
from dashboard.engines.keywords import *
from utils.general_helper import *
from utils.env import PDF_LINK

def getCIBCategory(cib):
    return CATEGORY_MAPPING.get(cib.cib_category, None)


def getDateOfClassification(fac):
    for key in DATE_OF_CLASSIFICATION:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]


def getStartDate(fac):
    for key in STARTING_DATE:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]


def getEndDateOfContract(fac):
    for key in END_DATE_OF_CONTRACT:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]


def getRemarks(fac):
    for key in REMARKS:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]


def getPaymentPeriod(fac):
    for key in PAYMENT_PERIOD:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]


def getTotalNumberOfInstallment(fac):
    for key in TOTAL_NUMBER_OF_INSTALLMENT:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]


def getNoOfRemainingInstallment(fac):
    for key in REMAINING_INSTALLMENT_NUMBER:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]


def getDateOfLastPayment(fac):
    for key in DATE_OF_LAST_PAYMENT:
        if key in fac["Ref"].keys():
            return fac["Ref"][key]


def getFacilityType(i):
    return FACILITY_CATEGORIES.get(i, "Unknown")


def getFundedOutstandingInstallment(df):
    df = df[df["Is Funded"] == "Yes"]
    df = df[df["Installment Type"] == "Installment"]
    return convertToMillion(df["Outstanding"].sum())


def getFundedOutstandingNonInstallment(df):
    df = df[df["Is Funded"] == "Yes"]
    df = df[df["Installment Type"] == "No Installment"]
    return convertToMillion(df["Outstanding"].sum())


def getFundedOutstandingTotal(df):
    return convertToFloat(getFundedOutstandingInstallment(df) + getFundedOutstandingNonInstallment(df))


def getNonFundedOutstanding(df):
    df = df[df["Is Funded"] == "No"]
    return convertToMillion(df["Outstanding"].sum())


def getTotalOutstanding(df):
    return convertToFloat(getFundedOutstandingTotal(df) + getNonFundedOutstanding(df))


def getOverdue(df):
    return convertToMillion(df["Overdue"].sum())


def getDefault(fac):
    return "Yes" if "Yes" in fac["Contract History"]["Default"].tolist() else "No"

def getTypeOfReschedule(fac):
    for key in RESCHEDULE_LOAN:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
    return "Not Rescheduled"

def getDateOfLastReschedule(fac):
    for key in LAST_RESCHEDULING_DATE:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
    return "Not Rescheduled"

def getTotalDisbursementAmount(fac):
    for key in TOTAL_DISBURSEMENT_AMOUNT:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getSummaryTableFields(category, concern_name, df):
    return {
        "CIB Category": category,
        "Name of Concern": concern_name,
        "Funded Outstanding Installment": convertToFloat(getFundedOutstandingInstallment(df)),
        "Funded Outstanding Non Installment": convertToFloat(getFundedOutstandingNonInstallment(df)),
        "Funded Outstanding Total": convertToFloat(getFundedOutstandingTotal(df)),
        "Non-Funded Outstanding": convertToFloat(getNonFundedOutstanding(df)),
        "Total Outstanding": convertToFloat(getTotalOutstanding(df)),
        "Overdue": convertToFloat(getOverdue(df)),
        "CL Status": general_engine.getClassFromSet(set(df["CL Status"].tolist())),
        "Default": "Yes" if "Yes" in set(df["Default"].tolist()) else "No",
        "CIB PDF View": re.sub(r'[,\[\]]', '', str(list(df['CIB Link']))).replace("'", ''),
        "Updated Overdue and CL Status": "Need More Clarification",
    }


def getSummaryTableSum(category, concern_name, df):
    return {
        "CIB Category": category,
        "Name of Concern": concern_name,
        "Funded Outstanding Installment": convertToFloat(df["Funded Outstanding Installment"].sum()),
        "Funded Outstanding Non Installment": convertToFloat(df["Funded Outstanding Non Installment"].sum()),
        "Funded Outstanding Total": convertToFloat(df["Funded Outstanding Total"].sum()),
        "Non-Funded Outstanding": convertToFloat(df["Non-Funded Outstanding"].sum()),
        "Total Outstanding": convertToFloat(df["Total Outstanding"].sum()),
        "Overdue": convertToFloat(df["Overdue"].sum()),
        "CL Status": general_engine.getClassFromSet(set(df["CL Status"].tolist())),
        "Default": "Yes" if "Yes" in set(df["Default"].tolist()) else "No",
        "CIB PDF View": "-",
        "Updated Overdue and CL Status": "Need More Clarification",
    }

def getSummaryTableTwoFields(category, concern_name, df):
    return {
        "CIB Category": category,
        "Name of Concern": concern_name,
        "Funded Installment": convertToFloat(getFundedOutstandingInstallment(df)),
        "Funded Non Installment": convertToFloat(getFundedOutstandingNonInstallment(df)),
        "Funded Total": convertToFloat(getFundedOutstandingTotal(df)),
        "Non-Funded": convertToFloat(getNonFundedOutstanding(df)),
        "Total": convertToFloat(getTotalOutstanding(df)),
        "Overdue": convertToFloat(getOverdue(df)),
        "Worst CL Status": general_engine.getClassFromSet(set(df["CL Status"].tolist())),
        "Default": "Yes" if "Yes" in set(df["Default"].tolist()) else "No",
        "Rescheduled Loan": "Not Implemented",
        "Loan STD": convertToFloat(df[df['CL Status'] == 'STD']['Outstanding'].sum()),
        "Loan SMA": convertToFloat(df[df['CL Status'] == 'SMA']['Outstanding'].sum()),
        "Loan SS": convertToFloat(df[df['CL Status'] == 'SS']['Outstanding'].sum()),
        "Loan DF": convertToFloat(df[df['CL Status'] == 'DF']['Outstanding'].sum()),
        "Loan BL": convertToFloat(df[df['CL Status'] == 'BL']['Outstanding'].sum()),
        "Loan BLW": convertToFloat(df[df['CL Status'] == 'BLW']['Outstanding'].sum()),
        "Loan Stay Order": "Need More Clarification",
        "Remarks": re.sub(r'[,\[\]]', '', str(list(df['Remarks']))).replace("'", ''),
    }

def getSummaryTableTwoSum(category, concern_name, df):
    return {
        "CIB Category": category,
        "Name of Concern": concern_name,
        "Funded Installment": convertToFloat(df["Funded Installment"].sum()),
        "Funded Non Installment": convertToFloat(df["Funded Non Installment"].sum()),
        "Funded Total": convertToFloat(df["Funded Total"].sum()),
        "Non-Funded": convertToFloat(df["Non-Funded"].sum()),
        "Total": convertToFloat(df["Total"].sum()),
        "Overdue": convertToFloat(df["Overdue"].sum()),
        "Worst CL Status": general_engine.getClassFromSet(set(df["Worst CL Status"].tolist())),
        "Default": "Yes" if "Yes" in set(df["Default"].tolist()) else "No",
        "Rescheduled Loan": "Not Implemented",
        "Loan STD": convertToFloat(df["Loan STD"].sum()),
        "Loan SMA": convertToFloat(df["Loan SMA"].sum()),
        "Loan SS": convertToFloat(df["Loan SS"].sum()),
        "Loan DF": convertToFloat(df["Loan DF"].sum()),
        "Loan BL": convertToFloat(df["Loan BL"].sum()),
        "Loan BLW": convertToFloat(df["Loan BLW"].sum()),
        "Loan Stay Order": "Need More Clarification",
        "Remarks": "-",
    }

def getOtherNonInstallmentST3(df):
    df = df[~df['Facility Type'].isin([OVERDRAFT+TIME_LOAN+LTR+TERM_LOAN])]
    df = df[df['Installment Type'] == "No Installment"]
    return {"Outstanding": convertToFloat(df['Outstanding'].sum()), "Overdue": convertToFloat(df['Overdue'].sum())}

def getOtherInstallmentST3(df):
    df = df[~df['Facility Type'].isin([OVERDRAFT+TIME_LOAN+LTR+TERM_LOAN])]
    df = df[df['Installment Type'] == "Installment"]
    return {"Outstanding": convertToFloat(df['Outstanding'].sum()), "Overdue": convertToFloat(df['Overdue'].sum()), "EMI": convertToFloat(df['Installment Amount'])}

def getSummaryTableThreeFundedFields(category, concern_name, df):
    return {
        "CIB Category": category,
        "Borrowing Company - Person": concern_name,
        "A - Overdraft - Cash Credit": convertToFloat(df[df['Facility Type'].isin(OVERDRAFT)]['Outstanding'].sum()),
        "Overdue - EOL of A": convertToFloat(df[df['Facility Type'].isin(OVERDRAFT)]['Overdue'].sum()),
        "B - Time Loan": convertToFloat(df[df['Facility Type'].isin(TIME_LOAN)]['Outstanding'].sum()),
        "Overdue - EOL of B": convertToFloat(df[df['Facility Type'].isin(TIME_LOAN)]['Overdue'].sum()),
        "C - LTR": convertToFloat(df[df['Facility Type'].isin(LTR)]['Outstanding'].sum()),
        "Overdue - EOL of C": convertToFloat(df[df['Facility Type'].isin(LTR)]['Overdue'].sum()),
        "D - Other Non Installment": getOtherNonInstallmentST3(df)['Outstanding'],
        "Overdue - EOL of D": getOtherNonInstallmentST3(df)['Overdue'],
        "E - Term Loan": convertToFloat(df[df['Facility Type'].isin(TERM_LOAN)]['Outstanding'].sum()),
        "EMI of E": convertToFloat(df[df['Facility Type'].isin(TERM_LOAN)]['Installment Amount'].sum()),
        "Overdue - EOL of E": convertToFloat(df[df['Facility Type'].isin(TERM_LOAN)]['Overdue'].sum()),
        "F - Other Installment Loan": getOtherInstallmentST3(df)['Outstanding'],
        "EMI of F": getOtherInstallmentST3(df)['Overdue'],
        "Overdue - EOL of F": getOtherInstallmentST3(df)['EMI'],
    }

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
        response[loan] = convertToFloat(df[df['Facility Type'].isin([loan])]['Outstanding'].sum())
    return response

def getSummaryTableThreeNonFundedSum(category, concern_name, df, non_funded_loans):
    response = {
        "CIB Category": category,
        "Borrowing Company - Person": concern_name,
    }
    for loan in non_funded_loans:
        response[loan] = convertToFloat(df[loan].sum())
    return response


def getSummaryOfFundedFacilityFields(row, i, installment):
    return {
        "SL": "B1.1 - " + convertToString(i + 1) if installment else "B2.1 - " + convertToString(i + 1),
        "Nature of Facility": row["Facility Type"],
        "Installment Type": row["Installment Type"],
        "Limit": convertToFloat(row["Limit"]),
        "Outstanding": convertToFloat(row["Outstanding"]),
        "Overdue": convertToFloat(row["Overdue"]),
        "Start Date": convertToString(row["Start Date"]),
        "End Date of Contract": convertToString(row["End Date of Contract"]),
        "Installment Amount": (convertToFloat(row["Installment Amount"]) if installment else "Not Applicable"),
        "Payment Period": (row["Payment Period (Monthly/Quarterly)"] if installment else "Not Applicable"),
        "Total No. of Installment": (row["Total No of Installment"] if installment else "Not Applicable"),
        "Total no. of Installment paid": ("Not Implemented" if installment else "Not Applicable"),
        "No. of Remaining Installment": (int(row["No of Remaining Installment"]) if installment else "Not Applicable"),
        "Date of Last Payment": convertToString(row["Date of Last Payment"]),
        "NPI": int(row["NPI"]) if installment else "Not Applicable",
        "Default": row["Default"],
    }

def getSummaryOfFundedFacilitySum(df, total_type, installment_type):
    return {
        "SL": "-",
        "Nature of Facility": total_type,
        "Installment Type": installment_type,
        "Limit": convertToFloat(df["Limit"].sum()),
        "Outstanding": convertToFloat(df['Outstanding'].sum()),
        "Overdue": convertToFloat(df["Overdue"].sum()),
        "Start Date": "-",
        "End Date of Contract": "-",
        "Installment Amount": convertToFloat(df['Installment Amount'].sum()),
        "Payment Period": "-",
        "Total No. of Installment": convertToFloat(df['Total No of Installment'].sum()),
        "Total no. of Installment paid": "Not Implemented",
        "No. of Remaining Installment": convertToFloat(df['No of Remaining Installment'].sum()),
        "Date of Last Payment": "-",
        "NPI": convertToInteger(df['NPI'].sum()),
        "Default": "Yes" if "Yes" in set(df['Default'].tolist()) else "No",
    }


def getCorporateDataFrame(cibs):
    df = pd.DataFrame()
    for cib in cibs:
        for i, fac_type in enumerate((cib.installment_facility, cib.noninstallment_facility, cib.credit_card_facility)):
            response = []
            if fac_type is not None:
                for fac in fac_type:
                    response.append(
                        {
                            "CIB Category": getCIBCategory(cib),
                            "Name": general_engine.getBorrowersName(cib.subject_info),
                            "Facility Type": general_engine.getFacilityType(fac),
                            "Phase": general_engine.getPhase(fac),
                            "Role": general_engine.getRole(fac),
                            "Is Funded": general_engine.isFunded(fac),
                            "Installment Type": getFacilityType(i),
                            "Outstanding": general_engine.getOutstanding(fac),
                            "Overdue": general_engine.getOverdue(fac),
                            "CL Status": general_engine.getCurrentCLStatus(fac),
                            "Default": getDefault(fac),
                            "Limit": general_engine.getLimit(fac),
                            "Loan/Limit (days of adjustment before/after)": "Need elaboration",
                            "Installment Amount": general_engine.getEMI(fac),
                            "Worse Classification Status": general_engine.getWorstCLStatus(fac),
                            "Date of Classification": getDateOfClassification(fac),
                            "Start Date": getStartDate(fac),
                            "End Date of Contract": getEndDateOfContract(fac),
                            "Writ no": "Need Elaboration",
                            "Remarks": getRemarks(fac),
                            "Payment Period (Monthly/Quarterly)": getPaymentPeriod(fac),
                            "Total No of Installment": getTotalNumberOfInstallment(fac),
                            "No of Remaining Installment": getNoOfRemainingInstallment(fac),
                            "Date of Last Payment": getDateOfLastPayment(fac),
                            "NPI": general_engine.getCurrentNPI(fac),
                            "Reschedule Type": getTypeOfReschedule(fac),
                            "Last Date of Reschedule": getDateOfLastReschedule(fac),
                            "Total Disbursement Amount": getTotalDisbursementAmount(fac),
                            "CIB Link": PDF_LINK + cib.pdf_name
                        }
                    )
            df = pd.concat([df, pd.DataFrame(response)], ignore_index=True)
    return df
