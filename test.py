import json

import pandas as pd

# from cib_data_class import cib_class
from Dharapat_New.cib_data_class import CIB as cib_class
from utils.parsing_utils.parsing_helpers import parse_contract_facility_info, parse_other_subjects_linked, \
    parse_contract_history, raw_to_dict, rem_colon
#
# cib_path = "C:/Users/USER/Downloads/NOMAN TERRY TOWEL MILLS LTD.. (1).json"
# # cib_path = "C:/Users/USER/Downloads/10218185784.json"
# with open(cib_path) as f:
#     cib_data = cib_class(json.load(f))
#     cib_data.perform_sanity_check()
#     # cib_raw = json.load(f)
# cib_path = "C:/Users/USER/Downloads/json_files (1)/json_files\CITY SUGAR INDUSTRIES LIMITED.json"
# cib_path = "C:/Users/USER/Downloads/1006202410545815394054_S0030359286_MD. ABDUR RAZZAQ.json"
# with open(cib_path) as f:
#     cib_data = cib_class(json.load(f))
#     cib_data.perform_sanity_check()
#     print("sanity done successfully")
#
#
# def parse_cib_header(raw_list : list):
#     return pd.DataFrame(raw_list[2:], columns=raw_list[1])
#
# def handle_inquired(raw_list: list):
#     if len(raw_list[1])==1: #check case 'Subject code:XXXXXXXXXX'
#         k,v = raw_list[1][0].split(':')
#         return {k:v}
#     else:
#         try:
#           return raw_to_dict(raw_list)
#         except:
#             response_dict = {}
#             for lst in raw_list:
#                 for row in lst:
#                     if ":" in row:
#                         response_dict[row.split(":")[0]] = row.split(":")[1]
#             return response_dict
#
# def raw_to_dict(raw_list: list):
#     dict_form = {}
#     for i in raw_list[1:]:
#         if i[0].strip() == '' and i[1].strip() == '':
#             pass
#         else:
#             dict_form[rem_colon(i[0].strip())] =  i[1].strip()
#         if i[2].strip() == '' and i[3].strip() == '':
#             pass
#         else:
#             dict_form[rem_colon(i[2].strip())] =  i[3].strip()
#     return dict_form
#
# def parse_address(raw_list:list):
#     return pd.DataFrame(raw_list[2:], columns=raw_list[1])
#
# def parse_facility_table(raw_list:list):
#     header1 = [h.strip() for h in raw_list[2] if len(h.strip()) > 1]
#
#     columns = []
#     columns.append(header1[0])
#
#     for category in header1[1:]:
#         columns.append(category + "_No.")
#         columns.append(category + "_Amount")
#
#     data_rows = raw_list[4:]
#     df = pd.DataFrame(data_rows, columns=columns)
#     df_melted = df.melt(id_vars=['Contract Category'], var_name='Product_Measure', value_name='Value')
#
#     df_melted['Product_Measure'] = df_melted['Product_Measure'].str.replace('.', '', regex=False)
#     df_melted[['Product', 'Measure']] = df_melted['Product_Measure'].str.rsplit('_', n=1, expand=True)
#     df_melted['Contract_Category_Clean'] = df_melted['Contract Category'].str.replace(r'[^\w\s]', '', regex=True)
#     df_melted['Contract_Category_Clean'] = df_melted['Contract_Category_Clean'].str.replace(' ', '_')
#     df_melted['Product'] = df_melted['Product'].str.replace(' ', '_')
#
#     df_melted['Contract_Measure'] = df_melted['Contract_Category_Clean'] + '_' + df_melted['Measure']
#     df_melted['Value'] = df_melted['Value'].replace({',': ''}, regex=True)
#     df_melted['Value'] = pd.to_numeric(df_melted['Value'], errors='coerce')
#
#     # Pivot the DataFrame
#     df_pivot = df_melted.pivot_table(
#         index='Product',
#         columns='Contract_Measure',
#         values='Value',
#         aggfunc='first'
#     )
#
#     df_pivot.columns = df_pivot.columns.get_level_values(0)
#     df_pivot = df_pivot.reset_index()
#
#     desired_products = ['Installments', 'Non-Installments', 'Credit_Cards', 'Total']
#     df_pivot = df_pivot[df_pivot['Product'].isin(desired_products)]
#
#     return df_pivot
#
# def handle_contract_facility(raw_list:list):
#     """
#     Parameters
#     ----------
#     raw_list: list
#         Expecting input keys:
#             -> 'DETAILS OF INSTALLMENT FACILITY(S)'
#             -> 'DETAILS OF NONINSTALLMENT FACILITY(S)'
#             -> 'DETAILS OF CREDIT CARD FACILITY(S)'
#
#     Returns
#     -------
#     A list of dictionaries
#     Each dictionary contains one contract facility
#     with keys ['Ref'], ['Other subjects linked to the same contract']
#           and ['Contract History']
#
#         Type
#         ----
#         'Ref' : dictionary
#         'Other subjects linked to the same contract' : pandas.DataFrame
#         'Contract History' : pandas.DataFrame
#
#     """
#     facility_list = []
#     for i, fac in enumerate(raw_list):
#         facility = {}
#         if i==0:
#             facility['Ref'] = parse_contract_facility_info(raw_list[i]['Ref'][1:])
#         else:
#             facility['Ref'] = parse_contract_facility_info(raw_list[i]['Ref'][:])
#
#         facility['Other subjects linked to the same contract'] = parse_other_subjects_linked(
#                                     raw_list[i]['Other subjects linked to the same contract'])
#
#         facility['Contract History'] = parse_contract_history(raw_list[i]['Contract History'])
#
#
#         facility_list.append(facility)
#
#     return facility_list
#
#
# def parse_facility_table_B(raw_list:list):
#     df = pd.DataFrame(raw_list[3:], columns=raw_list[2]+[' '])
#     temp_cols = df.columns.tolist()
#     for i, header in enumerate(temp_cols):
#         if header.strip()=='':
#             col_name = temp_cols[i-1]
#             temp_cols[i-1] = col_name+'_No.'
#             temp_cols[i] = col_name+'_Amount'
#     df.columns = temp_cols
#     df = df[1:]
#     return df
#
# # parse_cib_header(cib_raw['Credit Information Report'])
# #
# # handle_inquired(cib_raw['INQUIRED'])
# #
# # raw_to_dict(cib_raw['SUBJECT INFORMATION'])
# #
# # parse_address(cib_raw['ADDRESS'])
# #
# # raw_to_dict(cib_raw['1. SUMMARY OF FACILITY(S) AS BORROWER & CO-BORROWER'])
# #
# # parse_facility_table(cib_raw['1.(A) SUMMARY OF THE FUNDED FACILITIES AS BORROWER & CO-BORROWER'])
# # parse_facility_table(cib_raw['2.(A) SUMMARY OF THE FUNDED FACILITIES AS GUARANTOR'])
# # parse_facility_table_B(cib_raw['1.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS BORROWER & CO-BORROWER'])
# # parse_facility_table_B(cib_raw['2.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS GUARANTOR'])
# # # handle_contract_facility(cib_raw['DETAILS OF INSTALLMENT FACILITY(S)'])
# # handle_contract_facility(cib_raw['DETAILS OF NONINSTALLMENT FACILITY(S)'])
# # # handle_contract_facility(cib_raw['DETAILS OF CREDIT CARD FACILITY(S)'])
# #
# #
# # print("parsing done")

