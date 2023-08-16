from glob import glob
from cib_data_class import cib_class
import json
from json import load
from tqdm.notebook import tqdm

from datetime import  datetime, timedelta
import collections
from collections import Counter



def is_living(facility):
    if facility["Ref"]["Phase"] == "Living":
        return True
    else:
        return False

def isNonFunded(fac):
    """
    much faster than regex matching
    classification of non funded based on IDLC response
    Non-Funded : LC (Letter of Credit), BG (Bank Guarantee), Guarantee, Payment Guarantee
    """
    if ('non funded' in fac["Ref"]["Facility"].lower() or
        'letter of credit' in fac["Ref"]["Facility"].lower() or
        'guarantee' in fac["Ref"]["Facility"].lower() or
        'other indirect facility' in fac["Ref"]["Facility"].lower() ):
        return True
    return False
    
def tot_fund_terminated_loan(facility):
    
    No_ter_loan  = 0
    
    for fac in facility:
        
        if is_living(fac) != False and isNonFunded(fac)==False:
    
            No_ter_loan += 1
        
    return No_ter_loan

def tot_nonfund_terminated_loan(facility):
    
    No_ter_loan  = 0
    
    for fac in facility:
        
        if is_living(fac) != False and isNonFunded(fac)==True:
    
            No_ter_loan += 1
        
    return No_ter_loan

def get_class_from_set(classes : set):
    for classification in ('BLW', 'BL', 'DF', 'SS', 'SMA', 'UC', "STD"):
        if classification in classes:
            return classification
    return None

def get_worst_status(facility : dict):
    return get_class_from_set(set(facility["Contract History"].Status))


def funded_ins_limit(cibs):

    try:
        installment = []
        
        for cib in cibs:

            if type(cib.installment_facility) == list:
                for fac in cib.installment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) != True:
                            
                        installment.append(fac['Ref']['Sanction Limit'])
        return installment
    except Exception as exc:
        print("funded_ins_limit: ", exc)
        return None

def funded_ins_facility_name(cibs):                    

    try:                
        facility_name = []
        
        for cib in cibs:

            if type(cib.installment_facility) == list:
                
                for fac in cib.installment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) != True: 
                        
                        facility_name.append(fac['Ref']['Facility'])
                        
        return facility_name
    except Exception as exc:
        print("funded_ins_facility_name: ", exc)
        return None

def funded_ins_worse_cl_status(cibs):   
    try:
        cl_status = []
        
        for cib in cibs:

            if type(cib.installment_facility) == list:
                
                for fac in cib.installment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) != True: 
                        
                        cl_status.append(get_worst_status(fac))
                        
        return cl_status
    except Exception as exc:
        print("funded_ins_worse_cl_status: ", exc)
        return None
                    
def classification_date(fac):
    
    '''
    Helper function to extract starting date
    
    Output : day-month-year
    
    '''
    try: 
        if (fac['Ref']['Date of classification']) is None:
            date = 'Not present'
        else:
            date = fac['Ref']['Date of classification']
            date = (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
        return date
    except Exception as exc:
        print("classification_date: ",exc)
        return None
                  

def funded_ins_date_of_class(cibs):
    try:
        date = []
        for cib in cibs:

            if type(cib.installment_facility) == list:
                
                for fac in cib.installment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) != True: 
                        
                        date.append(classification_date(fac))
        return date
    except Exception as exc:
        print("funded_ins_date_of_class: ",exc)
        return None

def funded_non_ins(cibs):
    try:
        non_installment = []
        
        for cib in cibs:

            if type(cib.noninstallment_facility) == list:
                
                for fac in cib.noninstallment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) != True:
                            
                        non_installment.append(fac["Contract History"]['SancLmt'][0])
        return non_installment
    except Exception as exc:
        print("funded_non_ins: ",exc)
        return None    

def funded_non_ins_facility_name(cibs):   
    try:               
        facility_name = []
        
        for cib in cibs:

            if type(cib.noninstallment_facility) == list:
                
                for fac in cib.noninstallment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) != True: 
                        
                        facility_name.append(fac['Ref']['Facility'])
                        
        return facility_name
    except Exception as exc:
        print("funded_non_ins_facility_name: ",exc)
        return None

