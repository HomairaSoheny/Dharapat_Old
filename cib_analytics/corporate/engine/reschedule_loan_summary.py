import pandas as pd

def is_living(facility):
    if facility["Ref"]["Phase"] == "Living":
        return True
    else:
        return False
def isStayOrder(fac):
    if type(fac['Contract History']) == dict and 'Stay Order' in fac['Contract History'].keys():
        return True

def has_rescheduling_instance(fac : dict):
    for key in fac['Ref'].keys():
        if key.lower().replace(' ','')=='numberoftime(s)rescheduled':
            if fac['Ref'][key]!='' and fac['Ref'][key]!=0:
                return True

    for key in fac['Ref'].keys():
        if key.replace(' ','')=='Dateoflastrescheduling':
            if not isinstance(fac['Ref'][key], type(None)):
                return True

    return False
#def acc_name(fac):
#    return (fac['Ref']['Facility'])
def get_title_trade_name(cib):
    if 'Trade Name' in cib.subject_info.keys():
        return cib.subject_info['Trade Name']

    return cib.subject_info['Title, Name']
def reschedule_type(fac):
    for key in fac['Ref'].keys():
        if key.lower().replace(' ','')=='numberoftime(s)rescheduled':
            if fac['Ref'][key]!='' and type(fac['Ref'][key]) is  str:
                return (fac['Ref'][key])
            else: 
                return "--"
def no_reschedule_loan(fac):
    for key in fac['Ref'].keys():
        if key.lower().replace(' ','')=='numberoftime(s)rescheduled':
            if fac['Ref'][key]!='' and type(fac['Ref'][key]) is not str:
                return (int(fac['Ref'][key]))
            else: 
                return "--"
def sec_amount(fac):
    return (fac['Ref']['Security Amount'])

def last_res_date(fac):
    for key in fac['Ref'].keys():
        if key.replace(' ','')=='Dateoflastrescheduling':
            if (fac['Ref'][key]) is None:
                date = 'Not present'
            else:
                date = fac['Ref'][key]
                date = (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
            
    return date

def rescheduled_loan_borrow(cib_list:list):
    '''
    Summary of Rescheduled loan (installment and non-installment facility) facility table for borrower 
    '''
    try:
        columns = ['Name of account', 'type of Reschedule', 'No. of reschedule Loan', 'Amount', 'Date of last rescheduling']
        table = []
        
        for cib_data in cib_list:  
            acc_name = get_title_trade_name(cib_data)
            for facility in (cib_data.noninstallment_facility, cib_data.installment_facility):
                if not isinstance(facility, type(None)):
                    for fac in facility:
                        if  not isStayOrder(fac) and fac['Ref']['Role'] != "Guarantor": 
                            if is_living(fac) is True and has_rescheduling_instance(fac) is True:
                                    
                                row = [ acc_name,  reschedule_type(fac), no_reschedule_loan(fac), sec_amount(fac), last_res_date(fac)]
                                table.append(row)

                            
        table = pd.DataFrame(table, columns=columns)
        response = {
            "Name of account": table["Name of account"].tolist(),
            "type of Reschedule": table["type of Reschedule"].tolist(),
            "No. of reschedule Loan": table["No. of reschedule Loan"].tolist(),
            "Amount": table["Amount"].tolist(),
            "Date of last rescheduling": table["Date of last rescheduling"].tolist(),
        }
        
        return response
        
    except Exception as exc:
        print("function: reschedule_loan_borrow")
        print(exc)
        return []

    except Exception as exc:
        print("function: reschedule_loan_borrow")
        print(exc)
        return []


def rescheduled_loan_guran(cib_list:list):
    '''
    Summary of Rescheduled loan (installment and non-installment facility)  table for gurantor
    '''
    try: 
        columns = ['Name of account', 'type of Reschedule', 'Number of reschedule Loan', 'Amount', 'Date of last rescheduling']
        table = []
        for cib_data in cib_list:  
            acc_name = get_title_trade_name(cib_data)
            for facility in (cib_data.noninstallment_facility, cib_data.installment_facility):
                if not isinstance(facility, type(None)):
                    for fac in facility:
                        if  not isStayOrder(fac) and fac['Ref']['Role'] == "Guarantor": 
                            if is_living(fac) is True and has_rescheduling_instance(fac) is True:    
                                row = [ acc_name,  reschedule_type(fac), no_reschedule_loan(fac), sec_amount(fac), last_res_date(fac)]
                                table.append(row)

                            
        table = pd.DataFrame(table, columns=columns)
        return {
            "Name of account": table["Name of account"].tolist(),
            "type of Reschedule": table["type of Reschedule"].tolist(),
            "Number of reschedule Loan": table["Number of reschedule Loan"].tolist(),
            "Amount": table["Amount"].tolist(),
            "Date of last rescheduling": table["Date of last rescheduling"].tolist()
        }
        
    except Exception as exc:
        print("function: reschedule_loan_guran")
        print(exc)
        return []
