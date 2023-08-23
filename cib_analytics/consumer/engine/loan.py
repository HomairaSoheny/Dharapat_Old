def EMI_1(cibs):
    
    '''
    Installment amount - Installment facilility
    % of credit card limit - Credit card facility
    '''
    
    EMI = []
    if type(cibs.installment_facility) == list:
        for facility in cibs.installment_facility:
            if facility['Ref']['Phase'] == 'Living':
                EMI.append(facility['Ref']['Installment Amount'])
                
    if type(cibs.credit_card_facility) == list:
        for facility in cibs.credit_card_facility:
            outstand = (facility['Contract History'].sort_values('Date', ascending=False).Outstanding[0])
            credit = (facility['Ref']['Credit limit'])
            if outstand == 0 or (credit/outstand)*100 <= 60 :
                EMI.append(credit*(.02))
            else:
                EMI.append(outstand*(.05))
    return EMI