def funded_non_ins_worse_cl_status(cibs):   
    try: 
        cl_status = []
        
        for cib in cibs:

            if type(cib.noninstallment_facility) == list:
                
                for fac in cib.noninstallment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) != True: 
                        
                        cl_status.append(get_worst_status(fac))
                        
        return cl_status
    except Exception as exc:
        print("funded_non_ins_worse_cl_status: ",exc)
        return None
                    
def classification_date(fac):
    
    '''
    Helper function to extract starting date
    
    Output : day-month-year
    
    '''
    
    if (fac['Ref']['Date of classification']) is None:
        date = 'Not present'
    else:
        date = fac['Ref']['Date of classification']
        date = (date.strftime("%d")+'-'+date.strftime("%b")+'-'+date.strftime("%y"))
    return date

def funded_non_ins_date_of_class(cibs):

    try: 
        date = []
        for cib in cibs:

            if type(cib.noninstallment_facility) == list:
                
                for fac in cib.noninstallment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) != True: 
                        
                        date.append(classification_date(fac))
        return date     
    except Exception as exc:
        print("funded_non_ins_date_of_class: ", exc)
        return None         
   
def term_total_funded_loan(cibs):
        
    try:
     
        terminated_loan = 0
    
        for cib in cibs:

            if type(cib.installment_facility) == list:

                terminated_loan += (tot_fund_terminated_loan(cib.installment_facility))
                
            if type(cib.noninstallment_facility) == list:    
            
                terminated_loan += (tot_fund_terminated_loan(cib.noninstallment_facility))  
   
        return terminated_loan 
    except Exception as exc:
        print("term_total_funded_loan: ",exc)
        return None
    
def term_total_nonfunded_loan(cibs):

    try: 
        terminated_loan = 0
        for cib in cibs:

            if type(cib.installment_facility) == list:

                terminated_loan += (tot_nonfund_terminated_loan(cib.installment_facility))
        
            if type(cib.noninstallment_facility) == list:    
                terminated_loan += (tot_nonfund_terminated_loan(cib.noninstallment_facility))
                
        return terminated_loan 
    
    except Exception as exc:
        print("term_total_nonfunded_loan: ",exc)
        return None 
    
    
def nonfunded_facility_name(cibs):     

    try:               
                    
        facility_name = []
        
        for cib in cibs:
            
            if type(cib.installment_facility) == list:
                
                for fac in cib.installment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) == True: 
                        
                        facility_name.append(fac['Ref']['Facility'])
                        
            if type(cib.noninstallment_facility) == list:
                
                for fac in cib.noninstallment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) == True: 
                        
                        facility_name.append(fac['Ref']['Facility'])
                        
        return facility_name
    except Exception as exc:
        print("nonfunded_facility_name: ",exc)
        return None
    


def nonfunded_limit(cibs):

    try: 
        Sanc_limit = []
        
        for cib in cibs:
            
            if type(cib.installment_facility) == list:
                
                for fac in cib.installment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) == True:
                            
                        Sanc_limit.append(fac['Ref']['Sanction Limit'])
            
                        
            if type(cib.noninstallment_facility) == list:
                
                for fac in cib.noninstallment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) == True:
                            
                        Sanc_limit.append(fac['Ref']['SancLmt'][0])
                        
        return Sanc_limit

    except Exception as exc:
        print("nonfunded_limit: ",exc)
        return None

   
    
    
def nonfunded_worse_cl_status(cibs):  

    try:
        cl_status = []
        
        for cib in cibs:
            if type(cib.installment_facility) == list:
                
                for fac in cib.installment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) == True: 
                        
                        cl_status.append(get_worst_status(fac))
            
            if type(cib.noninstallment_facility) == list:
                
                for fac in cib.noninstallment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) == True: 
                        
                        cl_status.append(get_worst_status(fac))
              
        return cl_status  
    
    except Exception as exc:
        print("nonfunded_worse_cl_status: ",exc)
        return None 
    
    
    
def nonfunded_date_of_class(cibs):
    try: 
        date = []
        for cib in cibs:
            if type(cib.installment_facility) == list:
                
                for fac in cib.installment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) == True: 
                        
                        date.append(classification_date(fac))
                        
            if type(cib.noninstallment_facility) == list:
                
                for fac in cib.noninstallment_facility:
                    
                    if is_living(fac) == False and isNonFunded(fac) == True: 
                        
                        date.append(classification_date(fac))
        return date
    
    except Exception as exc:
            print("nonfunded_date_of_class: ",exc)
            return None
    



