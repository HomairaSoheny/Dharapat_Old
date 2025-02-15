from report.excel.general_helper import *
import pandas as pd

def generateSummaryTableWorksheet(writer, workbook, summary_table):

    title_format = getTitleFormat(workbook)
    header_bold_center = getHeaderBoldCenter(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)    
    normal_format = getNormalFormat(workbook)

    worksheet = writer.sheets["Summary Table - 1"]
    worksheet.merge_range("A1:J1", "Summary Table - 1", title_format)
    worksheet.merge_range("B2:J2", "BDT in Million", header_non_bold)
    worksheet.merge_range("B3:B4", "Name of Concern", header_format)
    worksheet.merge_range("C3:E3", "Funded Outstanding", header_bold_center)
    worksheet.write("C4", "Installment", header_format)
    worksheet.write("D4", "Non Installment", header_format)
    worksheet.write("E4", "Total", header_format)
    worksheet.merge_range("F3:F4", "Non-Funded Outstanding", header_format)
    worksheet.merge_range("G3:G4", "Total Outstanding", header_format)
    worksheet.merge_range("H3:H4", "Overdue", header_format)
    worksheet.merge_range("I3:I4", "CL Status", header_format)
    worksheet.merge_range("J3:J4", "Default", header_format)
    worksheet.merge_range("K1:K4", "CIB PDF View", header_format)
    worksheet.merge_range("L1:L4", "Updated Overdue and CL status", header_format)
    
    range_checker = (5, summary_table[0]["CIB Category"])
    
    for idx, row in enumerate(summary_table):
        format = header_format if row["Name of Concern"] in ("Sub Total", "Grand Total") else normal_format
        i = idx + 5
        if row['CIB Category'] != range_checker[1]:
            worksheet.merge_range("A"+str(range_checker[0])+":A"+str(i-1), summary_table[idx-1]['CIB Category'], header_format)
            range_checker = (i, row['CIB Category'])
        
        if row['Name of Concern'] == 'Grand Total':
            worksheet.merge_range("A"+str(range_checker[0])+":A"+str(i), summary_table[idx]['CIB Category'], header_format)
        
        worksheet.write("B" + str(i), row["Name of Concern"], format)
        worksheet.write("C" + str(i), row["Funded Outstanding Installment"], format)
        worksheet.write("D" + str(i), row["Funded Outstanding Non Installment"], format)
        worksheet.write("E" + str(i), row["Funded Outstanding Total"], format)
        worksheet.write("F" + str(i), row["Non-Funded Outstanding"], format)
        worksheet.write("G" + str(i), row["Total Outstanding"], format)
        worksheet.write("H" + str(i), row["Overdue"], format)
        worksheet.write("I" + str(i), row["CL Status"], format)
        worksheet.write("J" + str(i), row["Default"], format)
        worksheet.write_url("K" + str(i), row["CIB PDF View"].replace(" ", "\n"), format)
        worksheet.write("L" + str(i), row["Updated Overdue and CL Status"], format)
    worksheet.autofit()

