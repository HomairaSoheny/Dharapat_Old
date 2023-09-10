from ...general_helpers import is_living, isNonFunded, isStayOrder

def borrowing_com_per(cib_list):
    try:
        name = []
        for cib_data in cib_list:
            if cib_data.subject_info['Type of subject'].lower() == 'individual':
                name.append(str(cib_data.subject_info['Title, Name']))
            else:
                name.append(str(cib_data.subject_info['Trade Name']))
        return name
    except:
        return []

def a_overdraft(cib_list):
    try:
        total_loan = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.noninstallment_facility, type(None)):
                for fac in cib_data.noninstallment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if ('overdraft' in fac['Ref']['Facility'].lower() or
                            'cash credit' in fac['Ref']['Facility'].lower() or
                            'cc' in fac['Ref']['Facility'].lower() or
                            'od' in fac['Ref']['Facility'].lower()):
                            amount += 1
            total_loan.append(str(amount))
        return total_loan
    except:
        return []
    
def a_overdue(cib_list):
    try:
        total_overdue = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.noninstallment_facility, type(None)):
                for fac in cib_data.noninstallment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if ('overdraft' in fac['Ref']['Facility'].lower() or
                            'cash credit' in fac['Ref']['Facility'].lower() or
                            'cc' in fac['Ref']['Facility'].lower() or
                            'od' in fac['Ref']['Facility'].lower()):
                            amount += fac['Contract History'].Overdue[0]
            total_overdue.append(str(amount))
        return total_overdue
    except:
        return []

def b_time_loan(cib_list):
    try:
        total_loan = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.noninstallment_facility, type(None)):
                for fac in cib_data.noninstallment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if ('time loan' in fac['Ref']['Facility'].lower()):
                            amount += 1
            total_loan.append(str(amount))
        return total_loan
    except:
        return []                                 

def b_overdue(cib_list):
    try:
        total_overdue = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.noninstallment_facility, type(None)):
                for fac in cib_data.noninstallment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if ('time loan' in fac['Ref']['Facility'].lower()):
                            amount += 1
            total_overdue.append(str(amount))
        return total_overdue 
    except:
        return []
    
def c_ltr(cib_list):
    try:
        total_loan = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.noninstallment_facility, type(None)):
                for fac in cib_data.noninstallment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if ('ltr' in fac['Ref']['Facility'].lower()):
                            amount += 1
            total_loan.append(str(amount))
        return total_loan
    except:
        return []
    
def c_overdue(cib_list):
    try:
        total_overdue = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.noninstallment_facility, type(None)):
                for fac in cib_data.noninstallment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if ('ltr' in fac['Ref']['Facility'].lower()):
                            amount += 1
            total_overdue.append(str(amount))
        return total_overdue
    except:
        return []
    
def d_other_non_installment(cib_list):
    try:
        total_no_loan = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.noninstallment_facility, type(None)):
                for fac in cib_data.noninstallment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if (fac['Ref']['Facility'].lower()) == 'other non instalment contract':
                            amount +=  1
            total_no_loan.append(str(amount))
        return total_no_loan
    except: 
        return []
    
def d_overdue(cib_list):
    try:
        total_overdue = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.noninstallment_facility, type(None)):
                for fac in cib_data.noninstallment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if (fac['Ref']['Facility'].lower()) == 'other non instalment contract':
                            amount += fac['Contract History'].Overdue[0]
            total_overdue.append(str(amount))
        return total_overdue
    except: 
        return []

def e_term_loan(cib_list):
    try:
        total_no_loan = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.installment_facility, type(None)):
                for fac in cib_data.installment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if (fac['Ref']['Facility'].lower()) == 'term loan':
                            amount += 1
            total_no_loan.append(str(amount))
        return total_no_loan
    except: 
        return 

def e_emi(cib_list):
    try:
        total_loan = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.installment_facility, type(None)):
                for fac in cib_data.installment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if (fac['Ref']['Facility'].lower()) == 'term loan':
                            amount += fac['Ref']['Installment Amount']
            total_loan.append(str(amount))
        return total_loan
    except: 
        return []
    
def e_overdue(cib_list):
    try:
        total_loan = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.installment_facility, type(None)):
                for fac in cib_data.installment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if (fac['Ref']['Facility'].lower()) == 'term loan':
                            amount += fac['Contract History'].Overdue[0]
            total_loan.append(str(amount))
        return total_loan
    except: 
        return []
    
def f_other_installment_loan(cib_list):
    try:
        total_no_loan = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.installment_facility, type(None)):
                for fac in cib_data.installment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if (fac['Ref']['Facility'].lower()) == 'other instalment contract':
                            amount += 1
            total_no_loan.append(str(amount))
        return total_no_loan
    except: 
        return []
    
def f_emi(cib_list):
    try:
        total_loan = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.installment_facility, type(None)):
                for fac in cib_data.installment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if (fac['Ref']['Facility'].lower()) == 'other instalment contract':
                            amount += fac['Ref']['Installment Amount']
            total_loan.append(str(amount))
        return total_loan
    except: 
        return []
    
def f_overdue(cib_list):
    try:
        total_overdue = []
        for cib_data in cib_list:
            amount = 0
            if not isinstance(cib_data.installment_facility, type(None)):
                for fac in cib_data.installment_facility:
                    if not isStayOrder(fac) and is_living(fac) is True:
                        if (fac['Ref']['Facility'].lower()) == 'other instalment contract':
                            amount += fac['Contract History'].Overdue[0]
            total_overdue.append(str(amount))
        return total_overdue
    except: 
        return []

def total_lc(cib_list):
    try:
        total_lc = []
        for cib_data in cib_list:
            total_lc.append(str(cib_data.summary_1B.Living_Amount.values[1]))
        return total_lc
    except:
        return []
    
def total_indirect_liability(cib_list):
    try:
        indirect_liability = []
        for cib_data in cib_list:  
            indirect_liability.append(str(cib_data.summary_1B.Living_Amount.values[2]))
        return indirect_liability
    except:
        return []
    
    
def total_bg(cib_list):
    try:
        bank_gurantee = []
        for cib_data in cib_list:  
            bank_gurantee.append(str(cib_data.summary_1B.Living_Amount.values[0]))
        return bank_gurantee
    except:
        return []
