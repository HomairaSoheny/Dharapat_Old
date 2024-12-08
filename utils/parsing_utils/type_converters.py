"""
Functions for proper type conversion of parsed cib report fields
Some functions may break if key names or column names change
    e.g. if and when 'Requestdate' gets changed to 'Request date'
Fix -> change key and column names to new ones
"""

import pandas as pd
from datetime import datetime
import copy
from typing import Union
import re

def handle_date(date: str):
    if date == '-':
            return None
    else:
        if date != '':
            return datetime.strptime(re.sub("[^0-9/]", "", date), '%d/%m/%Y').date()

    #if value is '', keep as is
    return None

def handle_integer_conversion(i : str):
    try:
        return int(i.replace(',',''))
    except ValueError:
        # in case of unexpected decimal values
        return float(i.replace(',',''))

def convert_cib_header(df : pd.DataFrame):
    df = df.copy()
    df['Date of Inquiry'] = pd.to_datetime(df['Date of Inquiry'])
    return df

def convert_inquired(inq : dict):
    """
    Cases found:
    with 1 key, in CD, Corporate and SME
    with 5 keys, in SME and Corporate
    with 9 keys, in CD and SME -> DOB : datetime
    with 13 keys, in SME -> DOB : datetime
    """
    inq = inq.copy()
    if 'DOB' in inq.keys():
        inq['DOB'] = handle_date(inq['DOB'])

    return inq

def convert_subject_info(sub : dict):
    """
    Cases found:
    20 keys, in CD, SME and Corporate -> 'Date of birth' : datetime
    13 keys, in SME and Corporate -> 'Registration date' : datetime
    some keys may have the value '-'
    """
    sub = sub.copy()

    if 'Date of birth' in sub.keys():
        sub['Date of birth'] = handle_date(sub['Date of birth'])

    if 'Registration date' in sub.keys():
        sub['Registration date'] = handle_date(sub['Registration date'])

    return sub

def convert_summary_1_2(s : dict):
    s = s.copy()
    for key in s.keys():
        s[key] = handle_integer_conversion(s[key])

    return s

def convert_facility_table(df : pd.DataFrame):
    df = df.copy()
    for i in df.columns[1:]:
        df[i] = pd.to_numeric(df[i].apply(lambda x:x.replace(',','')))

    return df

def convert_req_contracts(df : pd.DataFrame):
    df = df.copy()
    df['Request date'] = pd.to_datetime(df['Request date'], dayfirst=True)
    for key in df.columns:
        if key.replace(' ','') == 'TotalRequestedAmount':
            Total_Requested_Amount = key
            break
    df[Total_Requested_Amount] = pd.to_numeric(df[Total_Requested_Amount].apply(lambda x:x.replace(',','')))

    return df

#sort by date - 1st row latest date

def convert_contract_history(df: Union[pd.DataFrame, dict]):
    """
    For handling contract history tables in all facilities
        -> installment, noninstallment and credit card
    """
    df = df.copy()
    if type(df)==dict:
        return df
    
    if 'Accounting Date' in df.columns:
        df.rename(columns={'Accounting Date': 'Date'}, inplace=True)


    df.Date = pd.to_datetime(df.Date, dayfirst=True)
    for col in df.columns:
        if col not in ('Date', 'Status', 'Default'):
            #df[col] = pd.to_numeric(df[col].apply(lambda x:x.replace(',','')))
            df[col] = df[col].apply(lambda x: x.replace(',', '') if isinstance(x, str) else x)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df.sort_values('Date', ascending=False)    


def convert_installment_facility(facilities : list):
    '''
    Meant for both installment and non-installment facilities
    '''
    facilities = copy.deepcopy(facilities)
    for fac in facilities:
        #all date conversions for installment & noninstallment facilities
        for date in ('Date of Last Update', 'Date of Law suit', 'Date of last payment', 'Starting date',
                     'Date of classification', 'End date of contract', 'Date of last rescheduling'):
            try:
                fac['Ref'][date] = handle_date(fac['Ref'][date])
            except KeyError:
                #handle joining of words due to line break
                for key in fac['Ref'].keys():
                    if key.replace(' ','') == date.replace(' ',''):
                        date = key
                        fac['Ref'][date] = handle_date(fac['Ref'][date])
                        break

        #converting all possible numbers to integer
        for key in fac['Ref'].keys():
            if type(fac['Ref'][key]) == str and fac['Ref'][key].replace(',','').isnumeric():
                fac['Ref'][key] = handle_integer_conversion(fac['Ref'][key])

        #handling contract history
        fac['Contract History'] = convert_contract_history(fac['Contract History'])

    return facilities

def convert_credit_card_facility(facilities : list):
    facilities = copy.deepcopy(facilities)

    for fac in facilities:
        #all date conversion for installment & noninstallment facilities
        for date in ('Date of Last Update', 'Date of Law suit', 'Starting date',
                     'Date of classification', 'End date of contract', 'Date of last rescheduling'):
            try:
                fac['Ref'][date] = handle_date(fac['Ref'][date])
            except KeyError:
                #handle joining of words due to line break
                for key in fac['Ref'].keys():
                    if key.replace(' ','') == date.replace(' ',''):
                        date = key
                        fac['Ref'][date] = handle_date(fac['Ref'][date])
                        break

        #converting all possible numbers to integer
        for key in fac['Ref'].keys():
            if type(fac['Ref'][key]) == str and fac['Ref'][key].replace(',','').isnumeric():
                fac['Ref'][key] = handle_integer_conversion(fac['Ref'][key])

        #handling contract history
        fac['Contract History'] = convert_contract_history(fac['Contract History'])

    return facilities