import os,glob

# folder_path = 'C:/Users/USER/Downloads/For IM-20241015T092341Z-001/For IM/CIB - Corporate/CIB JMI Group'  # specify the folder path
folder_path = 'C:/Users/USER/Downloads/json_files (1)/json_files'
json_files = glob.glob(os.path.join(folder_path, '*.json'))

# List all files in the directory
a=0
# for file_name in os.listdir(folder_path):
#     if os.path.isfile(os.path.join(folder_path, file_name)):  # ensure it's a file, not a directory
#         print(file_name)
#         with open(file_name) as f:
#             cib_data = cib_class(json.load(f))
#             cib_data.perform_sanity_check()
#         a= a+1
#
for file_path in json_files:
    print(file_path)
    with open(file_path) as f:
        cib_data = cib_class(json.load(f))
        if cib_data.installment_facility:
            for each in cib_data.installment_facility:
                if each['Ref']['Phase'] == 'Terminated':
                    print(each['Ref']['Phase'])
        if cib_data.noninstallment_facility:
            for each in cib_data.noninstallment_facility:
                if each['Ref']['Phase'] == 'Terminated':
                    print(each['Ref']['Phase'])
        if cib_data.credit_card_facility:
            for each in cib_data.credit_card_facility:
                if each['Ref']['Phase'] == 'Terminated':
                    print(each['Ref']['Phase'])
        if pd.to_datetime(cib_data.cib_header['Date of Inquiry']).dt.date[0] < pd.to_datetime('2024-06-15').date():
            continue
        cib_data.perform_sanity_check()
    a = a + 1

print(a)