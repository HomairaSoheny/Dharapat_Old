def st_date(fac):
    try:
        
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
    except Exception as e:
        print(e)
        return []


def ex_date(fac):
    try:
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
    except Exception as e:
        print(e)
        return []

def pos_date(fac):
    try:
            
        '''
        Helper function to extract the recent date of contract history
        
        '''
        
        date = (fac['Contract History']['Date'][0]).date()
        
        return (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
    except Exception as e:
        print(e)
        return []
    


                    
                    
def app_business(cibs):
    try:
        '''
        list of subject code of applicannt's buisness
        
        '''
        list_buisness = []
        if cibs.company_list is None:
            return None
        else:
            list_buisness = (cibs.company_list['CIB subject code']).unique()
            return list_buisness
    except Exception as e:
        print(e)
        return []

def Borrowers_name(cibs):
    '''
        Will extract the borrower name 
        from "Other subjects linked to the same contract" for each facilility
        
    '''
    try:
        list_app = app_business(cibs)
    
        Borrow_name = []
        if cibs.installment_facility is not None: 
            for fac in cibs.installment_facility:
                if (fac['Ref']['Phase']) == 'Living':


                    if  (fac["Ref"]['Role']) == 'Borrower':

                        if cibs.subject_info['Type of subject'].lower() == 'individual':

                            Borrow_name.append(cibs.subject_info['Title, Name'])

                    else: 
                        if fac['Other subjects linked to the same contract'] is not None:

                            for j in range(len(fac['Other subjects linked to the same contract'])):
                                if (fac['Other subjects linked to the same contract'].iloc[j]["Role"]) == "Borrower": # and \
                                    #fac['Other subjects linked to the same contract'].iloc[j]['CIB subject code'] in list_app:
                                    Borrow_name.append(fac['Other subjects linked to the same contract'].iloc[j]["Name"])
                                    
                    

        if cibs.noninstallment_facility is not None:

            for fac in cibs.noninstallment_facility:

                if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':


                    if  (fac["Ref"]['Role']) == 'Borrower':

                        if cibs.subject_info['Type of subject'].lower() == 'individual':

                            Borrow_name.append(cibs.subject_info['Title, Name'])

                    else: 
                        if fac['Other subjects linked to the same contract'] is not None:

                            for j in range(len(fac['Other subjects linked to the same contract'])):
                                if (fac['Other subjects linked to the same contract'].iloc[j]["Role"]) == "Borrower":# and \
                                    #fac['Other subjects linked to the same contract'].iloc[j]['CIB subject code'] in list_app:
                                    Borrow_name.append(fac['Other subjects linked to the same contract'].iloc[j]["Name"])

        return Borrow_name           

    except Exception as e:
        print(e)
        return []


def get_Applicants_Role(cibs):
    try:
        '''
        Only the role of applicant's
        Output ->  Sequential list   
        
        ''' 
        app_role  = []
        
        if cibs.installment_facility is not None: 
            for fac in cibs.installment_facility:
                if (fac['Ref']['Phase']) == 'Living': #and fac['Other subjects linked to the same contract'] is not None :
                    app_role.append(fac["Ref"]['Role'])
        if cibs.noninstallment_facility is not None:
            for fac in cibs.noninstallment_facility:
                if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                    app_role.append(fac["Ref"]['Role'])    
        return app_role 

    except Exception as e:
        print(e)
        return []

def get_facility_name(cibs):
    try:
        facility = []
        
        if cibs.installment_facility is not None: 
            for fac in cibs.installment_facility:
                if (fac['Ref']['Phase']) == 'Living' and fac['Other subjects linked to the same contract'] is not None:
                    facility.append(fac['Ref']['Facility'])
        if cibs.noninstallment_facility is not None:
             for fac in cibs.noninstallment_facility :
                if (fac['Ref']['Phase']) == 'Living' and fac['Other subjects linked to the same contract'] is not None and \
                        fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                    facility.append(fac['Ref']['Facility'])
        return facility

    except Exception as e:
        print(e)
        return []


def sanc_limit(cibs):
    try:
        
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

                if (fac['Ref']['Phase']) == 'Living'  and fac['Ref']['Facility']=='Cash Credit against Hypothecation':

                    limit.append(fac['Contract History']['SancLmt'][0])
        return limit
     

        
    except Exception as e:
        print(e)
        return []
    



def get_position_date(cibs):
    try:
        
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

                if (fac['Ref']['Phase']) == 'Living'  and fac['Ref']['Facility']=='Cash Credit against Hypothecation':

                    position_date.append(pos_date(fac))   
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

        list_app = app_business(cibs)


        if cibs.installment_facility is not None: 

            for fac in cibs.installment_facility:

                    if (fac['Ref']['Phase']) == 'Living':
                        outstanding.append(fac['Contract History'].sort_values('Date', ascending=False).Outstanding[0])

            if cibs.noninstallment_facility is not None:

                for fac in cibs.noninstallment_facility :

                    if (fac['Ref']['Phase']) == 'Living'  and fac['Ref']['Facility']=='Cash Credit against Hypothecation':

                        outstanding.append(fac['Contract History'].sort_values('Date', ascending=False).Outstand[0])

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
        list_app = app_business(cibs)

        if cibs.installment_facility is not None: 

            for fac in cibs.installment_facility:

                if (fac['Ref']['Phase']) == 'Living':# and fac['Other subjects linked to the same contract'] is not None :

                        overdue.append(fac['Contract History'].sort_values('Date', ascending=False).Overdue[0])
        if cibs.noninstallment_facility is not None:

            for fac in cibs.noninstallment_facility :

                if (fac['Ref']['Phase']) == 'Living'  and  fac['Ref']['Facility']=='Cash Credit against Hypothecation':#fac['Other subjects linked to the same contract'] is not None and \

                    overdue.append(fac['Contract History'].sort_values('Date', ascending=False).Overdue [0])
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
        if cibs.installment_facility is not None: 
            for fac in cibs.installment_facility:
                if (fac['Ref']['Phase']) == 'Living' and fac['Other subjects linked to the same contract'] is not None:
                    sta.append((fac['Contract History']).sort_values('Date', ascending=False).Status[0])
        if cibs.noninstallment_facility is not None:
            for fac in cibs.noninstallment_facility :
                if (fac['Ref']['Phase']) == 'Living'  and  fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                    sta.append((fac['Contract History']).sort_values('Date', ascending=False).Status[0])
        return sta

    except Exception as e:
        print(e)
        return []

def EMI_3(cibs):
    try:
        '''
       
        Interest Rate of CC-Hypo / OD (%) will be inputted manually

        EMI of Term Loan or Monthly Interest of CC/OD
        
        Monthly Interset of CC/OD= (CC Limit × %) ÷ 12
        
        '''
        EMI = []
        Ir = 60
        list_app = app_business(cibs)


        if type(cibs.installment_facility) == list:
            for fac in cibs.installment_facility:
                if fac['Ref']['Phase'] == 'Living': 
                    EMI.append(fac['Ref']['Installment Amount'])

        if type(cibs.noninstallment_facility) == list:

            for fac in cibs.noninstallment_facility:
                if (fac['Ref']['Phase']) == 'Living' and  fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                    CC_limit = (fac['Contract History']['SancLmt'][0])
                    Mon_Ir = (CC_limit * (Ir/100) )/12

                    EMI.append(round(Mon_Ir))

        return EMI 
        

    except Exception as e:
        print(e)
        return []

def Loan_start_date(cibs):
    try:
        
        '''
        Extract loan starting date in a list
        
        Output: d-m-y
        
        '''
        date_str = []
        list_app = app_business(cibs)

        if cibs.installment_facility is not None: 

            for fac in cibs.installment_facility:

                if (fac['Ref']['Phase']) == 'Living' : 
                    date_str.append(st_date(fac))

        if cibs.noninstallment_facility is not None:

            for fac in cibs.noninstallment_facility :

                if (fac['Ref']['Phase']) == 'Living' and fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                    #    fac['Ref']['Facility']=='Cash Credit against Hypothecation':

                    date_str.append(st_date(fac))

        return date_str

  
    except Exception as e:
        print(e)
        return []




def Loan_expiry_date(cibs):
    try:
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
                        #fac['Ref']['Facility']=='Cash Credit against Hypothecation':
                    date_str.append(ex_date(fac))

        return date_str
    except Exception as e:
        print(e)
        return []
