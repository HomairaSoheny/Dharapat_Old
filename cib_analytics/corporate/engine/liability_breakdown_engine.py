def company_or_person(cib_list):
    try:
        return []
    except:
        return []
    
def a_overdraft(cib_list):
    try:
        return []
    except:
        return []

def a_overdue(cib_list):
    try:
        return []
    except:
        return []

def b_time_loan(cib_list):
    try:
        return []
    except:
        return []

def b_overdue(cib_list):
    try:
        return []
    except:
        return []

def c_ltr(cib_list):
    try:
        return []
    except:
        return []

def c_overdue(cib_list):
    try:
        return []
    except:
        return []

def d_other_non_installment(cib_list):
    try:
        return []
    except:
        return []

def d_overdue(cib_list):
    try:
        return []
    except:
        return []

def e_term_loan(cib_list):
    try:
        return []
    except:
        return []

def e_emi(cib_list):
    try:
        return []
    except:
        return []

def e_overdue(cib_list):
    try:
        return []
    except:
        return []

def f_other_installment_loan(cib_list):
    try:
        return []
    except:
        return []

def f_emi(cib_list):
    try:
        return []
    except:
        return []

def f_overdue(cib_list):
    try:
        return []
    except:
        return []

def total_lc(cib_list):
    try:
        return []
    except:
        return []

def total_indirect_liability(cib_list):
    try:
        indirect_liability = []
        for cib_data in cib_list:  
            if not isinstance(cib_data.noninstallment_facility, type(None)):
                for fac in cib_data.noninstallment_facility:
                    if not isStayOrder(fac) and isNonFunded(fac) is True: 
                        if is_living(fac) is True and (fac['Ref']['Facility'].lower()) == 'other indirect facility (non funded)' :
                            indirect_liability.append(fac['Contract History'].Overdue[0])
        return indirect_liability
    except:
        return []
def total_bg(cib_list):
    try:
        overdue_amount = []
        for cib_data in cib_list:  
            if not isinstance(cib_data.noninstallment_facility, type(None)):
                for fac in cib_data.noninstallment_facility:
                    if not isStayOrder(fac) and isNonFunded(fac) is True: 
                        if is_living(fac) is True and (fac['Ref']['Facility'].lower()) == 'guarantee (non funded)' :
                            overdue_amount.append(fac['Contract History'].Overdue[0])
        return overdue_amount
    except:
        return []
