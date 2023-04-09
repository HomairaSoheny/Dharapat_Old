def Borrowers_name(cibs):
    try:
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
    
def avg_get_overdue(cibs):
    try:
        '''
        Last 12 months average outstanding, only for Credit card 
        For installment facility taking "--"
        
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

def EMI_2(cibs):
    try:
        
        '''
        
        Response of PBL:  {In case of Term Loan, you will only include the
                        EMI amount (Monthly Installment). In case of type
                        of EMI (Quarterly / Half Yearly), you will convert
                        the Quarterly / Half Yearly EMI into Monthly
                        Installment.
                        
                        For credit card
                        (1) = if &lt;60% usage of Card Limit, then (Credit Card Limit × 2%) or
                        (2) = if &gt;60% usage of Card Limit, then (Credit Card Outstanding × 5%)
                        
                        For example,
                        (1) if Credit Card Limit is Tk. 1.00 lac &amp; Outstanding is Tk. 59,000 which is 59% usage 
                            of card limit (or less than 60% usage), then formula will be Credit Card Limit Tk. 1.00 lac X 2% = Tk. 2,000.
                        (2) if Credit Card Limit is Tk. 1.00 lac &amp; Outstanding is Tk. 70,000 which is 70% usage
                                of card limit (or more than 60% usage), then formula will be Credit Card Outstanding Tk.70,000 X 5% = Tk. 3,500.
        '''
        
        EMI = []        
        if type(cibs.installment_facility) == list:            
            for facility in cibs.installment_facility:                
                if facility['Ref']['Phase'] == 'Living':                
                    if facility['Ref']['Payments periodicity'].lower()  == 'quarterly installments':                    
                        EMI.append(round((facility['Ref']['Installment Amount'])/4))            
                    elif facility['Ref']['Payments periodicity'].lower()   == 'half yearly installments':
                        EMI.append(round((facility['Ref']['Installment Amount'])/6))
                    else:
                        EMI.append(facility['Ref']['Installment Amount'])

        if type(cibs.credit_card_facility) == list:
            for facility in cibs.credit_card_facility:
                if facility['Ref']['Phase'] == 'Living':
                    credit = (facility['Ref']['Credit limit'])
                    outstand = (facility['Contract History'].sort_values('Date', ascending=False).Outstanding[0])
                    if round(credit*(.6)) >= outstand :
                        EMI.append(round(credit*.02))
                    else:
                        EMI.append(outstand*(.05))
        
        return EMI
    except Exception as e:
        print(e)
        return []
               
def Loan_start_date(cibs):  
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
   
def Loan_expiry_date(cibs):
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
