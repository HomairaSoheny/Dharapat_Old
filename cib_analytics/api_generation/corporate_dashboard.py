from ..corporate.corporate_class_liability_breakdown import corporate_class_liability_breakdown
from ..corporate.corporate_class_summary_CIB_lIability import corporate_class_summary_CIB_liability
from ..corporate_summary.facility_summary_class import facility_summary_table_class
from ..corporate_summary.corporate_summary_class import summary_table_class
from ..corporate_summary.expired_but_showing_live_class import expired_but_showing_live_table_class
import json

def summary_table(cibs):
    try:
        get_summary_table = summary_table_class(cibs)
        response = []
        for i in range (len(get_summary_table.concern_name)):
                if i<(len(get_summary_table.concern_name)-1):
                    response.append({
                        'Concern name':get_summary_table.concern_name[i],
                        'Funded outstanding': {
                            'Installment': get_summary_table.funded_ins_data[i],
                            'Non installment': get_summary_table.funded_non_ins_data[i],
                            'Total':get_summary_table.total_funded_amount[i]
                        },
                        'Non funded outstanding': get_summary_table.non_funded_amount[i], 
                        'Total outstanding': get_summary_table.total_amount[i],
                        'Overdue': get_summary_table.overdue_amount[i],
                        'Status': get_summary_table.status[i]
                        })
                else:
                    response.append({
                            'Concern name':'sub_total',
                            'Funded outstanding': {
                                'Installment': sum(get_summary_table.funded_ins_data),
                                'Non installment': sum(get_summary_table.funded_non_ins_data),
                                'Total':sum(get_summary_table.total_funded_amount)
                            },
                            'Non funded outstanding': sum(get_summary_table.non_funded_amount), 
                            'Total outstanding': sum(get_summary_table.total_amount),
                            'Overdue': sum(get_summary_table.overdue_amount),
                            'Status': None
                            })  
        return response
    
    except Exception as exc:
        print("Error on CIB summary Table")
        print(exc)
        return []

    

def summary_of_facility(cib_list):
  
    try:
        get_fac_summary = facility_summary_table_class(cib_list)
        Funded_ins_borrower = ((get_fac_summary.Funded_ins_bor).to_json(orient = 'records'))
        Funded_nonins_borrower = ((get_fac_summary.Funded_nonins_bor).to_json(orient = 'records'))
        Funded_ins_guran = ((get_fac_summary.Funded_ins_guran).to_json(orient = 'records'))
        Funded_nonins_guran = ((get_fac_summary.Funded_non_ins_guran).to_json(orient = 'records'))
        Non_Funded_bor = ((get_fac_summary.Nonfunded_bor).to_json(orient = 'records'))
        Non_Funded_guran =  ((get_fac_summary.Nonfunded_bor).to_json(orient = 'records'))
        response = {
                "Summary of funded facility for borrower" : json.loads(Funded_ins_borrower) + json.loads(Funded_nonins_borrower),
                "Summary of funded facility for gurantor" : json.loads(Funded_ins_guran)+ json.loads(Funded_nonins_guran),
                "Summary of non funded facility for borrower": json.loads(Non_Funded_bor),
                "Summary of non funded facility for gurantor": json.loads(Non_Funded_guran)
            }
    
        return response
    except Exception as exc:
        print("Error on CIB summary of facility Table")
        print(exc)
        return []
def summary_of_expired_but_showing_live(cib_list):
    try:

        get_ex_summary = expired_but_showing_live_table_class(cib_list)
        Funded_ins = ((get_ex_summary.Funded_ins).to_json(orient = 'records'))
        Funded_nonins = ((get_ex_summary.Funded_nonins).to_json(orient = 'records'))
        Non_Funded = ((get_ex_summary.Nonfunded).to_json(orient = 'records'))
        response = {
                    "Summary of funded facility" : json.loads(Funded_ins) + json.loads(Funded_nonins),
                    "Summary of non funded facility": json.loads(Non_Funded)
                }
        return response
    except Exception as exc:
        print("Error on CIB summary of expired but showing live Table")
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
        "liability type wise break up": liability_type_wise_breakup(cib),
        "summary table": summary_table(cib),
        "summary of facility": summary_of_facility(cib),
        "summary of expired but showing live": summary_of_expired_but_showing_live(cib)
    }
    
    return corporate_response