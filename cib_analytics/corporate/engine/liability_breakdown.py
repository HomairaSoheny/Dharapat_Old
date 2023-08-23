from ...general_helpers import is_living, isNonFunded, isStayOrder

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
        total_lc = []
        for cib_data in cib_list:
            total_lc.append(cib_data.summary_1B.Living_Amount.values[1])
        return total_lc
    except:
        return []
    
def total_indirect_liability(cib_list):
    try:
        indirect_liability = []
        for cib_data in cib_list:  
            indirect_liability.append(cib_data.summary_1B.Living_Amount.values[2])   
        return indirect_liability
    except:
        return []
    
    
def total_bg(cib_list):
    try:
        bank_gurantee = []
        for cib_data in cib_list:  
            bank_gurantee.append(cib_data.summary_1B.Living_Amount.values[0])
        return bank_gurantee
    except:
        return []
