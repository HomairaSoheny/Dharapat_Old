from ..cib_data_class import cib_class
from ..api_generation.consumer_dashboard import get_credit_card_table, get_loan_table, get_personal_loan_table
import pandas as pd
from io import BytesIO
import xlsxwriter
import datetime

def create_report_dashboard(cib_datas, output_dir: str):
    Output = output_dir + f'\\filename dashboard {datetime.datetime.now().strftime("%d-%m-%Y %Hh%Mm%Ss")}.xlsx'
    io = BytesIO()
    writer = pd.ExcelWriter(io, engine='xlsxwriter', )

    for cib in cib_datas:
        generate_consumer_spreadsheet(writer, cib)
    
    return writer, io

def generate_consumer_spreadsheet(writer, cib):

    credit_card_table = pd.DataFrame(data=cib['credit_facilities_in_the_name_of_applicant_for_credit_card'])
    loan_table = pd.DataFrame(data=cib['credit_facilities_is_the_name_of_applicant_for_personal_loan_car_loan_home_loan'])
    personal_loan_table = pd.DataFrame(data=cib['credit_facilities_in_the_name_of_applicants_business_for_personal_loan_car_loan_home_loan_credit_card'])

    #writer = pd.ExcelWriter('consumer.xlsx', engine='xlsxwriter', )
    #writer = xlsxwriter.Workbook(io, {'nan_inf_to_errors': True})
    #writer = pd.ExcelWriter(io, engine='xlsxwriter', )

    personal_loan_table.to_excel(writer, sheet_name="1", index=False)
    credit_card_table.to_excel(writer, sheet_name="2", index=False)
    loan_table.to_excel(writer, sheet_name="3", index=False)
    

    for column in personal_loan_table:
        column_length = max(personal_loan_table[column].astype(str).map(len).max(), len(column))
        col_idx = personal_loan_table.columns.get_loc(column)
        writer.sheets["1"].set_column(col_idx, col_idx, column_length)

    for column in credit_card_table:
        column_length = max(credit_card_table[column].astype(str).map(len).max(), len(column))
        col_idx = credit_card_table.columns.get_loc(column)
        writer.sheets["2"].set_column(col_idx, col_idx, column_length)
    
    for column in loan_table:
        column_length = max(loan_table[column].astype(str).map(len).max(), len(column))
        col_idx = loan_table.columns.get_loc(column)
        writer.sheets["3"].set_column(col_idx, col_idx, column_length)