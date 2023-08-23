from ..corporate.corporate_class_liability_breakdown import CorporateLiabilityBreakdownClass
from ..corporate.corporate_class_summary_CIB_lIability import CorporateSummaryCIBLiabilityClass
from ..corporate.corporate_summary_class import CorporateSummaryTableClass
from ..corporate.facility_summary_class import CorporateFacilitySummaryTableClass
from ..corporate.expired_but_showing_live_class import CorporateExpiredButShowingLiveClass
from ..corporate.terminated_loan_funded_class import TerminatedLoanFundedTableClass
from ..corporate.terminated_loan_nonfunded_class import TerminatedLoanNonfundedTableClass
from ..corporate.requested_loan_class import RequestedLoanSummaryTableClass
from ..corporate.reschedule_loan_summary_class import RescheduleLoanSummaryTableClass
from ..corporate.stay_order_summary_class import StayOrderSummaryClass

def get_category_wise_summary_table(cib_list):
    try:
        cibs = {"Type a": [],
                "Type b": [],
                "Type c": [],
                "Type d": [],
                "Type e": [],
                "Type f": [],
                "Type g": [],
                "Type h": [],
                "Type i": []}
        for cib in cib_list:
            if cib.cib_category == "Type a":
                cibs["Type a"].append(cib)
            elif cib.cib_category == "Type b":
                cibs["Type b"].append(cib)
            elif cib.cib_category == "Type c":
                cibs["Type c"].append(cib)
            elif cib.cib_category == "Type d":
                cibs["Type d"].append(cib)
            elif cib.cib_category == "Type e":
                cibs["Type e"].append(cib)
            elif cib.cib_category == "Type f":
                cibs["Type f"].append(cib)
            elif cib.cib_category == "Type g":
                cibs["Type g"].append(cib)
            elif cib.cib_category == "Type h":
                cibs["Type h"].append(cib)
            elif cib.cib_category == "Type i":
                cibs["Type i"].append(cib)
        for cib in cibs:
            cibs[cib] = summary_table(cibs[cib])
        return cibs
    except Exception as exc:
        print("Error on summary table")
        print(exc)
        return {}
    


def summary_table(cibs):
    try:
        summary_table = CorporateSummaryTableClass(cibs)
        response = []
        for i in range(len(summary_table.concern_name)):
            if i < (len(summary_table.concern_name)-1):
                response.append({
                    'Concern name': str(summary_table.concern_name[i]),
                    'Funded outstanding': {
                        'Installment': str(summary_table.funded_ins_data[i]),
                        'Non installment': str(summary_table.funded_non_ins_data[i]),
                        'Total': str(summary_table.total_funded_amount[i])
                    },
                    'Non funded outstanding': str(summary_table.non_funded_amount[i]),
                    'Total outstanding': str(summary_table.total_amount[i]),
                    'Overdue': str(summary_table.overdue_amount[i]),
                    'Status': str(summary_table.status[i])
                })
            else:
                response.append({
                    'Concern name': 'sub_total',
                    'Funded outstanding': {
                        'Installment': str(sum(summary_table.funded_ins_data)),
                        'Non installment': str(sum(summary_table.funded_non_ins_data)),
                        'Total': str(sum(summary_table.total_funded_amount))},
                    'Non funded outstanding': str(sum(summary_table.non_funded_amount)),
                    'Total outstanding': str(sum(summary_table.total_amount)),
                    'Overdue': str(sum(summary_table.overdue_amount)),
                    'Status': "",
                })
        return response

    except Exception as exc:
        print("Error on CIB summary Table")
        print(exc)
        return []


def summary_of_facility(cib_list):
    try:
        fac_summary = CorporateFacilitySummaryTableClass(cib_list)
        response = {
            "Summary of funded facility for borrower": {"funded_ins_borrower": fac_summary.funded_ins_bor,
                                                        "funded_nonins_borrower": fac_summary.funded_nonins_bor},
            "Summary of funded facility for gurantor" : {"funded_ins_guran": fac_summary.funded_ins_guran,
                                                        "funded_nonins_guran": fac_summary.funded_non_ins_guran},
            "Summary of non funded facility for borrower": fac_summary.nonfunded_bor,
            "Summary of non funded facility for gurantor": fac_summary.nonfund_guran
        }

        return response
    except Exception as exc:
        print("Error on CIB summary of facility Table")
        print(exc)
        return []
    
