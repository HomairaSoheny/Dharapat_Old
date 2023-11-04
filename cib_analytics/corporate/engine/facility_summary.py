import pandas as pd
from ...general_helpers import is_living, isNonFunded, isStayOrder, get_worst_status, get_status

def start_date(fac):
    
    '''
    Helper function to extract starting date
    
    Output : day-month-year
    
    '''
    
    if (fac['Ref']['Starting date']) is None:
        date = 'Not present'
    else:
        date = fac['Ref']['Starting date']
        date = str(date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
    return date

def end_date(fac):
    '''
    Helper function to extract starting date
    
    Output : day-month-year
    
    '''
    
    if (fac['Ref']['End date of contract']) is None:
        date = 'Not present'
    else:
        date = fac['Ref']['End date of contract']
        date = str(date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
    return date


def last_pay_date(fac):
    '''
    Helper function to extract date of last payment
    
    Output : day-month-year
    
    '''
    if (fac['Ref']['Date of last payment']) is None:
        date = 'Not present'
    else:
        date = fac['Ref']['Date of last payment']
        date = (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
    return str(date)

def get_NPI(fac : dict):
    '''
    Return 
    ----------
    Npi from NPI column of installment facility
    
    '''
    if not isStayOrder(fac):
        return str(fac["Contract History"].NPI[0])
    return "None"

def funded_ins(fac):
    """
    returns
    -------
        Installment Facility : Latest value of "Sanction Limit" from "Contract History"
            for Installment facilities with Stay Order (No contract history), returns <None>
    
    """
    if not isStayOrder(fac):
        return str(fac['Ref']['Sanction Limit'])
    return "None"    

def funded_non_ins(fac):
    """
    returns
    -------
        Non-Installment Facility : Latest value of "SancLmt" from "Contract History"
            for Non-Installment facilities with Stay Order (No contract history), returns <None>
        
    """
    if not isStayOrder(fac):
        return str(fac["Contract History"].SancLmt.values[0])
    return "None"

def facility_name(fac):                    
    return str(fac['Ref']['Facility'])

def get_outstanding(fac):
    """
    if not Stay Order
        Installment Facility : latest Outstand value from Contract History 
        Non-Installment Facility : lastest Outstand value from Contract History
        Credit Card Facility : lastest Outstanding value from Contract History
    """
    if not isStayOrder(fac):
        if "Outstand" in fac["Contract History"].columns:
            return str(fac["Contract History"].Outstand[0])
        return str(fac["Contract History"].Outstanding[0])
    return "None"

def funded_ins_overdue(fac):
    if not isStayOrder(fac):
        return str(fac['Contract History']['Overdue'][0])
    return "None"

def funded_non_ins_overdue(fac):
    if not isStayOrder(fac):
        return str(fac['Contract History'].sort_values('Date', ascending=False).Overdue[0])
    return "None"
                        
def funded_ins_amount(fac):
    return str(fac['Ref']['Installment Amount'])
                            
def funded_pay_period(fac):
    return str(fac['Ref']['Payments periodicity'])

def no_installment(fac):
    return str(fac['Ref']['Total number of installments'])
                            

def no_installment_paid(fac):
    
    return str((fac['Ref']['Total number of installments']) - (fac['Ref']['Remaining installments Number']))

def remaining_ins(fac):
    return str(fac['Ref']['Remaining installments Number'])

def pay_period(fac): 
    return str(fac['Ref']['Payments periodicity'])
                        
def reorganized_credit(fac):
    return str(fac['Ref']['Reorganized credit'])
     
def default(fac):
    if isStayOrder(fac):
        return "None"
    return str(fac['Contract History'].Default[0])

def get_remarks(fac: dict):
    if fac['Ref']['Remarks'] is not None:
        return str(fac['Ref']['Remarks'])
    return "None"

def funded_ins_borrow(cib_list:list):
    '''
    Summary of funded (installment and non-installment facility) facility table for borrower 
    '''
    
    columns = ['Installment', 'Limit', 'Outstanding', 'Overdue', 'Start Date','End Date of Contract', 'Installment amount', 'Payment Period', 
              'Total No. of Installment', 'Total no. of Installment paid', 'No. of Remaining Installment','Date of Last Payment', 'NPI (No.)',
              'Default ', 'Current Status','Worst Status', 'Reorganized Credit', 'Remarks']
    table = []
    for cib_data in cib_list:
        if type(cib_data.installment_facility) == list:
            for fac in cib_data.installment_facility:
                 if fac['Ref']['Role'] != "Guarantor": 
                    if is_living(fac) == True and isNonFunded(fac) != True:
                        
                        row = [facility_name(fac),funded_ins(fac),get_outstanding(fac),  funded_ins_overdue(fac),
                            start_date(fac), end_date(fac), funded_ins_amount(fac), pay_period(fac), no_installment(fac),
                            no_installment_paid(fac), remaining_ins(fac), last_pay_date(fac), get_NPI(fac), default(fac), 
                            get_status(fac), get_worst_status(fac), reorganized_credit(fac),  get_remarks(fac)]
        
                        
                        table.append(row)
    table = pd.DataFrame(table, columns = columns)
    response = {
        "Installment": table["Installment"].tolist(),
        "Limit": table["Limit"].tolist(),
        "Outstanding": table["Outstanding"].tolist(),
        "Overdue": table["Overdue"].tolist(),
        "Start Date": table["Start Date"].tolist(),
        "End Date of Contract": table["End Date of Contract"].tolist(),
        "Installment amount": table["Installment amount"].tolist(),
        "Payment Period": table["Payment Period"].tolist(),
        "Total No. of Installment": table["Total No. of Installment"].tolist(),
        "Total no. of Installment paid": table["Total no. of Installment paid"].tolist(),
        "No. of Remaining Installment": table["No. of Remaining Installment"].tolist(),
        "Date of Last Payment": table["Date of Last Payment"].tolist(),
        "NPI (No.)": table["NPI (No.)"].tolist(),
        "Default ": table["Default "].tolist(),
        "Current Status": table["Current Status"].tolist(),
        "Worst Status": table["Worst Status"].tolist(),
        "Reorganized Credit": table["Reorganized Credit"].tolist(),
        "Remarks": table["Remarks"].tolist()
    }            
    # return pd.DataFrame(table, columns = columns)
    return response

def funded_nonins_borrow(cib_list:list):
    '''
    Summary of funded (installment and non-installment facility) facility table for borrower 
    '''
    columns = ['Non Installment', 'Limit', 'Outstanding', 'Overdue', 'Start Date','End Date of Contract', 'Installment amount', 'Payment Period', 
              'Total No. of Installment', 'Total no. of Installment paid', 'No. of Remaining Installment','Date of Last Payment', 'NPI (No.)',
              'Default ', 'Current Status','Worst Status', 'Reorganized Credit', 'Remarks']
    table = []
    for cib_data in cib_list: 
      
        if type(cib_data.noninstallment_facility) == list:
            for fac in cib_data.noninstallment_facility:
                 if fac['Ref']['Role'] != "Guarantor": 
                    if is_living(fac) == True and isNonFunded(fac) != True:
                        
                        row = [facility_name(fac),funded_non_ins(fac), get_outstanding(fac),  funded_non_ins_overdue(fac),
                            start_date(fac), end_date(fac),' ' , ' ', ' ',' ', ' ', ' ', ' ', ' ', 
                            get_status(fac), get_worst_status(fac), reorganized_credit(fac),  get_remarks(fac)]
                        table.append(row)
                        
    table = pd.DataFrame(table, columns = columns)
    response = {
        "Non Installment": table["Non Installment"].tolist(),
        "Limit": table["Limit"].tolist(),
        "Outstanding": table["Outstanding"].tolist(),
        "Overdue": table["Overdue"].tolist(),
        "Start Date": table["Start Date"].tolist(),
        "End Date of Contract": table["End Date of Contract"].tolist(),
        "Installment amount": table["Installment amount"].tolist(),
        "Payment Period": table["Payment Period"].tolist(),
        "Total No. of Installment": table["Total No. of Installment"].tolist(),
        "Total no. of Installment paid": table["Total no. of Installment paid"].tolist(),
        "No. of Remaining Installment": table["No. of Remaining Installment"].tolist(),
        "Date of Last Payment": table["Date of Last Payment"].tolist(),
        "NPI (No.)": table["NPI (No.)"].tolist(),
        "Default ": table["Default "].tolist(),
        "Current Status": table["Current Status"].tolist(),
        "Worst Status": table["Worst Status"].tolist(),
        "Reorganized Credit": table["Reorganized Credit"].tolist(),
        "Remarks": table["Remarks"].tolist(),
    }                     
    #return pd.DataFrame(table, columns=columns)
    return response


def funded_ins_guran(cib_list:list):
    '''
    Summary of funded (installment) facility table for gurantor 
    '''
    
    columns = ['Installment', 'Limit', 'Outstanding', 'Overdue', 'Start Date','End Date of Contract', 'Installment amount', 'Payment Period', 
              'Total No. of Installment', 'Total no. of Installment paid', 'No. of Remaining Installment','Date of Last Payment', 'NPI (No.)',
              'Default ', 'Current Status','Worst Status', 'Reorganized Credit', 'Remarks']

    table = []
    for cib_data in cib_list:
        if type(cib_data.installment_facility) == list:
            for fac in cib_data.installment_facility:
                 if fac['Ref']['Role'] == "Guarantor": 
                    if is_living(fac) == True and isNonFunded(fac) != True:
                        row = [facility_name(fac),funded_ins(fac),get_outstanding(fac),  funded_ins_overdue(fac),
                            start_date(fac), end_date(fac), funded_ins_amount(fac), pay_period(fac), no_installment(fac),
                            no_installment_paid(fac), remaining_ins(fac), last_pay_date(fac), get_NPI(fac), default(fac), 
                            get_status(fac), get_worst_status(fac), reorganized_credit(fac),  get_remarks(fac)]
                        table.append(row)
    table = pd.DataFrame(table, columns=columns)
    response = {
        "Installment": table["Installment"].tolist(),
        "Limit": table["Limit"].tolist(),
        "Outstanding": table["Outstanding"].tolist(),
        "Overdue": table["Overdue"].tolist(),
        "Start Date": table["Start Date"].tolist(),
        "End Date of Contract": table["End Date of Contract"].tolist(),
        "Installment amount": table["Installment amount"].tolist(),
        "Payment Period": table["Payment Period"].tolist(),
        "Total No. of Installment": table["Total No. of Installment"].tolist(),
        "Total no. of Installment paid": table["Total no. of Installment paid"].tolist(),
        "No. of Remaining Installment": table["No. of Remaining Installment"].tolist(),
        "Date of Last Payment": table["Date of Last Payment"].tolist(),
        "NPI (No.)": table["NPI (No.)"].tolist(),
        "Default ": table["Default "].tolist(),
        "Current Status": table["Current Status"].tolist(),
        "Worst Status": table["Worst Status"].tolist(),
        "Reorganized Credit": table["Reorganized Credit"].tolist(),
        "Remarks": table["Remarks"].tolist(),
    }
    return response

def funded_nonins_guran(cib_list:list):
    '''
    Summary of funded (non-installment) facility table for gurantor 
    '''
    columns = ['Non Installment', 'Limit', 'Outstanding', 'Overdue', 'Start Date','End Date of Contract', 'Installment amount', 'Payment Period', 
              'Total No. of Installment', 'Total no. of Installment paid', 'No. of Remaining Installment','Date of Last Payment', 'NPI (No.)',
              'Default ', 'Current Status','Worst Status', 'Reorganized Credit', 'Remarks']

    table = []
    for cib_data in cib_list:                       
        if type(cib_data.noninstallment_facility) == list:
            for fac in cib_data.noninstallment_facility:
                 if fac['Ref']['Role'] == "Guarantor": 
                    if is_living(fac) == True and isNonFunded(fac) != True:
                        
                        row = [facility_name(fac),funded_non_ins(fac), get_outstanding(fac),  funded_non_ins_overdue(fac),
                            start_date(fac), end_date(fac),' ' , ' ', ' ',' ', ' ', ' ', ' ', ' ', 
                            get_status(fac), get_worst_status(fac), reorganized_credit(fac),  get_remarks(fac)]
        
                        table.append(row)
                        
    table = pd.DataFrame(table, columns = columns)
    response = {
        "Non Installment": table["Non Installment"].tolist(),
        "Limit": table["Limit"].tolist(),
        "Outstanding": table["Outstanding"].tolist(),
        "Overdue": table["Overdue"].tolist(),
        "Start Date": table["Start Date"].tolist(),
        "End Date of Contract": table["End Date of Contract"].tolist(),
        "Installment amount": table["Installment amount"].tolist(),
        "Payment Period": table["Payment Period"].tolist(),
        "Total No. of Installment": table["Total No. of Installment"].tolist(),
        "Total no. of Installment paid": table["Total no. of Installment paid"].tolist(),
        "No. of Remaining Installment": table["No. of Remaining Installment"].tolist(),
        "Date of Last Payment": table["Date of Last Payment"].tolist(),
        "NPI (No.)": table["NPI (No.)"].tolist(),
        "Default ": table["Default "].tolist(),
        "Current Status": table["Current Status"].tolist(),
        "Worst Status": table["Worst Status"].tolist(),
        "Reorganized Credit": table["Reorganized Credit"].tolist(),
        "Remarks": table["Remarks"].tolist(),
    }
                        
    #return pd.DataFrame(table, columns=columns)
    return response


def nonfunded_borrow(cib_list:list):
    '''
    Summary of Non funded (installment and non-installment facility) facility table for borrower 
    '''
    
    columns = ['Non Installment', 'Limit', 'Outstanding', 'Overdue', 'Start Date','End Date of Contract', 'Installment amount', 'Payment Period', 
              'Total No. of Installment', 'Total no. of Installment paid', 'No. of Remaining Installment','Date of Last Payment', 'NPI (No.)',
              'Default ', 'Current Status','Worst Status', 'Reorganized Credit', 'Remarks']
    table = []
    for cib_data in cib_list:  
        if type(cib_data.noninstallment_facility) == list:
            for fac in cib_data.noninstallment_facility:
                 if fac['Ref']['Role'] != "Guarantor": 
                    if is_living(fac) == True and isNonFunded(fac) == True:
                        
                        row = [facility_name(fac),funded_non_ins(fac), get_outstanding(fac),  funded_non_ins_overdue(fac),
                            start_date(fac), end_date(fac),' ' , ' ', ' ',' ', ' ', ' ', ' ', ' ', 
                            get_status(fac), get_worst_status(fac), reorganized_credit(fac),  get_remarks(fac)]
                        table.append(row)

                        
    table = pd.DataFrame(table, columns = columns)
    response = {
        "Non Installment": table["Non Installment"].tolist(),
        "Limit": table["Limit"].tolist(),
        "Outstanding": table["Outstanding"].tolist(),
        "Overdue": table["Overdue"].tolist(),
        "Start Date": table["Start Date"].tolist(),
        "End Date of Contract": table["End Date of Contract"].tolist(),
        "Installment amount": table["Installment amount"].tolist(),
        "Payment Period": table["Payment Period"].tolist(),
        "Total No. of Installment": table["Total No. of Installment"].tolist(),
        "Total no. of Installment paid": table["Total no. of Installment paid"].tolist(),
        "No. of Remaining Installment": table["No. of Remaining Installment"].tolist(),
        "Date of Last Payment": table["Date of Last Payment"].tolist(),
        "NPI (No.)": table["NPI (No.)"].tolist(),
        "Default ": table["Default "].tolist(),
        "Current Status": table["Current Status"].tolist(),
        "Worst Status": table["Worst Status"].tolist(),
        "Reorganized Credit": table["Reorganized Credit"].tolist(),
        "Remarks": table["Remarks"].tolist(),
    }
                        
    #return pd.DataFrame(table, columns=columns)
    return response

def nonfunded_guran(cib_list:list):
    '''
    Summary of Non funded (installment and non-installment facility) facility table for borrower 
    '''
    
    columns = ['Non Installment', 'Limit', 'Outstanding', 'Overdue', 'Start Date','End Date of Contract', 'Installment amount', 'Payment Period', 
              'Total No. of Installment', 'Total no. of Installment paid', 'No. of Remaining Installment','Date of Last Payment', 'NPI (No.)',
              'Default ', 'Current Status','Worst Status', 'Reorganized Credit', 'Remarks']
    table = []
    for cib_data in cib_list:  
        if type(cib_data.noninstallment_facility) == list:
            for fac in cib_data.noninstallment_facility:
                 if fac['Ref']['Role'] == "Guarantor": 
                    if is_living(fac) == True and isNonFunded(fac) == True:
                        
                        row = [facility_name(fac),funded_non_ins(fac), get_outstanding(fac),  funded_non_ins_overdue(fac),
                            start_date(fac), end_date(fac),' ' , ' ', ' ',' ', ' ', ' ', ' ', ' ', 
                            get_status(fac), get_worst_status(fac), reorganized_credit(fac),  get_remarks(fac)]
                        table.append(row)

                        
    table = pd.DataFrame(table, columns = columns)
    response = {
        "Non Installment": table["Non Installment"].tolist(),
        "Limit": table["Limit"].tolist(),
        "Outstanding": table["Outstanding"].tolist(),
        "Overdue": table["Overdue"].tolist(),
        "Start Date": table["Start Date"].tolist(),
        "End Date of Contract": table["End Date of Contract"].tolist(),
        "Installment amount": table["Installment amount"].tolist(),
        "Payment Period": table["Payment Period"].tolist(),
        "Total No. of Installment": table["Total No. of Installment"].tolist(),
        "Total no. of Installment paid": table["Total no. of Installment paid"].tolist(),
        "No. of Remaining Installment": table["No. of Remaining Installment"].tolist(),
        "Date of Last Payment": table["Date of Last Payment"].tolist(),
        "NPI (No.)": table["NPI (No.)"].tolist(),
        "Default ": table["Default "].tolist(),
        "Current Status": table["Current Status"].tolist(),
        "Worst Status": table["Worst Status"].tolist(),
        "Reorganized Credit": table["Reorganized Credit"].tolist(),
        "Remarks": table["Remarks"].tolist(),
    }
                        
    #return pd.DataFrame(table, columns=columns)
    return response

