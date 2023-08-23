from itertools import zip_longest
from ...general_helpers import is_living, isNonFunded, isStayOrder



def get_class_from_set(classes : set):
    for classification in ('BLW', 'BL', 'DF', 'SS', 'SMA', 'UC', "STD"):
        if classification in classes:
            return classification
    return None

def get_worst_status(facility : dict):
    if not isStayOrder(facility):
        return get_class_from_set(set(facility["Contract History"].Status))

    return None

def get_concern_name(cibs):
    try: 
        name = []
        for cib in cibs:
            if 'Trade Name' in cib.subject_info.keys():
                name.append(cib.subject_info['Trade Name'])
            else:
                name.append(cib.subject_info['Title, Name'])
        return name
    except:
        return []


def get_outs_fund_ins(cibs):
    
    try:
    
        installment_list = []

        for cib in cibs:
            installment = 0
            if type(cib.installment_facility) == list:
                        
                for facility in cib.installment_facility:

                    if is_living(facility) == True:

                        if isNonFunded(facility) is False:  

                            installment += (facility["Contract History"]["Outstanding"][0])
            installment_list.append(installment)
        return installment_list
    except:

         return []
    
def get_outs_fund_non_ins(cibs):
    try:
        non_installment_list = []
    
        for cib in cibs:
            non_installment = 0

            if type(cib.noninstallment_facility ) == list:
                        
                for facility in cib.noninstallment_facility:

                    if is_living(facility) == True:

                        if isNonFunded(facility) == False:  

                            non_installment += (facility["Contract History"]["Outstand"][0])
            non_installment_list.append(non_installment)
        return non_installment_list
    except:

         return []
def get_total_fund_out(cibs):
    try:
      
        fund_ins_outs = get_outs_fund_ins(cibs)
        fund_non_ins_outs = get_outs_fund_non_ins(cibs)
       
        return [sum(n) for n in zip_longest(fund_ins_outs, fund_non_ins_outs, fillvalue=0)]
        
        
    except:

         return []
def get_outs_non_fund(cibs):
    try:
    
        non_fund_list = []

        for cib in cibs:
            non_fund = 0
            
            if type(cib.noninstallment_facility ) == list:
                        
                for facility in cib.noninstallment_facility:

                    if is_living(facility) == True:

                        if isNonFunded(facility):  

                            non_fund += (facility["Contract History"]["Outstand"][0])
                                
            non_fund_list.append(non_fund)
        return non_fund_list

    except:
        return []
def get_outs_total(cibs):
    try:
        fund  = get_total_fund_out(cibs)
        non_fund = get_outs_non_fund(cibs)
        total_outs = []
        for i in range(len(fund)):
            total_outs.append(fund[i]+non_fund[i])

        return [sum(n) for n in zip_longest(fund,non_fund, fillvalue=0)]
    except:
        return []
def get_overdue(cibs):
    try:
        list_overdue = []

        for cib in cibs:
            
            overdue = 0
        
            for fac_type in (cib.installment_facility,cib.noninstallment_facility,cib.credit_card_facility):
                if fac_type is not None:
                    for fac in fac_type:
                        if (fac['Ref']['Phase']) == 'Living':
                            if isNonFunded(fac):  
                                overdue += ((fac["Contract History"]).sort_values("Date", ascending=False).Overdue[0])
            
            list_overdue.append( overdue)
        return list_overdue 
    except:
        return []

def get_UC_or_STD(self):
        """
        Return 'UC' or 'STD' based on which terminology is used in CIB
        """
        if "UC_Amount" in self.summary_1A.columns:
            return "UC"
        else:
            return "STD"
def current_status(cib):
    '''
    Sequence of checking *must* be:
    summary_1B: 'Stay order_No.'
    summary_1A: 'Stay Order_No.'->BLW_No.'->'BL_No.'->'DF_No.'->'SS_No.'->'SMA_No.'
    '''

    if cib.summary_1B['Stay order_No.'].sum() > 0 or cib.summary_2B['Stay order_No.'].sum() > 0:
        return "Stay Order"

    for column in ('Stay Order_No.', 'BLW_No.', 'BL_No.', 'DF_No.', 'SS_No.', 'SMA_No.'):
        if cib.summary_1A[column].sum() > 0 or cib.summary_2A[column].sum() > 0:
            return column.replace('_No.', '')

    return cib.get_UC_or_STD()    
def get_status(cibs):
    try: 
        status_list = []
        for cib in cibs:
            status_list.append(current_status(cib))
        return status_list
    except:
        return []


