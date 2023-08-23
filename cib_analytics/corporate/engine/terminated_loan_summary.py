from ...general_helper import is_living, isNonFunded
    
def tot_fund_terminated_loan(facility):
    no_ter_loan  = 0
    for fac in facility:
        if is_living(fac) is False and isNonFunded(fac) is False:
            no_ter_loan += 1   
    return no_ter_loan

def tot_nonfund_terminated_loan(facility):
    no_ter_loan  = 0
    for fac in facility:
        if is_living(fac) is False and isNonFunded(fac) is True:
            no_ter_loan += 1
    return no_ter_loan

def get_class_from_set(classes : set):
    for classification in ('BLW', 'BL', 'DF', 'SS', 'SMA', 'UC', "STD"):
        if classification in classes:
            return classification
    return None

def get_worst_status(facility : dict):
    return get_class_from_set(set(facility["Contract History"].Status.tolist()))


def funded_ins_limit(cibs):
    try:
        installment = []
        for cib in cibs:
            if type(cib.installment_facility) == list:
                for fac in cib.installment_facility:                    
                    if is_living(fac) == False and isNonFunded(fac) != True:                            
                        installment.append(str(fac['Ref']['Sanction Limit']))
        return installment
    except Exception as exc:
        print("funded_ins_limit: ", exc)
        return []

def funded_ins_facility_name(cibs):                    
    try:                
        facility_name = []
        for cib in cibs:
            if type(cib.installment_facility) == list:
                for fac in cib.installment_facility:
                    if is_living(fac) == False and isNonFunded(fac) != True: 
                        facility_name.append(str(fac['Ref']['Facility']))
        return facility_name
    except Exception as exc:
        print("funded_ins_facility_name: ", exc)
        return []

def funded_ins_worse_cl_status(cibs):   
    try:
        cl_status = []        
        for cib in cibs:
            if type(cib.installment_facility) == list:
                for fac in cib.installment_facility:
                    if is_living(fac) == False and isNonFunded(fac) != True: 
                        cl_status.append(get_worst_status(fac))
        return cl_status
    except Exception as exc:
        print("funded_ins_worse_cl_status: ", exc)
        return []
                    