def summary_of_reschedule_loan(cibs):
    try:
        res_summary = RescheduleLoanSummaryTableClass(cibs)
        response = {
                "Summary of reschedule loan for borrower": res_summary.reschedule_loan_for_borrower,
                "Summary of reschedule loan for gurantor": res_summary.reschedule_loan_for_gurantor
        }
        return response
    
    except Exception as exc:
        print("Error on CIB summary of Reschedule Loan Table")
        print(exc)
        return []
    
def summary_of_stay_order(cibs):
    try: 
        stay_summary = StayOrderSummaryClass(cibs)
        response = {
            "Summary of stay order for Borrower": stay_summary.stay_order_borrower,
            "Summary of stay order for Gurantor": stay_summary.stay_order_gurantor
        }
        return response
    
    except Exception as exc:
        print("Error on CIB summary of Stay order Table")
        print(exc)
        return []
    
def summary_of_expired_but_showing_live(cib_list):
    try:
        get_ex_summary = CorporateExpiredButShowingLiveClass(cib_list)
        response = {
            "Summary of funded facility": {"funded_ins": get_ex_summary.funded_ins,
                                           "funded_nonins": get_ex_summary.funded_nonins},
            "Summary of non funded facility": get_ex_summary.nonfunded
        }
        return response
    except Exception as exc:
        print("Error on CIB summary of expired but showing live Table")
        print(exc)
        return []
    
def summary_of_funded_terminated_loan(cib_list):
    try:
        get_summary_terminated = TerminatedLoanFundedTableClass(cib_list)
        response = {}
        response['Total funded terminated loan'] = get_summary_terminated.number_of_funded_terminated_loan
        response['Installment Table'] = []
        response['Non Installment Table'] = []
    
        for i in range (len(get_summary_terminated.funded_facility_name)):
          
            response['Installment Table'].append({
                "Installment":get_summary_terminated.funded_facility_name[i],
                "Limit": get_summary_terminated.funded_ins_limit[i],
                "Worse classification status": get_summary_terminated.funded_ins_worse_cl_status[i],
                "Date of classification status": get_summary_terminated.funded_date_of_classification[i]
            })
        for i in range (len(get_summary_terminated.funded_nonins_facility_name)):
        
            response['Non Installment Table'].append({
                "Non installment":get_summary_terminated.funded_nonins_facility_name[i],
                "Limit": get_summary_terminated.funded_nonins_limit[i],
                "Worse classification status": get_summary_terminated.funded_nonins_worse_cl_status[i],
                "Date of classification status": get_summary_terminated.funded_nonins_date_of_classification[i]
            })
        return response
    except Exception as exc:
        print("Error on CIB summary of terminated loan table")
        print(exc)
        return []
    
def summary_of_nonfunded_terminated_loan(cib_list):
    try:   
        get_summary_terminated = TerminatedLoanNonfundedTableClass(cib_list)
        response = {}
        response['Total non funded terminated loan'] = get_summary_terminated.Total_nonfunded_terminated_loan
        response['Facility Table'] = []
        for i in range (len(get_summary_terminated.Non_funded_facility_name)):
            
            response['Facility Table'].append({
                "Facility":get_summary_terminated.Non_funded_facility_name[i],
                "Limit": get_summary_terminated.Non_funded_ins_limit[i],
                "Worse classification status": get_summary_terminated.Non_funded_ins_worse_cl_status[i],
                "Date of classification status": get_summary_terminated.Non_Funded_date_of_classification[i]
            })
        return response
    except Exception as exc:
        print("Error on CIB summary of terminated loan table")
        print(exc)
        return []
    