def generateSummaryTableTwoWorksheet(writer, workbook, summary_table_two):
    title_format = getTitleFormat(workbook)
    header_bold_center = getHeaderBoldCenter(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)    
    normal_format = getNormalFormat(workbook)
    
    
    worksheet = writer.sheets["Summary Table - 2"]
    worksheet.merge_range("A1:Q1", "Summary Table - 2", title_format)
    worksheet.merge_range("B2:J2", "BDT in Million", header_non_bold)
    worksheet.merge_range("B3:B4", "Concern Name", header_format)
    worksheet.merge_range("C3:E3", "Funded", header_bold_center)
    worksheet.write("C4", "Installment", header_format)
    worksheet.write("D4", "Non Installment", header_format)
    worksheet.write("E4", "Total", header_format)
    worksheet.merge_range("F3:F4", "Non-Funded", header_format)
    worksheet.merge_range("G3:G4", "Total", header_format)
    worksheet.merge_range("H3:H4", "Overdue", header_format)
    worksheet.merge_range("I3:I4", "Worst CL Status", header_format)
    worksheet.merge_range("J3:J4", "Rescheduled Loan (Amount)", header_format)
    worksheet.merge_range("K3:Q3", "Loan Amount", header_format)
    worksheet.write("K4", "STD", header_format)
    worksheet.write("L4", "SMA", header_format)
    worksheet.write("M4", "SS", header_format)
    worksheet.write("N4", "DF", header_format)
    worksheet.write("O4", "BL", header_format)
    worksheet.write("P4", "BLW", header_format)
    worksheet.write("Q4", "Stay Order", header_format)
    worksheet.merge_range("R3:R4", "Remarks (CIB) related to classified liability", header_format)
    
    range_checker = (5, summary_table_two[0]["CIB Category"])
    
    for idx, row in enumerate(summary_table_two):
        format = header_format if row["Name of Concern"] in ("Sub Total", "Grand Total") else normal_format
        i = idx + 5
        if row['CIB Category'] != range_checker[1]:
            worksheet.merge_range("A"+str(range_checker[0])+":A"+str(i-1), summary_table_two[idx-1]['CIB Category'], header_format)
            range_checker = (i, row['CIB Category'])
        
        if row['Name of Concern'] == 'Grand Total':
            worksheet.merge_range("A"+str(range_checker[0])+":A"+str(i), summary_table_two[idx]['CIB Category'], header_format)
        
        worksheet.write("B" + str(i), row["Name of Concern"], format)
        worksheet.write("C" + str(i), row["Funded Installment"], format)
        worksheet.write("D" + str(i), row["Funded Non Installment"], format)
        worksheet.write("E" + str(i), row["Funded Total"], format)
        worksheet.write("F" + str(i), row["Non-Funded"], format)
        worksheet.write("G" + str(i), row["Total"], format)
        worksheet.write("H" + str(i), row["Overdue"], format)
        worksheet.write("I" + str(i), row["Worst CL Status"], format)
        worksheet.write("J" + str(i), row["Rescheduled Loan"], format)
        worksheet.write("K" + str(i), row["Loan STD"], format)
        worksheet.write("L" + str(i), row["Loan SMA"], format)
        worksheet.write("M" + str(i), row["Loan SS"], format)
        worksheet.write("N" + str(i), row["Loan DF"], format)
        worksheet.write("O" + str(i), row["Loan BL"], format)
        worksheet.write("P" + str(i), row["Loan BLW"], format)
        worksheet.write("Q" + str(i), row["Loan Stay Order"], format)
        worksheet.write("R" + str(i), row["Remarks"], format)
    worksheet.autofit()
        
    


def generateFundedTerminatedFacilityTableWorksheet(writer, workbook, funded_terminated_facility_summary_table):
    title_format = getTitleFormat(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)
    normal_bold_format = getNormalBoldFormat(workbook)

    
    worksheet = writer.sheets["terminated facility"]
    worksheet.merge_range("A1:E1", "Summary of terminated facility (Funded)", title_format)
    worksheet.merge_range("A2:D2", "Total number of funded terminated loan", header_format)
    worksheet.write("E2", "BDT in Million", header_non_bold)
    worksheet.write("A3", "Installment", header_format)
    worksheet.write("B3", "Limit", header_format)
    worksheet.write("C3", "Loan/Limit (days of adjustment before/after)", header_format)
    worksheet.write("D3", "Worse Classification status", header_format)
    worksheet.write("E3", "Date of classification", header_format)

    for idx, row in enumerate(funded_terminated_facility_summary_table['Funded']):
        i = idx+4
        worksheet.write("A" + str(i), row["Installment"], normal_format)
        worksheet.write("B" + str(i), row["Limit"], normal_format)
        worksheet.write("C" + str(i), row["Loan/Limit (days of adjustment before/after)"], normal_format)
        worksheet.write("D" + str(i), row["Worse Classification Status"], normal_format)
        worksheet.write("E" + str(i), row["Date of Classification"], normal_format)

    data = funded_terminated_facility_summary_table['Funded']
    worksheet.write(f'A{len(data)+4}','Sub Total',normal_bold_format)
    total_formula = f'SUM(B4:B{len(data)+3})'
    worksheet.write_formula(f'B{len(data)+4}', f'={total_formula}', normal_bold_format)
    worksheet.autofit()


def generateNonFundedTerminatedFacilityTableWorksheet(writer, workbook, terminated_facility_summary_table):
    title_format = getTitleFormat(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)
    normal_bold_format = getNormalBoldFormat(workbook)


    worksheet = writer.sheets["terminated facility"]
    worksheet.merge_range("G1:K1", "Summary of terminated facility (Non-Funded)", title_format)
    worksheet.merge_range("G2:J2", "Total number of non funded terminated loan", header_format)
    worksheet.write("K2", "BDT in Million", header_non_bold)
    worksheet.write("G3", "Non-Installment", header_format)
    worksheet.write("H3", "Limit", header_format)
    worksheet.write("I3", "Loan/Limit (days of adjustment before/after)", header_format)
    worksheet.write("J3", "Worse Classification status", header_format)
    worksheet.write("K3", "Date of classification", header_format)

    for idx, row in enumerate(terminated_facility_summary_table['Non Funded']):
        i = idx+4
        worksheet.write("G" + str(i), row["Non-Installment"], normal_format)
        worksheet.write("H" + str(i), row["Limit"], normal_format)
        worksheet.write("I" + str(i), row["Loan/Limit (days of adjustment before/after)"], normal_format)
        worksheet.write("J" + str(i), row["Worse Classification Status"], normal_format)
        worksheet.write("K" + str(i), row["Date of Classification"], normal_format)

    data = terminated_facility_summary_table['Non Funded']
    worksheet.write(f'G{len(data)+4}','Sub Total',normal_bold_format)
    total_formula = f'SUM(H4:H{len(data)+3})'
    worksheet.write_formula(f'H{len(data)+4}', f'={total_formula}', normal_bold_format)
    worksheet.autofit()


