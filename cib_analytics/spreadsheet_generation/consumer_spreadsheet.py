import pandas as pd
from io import BytesIO
import datetime

def create_report_dashboard(cib_datas, output_dir: str):
    Output = output_dir + f'\\filename dashboard {datetime.datetime.now().strftime("%d-%m-%Y %Hh%Mm%Ss")}.xlsx'
    io = BytesIO()
    writer = pd.ExcelWriter(io, engine='xlsxwriter', )

    for cib in cib_datas:
        generate_consumer_spreadsheet(writer, cib)
    
    return writer, io

def generate_consumer_spreadsheet(writer, cib):

    credit_card_table = pd.DataFrame(data=cib["credit_facilities_in_the_name_of_applicant_for_credit_card"])
    loan_table = pd.DataFrame(data=cib["credit_facilities_is_the_name_of_applicant_for_personal_loan_car_loan_home_loan"])
    personal_loan_table = pd.DataFrame(data=cib["credit_facilities_in_the_name_of_applicants_business_for_personal_loan_car_loan_home_loan_credit_card"])

    personal_loan_table.to_excel(writer, sheet_name="credit facilities in the name of applicants business for personal loan car loan home loan credit card", index=False)
    credit_card_table.to_excel(writer, sheet_name="credit facilities in the name of applicant for credit card", index=False)
    loan_table.to_excel(writer, sheet_name="credit facilities is the name of applicant for personal loan car loan home loan", index=False)
    

    for column in personal_loan_table:
        column_length = max(personal_loan_table[column].astype(str).map(len).max(), len(column))
        col_idx = personal_loan_table.columns.get_loc(column)
        writer.sheets["credit facilities in the name of applicants business for personal loan car loan home loan credit card"].set_column(col_idx, col_idx, column_length)

    for column in credit_card_table:
        column_length = max(credit_card_table[column].astype(str).map(len).max(), len(column))
        col_idx = credit_card_table.columns.get_loc(column)
        writer.sheets["credit facilities in the name of applicant for credit card"].set_column(col_idx, col_idx, column_length)
    
    for column in loan_table:
        column_length = max(loan_table[column].astype(str).map(len).max(), len(column))
        col_idx = loan_table.columns.get_loc(column)
        writer.sheets["credit facilities is the name of applicant for personal loan car loan home loan"].set_column(col_idx, col_idx, column_length)