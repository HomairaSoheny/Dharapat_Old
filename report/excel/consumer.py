import pandas as pd

def align_center(x):
    return ['text-align: left' for x in x]

def generateConsumerSpreadsheet(writer, cib_report):
    workbook = writer.book
    start_row = 13
    
    header_format = workbook.add_format(
    {
        "bold": True,
        "text_wrap": True,
        "valign": "top",
        "fg_color": "#D7E4BC",
        "border": 1,
        'font_size': 14
    })
    
    title_format = workbook.add_format({
        "text_wrap": True,
        "valign": "top",
        "align": "right",
        "border": 1,
    })
    bold = workbook.add_format({
        'bold': True,
        'font_size': 17
        })
    
    df = pd.DataFrame(cib_report["Credit Facilities as Applicant - Live (As Borrower)"]['Term Loan'])
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="CIB Summary Analysis", startrow=start_row, index=False, header=True)
    worksheet = writer.sheets["CIB Summary Analysis"]
    worksheet.write("A"+str(start_row), 'Term Loan', header_format)
    worksheet.write("A"+str(start_row-1), 'Credit Facilities as Applicant - Live (As Borrower)', bold)
    start_row += df.shape[0] + 6
    
    df = pd.DataFrame(cib_report["Credit Facilities as Applicant - Live (As Borrower)"]['Credit Card'])
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="CIB Summary Analysis", startrow=start_row, index=False)
    worksheet.write("A"+str(start_row), 'Credit Card', header_format)
    start_row += df.shape[0] + 6
    
    df = pd.DataFrame(cib_report["Credit Facilities as Applicant - Live (As Borrower)"]['Others'])
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="CIB Summary Analysis", startrow=start_row, index=False)
    worksheet.write("A"+str(start_row), 'Other', header_format)
    start_row += df.shape[0] + 6
    
    df = pd.DataFrame(cib_report["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"]['Term Loan'])
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="CIB Summary Analysis", startrow=start_row, index=False)
    worksheet.write("A"+str(start_row), 'Term Loan', header_format)
    worksheet.write("A"+str(start_row-1), 'Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)', bold)
    start_row += df.shape[0] + 6
    
    df = pd.DataFrame(cib_report["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"]['Credit Card'])
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="CIB Summary Analysis", startrow=start_row, index=False)
    worksheet.write("A"+str(start_row), 'Credit Card', header_format)
    start_row += df.shape[0] + 6
    
    df = pd.DataFrame(cib_report["Credit Facilities as Applicant - Terminated - Last 12 Months (As Borrower)"]['Others'])
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="CIB Summary Analysis", startrow=start_row, index=False)
    worksheet.write("A"+str(start_row), 'Other', header_format)
    start_row += df.shape[0] + 6
    
    df = pd.DataFrame(cib_report["Credit Facilities as Guarantor - Live (As Guarantor)"]['Term Loan'])
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="CIB Summary Analysis", startrow=start_row, index=False)
    worksheet.write("A"+str(start_row), 'Term Loan', header_format)
    worksheet.write("A"+str(start_row-1), 'Credit Facilities as Guarantor - Live (As Guarantor)', bold)
    start_row += df.shape[0] + 6
    
    df = pd.DataFrame(cib_report["Credit Facilities as Guarantor - Live (As Guarantor)"]['Credit Card'])
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="CIB Summary Analysis", startrow=start_row, index=False)
    worksheet.write("A"+str(start_row), 'Credit Card', header_format)
    start_row += df.shape[0] + 6
    
    df = pd.DataFrame(cib_report["Credit Facilities as Guarantor - Live (As Guarantor)"]['Others'])
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="CIB Summary Analysis", startrow=start_row, index=False)
    worksheet.write("A"+str(start_row), 'Other', header_format)
    start_row += df.shape[0] + 6
    
    df = pd.DataFrame(cib_report["Credit Facilities in the Name of Business - Live"]['Term Loan'])
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="CIB Summary Analysis", startrow=start_row, index=False)
    worksheet.write("A"+str(start_row), 'Term Loan', header_format)
    worksheet.write("A"+str(start_row-1), 'Credit Facilities in the Name of Business - Live', bold)
    start_row += df.shape[0] + 6
    
    df = pd.DataFrame(cib_report["Credit Facilities in the Name of Business - Live"]['Credit Card'])
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="CIB Summary Analysis", startrow=start_row, index=False)
    worksheet.write("A"+str(start_row), 'Credit Card', header_format)
    start_row += df.shape[0] + 6
    
    df = pd.DataFrame(cib_report["Credit Facilities in the Name of Business - Live"]['Others'])
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="CIB Summary Analysis", startrow=start_row, index=False)
    worksheet.write("A"+str(start_row), 'Other', header_format)

    worksheet.write('A1', 'CIB Report of', header_format)
    worksheet.write('B1', cib_report['CIB Report of'], title_format)
    worksheet.write('A2', 'NID Number', header_format)
    worksheet.write('B2', cib_report['NID Number'], title_format)
    worksheet.write('A3', "Father's Name", header_format)
    worksheet.write('B3', cib_report["Fathers Name"], title_format)
    worksheet.write('A4', 'No of Living Contracts', header_format)
    worksheet.write('B4', cib_report['No of Living Contracts'], title_format)
    worksheet.write('A5', 'Total Outstanding', header_format)
    worksheet.write('B5', cib_report['Total Outstanding'], title_format)
    worksheet.write('A6', 'Total Overdue', header_format)
    worksheet.write('B6', cib_report['Total Overdue'], title_format)
    worksheet.write('A7', 'Current Status', header_format)
    worksheet.write('B7', cib_report['Current Status'], title_format)
    worksheet.write('A8', 'Overall Worst Status', header_format)
    worksheet.write('B8', cib_report['Overall Worst Status'], title_format)

    worksheet.autofit()