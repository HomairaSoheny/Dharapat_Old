def borrowers_name(cibs)->list:
    '''
    Will extract the borrower name 
    from "Other subjects linked to the same contract" for each facilility
    
    Outpu -> List of strings
    '''
    borrow_name = []
    for fac_type in (cibs.installment_facility,cibs.credit_card_facility):
        if fac_type is not None:
            for i in fac_type:
                if (i['Ref']['Phase']) == 'Living':
                    
                    if  (i["Ref"]['Role']) == 'Borrower':
                        if cibs.subject_info['Type of subject'].lower() == 'individual':
                            for key in ['Title, Name', 'Title', 'Name']:
                                if key in cibs.subject_info.keys():
                                    title_ = cibs.subject_info[key]
                                else:
                                    title_ = str(cibs.subject_info)
                        else: # Company cib
                            title_ = cibs.subject_info['Trade Name']
                        
                        borrow_name.append(title_)
            
                    elif i['Other subjects linked to the same contract'] is not None:
                        for j in range(len(i['Other subjects linked to the same contract'])):
                            if (i['Other subjects linked to the same contract'].iloc[j]["Role"]) == "Borrower":
                                borrow_name.append(i['Other subjects linked to the same contract'].iloc[j]["Name"])
                    else:    
                        borrow_name.append("Not given")            
    return borrow_name

def get_applicants_role(cibs):
    try:
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
    except Exception as e:
        print(e)
        return []

def get_facility_name(cibs):
    try:
        '''
        output - list of strings (facility name)
        
        '''    
        fac_name = []
        for fac_type in (cibs.installment_facility,cibs.credit_card_facility):
            if fac_type is not None:
                for i in fac_type:
                    if (i['Ref']['Phase']) == 'Living':
                        fac_name.append(i['Ref']['Facility'])
        return fac_name
    except Exception as e:
        print(e)
        return []

def get_sanction_limit(cibs):
    try:
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
    except Exception as e:
        print(e)
        return []

def get_position_date(cibs):
    try:
        '''
        list of dates
        
        '''
        
        position_date = []
        for fac_type in (cibs.installment_facility, cibs.credit_card_facility):
            if fac_type is not None:
                for fac in fac_type:
                    if (fac['Ref']['Phase']) == 'Living':
                        date = (fac['Contract History']['Date'][0]).date()
                        date_str = (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
                        position_date.append(date_str)
        return position_date
    except Exception as e:
        print(e)
        return []

def get_outstanding(cibs)->list:
    try:
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
    except Exception as e:
        print(e)
        return []

def get_overdue(cibs):
    try:
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
    except Exception as e:
        print(e)
        return []

def cl_status(cibs):
    try:
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
    except Exception as e:
        print(e)
        return []

def loan_expiry_date(cibs):
    try:
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
    except Exception as e:
        print(e)
        return []

def loan_start_date(cibs):  
    try:
        date_str = []
        for fac_type in (cibs.installment_facility, cibs.credit_card_facility):
            if fac_type is not None:
                for fac in fac_type:
                    if (fac['Ref']['Phase']) == 'Living':
                        if (fac['Ref']['End date of contract']) is None:
                            date_str.append('Not present')
                        else:
                            date = fac['Ref']['Starting date']
                            date_str.append(date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
        return date_str
    except Exception as e:
        print(e)
        return []