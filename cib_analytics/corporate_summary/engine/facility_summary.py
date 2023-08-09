import pandas as pd


def is_living(fac):
    if fac["Ref"]["Phase"] == "Living":
        return True
    else:
        return False
    
    
    
def isNonFunded(fac):
    """
    much faster than regex matching

    classification of non funded based on IDLC response
    Non-Funded : LC (Letter of Credit), BG (Bank Guarantee), Guarantee, Payment Guarantee
    """
    if ('non funded' in fac["Ref"]["Facility"].lower() or
        'letter of credit' in fac["Ref"]["Facility"].lower() or
        'guarantee' in fac["Ref"]["Facility"].lower() or
        'other indirect facility' in fac["Ref"]["Facility"].lower() ):

        return True
    
def get_status(fac : dict):
    if not isStayOrder(fac):
        return fac["Contract History"].Status[0]
    return None 

def get_class_from_set(classes : set):
    for classification in ('BLW', 'BL', 'DF', 'SS', 'SMA', 'UC', "STD"):
        if classification in classes:
            return classification
    return None
def get_worst_status(fac: dict):

    if not isStayOrder(fac):
        return get_class_from_set(set(fac["Contract History"].Status))

    return None

def start_date(fac):
    
    '''
    Helper function to extract starting date
    
    Output : day-month-year
    
    '''
    
    if (fac['Ref']['Starting date']) is None:
        date = 'Not present'
    else:
        date = fac['Ref']['Starting date']
        date = (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
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
        date = (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
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
    return date
def get_NPI(fac : dict):
    '''
    Return 
    ----------
    Npi from NPI column of installment facility
    
    '''
    if not isStayOrder(fac):
        return fac["Contract History"].NPI[0]

    return None

def isStayOrder(fac):
    if type(fac['Contract History']) == dict and 'Stay Order' in fac['Contract History'].keys():
        return True

    return False

def funded_ins(fac):
    """
    returns
    -------
        Installment Facility : Latest value of "Sanction Limit" from "Contract History"
            for Installment facilities with Stay Order (No contract history), returns <None>
    
    """
    if not isStayOrder(fac):
        return fac['Ref']['Sanction Limit']

    return None    

def funded_non_ins(fac):
    """
    returns
    -------
        Non-Installment Facility : Latest value of "SancLmt" from "Contract History"
            for Non-Installment facilities with Stay Order (No contract history), returns <None>
        
    """
      
    if not isStayOrder(fac):
        return fac["Contract History"].SancLmt.values[0]
    return None


def facility_name(fac):                    

    return fac['Ref']['Facility']


    

def get_outstanding(fac):
    """
    if not Stay Order
        Installment Facility : latest Outstand value from Contract History 
        Non-Installment Facility : lastest Outstand value from Contract History
        Credit Card Facility : lastest Outstanding value from Contract History
    """
    if not isStayOrder(fac):
        if "Outstand" in fac["Contract History"].columns:
            return fac["Contract History"].Outstand[0]

        return fac["Contract History"].Outstanding[0]

    return None
def funded_ins_overdue(fac):
    if not isStayOrder(fac):
        return fac['Contract History']['Overdue'][0]
    return None
def funded_non_ins_overdue(fac):
    if not isStayOrder(fac):
        return fac['Contract History'].sort_values('Date', ascending=False).Overdue [0]
    return None


                        
def funded_ins_amount(fac):

    return fac['Ref']['Installment Amount']
                            
def funded_pay_period(fac):
    
    return fac['Ref']['Payments periodicity']
                            



def no_installment(fac):

    return fac['Ref']['Total number of installments']
                            

def no_installment_paid(fac):
    
 
    paid_ins = (fac['Ref']['Total number of installments']) - (fac['Ref']['Remaining installments Number'])
                            
    return paid_ins

def remaining_ins(fac):
    return fac['Ref']['Remaining installments Number']
def pay_period(fac):
 
    return fac['Ref']['Payments periodicity']
                        
                            


def reorganized_credit(fac):
    return fac['Ref']['Reorganized credit']
     
    
def default(fac):
    
    if isStayOrder(fac):
        return None
    return fac['Contract History'].Default[0]

def get_remarks(fac: dict):
    if fac['Ref']['Remarks'] is not None:
        return fac['Ref']['Remarks']
    return None 
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
                
    return pd.DataFrame(table, columns = columns)
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
                        
    return pd.DataFrame(table, columns=columns)


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
    return pd.DataFrame(table, columns=columns)

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
                        
    return pd.DataFrame(table, columns=columns)


def Nonfunded_borrow(cib_list:list):
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

                        
    return pd.DataFrame(table, columns=columns)

def Nonfunded_guran(cib_list:list):
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

                        
    return pd.DataFrame(table, columns=columns)

