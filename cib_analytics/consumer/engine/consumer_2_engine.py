def Borrowers_name(cibs):
    '''
    Will extract the borrower name 
    from "Other subjects linked to the same contract" for each facilility
    
    '''
    Borrow_name = []
    for fac_type in (cibs.installment_facility,cibs.credit_card_facility):
        if fac_type is not None:
            for i in fac_type:
                if (i['Ref']['Phase']) == 'Living':
                    
                    if  (i["Ref"]['Role']) == 'Borrower':
                        if cibs.subject_info['Type of subject'].lower() == 'individual':
                            
                            title_ = cibs.subject_info['Title, Name']
                        else: # Company cib
                            title_ = cibs.subject_info['Trade Name']
                        
                        Borrow_name.append(title_)
            
                    elif i['Other subjects linked to the same contract'] is not None:
                        for j in range(len(i['Other subjects linked to the same contract'])):
                            if (i['Other subjects linked to the same contract'].iloc[j]["Role"]) == "Borrower":
                                Borrow_name.append(i['Other subjects linked to the same contract'].iloc[j]["Name"])
                    else:    
                        Borrow_name.append("Not given")            
    return Borrow_name                    

def get_Applicants_Role(cibs):
    '''
    Only the role of applicant's
    Output ->  Sequential list   
    
    ''' 
    app_role  = []
    for fac_type in (cibs.installment_facility,cibs.credit_card_facility):
        if fac_type is not None:
            for i in fac_type:
                if (i['Ref']['Phase']) == 'Living':
                    app_role.append(i["Ref"]['Role'])    
    return app_role 


def get_facility_name(cibs):
    
    fac_name = []
    for fac_type in (cibs.installment_facility,cibs.credit_card_facility):
        if fac_type is not None:
            for i in fac_type:
                if (i['Ref']['Phase']) == 'Living':
                    fac_name.append(i['Ref']['Facility'])
    return fac_name            

def get_sanction_limit(cibs):
    """ 
    Sanction limit of diffrent facilities
    
    Output -> Sequential list 
    
    """
    i = 0
    sanc_limit = []
    for fac_type in (cibs.installment_facility, cibs.credit_card_facility):
        if fac_type is not None:
            for fac in fac_type:
                if (fac['Ref']['Phase']) == 'Living':
                    if i == 0:
                        sanc_limit.append(fac['Ref']['Sanction Limit'])
                    
                    else:
                        sanc_limit.append(fac['Ref']['Credit limit'])                                 
        i = i+1 
    return sanc_limit        


def get_position_date(cibs):
    position_date = []
    for fac_type in (cibs.installment_facility, cibs.credit_card_facility):
        if fac_type is not None:
            for fac in fac_type:
                if (fac['Ref']['Phase']) == 'Living':
                    date = (fac['Contract History']['Date'][0]).date()
                    date_str = (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
                    position_date.append(date_str)
    return position_date


def get_outstanding(cibs)->list:
    '''
    List of Outstanding values

    '''
    outstanding = []
    for fac_type in (cibs.installment_facility, cibs.credit_card_facility):
        if fac_type is not None:
            for fac in fac_type:
                if (fac['Ref']['Phase']) == 'Living':
                    outstanding.append(fac['Contract History'].sort_values('Date', ascending=False).Outstanding[0])
    return outstanding                
           
def get_overdue(cibs):
    '''
    list of overdues
    
    '''
    overdue = []
    for fac_type in (cibs.installment_facility, cibs.credit_card_facility):
        if fac_type is not None:
            for fac in fac_type:
                if (fac['Ref']['Phase']) == 'Living':
                    overdue.append((fac['Contract History']).sort_values('Date', ascending=False).Overdue[0])
                
    return overdue

def avg_get_overdue(cibs):
    '''
    Last 12 months average outstanding, only for Credit card 
    For installment facility taking zero
    
    '''
    avg_cc = []
    if cibs.installment_facility is not None: 
        
        for fac in cibs.installment_facility:
            
            if (fac['Ref']['Phase']) == 'Living':
                
                avg_cc.append("--")
                
                
    if cibs.credit_card_facility is not None:
    
        for fac in cibs.credit_card_facility :
            
            if ((fac['Ref']['Phase']) == 'Living'):
                avg_cc.append((sum(fac['Contract History'].sort_values('Date', ascending=False).Overdue [:12]))/12)
    return avg_cc
                


def cl_status(cibs):
    '''
    List of status
    
    '''
    sta = []
    for fac_type in (cibs.installment_facility, cibs.credit_card_facility):
        if fac_type is not None:
            for fac in fac_type:
                if (fac['Ref']['Phase']) == 'Living':
                    sta.append((fac['Contract History']).sort_values('Date', ascending=False).Status[0])
    return sta

def EMI_2(cibs):
    
    EMI = []
    if type(cibs.installment_facility) == list:
        for facility in cibs.installment_facility:
            if facility['Ref']['Phase'] == 'Living':
                EMI.append(facility['Ref']['Installment Amount'])
                
    if type(cibs.credit_card_facility) == list:
        
        for facility in cibs.credit_card_facility:
            if facility['Ref']['Phase'] == 'Living':
                
                credit = (facility['Ref']['Credit limit'])    
                outstand = (facility['Contract History'].sort_values('Date', ascending=False)['Outstanding'][0])
                if outstand == 0:
                    EMI.append(float('inf'))

                if ((sum(facility['Contract History'].sort_values('Date', ascending=False)['Outstanding'][:12]))/12) == 0:
                    EMI.append(0)

                elif ((credit/outstand)*100 <= 60) :
                    EMI.append(credit*(.02))

                else:
                    EMI.append(outstand*(.05))
    
    
    return EMI 
               
def Loan_start_date(cibs):  
    date_str = []
    for fac_type in (cibs.installment_facility, cibs.credit_card_facility):
        if fac_type is not None:
            for fac in fac_type:
                if (fac['Ref']['Phase']) == 'Living':
                    date = fac['Ref']['Starting date']
                    date_str.append(date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
    return date_str
   
def Loan_expiry_date(cibs):
    date_str = []
    for fac_type in (cibs.installment_facility, cibs.credit_card_facility):
        if fac_type is not None:
            for fac in fac_type:
                if (fac['Ref']['Phase']) == 'Living':
                    if (fac['Ref']['End date of contract']) is None:
                        date_str.append('Not present')
                    else:
                        date = fac['Ref']['End date of contract']
                        date_str.append(date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
    return date_str