def classification_date(fac):
    
    '''
    Helper function to extract starting date
    
    Output : day-month-year
    
    '''
    try: 
        if (fac['Ref']['Date of classification']) is None:
            date = 'Not present'
        else:
            date = fac['Ref']['Date of classification']
            date = (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
        return str(date)
    except Exception as exc:
        print("classification_date: ",exc)
        return []
                  

def funded_ins_date_of_class(cibs):
    try:
        date = []
        for cib in cibs:
            if type(cib.installment_facility) == list:
                for fac in cib.installment_facility:
                    if is_living(fac) == False and isNonFunded(fac) != True: 
                        date.append(classification_date(fac))
        return date
    except Exception as exc:
        print("funded_ins_date_of_class: ",exc)
        return []

def funded_non_ins(cibs):
    try:
        non_installment = []        
        for cib in cibs:
            if type(cib.noninstallment_facility) == list:
                for fac in cib.noninstallment_facility:
                    if is_living(fac) == False and isNonFunded(fac) != True:
                        non_installment.append(str(fac["Contract History"]['SancLmt'][0]))
        return non_installment
    except Exception as exc:
        print("funded_non_ins: ",exc)
        return []

def funded_non_ins_facility_name(cibs):   
    try:               
        facility_name = []
        for cib in cibs:
            if type(cib.noninstallment_facility) == list:
                for fac in cib.noninstallment_facility:
                    if is_living(fac) == False and isNonFunded(fac) != True: 
                        facility_name.append(str(fac['Ref']['Facility']))
        return facility_name
    except Exception as exc:
        print("funded_non_ins_facility_name: ",exc)
        return []

def funded_non_ins_worse_cl_status(cibs):   
    try: 
        cl_status = []
        for cib in cibs:
            if type(cib.noninstallment_facility) == list:
                for fac in cib.noninstallment_facility:
                    if is_living(fac) == False and isNonFunded(fac) != True: 
                        cl_status.append(get_worst_status(fac))
        return cl_status
    except Exception as exc:
        print("funded_non_ins_worse_cl_status: ",exc)
        return []

def funded_non_ins_date_of_class(cibs):
    try: 
        date = []
        for cib in cibs:
            if type(cib.noninstallment_facility) == list:
                for fac in cib.noninstallment_facility:
                    if is_living(fac) == False and isNonFunded(fac) != True: 
                        date.append(classification_date(fac))
        return date
    except Exception as exc:
        print("funded_non_ins_date_of_class: ", exc)
        return []         
   
def term_total_funded_loan(cibs):
    try: 
        terminated_loan = 0
        for cib in cibs:
            if type(cib.installment_facility) == list:
                terminated_loan += (tot_fund_terminated_loan(cib.installment_facility))                
            if type(cib.noninstallment_facility) == list:                
                terminated_loan += (tot_fund_terminated_loan(cib.noninstallment_facility))  
        return terminated_loan 
    except Exception as exc:
        print("term_total_funded_loan: ",exc)
        return None
    
def term_total_nonfunded_loan(cibs):
    try: 
        terminated_loan = 0
        for cib in cibs:
            if type(cib.installment_facility) == list:
                terminated_loan += (tot_nonfund_terminated_loan(cib.installment_facility))
            if type(cib.noninstallment_facility) == list:    
                terminated_loan += (tot_nonfund_terminated_loan(cib.noninstallment_facility))
        return terminated_loan
    except Exception as exc:
        print("term_total_nonfunded_loan: ",exc)
        return None 
    
    
def nonfunded_facility_name(cibs):     
    try:               
        facility_name = []
        for cib in cibs:
            if type(cib.installment_facility) == list:
                for fac in cib.installment_facility:
                    if is_living(fac) == False and isNonFunded(fac) == True: 
                        facility_name.append(str(fac['Ref']['Facility']))
            if type(cib.noninstallment_facility) == list:
                for fac in cib.noninstallment_facility:
                    if is_living(fac) == False and isNonFunded(fac) == True:
                        facility_name.append(str(fac['Ref']['Facility']))
        return facility_name
    except Exception as exc:
        print("nonfunded_facility_name: ",exc)
        return []
    


def nonfunded_limit(cibs):
    try: 
        sanc_limit = []
        for cib in cibs:
            if type(cib.installment_facility) == list:
                for fac in cib.installment_facility:
                    if is_living(fac) == False and isNonFunded(fac) == True:
                        sanc_limit.append(str(fac['Ref']['Sanction Limit']))
            if type(cib.noninstallment_facility) == list:
                for fac in cib.noninstallment_facility:
                    if is_living(fac) == False and isNonFunded(fac) == True:
                        sanc_limit.append(str(fac['Ref']['SancLmt'][0]))
        return sanc_limit
    except Exception as exc:
        print("nonfunded_limit: ",exc)
        return []
    
def nonfunded_worse_cl_status(cibs):  
    try:
        cl_status = []
        for cib in cibs:
            if type(cib.installment_facility) == list:
                for fac in cib.installment_facility:
                    if is_living(fac) == False and isNonFunded(fac) == True: 
                        cl_status.append(get_worst_status(fac))
            if type(cib.noninstallment_facility) == list:
                for fac in cib.noninstallment_facility:
                    if is_living(fac) == False and isNonFunded(fac) == True: 
                        cl_status.append(get_worst_status(fac))
        return cl_status  
    
    except Exception as exc:
        print("nonfunded_worse_cl_status: ",exc)
        return None 
    
    
    
def nonfunded_date_of_class(cibs):
    try: 
        date = []
        for cib in cibs:
            if type(cib.installment_facility) == list:
                for fac in cib.installment_facility:
                    if is_living(fac) == False and isNonFunded(fac) == True: 
                        date.append(classification_date(fac))
            if type(cib.noninstallment_facility) == list:
                for fac in cib.noninstallment_facility:
                    if is_living(fac) == False and isNonFunded(fac) == True: 
                        date.append(classification_date(fac))
        return date
    except Exception as exc:
            print("nonfunded_date_of_class: ",exc)
            return None
    