def generateSummaryFundedFacilitiesInstallmentWorksheet(writer,workbook,funded_facility_table):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    worksheet = writer.sheets["funded facility"]

    worksheet.merge_range("A1:O1", "Summary of funded facility", title_format)
    worksheet.merge_range("A2:O2", "Installments", header_format)

    worksheet.write("A3", "Name of Concern", header_format)
    worksheet.write("B3", "Summary of Funded Facility", header_format)
    worksheet.write("C3", "Limit", header_format)
    worksheet.write("D3", "Outstanding", header_format)
    worksheet.write("E3", "Overdue", header_format)
    worksheet.write("F3", "Start Date", header_format)
    worksheet.write("G3", "End Date of Contract", header_format)
    worksheet.write("H3", "Installment Amount", header_format)
    worksheet.write("I3", "Payment Period", header_format)
    worksheet.write("J3", "Total no. of Installment", header_format)
    worksheet.write("K3", "Total no. of Installment paid", header_format)
    worksheet.write("L3", "No. of Remaining Installment", header_format)
    worksheet.write("M3", "Date of last payment", header_format)
    worksheet.write("N3", "NPI (No.)", header_format)
    worksheet.write("O3", "Default (Yes/No)", header_format)

    row = 4
    for concern_type in funded_facility_table.keys():
        if concern_type !=None:
            facility_list = [item for item in funded_facility_table[concern_type] if item['Installment Type'] == 'Installment']
            if len(facility_list)>0:
                worksheet.merge_range(f"A{row}:A{row+len(facility_list)-1}",concern_type,header_format)
                for idx,item in enumerate(facility_list):
                    if item["Nature of Facility"] =='Sub Total':
                        format = header_format
                    else:
                        format = normal_format
                    worksheet.write("B" + str(idx+row), item["Nature of Facility"], format)
                    worksheet.write("C" + str(idx+row), item["Limit"], format)
                    worksheet.write("D" + str(idx+row), item["Outstanding"], format)
                    worksheet.write("E" + str(idx+row), item["Overdue"], format)
                    worksheet.write("F" + str(idx+row), item["Start Date"], format)
                    worksheet.write("G" + str(idx+row), item["End Date of Contract"], format)
                    worksheet.write("H" + str(idx+row), item["Installment Amount"], format)
                    worksheet.write("I" + str(idx+row), item["Payment Period"], format)
                    worksheet.write("J" + str(idx+row), item["Total No. of Installment"], format)
                    worksheet.write("K" + str(idx+row), item["Total No. of Installment"], format)
                    worksheet.write("L" + str(idx+row), item["No. of Remaining Installment"], format)
                    worksheet.write("M" + str(idx+row), item["Date of Last Payment"], format)
                    worksheet.write("N" + str(idx+row), item["NPI"], format)
                    worksheet.write("O" + str(idx+row), item["Default"], format)
                    
            
                row += len(facility_list)
    worksheet.autofit()
    return row

