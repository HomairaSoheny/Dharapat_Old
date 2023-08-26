from cib_analytics.general_helpers import pad_dict_list
import pandas as pd

def generate_corporate_spreadsheet(writer, result):
    with writer as writer:
        create_summary_of_cib_liability_spreadsheet(writer, result["summary of cib liability"])
        liability_type_wise_breakup = result["liability type wise break up"]
        get_category_wise_summary_table = result["summary table"]
        summary_of_facility = result["summary of facility"] 
        summary_of_expired_but_showing_live = result["summary of expired but showing live"] 
        summary_of_funded_terminated_loan = result["summary of funded terminated loan"]
        summary_of_nonfunded_terminated_loan = result["summary of nonfunded terminated loan"] 
        summary_of_requested_loan = result["summary of requested loan"]
        summary_of_reschedule_loan = result["summary of reschedule loan"]
        summary_of_stay_order = result["summary of stay order"]

def create_summary_of_cib_liability_spreadsheet(workbook, analysed_data):
    len = 2
    for key in analysed_data:
        data = analysed_data[key]
        data = {
            "installment": data["funded"]["installment"],
            "no_installment": data["funded"]["no_installment"],
            "funded total": data["funded"]["total"],
            "total": data["total"],
            "overdue": data["overdue"],
            "cl status": data["cl status"],
            "default": data["default"],
            'STD': data['loan amount']["STD"],
            'SMA': data['loan amount']["SMA"],
            'SS': data['loan amount']["SS"],
            'DF': data['loan amount']["DF"],
            'BL': data['loan amount']["BL"],
            'BLW': data['loan amount']["BLW"],
            'stay_order': data['loan amount']["stay_order"],
            "remarks": data["remarks"]   
        }
        df = pd.DataFrame(pad_dict_list(data, 0))
        if key == "Type a":
            df.to_excel(workbook, sheet_name="summary of cib liability", startrow=len)
            workbook.sheets["summary of cib liability"].merge_range("A"+str(len-1)+":P"+str(len-1), "Type a")
            workbook.sheets["summary of cib liability"].merge_range("B"+str(len)+":D"+str(len), "Funded")
            workbook.sheets["summary of cib liability"].merge_range("I"+str(len)+":O"+str(len), "Loan Amount")
        else:
            df.to_excel(workbook, sheet_name="summary of cib liability", startrow=len)
            workbook.sheets["summary of cib liability"].merge_range("A"+str(len-1)+":P"+str(len-1), key)
            workbook.sheets["summary of cib liability"].merge_range("B"+str(len)+":D"+str(len), "Funded")
            workbook.sheets["summary of cib liability"].merge_range("I"+str(len)+":O"+str(len), "Loan Amount")
        len += df.shape[0]+5