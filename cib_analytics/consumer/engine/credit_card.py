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