from datetime import timedelta

def is_living(facility):
    '''
    input -> details of facility
    output -> Bool
    if "phase" is living then True, else False
    '''
    if facility["Ref"]["Phase"] == "Living":
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

    return False

def isStayOrder(facility):
    
    '''
    input -> details of a facility
    output -> Bool
    if "stay order" key present in that specific transactional history return True
   
   ''' 
    if type(facility['Contract History']) == dict and 'Stay Order' in facility['Contract History'].keys():
        return True

    return False



def get_UC_or_STD(cib_data):
        """
        Return 'UC' or 'STD' based on which terminology is used in CIB
        """
        if "UC_Amount" in cib_data.summary_1A.columns:
            return "UC"
        else:
            return "STD"
        
        
def current_status(cib_data):
    '''
    Sequence of checking *must* be:
    summary_1B: 'Stay order_No.'
    summary_1A: 'Stay Order_No.'->BLW_No.'->'BL_No.'->'DF_No.'->'SS_No.'->'SMA_No.'
    '''
    if cib_data.summary_1B['Stay order_No.'].sum() > 0 or cib_data.summary_2B['Stay order_No.'].sum() > 0:
        return "Stay Order"

    for column in ('Stay Order_No.', 'BLW_No.', 'BL_No.', 'DF_No.', 'SS_No.', 'SMA_No.'):
        if cib_data.summary_1A[column].sum() > 0 or cib_data.summary_2A[column].sum() > 0:
            return column.replace('_No.', '')

    return cib_data.get_UC_or_STD()
   

def inquired_date(cib_data):
    '''
    Extract the date of inquiry or the download date of the cib

    '''
    date = cib_data.cib_header['Date of Inquiry'][0].date()
    
    return date



def loan_investment_request(cib_data)-> int:
    '''
    If there's any loaninvestmet request within 3 months of inquired date
    
    '''
    inq_date = inquired_date(cib_data)
    length = 0
    within = 92
    date = []

    if (cib_data.req_contracts) is not None:
        for i in range (len(cib_data.req_contracts)):
            if cib_data.req_contracts['Role'][i] != 'Guarantor':
                date_req = cib_data.req_contracts['Request date'][i].date()
                if (inq_date - (date_req)) < timedelta(days = within):
                    length += 1
                    date.append(date_req)
            
    return length, date  


def get_sanc_limit(cib_data)->int:
    sanctioned_limit_funded = 0
    sanctioned_limit_nonfunded = 0
    
    if cib_data.installment_facility is not None:
        for fac in cib_data.installment_facility:
            if is_living(fac) == True and fac["Ref"]["Role"]!='Guarantor' and not isStayOrder(fac):
                if isNonFunded(fac):
                    sanctioned_limit_nonfunded += fac['Ref']['Sanction Limit']
                else:
                    sanctioned_limit_funded += fac['Ref']['Sanction Limit']
                    
    if cib_data.noninstallment_facility is not None:              
        for fac in cib_data.noninstallment_facility:
            if is_living(fac) == True and fac["Ref"]["Role"]!='Guarantor' and not isStayOrder(fac):
                if isNonFunded(fac):
                    sanctioned_limit_nonfunded += fac['Contract History']['SancLmt'][0]
                else:
                    sanctioned_limit_funded += fac['Contract History']['SancLmt'][0]
                    
    if cib_data.credit_card_facility is not None:   
        for fac in cib_data.credit_card_facility:
            if is_living(fac) == True and fac["Ref"]["Role"]!='Guarantor'and not isStayOrder(fac):
                if isNonFunded(fac):
                    sanctioned_limit_nonfunded += fac['Ref']['Credit limit']
                else:
                    sanctioned_limit_funded += fac['Ref']['Credit limit']
        
    return sanctioned_limit_funded, sanctioned_limit_nonfunded 


                        
def get_outstanding(cib_data):
    
    if 'Contract Category' in cib_data.summary_1A.columns:
        ni_row = [i for i in cib_data.summary_1A['Contract Category'].values if i.replace(' ','')=='Non-Installments'][0]
        outstanding_funded = cib_data.summary_1A.set_index('Contract Category').loc[ni_row, cib_data.get_UC_or_STD()+'_Amount']
    else:
        ni_row = [i for i in cib_data.summary_1A['Contract'].values if i.replace(' ','')=='Non-Installments'][0]
        outstanding_funded = cib_data.summary_1A.set_index('Contract').loc[ni_row, cib_data.get_UC_or_STD()+'_Amount']

    outstanding_nonfunded = cib_data.summary_1B.Living_Amount.values[-1]

    return outstanding_funded, outstanding_nonfunded    


def get_overdue(cib_data):
    
    overdue_funded = 0
    overdue_nonfunded = 0
    
    if cib_data.installment_facility is not None:
        for fac in cib_data.installment_facility:
            if not isStayOrder(fac):
                if is_living(fac) and fac["Ref"]["Role"]!='Guarantor': # Borrower / Co-borrowers
                    if isNonFunded(fac):
                        overdue_nonfunded += fac["Contract History"].Overdue.values[0]
                    else:
                        overdue_funded += fac["Contract History"].Overdue.values[0]

    if cib_data.noninstallment_facility is not None:
        for fac in cib_data.noninstallment_facility:
            if not isStayOrder(fac):
                if is_living(fac) and fac["Ref"]["Role"]!='Guarantor': # Borrower / Co-borrowers
                    if isNonFunded(fac):
                        overdue_nonfunded += fac["Contract History"].Overdue.values[0]
                    else:
                        overdue_funded += fac["Contract History"].Overdue.values[0]
                        
    if cib_data.credit_card_facility is not None:
        for fac in cib_data.credit_card_facility:
            if not isStayOrder(fac):
                if is_living(fac) and fac["Ref"]["Role"]!='Guarantor': # Borrower / Co-borrowers
                    if isNonFunded(fac):
                        overdue_nonfunded += fac["Contract History"].Overdue.values[0]
                    else:
                        overdue_funded += fac["Contract History"].Overdue.values[0]
                        
        

    return overdue_funded, overdue_nonfunded

