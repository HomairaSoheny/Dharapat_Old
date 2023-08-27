from cib_analytics.general_helpers import pad_dict_list
import pandas as pd

def generate_corporate_spreadsheet(writer, result):
    with writer as writer:
        create_summary_of_cib_liability_spreadsheet(writer, result["summary of cib liability"])
        create_libility_type_wise_break_up_spreadsheet(writer, result["liability type wise break up"])
        create_summary_table_spreaksheet(writer, result["summary table"])
        summary_of_facility = result["summary of facility"] 
        summary_of_expired_but_showing_live = result["summary of expired but showing live"] 
        create_summary_of_funded_terminated_loan_spreadsheet(writer, result["summary of funded terminated loan"])
        create_summary_of_non_funded_terminated_loan_spreadsheet(writer, result["summary of nonfunded terminated loan"] )
        create_summary_of_requested_loan_spreadsheet(writer, result["summary of requested loan"])
        create_summary_of_reschedule_loan_spreadsheet(writer, result["summary of reschedule loan"])
        create_summary_of_stay_order_spreadsheet(writer, result["summary of stay order"])

def create_summary_table_spreaksheet(workbook, analysed_data):
    len = 2
    for key in analysed_data:
        fixed_dict_data = []
        if analysed_data[key] == []:
            analysed_data[key] = [{
                    "Concern name": [],
                    "Funded outstanding": {
                        "Installment": [],
                        "Non installment": [],
                        "Total": [],   
                    },
                    "Non funded outstanding": [],
                    "Total outstanding": [],
                    "Overdue": [],
                    "Status": []
                }]
        for data in analysed_data[key]:
            fixed_dict_data.append({
                "Concern name": data["Concern name"],
                "Installment": data["Funded outstanding"]["Installment"],
                "Non Installment": data["Funded outstanding"]["Non installment"],
                "Total": data["Funded outstanding"]["Total"],
                "Non funded outstanding": data["Non funded outstanding"],
                "Total outstanding": data["Total outstanding"],
                "Overdue": data["Overdue"],
                "Status": data["Status"]
                })
        df = pd.DataFrame(fixed_dict_data)
        df.to_excel(workbook, sheet_name="summary table", startrow=len)
        workbook.sheets["summary table"].merge_range("A"+str(len-1)+":I"+str(len-1), key)
        workbook.sheets["summary table"].merge_range("C"+str(len)+":E"+str(len), "Funded Outstanding")
        len += df.shape[0]+5
        
    

def create_summary_of_stay_order_spreadsheet(workbook, analysed_data):
    df = pd.DataFrame(analysed_data["Summary of stay order for Borrower"])
    df.to_excel(workbook, sheet_name="Summary of stay order", startrow=1)
    workbook.sheets["Summary of stay order"].merge_range("A1:F1", "Summary of stay order for Borrower")
    
    len = df.shape[0]+5
    
    df = pd.DataFrame(analysed_data["Summary of stay order for Gurantor"])
    df.to_excel(workbook, sheet_name="Summary of stay order", startrow=len)
    workbook.sheets["Summary of stay order"].merge_range("A"+str(len)+":F"+str(len), "Summary of stay order for Gurantor")

def create_summary_of_reschedule_loan_spreadsheet(workbook, analysed_data):
    df = pd.DataFrame(analysed_data["Summary of reschedule loan for borrower"])
    df.to_excel(workbook, sheet_name="Summary of reschedule loan", startrow=1)
    workbook.sheets["Summary of reschedule loan"].merge_range("A1:F1", "Summary of reschedule loan for borrower")
    
    len = df.shape[0]+5
    
    df = pd.DataFrame(analysed_data["Summary of reschedule loan for gurantor"])
    df.to_excel(workbook, sheet_name="Summary of reschedule loan", startrow=len)
    workbook.sheets["Summary of reschedule loan"].merge_range("A"+str(len)+":F"+str(len), "Summary of reschedule loan for gurantor")

def create_summary_of_requested_loan_spreadsheet(workbook, analysed_data):
    df = pd.DataFrame(analysed_data)
    df.to_excel(workbook, sheet_name="summary of requested loan")

def create_summary_of_non_funded_terminated_loan_spreadsheet(workbook, analysed_data):
    df = pd.DataFrame(analysed_data["Facility Table"])
    df.to_excel(workbook, sheet_name="non funded terminated loan", startrow=1)
    workbook.sheets["non funded terminated loan"].merge_range("A1:E1", "Facility Table")

def create_summary_of_funded_terminated_loan_spreadsheet(workbook, analysed_data):
    df = pd.DataFrame(analysed_data["Installment Table"])
    df.to_excel(workbook, sheet_name="funded terminated loan", startrow=1)
    workbook.sheets["funded terminated loan"].merge_range("A1:E1", "Installment Table")
    
    len = df.shape[0]+5
    
    df = pd.DataFrame(analysed_data["Non Installment Table"])
    df.to_excel(workbook, sheet_name="funded terminated loan", startrow=len)
    workbook.sheets["funded terminated loan"].merge_range("A"+str(len)+":E"+str(len), "Non Installment Table")

def create_libility_type_wise_break_up_spreadsheet(workbook, analysed_data):
    len = 1
    for key in analysed_data:
        data = analysed_data[key]
        df = pd.DataFrame(pad_dict_list(data, 0))
        df.to_excel(workbook, sheet_name="liability type wise break up", startrow=len)
        workbook.sheets["liability type wise break up"].merge_range("A"+str(len)+":R"+str(len), key)
        len += df.shape[0]+5
            
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