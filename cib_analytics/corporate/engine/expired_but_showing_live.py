import pandas as pd

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
    
def expired_live_loan_check(fac, date_of_inquiry):

    if fac['Ref']['End date of contract'] is not None and ((fac['Ref']['End date of contract'])<(date_of_inquiry)):
        return True
    return False

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

def get_status(fac : dict):

    try:
        if not isStayOrder(fac):
            return fac["Contract History"].Status[0]
        return None 
    except Exception as exc:
        print(exc)
        return None
    
def get_class_from_set(classes : set):
    for classification in ('BLW', 'BL', 'DF', 'SS', 'SMA', 'UC', "STD"):
        if classification in classes:
            return classification
    return None
    
def get_worst_status(fac: dict):

    try:
        if not isStayOrder(fac):
            return get_class_from_set(set(fac["Contract History"].Status))

        return None
    except Exception as exc:
        print(exc)
        return None
    

def end_date(fac):
    
    '''
    Helper function to extract starting date
    
    Output : day-month-year
    
    '''
    try: 
        if (fac['Ref']['End date of contract']) is None:
            date = 'Not present'
        else:
            date = fac['Ref']['End date of contract']
            date = (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
        return date
    except Exception as exc:
        print(exc)
        return None


def last_pay_date(fac):
    
    '''
    Helper function to extract date of last payment
    
    Output : day-month-year
    
    '''
    try:
        if (fac['Ref']['Date of last payment']) is None:
            date = 'Not present'
        else:
            date = fac['Ref']['Date of last payment']
            date = (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
        return date
    except Exception as exc:
        print(exc)
        return None
    
def get_NPI(fac : dict):
    '''
    Return 
    ----------
    Npi from NPI column of installment facility
    
    '''
    try: 
        if not isStayOrder(fac):
            return fac["Contract History"].NPI[0]

        return None
    except Exception as exc:
        print(exc)
        return None


def is_living(fac):
    if fac["Ref"]["Phase"] == "Living":
        return True
    else:
        return False
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
    try: 
        if not isStayOrder(fac):
            return fac['Ref']['Sanction Limit']

        return None  
    except Exception as exc:
        print(exc)
        return None

    
def funded_non_ins(fac):
    """
    returns
    -------
        Non-Installment Facility : Latest value of "SancLmt" from "Contract History"
            for Non-Installment facilities with Stay Order (No contract history), returns <None>
        
    """
    try:  
        if not isStayOrder(fac):
            return fac["Contract History"].SancLmt.values[0]
        return None
    except Exception as exc:
        print(exc)
        return None


def facility_name(fac):                    
    try:
        return fac['Ref']['Facility']
    except Exception as exc:
        print(exc)
        return None

    

def get_outstanding(fac):
    """
    if not Stay Order
        Installment Facility : latest Outstand value from Contract History 
        Non-Installment Facility : lastest Outstand value from Contract History
        Credit Card Facility : lastest Outstanding value from Contract History
    """
    try:
        if not isStayOrder(fac):
            if "Outstand" in fac["Contract History"].columns:
                return fac["Contract History"].Outstand[0]

            return fac["Contract History"].Outstanding[0]
    except Exception as exc:
        print(exc)
        return None

    return None


def funded_ins_overdue(fac):
    try:
        if not isStayOrder(fac):
            return fac['Contract History']['Overdue'][0]
        return None
    except Exception as exc:
        print(exc)
        return None
    

def funded_non_ins_overdue(fac):
    try:
        if not isStayOrder(fac):
            return fac['Contract History'].sort_values('Date', ascending=False).Overdue [0]
        return None
    except Exception as exc:
        print(exc)
        return None


                        
def funded_ins_amount(fac):
    try:
        return fac['Ref']['Installment Amount']
    except Exception as exc:
        print(exc)
        return None
                            
def funded_pay_period(fac):
    try:
        return fac['Ref']['Payments periodicity']
    except Exception as exc:
        print(exc)
        return None
                            



def no_installment(fac):

    try:
        return fac['Ref']['Total number of installments']
    except Exception as exc:
        print(exc)
        return None
                            

def no_installment_paid(fac):
    
    try:
        paid_ins = (fac['Ref']['Total number of installments']) - (fac['Ref']['Remaining installments Number'])
                                
        return paid_ins
    except Exception as exc:
        print(exc)
        return None

def remaining_ins(fac):
    try:
        return fac['Ref']['Remaining installments Number']
    except Exception as exc:
        print(exc)
        return None


def pay_period(fac):
    try:
        return fac['Ref']['Payments periodicity']
    except Exception as exc:
        print(exc)
        return None
                        
                            


def reorganized_credit(fac):
    try:
        return fac['Ref']['Reorganized credit']
    except Exception as exc:
        print(exc)
        return None
     
    
def default(fac):
    try: 
        if isStayOrder(fac):
            return None
        return fac['Contract History'].Default[0]
    except Exception as exc:
        print(exc)
        return None
    
def get_remarks(fac: dict):
    try: 
        if fac['Ref']['Remarks'] is not None:
            return fac['Ref']['Remarks']
        return None 
    except Exception as exc:
        print(exc)
        return None

def funded_nonins(cib_list:list):
    '''
    Summary of funded (non-installment facility) facility table for borrower, co-borrower and gurantor 
    '''
    columns = ['Non Installment', 'Limit', 'Outstanding', 'Overdue', 'Start Date','End Date of Contract', 'Installment amount', 'Payment Period', 
              'Total No. of Installment', 'Total no. of Installment paid', 'No. of Remaining Installment','Date of Last Payment', 'NPI (No.)',
              'Default ', 'Current Status','Worst Status', 'Reorganized Credit', 'Remarks']
    table = []
    for cib_data in cib_list: 
        date_of_inquiry =  cib_data.cib_header['Date of Inquiry'][0].date() 
        if type(cib_data.noninstallment_facility) == list:
            for fac in cib_data.noninstallment_facility:
                if is_living(fac) == True and isNonFunded(fac) != True:
                    if expired_live_loan_check(fac,date_of_inquiry) == True:    
                        row = [facility_name(fac),funded_non_ins(fac), get_outstanding(fac),  funded_non_ins_overdue(fac),
                            start_date(fac), end_date(fac),' ' , ' ', ' ',' ', ' ', ' ', ' ', ' ', 
                            get_status(fac), get_worst_status(fac), reorganized_credit(fac),  get_remarks(fac)]
        
                        table.append(row)
                        
    return pd.DataFrame(table, columns=columns)


def nonfunded_details(cib_list:list):
    '''
    Summary of Non funded (installment and non-installment facility) facility table for borrower 
    '''
    
    columns = ['Non Installment', 'Limit', 'Outstanding', 'Overdue', 'Start Date','End Date of Contract', 'Installment amount', 'Payment Period', 
              'Total No. of Installment', 'Total no. of Installment paid', 'No. of Remaining Installment','Date of Last Payment', 'NPI (No.)',
              'Default ', 'Current Status','Worst Status', 'Reorganized Credit', 'Remarks']
    table = []
    for cib_data in cib_list:  
        date_of_inquiry =  cib_data.cib_header['Date of Inquiry'][0].date() 
        if type(cib_data.noninstallment_facility) == list:
            for fac in cib_data.noninstallment_facility: 
                if is_living(fac) == True and isNonFunded(fac) == True:
                    if expired_live_loan_check(fac,date_of_inquiry) == True:    
                        row = [facility_name(fac),funded_non_ins(fac), get_outstanding(fac),  funded_non_ins_overdue(fac),
                            start_date(fac), end_date(fac),' ' , ' ', ' ',' ', ' ', ' ', ' ', ' ', 
                            get_status(fac), get_worst_status(fac), reorganized_credit(fac),  get_remarks(fac)]
                        table.append(row)

                        
    return pd.DataFrame(table, columns=columns)
def funded_ins_details(cib_list:list):
    '''
    Summary of funded (installment and non-installment facility) facility table for borrower 
    '''
    
    columns = ['Installment', 'Limit', 'Outstanding', 'Overdue', 'Start Date','End Date of Contract', 'Installment amount', 'Payment Period', 
              'Total No. of Installment', 'Total no. of Installment paid', 'No. of Remaining Installment','Date of Last Payment', 'NPI (No.)',
              'Default ', 'Current Status','Worst Status', 'Reorganized Credit', 'Remarks']
    table = []
    for cib_data in cib_list:
        date_of_inquiry = cib_data.cib_header['Date of Inquiry'][0].date() 
        
        if type(cib_data.installment_facility) == list:
            for fac in cib_data.installment_facility: 
                if is_living(fac) == True and isNonFunded(fac) != True:
                    if expired_live_loan_check(fac,date_of_inquiry) == True:   
                        row = [facility_name(fac),funded_ins(fac),get_outstanding(fac),  funded_ins_overdue(fac),
                            start_date(fac), end_date(fac), funded_ins_amount(fac), pay_period(fac), no_installment(fac),
                            no_installment_paid(fac), remaining_ins(fac), last_pay_date(fac), get_NPI(fac), default(fac), 
                            get_status(fac), get_worst_status(fac), reorganized_credit(fac),  get_remarks(fac)]
        
                            
                        table.append(row)
                    
    return pd.DataFrame(table, columns = columns)

