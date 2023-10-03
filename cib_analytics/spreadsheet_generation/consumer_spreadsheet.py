import pandas as pd

def generate_consumer_spreadsheet(writer, cib):
    basic_info = pd.DataFrame(data=cib["basic_info"], index=[0]).T.reset_index()
    credit_card_loan = pd.DataFrame(data=cib["credit_facilities_in_the_name_of_applicant_for_credit_card"])
    personal_loan = pd.DataFrame(data=cib["credit_facilities_is_the_name_of_applicant_for_personal_loan_car_loan_home_loan"])
    business_loan = pd.DataFrame(data=cib["credit_facilities_in_the_name_of_applicants_business_for_personal_loan_car_loan_home_loan_credit_card"])

    # business_loan.to_excel(writer, sheet_name="business loan", index=False)
    # credit_card_loan.to_excel(writer, sheet_name="personal credit card", index=False)
    # personal_loan.to_excel(writer, sheet_name="personal loan", index=False)
    
    row, col = 8, 2
    # merge_format = writer.add_format(
    # {
    #     "bold": 1,
    #     "border": 1,
    #     "align": "center",
    #     "valign": "vcenter",
    #     "fg_color": "yellow",
    # })
    
    basic_info.to_excel(writer, sheet_name="Consumer Report", startrow=2, startcol=2, index=False)
    writer.sheets["Consumer Report"].merge_range("C3:D3", "CIB Informantion")
    
    writer.sheets["Consumer Report"].merge_range("C8:R8", "Credit facilities in the name of applicant: (For Personal Loan/Car Loan/Home Loan)")
    credit_card_loan.to_excel(writer, sheet_name="Consumer Report", startrow=row, startcol=col, index=False).set_text_wrap()
    row += credit_card_loan.shape[0]+3
    
    writer.sheets["Consumer Report"].merge_range("C"+str(row)+":R"+str(row), "Credit facilities in the name of applicant: (For Credit Card)")
    personal_loan.to_excel(writer, sheet_name="Consumer Report", startrow=row, startcol=col, index=False)
    row += personal_loan.shape[0]+3
    
    writer.sheets["Consumer Report"].merge_range("C"+str(row)+":R"+str(row), "Credit facilities in the name of applicant's business: (For Car Loan/Home Loan/Credit Card)")
    personal_loan.to_excel(writer, sheet_name="Consumer Report", startrow=row, startcol=col, index=False)
    
    

    # for column in business_loan:
    #     column_length = max(business_loan[column].astype(str).map(len).max(), len(column))
    #     col_idx = business_loan.columns.get_loc(column)
    #     writer.sheets["business loan"].set_column(col_idx, col_idx, column_length)

    # for column in credit_card_loan:
    #     column_length = max(credit_card_loan[column].astype(str).map(len).max(), len(column))
    #     col_idx = credit_card_loan.columns.get_loc(column)
    #     writer.sheets["personal credit card"].set_column(col_idx, col_idx, column_length)
    
    # for column in personal_loan:
    #     column_length = max(personal_loan[column].astype(str).map(len).max(), len(column))
    #     col_idx = personal_loan.columns.get_loc(column)
    #     writer.sheets["personal loan"].set_column(col_idx, col_idx, column_length)