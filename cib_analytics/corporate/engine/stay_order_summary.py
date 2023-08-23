import pandas as pd
def isStayOrder(fac):
    if type(fac['Contract History']) == dict and 'Stay Order' in fac['Contract History'].keys():
        return True
    else: 
        return False
def get_title_trade_name(cib):
    if 'Trade Name' in cib.subject_info.keys():
        return cib.subject_info['Trade Name']

    return cib.subject_info['Title, Name']


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
def fac_name(fac):

    if isNonFunded(fac) == True:
        return ('Non funded')
    else: 
        return ('Funded')
    
def remarks(fac):
    if fac['Ref']['Remarks'] is not None:
        return fac['Ref']['Remarks']
    else: 
        return ('--')
    
def Stayorder_amount(fac):
    return fac['Ref']['Security Amount']

def stay_order_borrower(cib_list:list):
    '''
    Summary of stay order (installment and non-installment facility) facility table
    '''
    try:
        columns = ['Name of account', 'Nature of facility', 'Stayorder amount', 'Writ no', 'Remarks']
        table = []
        for cib in cib_list:  
            acc_name = get_title_trade_name(cib)
            for facility in (cib.noninstallment_facility, cib.installment_facility):
                if not isinstance(facility, type(None)):
                    for fac in facility:
                        if isStayOrder(fac) is True and fac['Ref']['Role'] != "Guarantor": 
                            row = [ acc_name, fac_name(fac), Stayorder_amount(fac),'--', remarks(fac)]
                            table.append(row)

                            
        table = pd.DataFrame(table, columns=columns)
        return {
            "Name of account": table["Name of account"].tolist(),
            "Nature of facility": table["Nature of facility"].tolist(),
            "Stayorder amount": table["Stayorder amount"].tolist(),
            "Writ no": table["Writ no"].tolist(),
            "Remarks": table["Remarks"].tolist()
        }
        
    except Exception as exc:
        print("function: stay_order_borrower")
        print(exc)
        return []



def stay_order_gurantor(cib_list:list):
    '''
    Summary of stay order (installment and non-installment facility) facility table
    '''
    try:
        columns = ['Name of account', 'Nature of facility', 'Stayorder amount', 'Writ no', 'Remarks']
        table = []
        for cib in cib_list:  
            acc_name = get_title_trade_name(cib)
            for facility in (cib.noninstallment_facility, cib.installment_facility):
                if not isinstance(facility, type(None)):
                    for fac in facility:
                        if isStayOrder(fac) is True and fac['Ref']['Role'] == "Guarantor": 
                            row = [ acc_name, fac_name(fac), Stayorder_amount(fac),'--', remarks(fac)]
                            table.append(row)
                                                
        table = pd.DataFrame(table, columns=columns)
        return {
            "Name of account": table["Name of account"].tolist(),
            "Nature of facility": table["Nature of facility"].tolist(),
            "Stayorder amount": table["Stayorder amount"].tolist(),
            "Writ no": table["Writ no"].tolist(),
            "Remarks": table["Remarks"].tolist()
        }
        
    except Exception as exc:
        print("function: stay_order_gurantor")
        print(exc)
        return []