def generateSummaryFundedFacilitiesNonInstallmentWorksheet(writer,workbook,funded_facility_table, starting_row):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    worksheet = writer.sheets["funded facility"]

    starting_row+=1

    worksheet.merge_range(f"A{starting_row}:P{starting_row}", "Summary of funded facility", title_format)
    worksheet.merge_range(f"A{starting_row+1}:P{starting_row+1}", "Non Installments", title_format)
    

    worksheet.write(f"A{starting_row+2}", "Name of Concern", header_format)
    worksheet.write(f"B{starting_row+2}", "Summary of Funded Facility", header_format)
    worksheet.write(f"C{starting_row+2}", "Limit", header_format)
    worksheet.write(f"D{starting_row+2}", "Outstanding", header_format)
    worksheet.write(f"E{starting_row+2}", "Overdue", header_format)
    worksheet.write(f"F{starting_row+2}", "Start Date", header_format)
    worksheet.write(f"G{starting_row+2}", "End Date of Contract", header_format)
    worksheet.write(f"H{starting_row+2}", "Installment Amount", header_format)
    worksheet.write(f"I{starting_row+2}", "Payment Period (Monthly/ Quarterly/ Half yearly/ Annually)", header_format)
    worksheet.write(f"J{starting_row+2}", "Total no. of Installment", header_format)
    worksheet.write(f"K{starting_row+2}", "Total no. of Installment paid", header_format)
    worksheet.write(f"L{starting_row+2}", "No. of Remaining Installment", header_format)
    worksheet.write(f"M{starting_row+2}", "Date of last payment", header_format)
    worksheet.write(f"N{starting_row+2}", "NPI (No.)", header_format)
    worksheet.write(f"O{starting_row+2}", "Default (Yes/No)", header_format)

    row = starting_row + 3
    
    for concern_type in funded_facility_table.keys():
        if concern_type !=None:
            facility_list = [item for item in funded_facility_table[concern_type] if item['Installment Type'] == 'No Installment']
            if len(facility_list)>0:
                worksheet.merge_range(f"A{row}:A{row+len(facility_list)-1}",concern_type,header_format)
                for idx,item in enumerate(facility_list):
                    if item["Nature of Facility"] =='Sub Total':
                        format = header_format
                    else:
                        format = normal_format
                    worksheet.write("B" + str(idx+row), item["Nature of Facility"], format)
                    worksheet.write("C" + str(idx+row), item["Limit"], format)
                    worksheet.write("D" + str(idx+row), item["Outstanding"], format)
                    worksheet.write("E" + str(idx+row), item["Overdue"], format)
                    worksheet.write("F" + str(idx+row), item["Start Date"], format)
                    worksheet.write("G" + str(idx+row), item["End Date of Contract"], format)
                    worksheet.write("H" + str(idx+row), item["Installment Amount"], format)
                    worksheet.write("I" + str(idx+row), item["Payment Period"], format)
                    worksheet.write("J" + str(idx+row), item["Total No. of Installment"], format)
                    worksheet.write("K" + str(idx+row), item["Total No. of Installment"], format)
                    worksheet.write("L" + str(idx+row), item["No. of Remaining Installment"], format)
                    worksheet.write("M" + str(idx+row), item["Date of Last Payment"], format)
                    worksheet.write("N" + str(idx+row), item["NPI"], format)
                    worksheet.write("O" + str(idx+row), item["Default"], format)
            
                row += len(facility_list) 
    worksheet.autofit()
    

    

def generateSummaryNonFundedFacilitiesWorksheet(writer,workbook,non_funded_facility_table):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    worksheet = writer.sheets["non funded facility"]
    worksheet.merge_range("A1:P2", "Summary of non funded facility", title_format)

    worksheet.write("A3", "Name of Concern", header_format)
    worksheet.write("B3", "Facility Name", header_format)
    worksheet.write("C3", "Limit", header_format)
    worksheet.write("D3", "Outstanding", header_format)
    worksheet.write("E3", "Start Date", header_format)
    worksheet.write("F3", "End Date of Contract", header_format)
    worksheet.write("G3", "Default (Yes/No)", header_format)

    format = normal_format
    row = 4
    for concern_type in non_funded_facility_table.keys():
        if concern_type !=None and len(non_funded_facility_table[concern_type])>0:
            facility_list = [item for item in non_funded_facility_table[concern_type]]
            worksheet.merge_range(f"A{row}:A{row+len(facility_list)-1}",concern_type,header_format)

            for idx,item in enumerate(facility_list):
                worksheet.write("B" + str(idx+row), item["Nature of Facility"], format)
                worksheet.write("C" + str(idx+row), item["Limit"], format)
                worksheet.write("D" + str(idx+row), item["Outstanding"], format)
                worksheet.write("E" + str(idx+row), item["Start Date"], format)
                worksheet.write("F" + str(idx+row), item["End Date of Contract"], format)
                worksheet.write("G" + str(idx+row), item["Default"], format)
                
        
            row += len(facility_list) 
    worksheet.autofit()

    

