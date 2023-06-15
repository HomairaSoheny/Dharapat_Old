def isNonFunded(fac):
    if ('non funded' in fac["Ref"]["Facility"].lower() or
        'letter of credit' in fac["Ref"]["Facility"].lower() or
        'guarantee' in fac["Ref"]["Facility"].lower() or
        'other indirect facility' in fac["Ref"]["Facility"].lower() ):
        return True
    return False

def funded_installment(cib):
    try:
        response = 0
        if cib.installment_facility is None:
            return "Installment Facility not Found"
        for facility in cib.installment_facility:
            if isNonFunded(facility) is False:
                response += facility['Ref']['Installment Amount']
        return response
    except:
        return "Error"

def funded_no_installment(cib):
    try:
        response = 0
        if cib.noninstallment_facility is None:
            return "Non Installment Facility Not Found"
        for facility in cib.noninstallment_facility:
            if isNonFunded(facility) is False:
                response += facility['Ref']['Security Amount']
        return response
    except:
        return "Error"

def funded_total(cib):
    try:
        return funded_installment(cib) + funded_no_installment(cib)
    except:
        return "Error"
    
def non_funded_total(cib):
    try:
        response = 0
        if cib.installment_facility is not None:
            for facility in cib.installment_facility:
                if isNonFunded(facility) is True:
                    response += facility['Ref']['Installment Amount']
        if cib.noninstallment_facility is not None:
            for facility in cib.noninstallment_facility:
                if isNonFunded(facility) is True:
                    response += facility['Ref']['Security Amount']
        return response
    except:
        return "Error"

def total(cib):
    try:
        return funded_total(cib) + non_funded_total(cib)
    except:
        return "Error"

def get_overdue(cib):
    try:
        overdue = []
        for fac_type in (cib.installment_facility, cib.credit_card_facility):
            if fac_type is not None:
                for fac in fac_type:
                    if (fac['Ref']['Phase']) == 'Living':
                        overdue.append((fac['Contract History']).sort_values('Date', ascending=False).Overdue[0])  
        return sum(overdue)
    except:
        return []

def get_cl_status(cib):
    try:
        status = []
        for fac_type in (cib.installment_facility, cib.credit_card_facility):
            if fac_type is not None:
                for fac in fac_type:
                    if (fac['Ref']['Phase']) == 'Living':
                        status.append((fac['Contract History']).sort_values('Date', ascending=False).Status[0])
        if 'UC' in status:
            return 'UC'
        return ''
    except:
        return "Error"

def get_default(cib):
    try:
        return "Yet to be implemented"
    except:
        return "Error"
    
def get_std(cib):
    try:
        return "Yet to be implemented"
    except:
        return "Error"

def get_sma(cib):
    try:
        return "Yet to be implemented"
    except:
        return "Error"

def get_ss(cib):
    try:
        return "Yet to be implemented"
    except:
        return "Error"

def get_df(cib):
    try:
        return "Yet to be implemented"
    except:
        return "Error"
    
def get_bl(cib):
    try:
        return "Yet to be implemented"
    except:
        return "Error"

def get_blw(cib):
    try:
        return "Yet to be implemented"
    except:
        return "Error"

def get_stay_order(cib):
    try:
        return "Yet to be implemented"
    except:
        return "Error"

def get_remarks(cib):
    try:
        return "Yet to be implemented"
    except:
        return "Error"