def summary_of_requested_loan(cib_list):
    try:
        get_summary_requested = RequestedLoanSummaryTableClass(cib_list)
        response = {
            "Type of Contract": get_summary_requested.Funded_ins_bor["Type of Contract"].tolist(),
            "Facility": get_summary_requested.Funded_ins_bor["Facility"].tolist(),
            "Role": get_summary_requested.Funded_ins_bor["Role"].tolist(),
            "Total Requested Amount": get_summary_requested.Funded_ins_bor["Total Requested Amount"].tolist(),
            "Request date": [str(date.date()) for date in get_summary_requested.Funded_ins_bor["Request date"].tolist()]
        }
        return response
    except Exception as exc:
        print("Error on CIB summary of facility Table")
        print(exc)
        return []
    

def summary_of_cib_liability(cib_list):
    try:
        cibs = {"Type a": [],
                "Type b": [],
                "Type c": [],
                "Type d": [],
                "Type e": [],
                "Type f": [],
                "Type g": [],
                "Type h": [],
                "Type i": []}
        for cib in cib_list:
            if cib.cib_category == "Type a":
                cibs["Type a"].append(cib)
            elif cib.cib_category == "Type b":
                cibs["Type b"].append(cib)
            elif cib.cib_category == "Type c":
                cibs["Type c"].append(cib)
            elif cib.cib_category == "Type d":
                cibs["Type d"].append(cib)
            elif cib.cib_category == "Type e":
                cibs["Type e"].append(cib)
            elif cib.cib_category == "Type f":
                cibs["Type f"].append(cib)
            elif cib.cib_category == "Type g":
                cibs["Type g"].append(cib)
            elif cib.cib_category == "Type h":
                cibs["Type h"].append(cib)
            elif cib.cib_category == "Type i":
                cibs["Type i"].append(cib)
        for cib in cibs:
            cibs[cib] = aggregate_corporate_cib(cibs[cib])
        return cibs
    except Exception as exc:
        print("Error on summary_of_cib_liability")
        print(exc)
        return {}


def aggregate_corporate_cib(cib_list):
    response = {
        "funded": {
            "installment": [],
            "no_installment": [],
            "total": []
        },
        "non_funded": [],
        "total": [],
        "overdue": [],
        "cl status": [],
        "default": [],
        "loan amount": {
            "STD": [],
            "SMA": [],
            "SS": [],
            "DF": [],
            "BL": [],
            "BLW": [],
            "stay_order": []
        },
        "remarks": []
    }
    for cib in cib_list:
        summary = CorporateSummaryCIBLiabilityClass(cib)
        response["funded"]["installment"] += list(summary.funded["installment"])
        response["funded"]["no_installment"] += list(summary.funded["no_installment"])
        response["funded"]["total"] += list(summary.funded["total"])
        response["non_funded"] += list(summary.non_funded)
        response["total"] += list(summary.total)
        response["overdue"] += list(summary.overdue)
        response["cl status"] += list(summary.cl_status)
        response["default"] += list(summary.default)
        response["loan amount"]["STD"] += list(summary.loan_amount["STD"])
        response["loan amount"]["SMA"] += list(summary.loan_amount["SMA"])
        response["loan amount"]["SS"] += list(summary.loan_amount["SS"])
        response["loan amount"]["DF"] += list(summary.loan_amount["DF"])
        response["loan amount"]["BL"] += list(summary.loan_amount["BL"])
        response["loan amount"]["BLW"] += list(summary.loan_amount["BLW"])
        response["loan amount"]["stay_order"] += list(summary.loan_amount["stay_order"])
        response["remarks"] += list(summary.remarks)

    return response


def liability_type_wise_breakup(cibs):
    liabilities = CorporateLiabilityBreakdownClass(cibs)
    return liabilities.response


def get_corporate_dashboard(cibs):
    corporate_response = {
        "summary of cib liability": summary_of_cib_liability(cibs),
        "liability type wise break up": liability_type_wise_breakup(cibs),
        "summary table": get_category_wise_summary_table(cibs),
        "summary of facility": summary_of_facility(cibs),
        "summary of expired but showing live": summary_of_expired_but_showing_live(cibs),
        "summary of funded terminated loan": summary_of_funded_terminated_loan(cibs),
        "summary of nonfunded terminated loan": summary_of_nonfunded_terminated_loan(cibs),
        "summary of requested loan": summary_of_requested_loan(cibs),
        "summary of reschedule loan": summary_of_reschedule_loan(cibs),
        "summary of stay order": summary_of_stay_order(cibs)
    }

    return corporate_response