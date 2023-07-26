from ..corporate.corporate_class_liability_breakdown import corporate_class_liability_breakdown
from ..corporate.corporate_class_summary_CIB_lIability import corporate_class_summary_CIB_liability

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
        print("Error on consumer table 2")
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
        summary = corporate_class_summary_CIB_liability(cib)
        response["funded"]["installment"] += summary.funded["installment"]
        response["funded"]["no_installment"] += summary.funded["no_installment"]
        response["funded"]["total"] += summary.funded["total"]
        response["non_funded"] += list(summary.non_funded)
        response["total"] += list(summary.total)
        response["overdue"] += list(summary.overdue)
        response["cl status"] += list(summary.cl_status)
        response["default"] += list(summary.default)
        response["loan amount"]["STD"] += summary.loan_amount["STD"]
        response["loan amount"]["SMA"] += summary.loan_amount["SMA"]
        response["loan amount"]["SS"] += summary.loan_amount["SS"]
        response["loan amount"]["DF"] += summary.loan_amount["DF"]
        response["loan amount"]["BL"] += summary.loan_amount["BL"]
        response["loan amount"]["BLW"] += summary.loan_amount["BLW"]
        response["loan amount"]["stay_order"] += summary.loan_amount["stay_order"]
        response["remarks"] += summary.remarks
        
    return response
        

def liability_type_wise_breakup(cib):
    return []

def get_corporate_dashboard(cib):
    corporate_response = {
        "summary of cib liability": summary_of_cib_liability(cib),
        "liability type wise break up": liability_type_wise_breakup(cib)
    }
    
    return corporate_response