def generateSummaryRescheduleLoanBorrowerWorksheet(writer, workbook, reschedule_loan_summary_table):
    title_format = getTitleFormat(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    
    worksheet = writer.sheets["Reschedule Loan"]
    worksheet.merge_range("A1:E1", "Summary of Reschedule Loan for Borrower", title_format)
    worksheet.write("F1", "BDT in Million", header_non_bold)
    worksheet.write("A2", "Name of Account", header_format)
    worksheet.write("B2", "Type of Reschedule", header_format)
    worksheet.write("C2", "Expiry of reschedule Loan", header_format)
    worksheet.write("D2", "Amount", header_format)
    worksheet.write("E2", "Date of last rescheduling", header_format)
    worksheet.write("F2", "Link", header_format)

    for idx, row in enumerate(reschedule_loan_summary_table['Borrower'][:-1]):
        i = idx+3
        worksheet.write("A" + str(i), row["Name of Account"], normal_format)
        worksheet.write("B" + str(i), row["Type of Reschedule"], normal_format)
        worksheet.write("C" + str(i), row["Expiry of Reschedule Loan"], normal_format)
        worksheet.write("D" + str(i), row["Amount"], normal_format)
        worksheet.write("E" + str(i), str(row["Date of Last Rescheduling"]), normal_format)
        worksheet.write_url("F" + str(i), row["Link"], normal_format)

    data = reschedule_loan_summary_table['Borrower']
    worksheet.write(f'A{len(data)+4}','Sub Total',header_format)
    total_formula = f'SUM(D3:D{len(data)+3})'
    worksheet.write_formula(f'D{len(data)+4}', f'={total_formula}', header_format)
    worksheet.autofit()
    return len(data)+5


def generateSummaryRescheduleLoanGuarantorWorksheet(writer, workbook, reschedule_loan_summary_table,starting_row):
    title_format = getTitleFormat(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    starting_row+=1
    worksheet = writer.sheets["Reschedule Loan"]
    worksheet.merge_range(f"A{starting_row}:E{starting_row}", "Summary of Reschedule Loan for Guarantor", title_format)
    worksheet.write(f'F{starting_row}', "BDT in Million", header_non_bold)
    worksheet.write(f'A{starting_row+1}', "Name of Account", header_format)
    worksheet.write(f'B{starting_row+1}', "Type of Reschedule", header_format)
    worksheet.write(f'C{starting_row+1}', "Expiry of reschedule Loan", header_format)
    worksheet.write(f'D{starting_row+1}', "Amount", header_format)
    worksheet.write(f'E{starting_row+1}', "Date of last rescheduling", header_format)
    worksheet.write(f'F{starting_row+1}', "Link", header_format)

    starting_row+=2
    for idx, row in enumerate(reschedule_loan_summary_table['Guarantor'][:-1]):
        i = idx+starting_row
        worksheet.write("A" + str(i), row["Name of Account"], normal_format)
        worksheet.write("B" + str(i), row["Type of Reschedule"], normal_format)
        worksheet.write("C" + str(i), row["Expiry of Reschedule Loan"], normal_format)
        worksheet.write("D" + str(i), row["Amount"], normal_format)
        worksheet.write("E" + str(i), str(row["Date of Last Rescheduling"]), normal_format)
        worksheet.write_url("F" + str(i), row["Link"].replace(" ", "\n"), normal_format)

    data = reschedule_loan_summary_table['Guarantor'][:-1]
    worksheet.write(f'A{len(data)+starting_row}','Sub Total',header_format)
    total_formula = f'SUM(D{starting_row}:D{len(data)+(starting_row-1)})'
    worksheet.write_formula(f'D{len(data)+starting_row}', f'={total_formula}', header_format)
    worksheet.autofit()


def generateSummaryRequestedLoanWorksheet(writer, workbook, requested_loan_summary_table):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    
    worksheet = writer.sheets["Requested Loan"]
    worksheet.merge_range(f"A1:F1", "Summary of Requested Loan", title_format)
    worksheet.write(f'A2', "Type of Loan", header_format)
    worksheet.write(f'B2', "Facility", header_format)
    worksheet.write(f'C2', "Role", header_format)
    worksheet.write(f'D2', "Requested Amount", header_format)
    worksheet.write(f'E2', "Date of Request", header_format)
    worksheet.write(f'F2', "Link", header_format)

    
    for idx, row in enumerate(requested_loan_summary_table):
        i = idx+3
        worksheet.write("A" + str(i), row["Type of Loan"], normal_format)
        worksheet.write("B" + str(i), row["Facility"], normal_format)
        worksheet.write("C" + str(i), row["Role"], normal_format)
        worksheet.write("D" + str(i), float(row["Requested Amount"]), normal_format)
        worksheet.write("E" + str(i), str(row["Date of Request"]), normal_format)
        worksheet.write_url("F" + str(i), row["Link"].replace(" ", "\n"), normal_format)

    data = requested_loan_summary_table
    worksheet.write(f'A{len(data)+3}','Sub Total',header_format)
    total_formula = f'SUM(D3:D{len(data)+2})'
    worksheet.write_formula(f'D{len(data)+3}', f'={total_formula}', header_format)
    worksheet.autofit()


def generateSummaryStayOrderBorrowerWorksheet(writer, workbook, stay_order_summary_table):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    
    worksheet = writer.sheets["Stay Order"]
    worksheet.merge_range(f"A1:F1", "Summary of Stay Order for Borrower", title_format)
    worksheet.write(f'A2', "Name of Account", header_format)
    worksheet.write(f'B2', "Nature of Facility", header_format)
    worksheet.write(f'C2', "StayOrder Amount", header_format)
    worksheet.write(f'D2', "Writ no.", header_format)
    worksheet.write(f'E2', "Remarks", header_format)
    worksheet.write(f'F2', "Link", header_format)

    
    for idx, row in enumerate(stay_order_summary_table['Borrower']):
        i = idx+3
        worksheet.write("A" + str(i), row["Name of account"], normal_format)
        worksheet.write("B" + str(i), row["Nature of facility"], normal_format)
        worksheet.write("C" + str(i), (row["Stayorder amount"]), normal_format)
        worksheet.write("D" + str(i), row["Writ no"], normal_format)
        worksheet.write("E" + str(i), row["Remarks"], normal_format)
        worksheet.write_url("F" + str(i), row["Link"].replace(" ", "\n"), normal_format)

    data = stay_order_summary_table['Borrower']
    worksheet.write(f'A{len(data)+3}','Sub Total',header_format)
    total_formula = f'SUM(C3:C{len(data)+2})'
    worksheet.write_formula(f'C{len(data)+3}', f'={total_formula}', header_format)
    worksheet.autofit()
    return len(data)+4


def generateSummaryStayOrderGuarantorWorksheet(writer, workbook, stay_order_summary_table,starting_row):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)


    starting_row +=1

    worksheet = writer.sheets["Stay Order"]
    worksheet.merge_range(f"A{starting_row}:F{starting_row}", "Summary of Stay Order for Guarantor", title_format)
    worksheet.write(f'A{starting_row+1}', "Name of Account", header_format)
    worksheet.write(f'B{starting_row+1}', "Nature of Facility", header_format)
    worksheet.write(f'C{starting_row+1}', "StayOrder Amount", header_format)
    worksheet.write(f'D{starting_row+1}', "Writ no.", header_format)
    worksheet.write(f'E{starting_row+1}', "Remarks", header_format)
    worksheet.write(f'F{starting_row+1}', "Link", header_format)

    starting_row+=2
    for idx, row in enumerate(stay_order_summary_table['Guarantor']):
        i = idx+starting_row
        worksheet.write("A" + str(i), row["Name of account"], normal_format)
        worksheet.write("B" + str(i), row["Nature of facility"], normal_format)
        worksheet.write("C" + str(i), (row["Stayorder amount"]), normal_format)
        worksheet.write("D" + str(i), row["Writ no"], normal_format)
        worksheet.write("E" + str(i), row["Remarks"], normal_format)
        worksheet.write_url("F" + str(i), row["Link"].replace(" ", "\n"), normal_format)

    data = stay_order_summary_table['Guarantor']
    worksheet.write(f'A{len(data)+starting_row}','Sub Total',header_format)
    total_formula = f'SUM(C{starting_row}:C{len(data)+(starting_row-1)})'
    worksheet.write_formula(f'C{len(data)+starting_row}', f'={total_formula}', header_format)
    worksheet.autofit()

def generateExpiredButShowingLiveWorksheet(writer, workbook, expired_but_showing_live):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)
    
    worksheet = writer.sheets["Expired But Showing Live"]
    
    worksheet.merge_range("A1:M1", "Expired Loan But Showing Live (Funded)", title_format)
    worksheet.merge_range("Q1:W1", "Expired Loan But Showing Live (Non Funded)", title_format)
    
    
    worksheet.write("A2", "Nature of Facility", header_format)
    worksheet.write("B2", "Limit", header_format)
    worksheet.write("C2", "Outstanding", header_format)
    worksheet.write("D2", "Overdue", header_format)
    worksheet.write("E2", "Start Date", header_format)
    worksheet.write("F2", "End Date of Contract", header_format)
    worksheet.write("G2", "Installment Amount", header_format)
    worksheet.write("H2", "Payment Period", header_format)
    worksheet.write("I2", "Total No of Installment", header_format)
    worksheet.write("J2", "No of Remaining Installment", header_format)
    worksheet.write("K2", "Date of Last Payment", header_format)
    worksheet.write("L2", "NPI", header_format)
    worksheet.write("M2", "Default", header_format)
    
    worksheet.write("Q2", "Nature of Facility", header_format)
    worksheet.write("R2", "Limit", header_format)
    worksheet.write("S2", "Outstanding", header_format)
    worksheet.write("T2", "Overdue", header_format)
    worksheet.write("U2", "Start Date", header_format)
    worksheet.write("V2", "End Date of Contract", header_format)
    worksheet.write("W2", "Default", header_format)
    
    for i, item in enumerate(expired_but_showing_live['Summary of Funded Facility']):
        worksheet.write("A" + str(i+3), item["Nature of Facility"], normal_format)
        worksheet.write("B" + str(i+3), item["Limit"], normal_format)
        worksheet.write("C" + str(i+3), item["Outstanding"], normal_format)
        worksheet.write("D" + str(i+3), item["Overdue"], normal_format)
        worksheet.write("E" + str(i+3), item["Start Date"], normal_format)
        worksheet.write("F" + str(i+3), item["End Date of Contract"], normal_format)
        worksheet.write("G" + str(i+3), item["Installment Amount"], normal_format)
        worksheet.write("H" + str(i+3), item["Payment Period"], normal_format)
        worksheet.write("I" + str(i+3), item["Total No of Installment"], normal_format)
        worksheet.write("J" + str(i+3), item["No of Remaining Installment"], normal_format)
        worksheet.write("K" + str(i+3), item["Date of Last Payment"], normal_format)
        worksheet.write("L" + str(i+3), item["NPI"], normal_format)
        worksheet.write("M" + str(i+3), item["Default"], normal_format)
    
    for i, item in enumerate(expired_but_showing_live['Summary of Non Funded Facility']):
        worksheet.write("Q" + str(i+3), item["Nature of Facility"], normal_format)
        worksheet.write("R" + str(i+3), item["Limit"], normal_format)
        worksheet.write("S" + str(i+3), item["Outstanding"], normal_format)
        worksheet.write("T" + str(i+3), item["Overdue"], normal_format)
        worksheet.write("U" + str(i+3), item["Start Date"], normal_format)
        worksheet.write("V" + str(i+3), item["End Date of Contract"], normal_format)
        worksheet.write("W" + str(i+3), item["Default"], normal_format)
    
    worksheet.autofit()
    


