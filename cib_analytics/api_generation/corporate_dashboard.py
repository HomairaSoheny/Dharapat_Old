from ..corporate.corporate_class_liability_breakdown import CorporateLiabilityBreakdownClass
from ..corporate.corporate_class_summary_CIB_lIability import CorporateSummaryCIBLiabilityClass
from ..corporate.corporate_summary_class import CorporateSummaryTableClass
from ..corporate.facility_summary_class import CorporateFacilitySummaryTableClass
from ..corporate.expired_but_showing_live_class import CorporateExpiredButShowingLiveClass
from ..corporate.terminated_loan_funded_class import TerminatedLoanFundedTableClass
from ..corporate.terminated_loan_nonfunded_class import TerminatedLoanNonfundedTableClass
from ..corporate.requested_loan_class import RequestedLoanSummaryTableClass

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
        get_summary_table = CorporateSummaryTableClass(cibs)
        response = []
        for i in range(len(get_summary_table.concern_name)):
            if i < (len(get_summary_table.concern_name)-1):
                response.append({
                    'Concern name': str(get_summary_table.concern_name[i]),
                    'Funded outstanding': {
                        'Installment': str(get_summary_table.funded_ins_data[i]),
                        'Non installment': str(get_summary_table.funded_non_ins_data[i]),
                        'Total': str(get_summary_table.total_funded_amount[i])
                    },
                    'Non funded outstanding': str(get_summary_table.non_funded_amount[i]),
                    'Total outstanding': str(get_summary_table.total_amount[i]),
                    'Overdue': str(get_summary_table.overdue_amount[i]),
                    'Status': str(get_summary_table.status[i])
                })
            else:
                response.append({
                    'Concern name': 'sub_total',
                    'Funded outstanding': {
                        'Installment': str(sum(get_summary_table.funded_ins_data)),
                        'Non installment': str(sum(get_summary_table.funded_non_ins_data)),
                        'Total': str(sum(get_summary_table.total_funded_amount))},
                    'Non funded outstanding': str(sum(get_summary_table.non_funded_amount)),
                    'Total outstanding': str(sum(get_summary_table.total_amount)),
                    'Overdue': str(sum(get_summary_table.overdue_amount)),
                    'Status': "",
                })
        return response

    except Exception as exc:
        print("Error on CIB summary Table")
        print(exc)
        return []


def summary_of_facility(cib_list):
    try:
        get_fac_summary = CorporateFacilitySummaryTableClass(cib_list)
        Funded_ins_borrower = get_fac_summary.funded_ins_bor
        Funded_nonins_borrower = get_fac_summary.funded_nonins_bor
        Funded_ins_guran = get_fac_summary.funded_ins_guran
        Funded_nonins_guran = get_fac_summary.funded_non_ins_guran
        Non_Funded_bor = get_fac_summary.nonfunded_bor
        Non_Funded_guran = get_fac_summary.nonfund_guran
        response = {
            "Summary of funded facility for borrower": {"funded_ins_borrower": Funded_ins_borrower,
                                                        "funded_nonins_borrower": Funded_nonins_borrower},
            "Summary of funded facility for gurantor" : {"funded_ins_guran": Funded_ins_guran,
                                                        "funded_nonins_guran": Funded_nonins_guran},
            "Summary of non funded facility for borrower": Non_Funded_bor,
            "Summary of non funded facility for gurantor": Non_Funded_guran
        }

        return response
    except Exception as exc:
        print("Error on CIB summary of facility Table")
        print(exc)
        return []


def summary_of_expired_but_showing_live(cib_list):
    try:

        get_ex_summary = CorporateExpiredButShowingLiveClass(cib_list)
        Funded_ins = get_ex_summary.Funded_ins
        Funded_nonins = get_ex_summary.Funded_nonins
        Non_Funded = get_ex_summary.Nonfunded
        response = {
            "Summary of funded facility": {"funded_ins": Funded_ins,
                                           "funded_nonins": Funded_nonins},
            "Summary of non funded facility": Non_Funded
        }
        return response
    except Exception as exc:
        print("Error on CIB summary of expired but showing live Table")
        print(exc)
        return []
    
def summary_of_funded_terminated_loan(cib_list):
    try:
        get_summary_terminated = TerminatedLoanFundedTableClass(cib_list)
        response = []
        response.append({'Total funded terminated loan': get_summary_terminated.number_of_funded_terminated_loan})
    
        for i in range (len(get_summary_terminated.Funded_facility_name)):
          
            response.append({
                "Installment":get_summary_terminated.Funded_facility_name[i],
                "Limit": get_summary_terminated.Funded_ins_limit[i],
                "Worse classification status": get_summary_terminated.Funded_ins_worse_cl_status[i],
                "Date of classification status": get_summary_terminated.Funded_date_of_classification[i]
            })
        for i in range (len(get_summary_terminated.Funded_nonins_facility_name)):
        
            response.append({
                "Non installment":get_summary_terminated.Funded_nonins_facility_name[i],
                "Limit": get_summary_terminated.Funded_nonins_limit[i],
                "Worse classification status": get_summary_terminated.Funded_nonins_worse_cl_status[i],
                "Date of classification status": get_summary_terminated.Funded_nonins_date_of_classification[i]
            })
        return response
    except Exception as exc:
        print("Error on CIB summary of terminated loan table")
        print(exc)
        return []
    
def summary_of_nonfunded_terminated_loan(cib_list):
    try:   
        get_summary_terminated = TerminatedLoanNonfundedTableClass(cib_list)
        response = []
        response.append({'Total non funded terminated loan': get_summary_terminated.Total_nonfunded_terminated_loan})
        for i in range (len(get_summary_terminated.Non_funded_facility_name)):
            
            response.append({
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


def liability_type_wise_breakup(cib):
    return []


def get_corporate_dashboard(cib):
    corporate_response = {
        "summary of cib liability": summary_of_cib_liability(cib),
        "liability type wise break up": liability_type_wise_breakup(cib),
        "summary table": get_category_wise_summary_table(cib),
        "summary of facility": summary_of_facility(cib),
        "summary of expired but showing live": summary_of_expired_but_showing_live(cib),
        "summary of funded terminated loan": summary_of_funded_terminated_loan(cib),
        "summary of nonfunded terminated loan": summary_of_nonfunded_terminated_loan(cib),
        "summary of requested loan": summary_of_requested_loan(cib)
    }

    return corporate_response
