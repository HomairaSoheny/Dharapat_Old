from ..corporate_summary.facility_summary_class import facility_summary_table_class
from ..corporate_summary.corporate_summary_class import summary_table_class
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
    






