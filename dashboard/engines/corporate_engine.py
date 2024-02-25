import pandas as pd
from dashboard.engines import general_engine
from dashboard.engines.keywords import *
from utils.general_helper import *
from utils.env import LINK


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
        "Updated Overdue and CL Status": "Need More Clarification",
    }


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
                            "CIB Link": LINK + cib.pdf_name
                        }
                    )
            df = pd.concat([df, pd.DataFrame(response)], ignore_index=True)
    return df