def generateSummaryTable3FundedWorksheet(writer,workbook,funded_summary_table_3):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    worksheet = writer.sheets["Summary Table 3 - Funded"]

    worksheet.merge_range("A1:P2", "Summary Table- 3: Liability type wise break up (only Live contracts) Funded", title_format)


    worksheet.write("A3", "Type of Concern", header_format)
    worksheet.write("B3", "Borrowing Company/ Person", header_format)
    worksheet.write("C3", "A. Overdraft/ Cash Credit", header_format)
    worksheet.write("D3", "Overdue/ EOL of A", header_format)
    worksheet.write("E3", "B. Time Loan", header_format)
    worksheet.write("F3", "Overdue/ EOL of B", header_format)
    worksheet.write("G3", "C. LTR", header_format)
    worksheet.write("H3", "Overdue/ EOL of C", header_format)
    worksheet.write("I3", "D. Other Non Installment", header_format)
    worksheet.write("J3", "Overdue/ EOL of D", header_format)
    worksheet.write("K3", "E. Term Loan", header_format)
    worksheet.write("L3", "EMI of E", header_format)
    worksheet.write("M3", "Overdue/ EOL of E", header_format)
    worksheet.write("N3", "F. Other Installment Loan", header_format)
    worksheet.write("O3", "EMI of F", header_format)
    worksheet.write("P3", "Overdue/ EOL of F", header_format)

    

    unique_cib_categories = {json_data.get('CIB Category', '') for json_data in funded_summary_table_3 if 'CIB Category' in json_data}

    row = 4
    for concern_type in unique_cib_categories:
        if concern_type !=None:
            concern_list = [item for item in funded_summary_table_3 if item['CIB Category'] == concern_type]

            worksheet.merge_range(f"A{row}:A{row+len(concern_list)-1}",concern_type,header_format)

            for idx,item in enumerate(concern_list):
                if item["Borrowing Company - Person"] == 'Sub Total':
                    format = header_format
                else:
                    format = normal_format
                worksheet.write("B" + str(idx+row), item["Borrowing Company - Person"], format)
                worksheet.write("C" + str(idx+row), item["A - Overdraft - Cash Credit"], format)
                worksheet.write("D" + str(idx+row), item["Overdue - EOL of A"], format)
                worksheet.write("E" + str(idx+row), item["B - Time Loan"], format)
                worksheet.write("F" + str(idx+row), item["Overdue - EOL of B"], format)
                worksheet.write("G" + str(idx+row), item["C - LTR"], format)
                worksheet.write("H" + str(idx+row), item["Overdue - EOL of C"], format)
                worksheet.write("I" + str(idx+row), item["D - Other Non Installment"], format)
                worksheet.write("J" + str(idx+row), item["Overdue - EOL of D"], format)
                worksheet.write("K" + str(idx+row), item["E - Term Loan"], format)
                worksheet.write("L" + str(idx+row), item["EMI of E"], format)
                worksheet.write("M" + str(idx+row), item["Overdue - EOL of E"], format)
                worksheet.write("N" + str(idx+row), item["F - Other Installment Loan"], format)
                worksheet.write("O" + str(idx+row), item["EMI of F"], format)
                worksheet.write("P" + str(idx+row), item["Overdue - EOL of F"], format)
        
            row += len(concern_list) 
    worksheet.autofit()
    

