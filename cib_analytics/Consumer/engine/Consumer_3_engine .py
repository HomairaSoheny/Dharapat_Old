

def st_date(fac):
    
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


def ex_date(fac):
    
    '''
    Helper function to extract End date of contract
    
    Output : day-month-year
    
    '''
    
    if (fac['Ref']['End date of contract']) is None:
        date = 'Not present'
    else:
        date = fac['Ref']['End date of contract']
        date = (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
    return date  


def pos_date(fac):
    
    '''
    Helper function to extract the recent date of contract history
    
    '''
    
    date = (fac['Contract History']['Date'][0]).date()
    
    return (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
 


def app_business(cibs):
    list_buisness = []
    if cibs.company_list is None:
        return None
    else:
        list_buisness = (cibs.company_list['CIB subject code']).unique()
        return list_buisness

def Borrowers_name(cibs):
    '''
    Will extract the borrower name 
    from "Other subjects linked to the same contract" for each facilility
    
    '''
    list_app = app_business(cibs)
    
    Borrow_name = []
    if cibs.installment_facility is not None: 
        for fac in cibs.installment_facility:
            if (fac['Ref']['Phase']) == 'Living':
                if i['Other subjects linked to the same contract'] is not None:
                    for j in range(len(i['Other subjects linked to the same contract'])):
                        if list_app is not None:
                            if (i['Other subjects linked to the same contract'].iloc[j]["Role"]) == "Borrower" and i['Other subjects linked to the same contract'].iloc[j]['CIB subject code'] in list_app:
                                Borrow_name.append(i['Other subjects linked to the same contract'].iloc[j]["Name"])
                            else:
                                 Borrow_name.append("Not given")  

                else:    
                    Borrow_name.append("Not given")  
    if cibs.noninstallment_facility is not None:
        for fac in cibs.noninstallment_facility:
            if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                if i['Other subjects linked to the same contract'] is not None:
                    for j in range(len(i['Other subjects linked to the same contract'])):
                        if list_app is not None:
                            if (i['Other subjects linked to the same contract'].iloc[j]["Role"]) == "Borrower" and i['Other subjects linked to the same contract'].iloc[j]['CIB subject code'] in list_app:
                                Borrow_name.append(i['Other subjects linked to the same contract'].iloc[j]["Name"])
                            else:
                                Borrow_name.append("Not given") 
                else:    
                    Borrow_name.append("Not given") 
    
    return Borrow_name                    



def get_Applicants_Role(cibs):
    '''
    Only the role of applicant's
    Output ->  Sequential list   
    
    ''' 
    app_role  = []
    
    if cibs.installment_facility is not None: 
        for fac in cibs.installment_facility:
            if (fac['Ref']['Phase']) == 'Living':
                app_role.append(i["Ref"]['Role'])
    if cibs.noninstallment_facility is not None:
        for fac in cibs.noninstallment_facility:
            if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                    app_role.append(i["Ref"]['Role'])    
    return app_role 


def get_facility_name(cibs):
    facility = []
    
    if cibs.installment_facility is not None: 
        for fac in cibs.installment_facility:
            if (fac['Ref']['Phase']) == 'Living':
                facility.append(fac['Ref']['Facility'])
    if cibs.noninstallment_facility is not None:
        for fac in cibs.noninstallment_facility :
            if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                facility.append(fac['Ref']['Facility'])
    return facility

def sanc_limit(cibs):
    
    '''
    Sanction limit for only installment and non-installment facility
    '''
    limit = []    
    if cibs.installment_facility is not None: 
        
        for fac in cibs.installment_facility:
            
            if (fac['Ref']['Phase']) == 'Living':
                
                limit.append(fac['Ref']['Sanction Limit'])
                
    if cibs.noninstallment_facility is not None:
        
        for fac in cibs.noninstallment_facility :
            
            if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                
                limit.append(fac['Contract History']['SancLmt'][0])
    return limit
    




def get_position_date(cibs):
    
    '''
    Recent contract history date
    
    Output: day-month-year
    
    '''
    
    position_date = []
    
    if cibs.installment_facility is not None: 
        
        for fac in cibs.installment_facility:
            
            if (fac['Ref']['Phase']) == 'Living':
                position_date.append(pos_date(fac))
                
    if cibs.noninstallment_facility is not None:
        
        for fac in cibs.noninstallment_facility :
            
            if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                
                position_date.append(pos_date(fac))   
                
    return position_date



def get_outstanding(cibs)->list:
    '''
    List of Outstanding values

    '''
    outstanding = []
    if cibs.installment_facility is not None: 
        
        for fac in cibs.installment_facility:
            
            if (fac['Ref']['Phase']) == 'Living':
                
                outstanding.append(fac['Contract History'].sort_values('Date', ascending=False).Outstanding[0])
                
    if cibs.noninstallment_facility is not None:
        
        for fac in cibs.noninstallment_facility :
            
            if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                
                outstanding.append(fac['Contract History'].sort_values('Date', ascending=False).Outstand[0])

    return outstanding                


def get_overdue(cibs):
    '''
    list of overdues
    
    '''
    overdue = []
    if cibs.installment_facility is not None: 
        
        for fac in cibs.installment_facility:
            
            if (fac['Ref']['Phase']) == 'Living':
                
                overdue.append(fac['Contract History'].sort_values('Date', ascending=False).Overdue[0])
                
    if cibs.noninstallment_facility is not None:
        
        for fac in cibs.noninstallment_facility :
            
            if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                
                overdue.append(fac['Contract History'].sort_values('Date', ascending=False).Overdue [0])
    return overdue


def cl_status(cibs):
    '''
    List of status
    
    '''
    sta = []
    if cibs.installment_facility is not None: 
        
        for fac in cibs.installment_facility:
            
            if (fac['Ref']['Phase']) == 'Living':
                
                sta.append((fac['Contract History']).sort_values('Date', ascending=False).Status[0])
                
    if cibs.noninstallment_facility is not None:
        
        for fac in cibs.noninstallment_facility :
            
            if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                
                sta.append((fac['Contract History']).sort_values('Date', ascending=False).Status[0])
            
    return sta

def EMI_3(cibs):
    
    '''
    

    Interest Rate of CC-Hypo / OD (%) will be inputted manually

    
    EMI of Term Loan or Monthly Interest of CC/OD
    
    Monthly Interset of CC/OD= (CC Limit × %) ÷ 12
    
    '''
    
    EMI = []
    Ir = 60
    
    if type(cibs.installment_facility) == list:
        for fac in cibs.installment_facility:
            if fac['Ref']['Phase'] == 'Living':
                EMI.append(fac['Ref']['Installment Amount'])
                
    if type(cibs.noninstallment_facility) == list:
        
        for fac in cibs.noninstallment_facility:
            if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                CC_limit = (fac['Ref']['Contract History']['SancLmt'][0])
                Mon_Ir = (CC_limit * (Ir/100) )/12

                EMI.append(round(Mon_Ir))

    return EMI 


def Loan_start_date(cibs):
    
    '''
    Extract loan starting date in a list
    
    Output: d-m-y
    
    '''
    
    date_str = []
    if cibs.installment_facility is not None: 
        
        for fac in cibs.installment_facility:
            
            if (fac['Ref']['Phase']) == 'Living':
                
                date_str.append(st_date(fac))
                
    if cibs.noninstallment_facility is not None:
        
        for fac in cibs.noninstallment_facility :
            
            if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                
                date_str.append(st_date(fac))

    return date_str




def Loan_expiry_date(cibs):
    
    '''
    Extract loan expiry date in a list
    
    Output: d-m-y
    
    '''
    
    date_str = []
    
    if cibs.installment_facility is not None: 
        
        for fac in cibs.installment_facility:
            
            if (fac['Ref']['Phase']) == 'Living':

                date_str.append(ex_date(fac))
                
    if cibs.noninstallment_facility is not None:

        for fac in cibs.noninstallment_facility :

            if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                date_str.append(ex_date(fac))
    
    return date_str





