import pandas as pd


def generateConsumerSpreadsheet(writer, cib_report):
    workbook = writer.book
    start_row = 13
    
    term_loan = pd.DataFrame(cib_report["Credit Facilities as Applicant - Live (As Borrower)"]["Term Loan"])
    term_loan.to_excel(writer, sheet_name="CIB Analysis Report", startrow=start_row, index=False)
    start_row += term_loan.shape[0] + 3
    
    worksheet = writer.sheets["CIB Analysis Report"]
    bold = workbook.add_format({'bold': True})
    
    worksheet.write("A10", "Credit Facilities as Applicant - Live (As Borrower)", bold)
    worksheet.write("A13", "Term Loan", bold)
    worksheet.write("A"+str(start_row), "Credit Card", bold)
    
    credit_card = pd.DataFrame(cib_report["Credit Facilities as Applicant - Live (As Borrower)"]["Credit Card"])
    credit_card.to_excel(writer, sheet_name="CIB Analysis Report", startrow=start_row, index=False)
    start_row += credit_card.shape[0] + 3
    
    worksheet.write("A"+str(start_row), "Others", bold)
    others = pd.DataFrame(cib_report["Credit Facilities as Applicant - Live (As Borrower)"]["Others"])
    others.to_excel(writer, sheet_name="CIB Analysis Report", startrow=start_row, index=False)
    start_row =+ others.shape[0] + 3
    
    worksheet.write("A"+str(start_row), "Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)", bold)
    start_row += 2
    
    worksheet.write("A"+str(start_row), "Credit Card", bold)
    term_loan = pd.DataFrame(cib_report["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"]["Term Loan"])
    term_loan.to_excel(writer, sheet_name="CIB Analysis Report", startrow=start_row, index=False)
    start_row += term_loan.shape[0] + 3
    
    worksheet.write("A"+str(start_row), "Credit Card", bold)
    credit_card = pd.DataFrame(cib_report["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"]["Credit Card"])
    credit_card.to_excel(writer, sheet_name="CIB Analysis Report", startrow=start_row, index=False)
    start_row += credit_card.shape[0] + 3
    
    worksheet.write("A"+str(start_row), "Others", bold)
    others = pd.DataFrame(cib_report["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"]["Others"])
    others.to_excel(writer, sheet_name="CIB Analysis Report", startrow=start_row, index=False)
    start_row =+ others.shape[0] + 3
    
    
    
    
    
    worksheet.write('A1', 'CIB Report of', bold)
    worksheet.write('B1', cib_report['CIB Report of'])
    worksheet.write('A2', 'NID Number', bold)
    worksheet.write('B2', cib_report['NID Number'])
    worksheet.write('A3', "Father's Name", bold)
    worksheet.write('B3', cib_report["Fathers Name"])
    worksheet.write('A4', 'No of Living Contracts', bold)
    worksheet.write('B4', cib_report['No of Living Contracts'])
    worksheet.write('A5', 'Total Outstanding', bold)
    worksheet.write('B5', cib_report['Total Outstanding'])
    worksheet.write('A6', 'Total Overdue', bold)
    worksheet.write('B6', cib_report['Total Overdue'])
    worksheet.write('A7', 'Current Status', bold)
    worksheet.write('B7', cib_report['Current Status'])
    worksheet.write('A8', 'Overall Worst Status', bold)
    worksheet.write('B8', cib_report['Overall Worst Status'])
    
    
    
    worksheet.autofit()
    
    
    
    return workbook