def generateSummaryTable3NonFundedWorksheet(writer, workbook, non_funded_summary_table_3):
    title_format = getTitleFormat(workbook)

    df = pd.DataFrame(non_funded_summary_table_3)
    df.style.apply(align_center, axis=0).to_excel(writer, sheet_name="Summary Table 3 - Non Funded", startrow=2, index=False)
    worksheet = writer.sheets["Summary Table 3 - Non Funded"]
    worksheet.merge_range("A1:F2", "Summary Table- 3: Liability type wise break up (only Live contracts) Non Funded", title_format)
    worksheet.autofit()


def generateCorporateSpreadsheet(writer, analysis_report):
    workbook = writer.book

    workbook.add_worksheet("Summary Table - 1")
    summary_table_1 = analysis_report["Summary Table - 1"]
    generateSummaryTableWorksheet(writer, workbook, summary_table_1)
    
    workbook.add_worksheet("terminated facility")
    funded_terminated_facility_summary_table = analysis_report["A - Summary of Terminated Facilities"]
    generateFundedTerminatedFacilityTableWorksheet(writer,workbook,funded_terminated_facility_summary_table)
    generateNonFundedTerminatedFacilityTableWorksheet(writer,workbook,funded_terminated_facility_summary_table)
    
    workbook.add_worksheet("funded facility")
    funded_facility_table = analysis_report['B - Summary of Facilities']['Summary of funded facility']
    row = generateSummaryFundedFacilitiesInstallmentWorksheet(writer,workbook,funded_facility_table)
    generateSummaryFundedFacilitiesNonInstallmentWorksheet(writer,workbook,funded_facility_table,row+1)

    workbook.add_worksheet("non funded facility")
    funded_facility_table = analysis_report['B - Summary of Facilities']['Summary of non funded facility']
    generateSummaryNonFundedFacilitiesWorksheet(writer,workbook,funded_facility_table)

    workbook.add_worksheet("Reschedule Loan")
    reschedule_loan_summary_table = analysis_report['C - Summary of Reschedule Loan']
    row = generateSummaryRescheduleLoanBorrowerWorksheet(writer,workbook,reschedule_loan_summary_table)
    generateSummaryRescheduleLoanGuarantorWorksheet(writer,workbook,reschedule_loan_summary_table,row)

    workbook.add_worksheet("Requested Loan")
    requested_loan_summary_table = analysis_report['D - Summary of Requested Loan']
    generateSummaryRequestedLoanWorksheet(writer,workbook,requested_loan_summary_table)

    workbook.add_worksheet("Stay Order")
    stay_order_summary_table = analysis_report['E - Summary of Stay Order']
    row = generateSummaryStayOrderBorrowerWorksheet(writer, workbook, stay_order_summary_table)
    generateSummaryStayOrderGuarantorWorksheet(writer, workbook, stay_order_summary_table,row)
    
    workbook.add_worksheet("Expired But Showing Live")
    expired_but_showing_live = analysis_report['F - Expired Loan But Showing Live']
    generateExpiredButShowingLiveWorksheet(writer, workbook, expired_but_showing_live)

    workbook.add_worksheet("Summary Table - 2")
    summary_table_2 = analysis_report["Summary Table - 2"]
    generateSummaryTableTwoWorksheet(writer, workbook, summary_table_2)
    
    workbook.add_worksheet("Summary Table 3 - Funded")
    funded_summary_table_3 = analysis_report['Summary Table - 3']['funded']
    generateSummaryTable3FundedWorksheet(writer,workbook,funded_summary_table_3)
    
    non_funded_summary_table_3 = analysis_report['Summary Table - 3']['non_funded']
    generateSummaryTable3NonFundedWorksheet(writer, workbook, non_funded_summary_table_3)
