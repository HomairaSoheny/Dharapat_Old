from ..api_generation.consumer_dashboard import get_credit_card_table, get_loan_table, get_personal_loan_table
import pandas as pd

def consumer_spreadsheet(cib):
    credit_card_table = pd.DataFrame(data=get_credit_card_table(cib))
    loan_table = pd.DataFrame(data=get_loan_table(cib))
    personal_loan_table = pd.DataFrame(data=get_personal_loan_table(cib))

    writer = pd.ExcelWriter('consumer.xlsx', engine='xlsxwriter', )

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

    writer.close()