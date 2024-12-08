from report.excel.general_helper import *
from utils.general_helper import *
import pandas as pd

def generateSummaryTableWorksheet(writer, workbook, summary_table,concern , start_row=1):

    title_format = getTitleFormat(workbook)
    header_bold_center = getHeaderBoldCenter(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)    
    normal_format = getNormalFormat(workbook)
    warning_format = getWarningFormat(workbook)
    warning_header_format = getHeaderWarningFormat(workbook)

    worksheet = writer.sheets["Summary Table - 1"]
    if concern:
        worksheet.merge_range(f"A{start_row}:P{start_row}", "Summary Table - 1 for Proprietorship Concern", title_format)
    else:
        worksheet.merge_range(f"A{start_row}:P{start_row}", "Summary Table - 1", title_format)
    worksheet.merge_range(f"B{start_row+1}:P{start_row+1}", "BDT", header_non_bold)
    worksheet.merge_range(f"B{start_row+2}:B{start_row+3}", "Name of Concern", header_format)
    worksheet.merge_range(f"C{start_row+2}:C{start_row+3}", "Position Date", header_format)
    worksheet.merge_range(f"D{start_row+2}:I{start_row+2}", "Funded Outstanding", header_bold_center)
    worksheet.write(f"D{start_row+3}", "Installment (In Million)", header_format)
    worksheet.write(f"E{start_row+3}", "Installment (Raw)", header_format)
    worksheet.write(f"F{start_row+3}", "Non Installment (In Million)", header_format)
    worksheet.write(f"G{start_row+3}", "Non Installment (Raw)", header_format)
    worksheet.write(f"H{start_row+3}", "Total (In Million)", header_format)
    worksheet.write(f"I{start_row+3}", "Total (Raw)", header_format)
    worksheet.merge_range(f"J{start_row+2}:J{start_row+3}", "Non-Funded Outstanding (In Million)", header_format)
    worksheet.merge_range(f"K{start_row+2}:K{start_row+3}", "Non-Funded Outstanding (Raw)", header_format)
    worksheet.merge_range(f"L{start_row+2}:L{start_row+3}", "Total Outstanding (In Million)", header_format)
    worksheet.merge_range(f"M{start_row+2}:M{start_row+3}", "Total Outstanding (Raw)", header_format)
    worksheet.merge_range(f"N{start_row+2}:N{start_row+3}", "Overdue (In Million)", header_format)
    worksheet.merge_range(f"O{start_row+2}:O{start_row+3}", "Overdue (Raw)", header_format)
    worksheet.merge_range(f"P{start_row+2}:P{start_row+3}", "CL Status (Borrower)", header_format)
    worksheet.merge_range(f"Q{start_row+2}:Q{start_row+3}", "Default", header_format)
    if not concern:
        worksheet.merge_range(f"R{start_row+2}:R{start_row+3}", "Worst CL as Guarantor", header_format)
        worksheet.merge_range(f"S{start_row+2}:S{start_row+3}", "Stay Order Remarks", header_format)
        worksheet.merge_range(f"T{start_row}:T{start_row+3}", "CIB PDF View", header_format)
        worksheet.merge_range(f"U{start_row}:U{start_row+3}", "Updated Overdue and CL status", header_format)
    else:
        worksheet.merge_range(f"R{start_row}:R{start_row+3}", "CIB PDF View", header_format)
        
    if len(summary_table) <1:
        return 5
    range_checker = (start_row+5, summary_table[0]["CIB Category"])
    if not concern:
        column_name = "Name of Concern"
    else:
        column_name = "Concerns Trade Name"
    for idx, row in enumerate(summary_table):
        
        format = header_format if 'Total' in row[column_name] else normal_format
        i = idx + start_row +5 
        if row['CIB Category'] != range_checker[1]:
            worksheet.merge_range("A"+str(range_checker[0])+":A"+str(i-1), summary_table[idx-1]['CIB Category'], header_format)
            range_checker = (i, row['CIB Category'])
        
        if row[column_name] == 'Grand Total':
            worksheet.merge_range("A"+str(range_checker[0])+":A"+str(i+1), summary_table[idx]['CIB Category'], header_format)

        worksheet.write("B" + str(i), row[column_name], format)
        worksheet.write("C" + str(i), row["Position Date"], format)
        
        alert_format = header_format if (row[column_name] in ("Sub Total", "Grand Total")) else (warning_format if row["Funded Outstanding Installment Alert"] == 'True' else normal_format)
        worksheet.write("D" + str(i), row["Funded Outstanding Installment"], alert_format)
        alert_format = header_format if (row[column_name] in ("Sub Total", "Grand Total")) else (warning_format if row["Funded Outstanding Installment Alert"] == 'True' else normal_format)
        worksheet.write("E" + str(i), convertToRaw(row["Funded Outstanding Installment"]), alert_format)
        
        alert_format = header_format if (row[column_name] in ("Sub Total", "Grand Total")) else (warning_format if row["Funded Outstanding Non Installment Alert"] == 'True' else normal_format)
        worksheet.write("F" + str(i), row["Funded Outstanding Non Installment"], alert_format)
        alert_format = header_format if (row[column_name] in ("Sub Total", "Grand Total")) else (warning_format if row["Funded Outstanding Non Installment Alert"] == 'True' else normal_format)
        worksheet.write("G" + str(i), convertToRaw(row["Funded Outstanding Non Installment"]), alert_format)
        
        alert_format = header_format if (row[column_name] in ("Sub Total", "Grand Total")) else (warning_format if row["Funded Outstanding Total Alert"] == 'True' else normal_format)
        worksheet.write("H" + str(i), row["Funded Outstanding Total"], alert_format)
        alert_format = header_format if (row[column_name] in ("Sub Total", "Grand Total")) else (warning_format if row["Funded Outstanding Total Alert"] == 'True' else normal_format)
        worksheet.write("I" + str(i), convertToRaw(row["Funded Outstanding Total"]), alert_format)
        
        alert_format = header_format if (row[column_name] in ("Sub Total", "Grand Total")) else (warning_format if row["Non-Funded Outstanding Alert"] == 'True' else normal_format)
        worksheet.write("J" + str(i), row["Non-Funded Outstanding"], alert_format)
        alert_format = header_format if (row[column_name] in ("Sub Total", "Grand Total")) else (warning_format if row["Non-Funded Outstanding Alert"] == 'True' else normal_format)
        worksheet.write("K" + str(i), convertToRaw(row["Non-Funded Outstanding"]), alert_format)

        worksheet.write("L" + str(i), row["Total Outstanding"], format)
        worksheet.write("M" + str(i), convertToRaw(row["Total Outstanding"]), format)

        worksheet.write("N" + str(i), row["Overdue"], format)
        worksheet.write("O" + str(i), convertToRaw(row["Overdue"]), format)

        worksheet.write("P" + str(i), row["CL Status"], format)
        worksheet.write("Q" + str(i), row["Default"], format)
        if not concern:
            worksheet.write("R" + str(i), row["Worst CL Status as Guarantor"], format)
            worksheet.write("S" + str(i), row["Stay Order Remarks"], format)
            worksheet.write_url("T" + str(i), row["CIB PDF View"].replace(" ", "\n"), format)
            worksheet.write("U" + str(i), row["Updated Overdue and CL Status"], format)
        else:
            worksheet.write_url("R" + str(i), row["CIB PDF View"].replace(" ", "\n"), format)
            
    worksheet.autofit()
    return i+1

def generateSummaryTableTwoWorksheet(writer, workbook, summary_table_two,concern, start_row=1):
    title_format = getTitleFormat(workbook)
    header_bold_center = getHeaderBoldCenter(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)    
    normal_format = getNormalFormat(workbook)
    
    
    worksheet = writer.sheets["Summary Table - 2"]
    if concern:
        worksheet.merge_range(f"A{start_row}:Q{start_row}", "Summary Table - 2 for Proprietorship Concern", title_format)
    else:
        worksheet.merge_range(f"A{start_row}:Q{start_row}", "Summary Table - 2", title_format)
    worksheet.merge_range(f"B{start_row+1}:J{start_row+1}", "BDT", header_non_bold)
    worksheet.merge_range(f"B{start_row+2}:B{start_row+3}", "Concern Name", header_format)
    worksheet.merge_range(f"C{start_row+2}:H{start_row+2}", "Funded", header_bold_center)
    worksheet.write(f"C{start_row+3}", "Installment (In Million)", header_format)
    worksheet.write(f"D{start_row+3}", "Installment (Raw)", header_format)
    worksheet.write(f"E{start_row+3}", "Non Installment (In Million)", header_format)
    worksheet.write(f"F{start_row+3}", "Non Installment (Raw)", header_format)
    worksheet.write(f"G{start_row+3}", "Total (In Million)", header_format)
    worksheet.write(f"H{start_row+3}", "Total (Raw)", header_format)
    worksheet.merge_range(f"I{start_row+2}:I{start_row+3}", "Non-Funded (In Million)", header_format)
    worksheet.merge_range(f"J{start_row+2}:J{start_row+3}", "Non-Funded (Raw)", header_format)
    worksheet.merge_range(f"K{start_row+2}:K{start_row+3}", "Total (In Million)", header_format)
    worksheet.merge_range(f"L{start_row+2}:L{start_row+3}", "Total (Raw)", header_format)
    worksheet.merge_range(f"M{start_row+2}:M{start_row+3}", "Overdue (In Million)", header_format)
    worksheet.merge_range(f"N{start_row+2}:N{start_row+3}", "Overdue (Raw)", header_format)
    worksheet.merge_range(f"O{start_row+2}:O{start_row+3}", "Worst CL Status", header_format)
    worksheet.merge_range(f"P{start_row+2}:P{start_row+3}", "Rescheduled Loan (Amount In Million)", header_format)
    worksheet.merge_range(f"Q{start_row+2}:W{start_row+2}", "Loan Amount (In Million)", header_format)
    worksheet.write(f"Q{start_row+3}", "STD", header_format)
    worksheet.write(f"R{start_row+3}", "SMA", header_format)
    worksheet.write(f"S{start_row+3}", "SS", header_format)
    worksheet.write(f"T{start_row+3}", "DF", header_format)
    worksheet.write(f"U{start_row+3}", "BL", header_format)
    worksheet.write(f"V{start_row+3}", "BLW", header_format)
    worksheet.write(f"W{start_row+3}", "Stay Order", header_format)
    worksheet.merge_range(f"X{start_row+2}:X{start_row+3}", "Remarks (CIB) related to classified liability", header_format)
    if len(summary_table_two) <1:
        return 5
    range_checker = (start_row+4, summary_table_two[0]["CIB Category"])
    
    for idx, row in enumerate(summary_table_two):
        format = header_format if row["Name of Concern"] in ("Sub Total", "Grand Total") else normal_format
        i = idx + 4+start_row
        if row['CIB Category'] != range_checker[1]:
            worksheet.merge_range("A"+str(range_checker[0])+":A"+str(i-1), summary_table_two[idx-1]['CIB Category'], header_format)
            range_checker = (i, row['CIB Category'])
        
        if row['Name of Concern'] == 'Grand Total':
            worksheet.merge_range("A"+str(range_checker[0])+":A"+str(i+1), summary_table_two[idx]['CIB Category'], header_format)
        
        worksheet.write("B" + str(i), row["Name of Concern"], format)
        worksheet.write("C" + str(i), row["Funded Installment"], format)
        worksheet.write("D" + str(i), convertToRaw(row["Funded Installment"]), format)
        worksheet.write("E" + str(i), row["Funded Non Installment"], format)
        worksheet.write("F" + str(i), convertToRaw(row["Funded Non Installment"]), format)
        worksheet.write("G" + str(i), row["Funded Total"], format)
        worksheet.write("H" + str(i), convertToRaw(row["Funded Total"]), format)
        worksheet.write("I" + str(i), row["Non-Funded"], format)
        worksheet.write("J" + str(i), convertToRaw(row["Non-Funded"]), format)
        worksheet.write("K" + str(i), row["Total"], format)
        worksheet.write("L" + str(i), convertToRaw(row["Total"]), format)
        worksheet.write("M" + str(i), row["Overdue"], format)
        worksheet.write("N" + str(i), convertToRaw(row["Overdue"]), format)
        worksheet.write("O" + str(i), row["Worst CL Status"], format)
        worksheet.write("P" + str(i), row["Rescheduled Loan"], format)
        worksheet.write("Q" + str(i), row["Loan STD"], format)
        worksheet.write("R" + str(i), row["Loan SMA"], format)
        worksheet.write("S" + str(i), row["Loan SS"], format)
        worksheet.write("T" + str(i), row["Loan DF"], format)
        worksheet.write("U" + str(i), row["Loan BL"], format)
        worksheet.write("V" + str(i), row["Loan BLW"], format)
        worksheet.write("W" + str(i), row["Loan Stay Order"], format)
        worksheet.write("X" + str(i), row["Remarks"], format)
    worksheet.autofit()
    return len(summary_table_two)+5

        
    


def generateFundedTerminatedFacilityTableWorksheet(writer, workbook, funded_terminated_facility_summary_table,concern, start_row = 1):
    title_format = getTitleFormat(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)
    normal_bold_format = getNormalBoldFormat(workbook)
    
    
    worksheet = writer.sheets["Terminated facility"]
    worksheet.set_column('A:F', 30)
    if concern:
        worksheet.merge_range(f"A{start_row}:G{start_row}", "Summary of terminated facility (Funded) for Proprietorship Concern", title_format)

    else:
        worksheet.merge_range(f"A{start_row}:H{start_row}", "Summary of terminated facility (Funded)", title_format)
    worksheet.merge_range(f"A{start_row+1}:G{start_row+1}", "Total number of funded terminated loan", header_format)
    worksheet.write(f"H{start_row+1}", "BDT", header_non_bold)
    worksheet.write(f"A{start_row+2}", "Category", header_format)
    worksheet.write(f"B{start_row+2}", "Name of the Concern", header_format)
    worksheet.write(f"C{start_row+2}", "Installment", header_format)
    worksheet.write(f"D{start_row+2}", "Limit (In Million)", header_format)
    worksheet.write(f"E{start_row+2}", "Limit (Raw)", header_format)
    worksheet.write(f"F{start_row+2}", "Loan/Limit (days of adjustment before/after)", header_format)
    worksheet.write(f"G{start_row+2}", "Worse Classification status", header_format)
    worksheet.write(f"H{start_row+2}", "Date of classification", header_format)
    
    i=0
    for idx, row in enumerate(funded_terminated_facility_summary_table['Funded']):
        i = idx+3+start_row
        
        worksheet.write("A" + str(i), row["Category"], normal_format)
        if concern:
            format = header_format if 'Total' in row["Concerns Trade Name"] else normal_format
            worksheet.write("B" + str(i), row["Concerns Trade Name"], format)
        else:
            format = header_format if 'Total' in row['Name of the Concern'] else normal_format
            worksheet.write("B" + str(i), row["Name of the Concern"], format)
        worksheet.write("A" + str(i), row["Category"], format)
        worksheet.write("C" + str(i), row["Installment"], format)
        worksheet.write("D" + str(i), row["Limit"], format)
        worksheet.write("E" + str(i), convertToRaw(row["Limit"]), format)
        worksheet.write("F" + str(i), row["Loan/Limit (days of adjustment before/after)"], format)
        worksheet.write("G" + str(i), row["Worse Classification Status"], format)
        worksheet.write("H" + str(i), row["Date of Classification"], format)

    data = funded_terminated_facility_summary_table['Funded']

    return i+start_row+2


def generateNonFundedTerminatedFacilityTableWorksheet(writer, workbook, terminated_facility_summary_table,concern,start_row=1):
    title_format = getTitleFormat(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)
    normal_bold_format = getNormalBoldFormat(workbook)


    worksheet = writer.sheets["Terminated facility"]
    if concern:
        worksheet.merge_range(f"J{start_row}:P{start_row}", "Summary of terminated facility (Non-Funded) for Proprietorship Concern", title_format)

    else:
        worksheet.merge_range(f"J{start_row}:Q{start_row}", "Summary of terminated facility (Non-Funded)", title_format)
    worksheet.merge_range(f"J{start_row+1}:P{start_row+1}", "Total number of non funded terminated loan", header_format)
    worksheet.write(f"Q{start_row+1}", "BDT in Million", header_non_bold)
    worksheet.write(f"J{start_row+2}", "Category", header_format)
    worksheet.write(f"K{start_row+2}", "Name of the Concern", header_format)
    worksheet.write(f"L{start_row+2}", "Non-Installment", header_format)
    worksheet.write(f"M{start_row+2}", "Limit (In Million)", header_format)
    worksheet.write(f"N{start_row+2}", "Limit (Raw)", header_format)
    worksheet.write(f"O{start_row+2}", "Loan/Limit (days of adjustment before/(after))", header_format)
    worksheet.write(f"P{start_row+2}", "Worse Classification status", header_format)
    worksheet.write(f"Q{start_row+2}", "Date of classification", header_format)
    i=0
    for idx, row in enumerate(terminated_facility_summary_table['Non Funded']):
        i = idx+3+start_row
        format = header_format if 'Total' in row['Non-Installment'] else normal_format
        worksheet.write("J" + str(i), row["Category"], format)
        if concern:
            worksheet.write("K" + str(i), row["Concerns Trade Name"], format)
        else:
            worksheet.write("K" + str(i), row["Name of the Concern"], format)
        worksheet.write("L" + str(i), row["Non-Installment"], format)
        worksheet.write("M" + str(i), row["Limit"], format)
        worksheet.write("N" + str(i), convertToRaw(row["Limit"]), format)
        worksheet.write("O" + str(i), row["Loan/Limit (days of adjustment before/after)"], format)
        worksheet.write("P" + str(i), row["Worse Classification Status"], format)
        worksheet.write("Q" + str(i), row["Date of Classification"], format)

    
    worksheet.autofit()
    return i+start_row+1


def generateSummaryFundedFacilitiesInstallmentWorksheet(writer,workbook,funded_facility_table,concern, start_row = 1):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    worksheet = writer.sheets["Funded Facility"]
    if concern:
        worksheet.merge_range(f"A{start_row}:S{start_row}", "Summary of funded facility for propreitorship concern", title_format)
    else:
        worksheet.merge_range(f"A{start_row}:S{start_row}", "Summary of funded facility", title_format)
    worksheet.merge_range(f"A{start_row+1}:S{start_row+1}", "Installments", header_format)

    worksheet.write(f"A{start_row+2}", "Category", header_format)
    worksheet.write(f"B{start_row+2}", "Name of Concern", header_format)
    worksheet.write(f"C{start_row+2}", "Nature of Facility", header_format)
    worksheet.write(f"D{start_row+2}", "Limit (In Million)", header_format)
    worksheet.write(f"E{start_row+2}", "Limit (Raw)", header_format)
    worksheet.write(f"F{start_row+2}", "Outstanding (In Million)", header_format)
    worksheet.write(f"G{start_row+2}", "Outstanding (Raw)", header_format)
    worksheet.write(f"H{start_row+2}", "Overdue (In Million)", header_format)
    worksheet.write(f"I{start_row+2}", "Overdue (Raw)", header_format)
    worksheet.write(f"J{start_row+2}", "Start Date", header_format)
    worksheet.write(f"K{start_row+2}", "End Date of Contract", header_format)
    worksheet.write(f"L{start_row+2}", "Installment Amount (In Million)", header_format)
    worksheet.write(f"M{start_row+2}", "Installment Amount (Raw)", header_format)
    worksheet.write(f"N{start_row+2}", "Payment Period", header_format)
    worksheet.write(f"O{start_row+2}", "Total no. of Installment", header_format)
    worksheet.write(f"P{start_row+2}", "Total no. of Installment paid", header_format)
    worksheet.write(f"Q{start_row+2}", "No. of Remaining Installment", header_format)
    worksheet.write(f"R{start_row+2}", "Date of last payment", header_format)
    worksheet.write(f"S{start_row+2}", "NPI (No.)", header_format)
    worksheet.write(f"T{start_row+2}", "Default (Yes/No)", header_format)

    row = start_row + 3
    if len(funded_facility_table)<1:
        return row+1
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
                    if concern:
                        worksheet.write("B" + str(idx+row), item["Concerns Trade Name"], format)
                    else:
                        worksheet.write("B" + str(idx+row), item["Name of the Concern"], format)
                    worksheet.write("C" + str(idx+row), item["Nature of Facility"], format)
                    worksheet.write("D" + str(idx+row), item["Limit"], format)
                    worksheet.write("E" + str(idx+row), convertToRaw(item["Limit"]), format)
                    worksheet.write("F" + str(idx+row), item["Outstanding"], format)
                    worksheet.write("G" + str(idx+row), convertToRaw(item["Outstanding"]), format)
                    worksheet.write("H" + str(idx+row), item["Overdue"], format)
                    worksheet.write("I" + str(idx+row), convertToRaw(item["Overdue"]), format)
                    worksheet.write("J" + str(idx+row), item["Start Date"], format)
                    worksheet.write("K" + str(idx+row), item["End Date of Contract"], format)
                    worksheet.write("L" + str(idx+row), item["Installment Amount"], format)
                    worksheet.write("M" + str(idx+row), convertToRaw(item["Installment Amount"]), format)
                    worksheet.write("N" + str(idx+row), item["Payment Period"], format)
                    worksheet.write("O" + str(idx+row), item["Total No. of Installment"], format)
                    worksheet.write("P" + str(idx+row), item["Total No. of Installment"], format)
                    worksheet.write("Q" + str(idx+row), item["No. of Remaining Installment"], format)
                    worksheet.write("R" + str(idx+row), item["Date of Last Payment"], format)
                    worksheet.write("S" + str(idx+row), item["NPI"], format)
                    worksheet.write("T" + str(idx+row), item["Default"], format)
                    
            
                row += len(facility_list)
    worksheet.autofit()
    return row+1

def generateSummaryFundedFacilitiesNonInstallmentWorksheet(writer,workbook,funded_facility_table,concern, starting_row):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    worksheet = writer.sheets["Funded Facility"]

    starting_row+=1

    if concern:
        worksheet.merge_range(f"A{starting_row}:S{starting_row}", "Summary of funded facility for propreitorship concern", title_format)
    else:
        worksheet.merge_range(f"A{starting_row}:S{starting_row}", "Summary of funded facility", title_format)
    worksheet.merge_range(f"A{starting_row+1}:S{starting_row+1}", "Non Installments", title_format)
    

    worksheet.write(f"A{starting_row+2}", "Name of Concern", header_format)
    worksheet.write(f"B{starting_row+2}", "Nature of Facility", header_format)
    worksheet.write(f"C{starting_row+2}", "Limit (In Million)", header_format)
    worksheet.write(f"D{starting_row+2}", "Limit (Raw)", header_format)
    worksheet.write(f"E{starting_row+2}", "Outstanding (In Million)", header_format)
    worksheet.write(f"F{starting_row+2}", "Outstanding (Raw)", header_format)
    worksheet.write(f"G{starting_row+2}", "Overdue (In Million)", header_format)
    worksheet.write(f"H{starting_row+2}", "Overdue (Raw)", header_format)
    worksheet.write(f"I{starting_row+2}", "Start Date", header_format)
    worksheet.write(f"J{starting_row+2}", "End Date of Contract", header_format)
    worksheet.write(f"K{starting_row+2}", "Installment Amount (In Million)", header_format)
    worksheet.write(f"L{starting_row+2}", "Installment Amount (Raw)", header_format)
    worksheet.write(f"M{starting_row+2}", "Payment Period (Monthly/ Quarterly/ Half yearly/ Annually)", header_format)
    worksheet.write(f"N{starting_row+2}", "Total no. of Installment", header_format)
    worksheet.write(f"O{starting_row+2}", "Total no. of Installment paid", header_format)
    worksheet.write(f"P{starting_row+2}", "No. of Remaining Installment", header_format)
    worksheet.write(f"Q{starting_row+2}", "Date of last payment", header_format)
    worksheet.write(f"R{starting_row+2}", "NPI (No.)", header_format)
    worksheet.write(f"S{starting_row+2}", "Default (Yes/No)", header_format)

    row = starting_row + 3
    if len(funded_facility_table)<1:
        return row+1
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
                    worksheet.write("D" + str(idx+row), convertToRaw(item["Limit"]), format)
                    worksheet.write("E" + str(idx+row), item["Outstanding"], format)
                    worksheet.write("F" + str(idx+row), convertToRaw(item["Outstanding"]), format)
                    worksheet.write("G" + str(idx+row), item["Overdue"], format)
                    worksheet.write("H" + str(idx+row), convertToRaw(item["Overdue"]), format)
                    worksheet.write("I" + str(idx+row), item["Start Date"], format)
                    worksheet.write("J" + str(idx+row), item["End Date of Contract"], format)
                    worksheet.write("K" + str(idx+row), item["Installment Amount"], format)
                    worksheet.write("L" + str(idx+row), convertToRaw(item["Installment Amount"]), format)
                    worksheet.write("M" + str(idx+row), item["Payment Period"], format)
                    worksheet.write("N" + str(idx+row), item["Total No. of Installment"], format)
                    worksheet.write("O" + str(idx+row), item["Total No. of Installment"], format)
                    worksheet.write("P" + str(idx+row), item["No. of Remaining Installment"], format)
                    worksheet.write("Q" + str(idx+row), item["Date of Last Payment"], format)
                    worksheet.write("R" + str(idx+row), item["NPI"], format)
                    worksheet.write("S" + str(idx+row), item["Default"], format)
            
                row += len(facility_list) 
    worksheet.autofit()
    return row+1
    

    

def generateSummaryNonFundedFacilitiesWorksheet(writer,workbook,non_funded_facility_table,concern, start_row=1):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    worksheet = writer.sheets["Non Funded Facility"]
    if concern:
            worksheet.merge_range(f"A{start_row}:I{start_row+1}", "Summary of non funded facility for proprietorship concern", title_format)
    else:
        worksheet.merge_range(f"A{start_row}:I{start_row+1}", "Summary of non funded facility", title_format)

    worksheet.write(f"A{start_row+2}", "Category", header_format)
    worksheet.write(f"B{start_row+2}", "Facility Name", header_format)
    worksheet.write(f"C{start_row+2}", "Limit (In Million)", header_format)
    worksheet.write(f"D{start_row+2}", "Limit (Raw)", header_format)
    worksheet.write(f"E{start_row+2}", "Outstanding (In Million)", header_format)
    worksheet.write(f"F{start_row+2}", "Outstanding (Raw)", header_format)
    worksheet.write(f"G{start_row+2}", "Start Date", header_format)
    worksheet.write(f"H{start_row+2}", "End Date of Contract", header_format)
    worksheet.write(f"I{start_row+2}", "Default (Yes/No)", header_format)

    format = normal_format
    row = start_row+3
    if len(non_funded_facility_table)<1:
        return row+1
    for concern_type in non_funded_facility_table.keys():
        if concern_type !=None and len(non_funded_facility_table[concern_type])>0:
            facility_list = [item for item in non_funded_facility_table[concern_type]]
            if len(facility_list)<2:
                worksheet.write(f"A{row}",concern_type,header_format)
            else:
                worksheet.merge_range(f"A{row}:A{row+len(facility_list)-1}",concern_type,header_format)

            for idx,item in enumerate(facility_list):
                format = header_format if 'Total' in item["Nature of Facility"] else normal_format
                worksheet.write("B" + str(idx+row), item["Nature of Facility"], format)
                worksheet.write("C" + str(idx+row), item["Limit"], format)
                worksheet.write("D" + str(idx+row), convertToRaw(item["Limit"]), format)
                worksheet.write("E" + str(idx+row), item["Outstanding"], format)
                worksheet.write("F" + str(idx+row), convertToRaw(item["Outstanding"]), format)
                worksheet.write("G" + str(idx+row), item["Start Date"], format)
                worksheet.write("H" + str(idx+row), item["End Date of Contract"], format)
                worksheet.write("I" + str(idx+row), item["Default"], format)
                
        
            row += len(facility_list) 
    worksheet.autofit()
    return row+1

    

def generateSummaryRescheduleLoanBorrowerWorksheet(writer, workbook, reschedule_loan_summary_table,concern, start_row = 1):
    title_format = getTitleFormat(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    
    worksheet = writer.sheets["Reschedule Loan"]
    if concern:
        worksheet.merge_range(f"A{start_row}:J{start_row}", "Summary of Reschedule Loan for Borrower (Propreitorship Concerns)", title_format)
    else:
        worksheet.merge_range(f"A{start_row}:J{start_row}", "Summary of Reschedule Loan for Borrower", title_format)

    worksheet.write(f"K{start_row}", "BDT", header_non_bold)
    worksheet.write(f"A{start_row+1}", "Category", header_format)
    worksheet.write(f"B{start_row+1}", "Name of Account", header_format)
    worksheet.write(f"C{start_row+1}", "Nature of Facility", header_format)
    worksheet.write(f"D{start_row+1}", "Type of Reschedule", header_format)
    worksheet.write(f"E{start_row+1}", "Expiry of reschedule Loan", header_format)
    worksheet.write(f"F{start_row+1}", "Amount (In Million)", header_format)
    worksheet.write(f"G{start_row+1}", "Amount (Raw)", header_format)
    worksheet.write(f"H{start_row+1}", "Outstanding (In Million)", header_format)
    worksheet.write(f"I{start_row+1}", "Outstanding (Raw)", header_format)
    worksheet.write(f"J{start_row+1}", "Date of last rescheduling", header_format)
    worksheet.write(f"K{start_row+1}", "Link", header_format)

    for idx, row in enumerate(reschedule_loan_summary_table['Borrower']):
        i = idx+2+start_row
        format = header_format if 'Total' in row['Nature of Facility'] else normal_format
        worksheet.write("A" + str(i), row["Category"], format)
        worksheet.write("B" + str(i), row["Name of Account"], format)
        worksheet.write("C" + str(i), row["Nature of Facility"], format)
        worksheet.write("D" + str(i), row["Type of Reschedule"], format)
        worksheet.write("E" + str(i), row["Expiry of Reschedule Loan"], format)
        worksheet.write("F" + str(i), row["Amount"], format)
        worksheet.write("G" + str(i), convertToRaw(row["Amount"]), format)
        worksheet.write("H" + str(i), row["Outstanding"], format)
        worksheet.write("I" + str(i), convertToRaw(row["Outstanding"]), format)
        worksheet.write("J" + str(i), str(row["Date of Last Rescheduling"]), format)
        worksheet.write_url("K" + str(i), row["Link"], format)

    data = reschedule_loan_summary_table['Borrower']
    # worksheet.write(f'A{len(data)+4}','Sub Total',header_format)
    # total_formula = f'SUM(D3:D{len(data)+3})'
    # worksheet.write_formula(f'D{len(data)+4}', f'={total_formula}', header_format)
    worksheet.autofit()
    return len(data)+5


def generateSummaryRescheduleLoanGuarantorWorksheet(writer, workbook, reschedule_loan_summary_table,concern,starting_row):
    title_format = getTitleFormat(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    starting_row+=1
    worksheet = writer.sheets["Reschedule Loan"]
    if concern:
        worksheet.merge_range(f"A{starting_row}:J{starting_row}", "Summary of Reschedule Loan for Guarantor (Propreitorship Concern)", title_format)
    else:
        worksheet.merge_range(f"A{starting_row}:J{starting_row}", "Summary of Reschedule Loan for Guarantor", title_format)
    worksheet.write(f'K{starting_row}', "BDT in Million", header_non_bold)
    worksheet.write(f'A{starting_row+1}', "Category", header_format)
    worksheet.write(f'B{starting_row+1}', "Name of Account", header_format)
    worksheet.write(f'C{starting_row+1}', "Nature of Facility", header_format)
    worksheet.write(f'D{starting_row+1}', "Type of Reschedule", header_format)
    worksheet.write(f'E{starting_row+1}', "Expiry of reschedule Loan", header_format)
    worksheet.write(f'F{starting_row+1}', "Amount (In Million)", header_format)
    worksheet.write(f'G{starting_row+1}', "Amount (Raw)", header_format)
    worksheet.write(f'H{starting_row+1}', "Outstanding (In Million)", header_format)
    worksheet.write(f'I{starting_row+1}', "Outstanding (Raw)", header_format)
    worksheet.write(f'J{starting_row+1}', "Date of last rescheduling", header_format)
    worksheet.write(f'K{starting_row+1}', "Link", header_format)

    starting_row+=2
    for idx, row in enumerate(reschedule_loan_summary_table['Guarantor']):
        i = idx+starting_row
        format = header_format if 'Total' in row["Nature of Facility"] else normal_format
        worksheet.write("A" + str(i), row["Category"], format)
        worksheet.write("B" + str(i), row["Name of Account"], format)
        worksheet.write("C" + str(i), row["Nature of Facility"], format)
        worksheet.write("D" + str(i), row["Type of Reschedule"], format)
        worksheet.write("E" + str(i), row["Expiry of Reschedule Loan"], format)
        worksheet.write("F" + str(i), row["Amount"], format)
        worksheet.write("G" + str(i), convertToRaw(row["Amount"]), format)
        worksheet.write("H" + str(i), row["Outstanding"], format)
        worksheet.write("I" + str(i), convertToRaw(row["Outstanding"]), format)
        worksheet.write("J" + str(i), str(row["Date of Last Rescheduling"]), format)
        worksheet.write_url("K" + str(i), row["Link"].replace(" ", "\n"), format)

    data = reschedule_loan_summary_table['Guarantor']
    
    worksheet.autofit()
    return len(data)+6


def generateSummaryRequestedLoanWorksheet(writer, workbook, requested_loan_summary_table,concern,start_row=1):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    
    worksheet = writer.sheets["Requested Loan"]
    if concern:
        worksheet.merge_range(f"A{start_row}:H{start_row}", "Summary of Requested Loan for proprietorship concern", title_format)
    else:
        worksheet.merge_range(f"A{start_row}:H{start_row}", "Summary of Requested Loan", title_format)
    worksheet.write(f'A{start_row+1}', "Category", header_format)
    worksheet.write(f'B{start_row+1}', "Type of Loan", header_format)
    worksheet.write(f'C{start_row+1}', "Facility", header_format)
    worksheet.write(f'D{start_row+1}', "Role", header_format)
    worksheet.write(f'E{start_row+1}', "Requested Amount (In Million)", header_format)
    worksheet.write(f'F{start_row+1}', "Requested Amount (Raw)", header_format)
    worksheet.write(f'G{start_row+1}', "Date of Request", header_format)
    worksheet.write(f'H{start_row+1}', "Link", header_format)

    
    for idx, row in enumerate(requested_loan_summary_table):
        i = idx+2+start_row
        format = header_format if 'Total' in row["Facility"] else normal_format
        worksheet.write("A" + str(i), row["Category"], format)
        worksheet.write("B" + str(i), row["Type of Loan"], format)
        worksheet.write("C" + str(i), row["Facility"], format)
        worksheet.write("D" + str(i), row["Role"], format)
        worksheet.write("E" + str(i), row["Requested Amount"], format)
        worksheet.write("F" + str(i), convertToRaw(row["Requested Amount"]), format)
        worksheet.write("G" + str(i), str(row["Date of Request"]), format)
        worksheet.write_url("H" + str(i), row["Link"].replace(" ", "\n"), format)

    data = requested_loan_summary_table
    
    worksheet.autofit()
    return len(data)+5


def generateSummaryStayOrderBorrowerWorksheet(writer, workbook, stay_order_summary_table):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    
    worksheet = writer.sheets["Stay Order"]
    worksheet.merge_range(f"A1:G1", "Summary of Stay Order for Borrower", title_format)
    worksheet.write(f'A2', "Name of Account", header_format)
    worksheet.write(f'B2', "Nature of Facility", header_format)
    worksheet.write(f'C2', "StayOrder Amount (In Million)", header_format)
    worksheet.write(f'D2', "StayOrder Amount (Raw)", header_format)
    worksheet.write(f'E2', "Writ no.", header_format)
    worksheet.write(f'F2', "Remarks", header_format)
    worksheet.write(f'G2', "Link", header_format)

    
    for idx, row in enumerate(stay_order_summary_table['Borrower']):
        i = idx+3
        format = header_format if 'Total' in row["Nature of facility"] else normal_format
        worksheet.write("A" + str(i), row["Name of account"], format)
        worksheet.write("B" + str(i), row["Nature of facility"], format)
        worksheet.write("C" + str(i), (row["Stayorder amount"]), format)
        worksheet.write("D" + str(i), convertToRaw(row["Stayorder amount"]), format)
        worksheet.write("E" + str(i), row["Writ no"], format)
        worksheet.write("F" + str(i), row["Remarks"], format)
        worksheet.write_url("G" + str(i), row["Link"].replace(" ", "\n"), format)

    data = stay_order_summary_table['Borrower']
    # worksheet.write(f'A{len(data)+3}','Sub Total',header_format)
    # total_formula = f'SUM(C3:C{len(data)+2})'
    # worksheet.write_formula(f'C{len(data)+3}', f'={total_formula}', header_format)
    worksheet.autofit()
    return len(data)+4


def generateSummaryStayOrderGuarantorWorksheet(writer, workbook, stay_order_summary_table,starting_row):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)


    starting_row +=1

    worksheet = writer.sheets["Stay Order"]
    worksheet.merge_range(f"A{starting_row}:G{starting_row}", "Summary of Stay Order for Guarantor", title_format)
    worksheet.write(f'A{starting_row+1}', "Name of Account", header_format)
    worksheet.write(f'B{starting_row+1}', "Nature of Facility", header_format)
    worksheet.write(f'C{starting_row+1}', "StayOrder Amount (In Million)", header_format)
    worksheet.write(f'D{starting_row+1}', "StayOrder Amount (Raw)", header_format)
    worksheet.write(f'E{starting_row+1}', "Writ no.", header_format)
    worksheet.write(f'F{starting_row+1}', "Remarks", header_format)
    worksheet.write(f'G{starting_row+1}', "Link", header_format)

    starting_row+=2
    for idx, row in enumerate(stay_order_summary_table['Guarantor']):
        i = idx+starting_row        
        format = header_format if 'Total' in row["Nature of facility"] else normal_format
        worksheet.write("A" + str(i), row["Name of account"], format)
        worksheet.write("B" + str(i), row["Nature of facility"], format)
        worksheet.write("C" + str(i), (row["Stayorder amount"]), format)
        worksheet.write("D" + str(i), convertToRaw(row["Stayorder amount"]), format)
        worksheet.write("E" + str(i), row["Writ no"], format)
        worksheet.write("F" + str(i), row["Remarks"], format)
        worksheet.write_url("G" + str(i), row["Link"].replace(" ", "\n"), format)

    data = stay_order_summary_table['Guarantor']
    # worksheet.write(f'A{len(data)+starting_row}','Sub Total',header_format)
    # total_formula = f'SUM(C{starting_row}:C{len(data)+(starting_row-1)})'
    # worksheet.write_formula(f'C{len(data)+starting_row}', f'={total_formula}', header_format)
    worksheet.autofit()

def generateExpiredButShowingLiveWorksheet(writer, workbook, expired_but_showing_live,concern,start_row=1):
    title_format = getTitleFormat(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)
    
    worksheet = writer.sheets["Expired But Showing Live"]
    
    if concern:
        worksheet.merge_range(f"A{start_row}:R{start_row}", "Expired Loan But Showing Live (Funded) for proprietorship concern", title_format)
        worksheet.merge_range(f"T{start_row}:AC{start_row}", "Expired Loan But Showing Live (Non Funded) for proprietorship concern", title_format)
    else:
        worksheet.merge_range(f"A{start_row}:R{start_row}", "Expired Loan But Showing Live (Funded)", title_format)
        worksheet.merge_range(f"T{start_row}:AC{start_row}", "Expired Loan But Showing Live (Non Funded)", title_format)
    
    
    worksheet.write(f"A{start_row+1}", "Nature of Facility", header_format)
    worksheet.write(f"B{start_row+1}", "Limit (In Million)", header_format)
    worksheet.write(f"C{start_row+1}", "Limit (Raw)", header_format)
    worksheet.write(f"D{start_row+1}", "Outstanding (In Million)", header_format)
    worksheet.write(f"E{start_row+1}", "Outstanding (Raw)", header_format)
    worksheet.write(f"F{start_row+1}", "Overdue (In Million)", header_format)
    worksheet.write(f"G{start_row+1}", "Overdue (Raw)", header_format)
    worksheet.write(f"H{start_row+1}", "Start Date", header_format)
    worksheet.write(f"I{start_row+1}", "End Date of Contract", header_format)
    worksheet.write(f"J{start_row+1}", "Installment Amount (In Million)", header_format)
    worksheet.write(f"K{start_row+1}", "Installment Amount (Raw)" , header_format)
    worksheet.write(f"L{start_row+1}", "Payment Period", header_format)
    worksheet.write(f"M{start_row+1}", "Total No of Installment", header_format)
    worksheet.write(f"N{start_row+1}", "Total No of Installment paid", header_format)
    worksheet.write(f"O{start_row+1}", "No of Remaining Installment", header_format)
    worksheet.write(f"P{start_row+1}", "Date of Last Payment", header_format)
    worksheet.write(f"Q{start_row+1}", "NPI", header_format)
    worksheet.write(f"R{start_row+1}", "Default", header_format)
    
    worksheet.write(f"T{start_row+1}", "Nature of Facility", header_format)
    worksheet.write(f"U{start_row+1}", "Limit (In Million)", header_format)
    worksheet.write(f"V{start_row+1}", "Limit (Raw)", header_format)
    worksheet.write(f"W{start_row+1}", "Outstanding (In Million)", header_format)
    worksheet.write(f"X{start_row+1}", "Outstanding (Raw)", header_format)
    worksheet.write(f"Y{start_row+1}", "Overdue (In Million)", header_format)
    worksheet.write(f"Z{start_row+1}", "Overdue (Raw)", header_format)
    worksheet.write(f"AA{start_row+1}", "Start Date", header_format)
    worksheet.write(f"AB{start_row+1}", "End Date of Contract", header_format)
    worksheet.write(f"AC{start_row+1}", "Default", header_format)
    
    for idx, item in enumerate(expired_but_showing_live['Summary of Funded Facility']):
        i = start_row+2+idx
        format = header_format if 'Total' in item["Nature of Facility"] else normal_format
        worksheet.write("A" + str(i), item["Nature of Facility"], format)
        worksheet.write("B" + str(i), item["Limit"], format)
        worksheet.write("C" + str(i), convertToRaw(item["Limit"]), format)
        worksheet.write("D" + str(i), item["Outstanding"], format)
        worksheet.write("E" + str(i), convertToRaw(item["Outstanding"]), format)
        worksheet.write("F" + str(i), item["Overdue"], format)
        worksheet.write("G" + str(i), convertToRaw(item["Overdue"]), format)
        worksheet.write("H" + str(i), item["Start Date"], format)
        worksheet.write("I" + str(i), item["End Date of Contract"], format)
        worksheet.write("J" + str(i), item["Installment Amount"], format)
        worksheet.write("K" + str(i), convertToRaw(item["Installment Amount"]), format)
        worksheet.write("L" + str(i), item["Payment Period"], format)
        worksheet.write("M" + str(i), item["Total No of Installment"], format)
        worksheet.write("N" + str(i), item['Total No of Installment paid'], format)
        worksheet.write("O" + str(i), item["No of Remaining Installment"], format)
        worksheet.write("P" + str(i), item["Date of Last Payment"], format)
        worksheet.write("Q" + str(i), item["NPI"], format)
        worksheet.write("R" + str(i), item["Default"], format)
    
    for idx, item in enumerate(expired_but_showing_live['Summary of Non Funded Facility']):
        i = start_row+2+idx
        format = header_format if 'Total' in item["Nature of Facility"] else normal_format
        worksheet.write("T" + str(i), item["Nature of Facility"], format)
        worksheet.write("U" + str(i), item["Limit"], format)
        worksheet.write("V" + str(i), convertToRaw(item["Limit"]), format)
        worksheet.write("W" + str(i), item["Outstanding"], format)
        worksheet.write("X" + str(i), convertToRaw(item["Outstanding"]), format)
        worksheet.write("Y" + str(i), item["Overdue"], format)
        worksheet.write("Z" + str(i), convertToRaw(item["Overdue"]), format)
        worksheet.write("AA" + str(i), item["Start Date"], format)
        worksheet.write("AB" + str(i), item["End Date of Contract"], format)
        worksheet.write("AC" + str(i), item["Default"], format)
    
    worksheet.autofit()
    return max(len(expired_but_showing_live['Summary of Non Funded Facility']),len(expired_but_showing_live['Summary of Funded Facility']))
    


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
            if row!=(row+len(concern_list)-1):
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
    # df = pd.DataFrame()
    # df.to_excel(writer, sheet_name="Summary Table - 1", index=False)

    sheet_names = ["Summary Table - 1", "Terminated facility", "Funded Facility", "Non Funded Facility", "Reschedule Loan",
                   "Requested Loan","Stay Order","Expired But Showing Live",
                   "Summary Table - 2","Summary Table 3 - Funded","Summary Table 3 - Non Funded"]

    for sheet_name in sheet_names:
        if len(sheet_name) >= 31:
            sheet_name = sheet_name[0:30]
        dummy_df = pd.DataFrame()
        dummy_df.to_excel(writer, sheet_name=sheet_name, index=False)

    # workbook.add_worksheet("Summary Table - 1")
    workbook = writer.book
    summary_table_1 = analysis_report["Summary Table - 1"]
    row = generateSummaryTableWorksheet(writer, workbook, summary_table_1,False)
    
    summary_table_1_concern = analysis_report['Summary Table - 1 for Proprietorship Concern']
    if len(summary_table_1_concern)>0:
        generateSummaryTableWorksheet(writer,workbook,summary_table_1_concern,True,row+2)
    
    # workbook.add_worksheet("Terminated facility")
    ter_obj = {
        "A - Summary of Terminated Facilities" : {
            "Funded" : analysis_report['A - Summary of Terminated Facilities : Funded'],
            "Non Funded": analysis_report['A - Summary of Terminated Facilities : Non-Funded']
        },
        "A1 - Summary of Terminated Facilities for Concerns" : {
            "Funded": analysis_report['A1 - Summary of Terminated Facilities for Concerns : Funded'],
            "Non Funded": analysis_report['A1 - Summary of Terminated Facilities for Concerns : Non-Funded']
        }
    }
    funded_terminated_facility_summary_table = ter_obj["A - Summary of Terminated Facilities"]
    last_row = generateFundedTerminatedFacilityTableWorksheet(writer,workbook,funded_terminated_facility_summary_table,concern = False)
    funded_terminated_facility_summary_table_concern = ter_obj['A1 - Summary of Terminated Facilities for Concerns']
    generateFundedTerminatedFacilityTableWorksheet(writer,workbook,funded_terminated_facility_summary_table_concern,True,last_row+2)

    last_row = generateNonFundedTerminatedFacilityTableWorksheet(writer,workbook,funded_terminated_facility_summary_table,False)
    funded_terminated_facility_summary_table_concern = ter_obj['A1 - Summary of Terminated Facilities for Concerns']
    generateNonFundedTerminatedFacilityTableWorksheet(writer,workbook,funded_terminated_facility_summary_table_concern,True,last_row+2)

    # workbook.add_worksheet("funded facility")
    funded = {}
    non_funded = {}
    funded_concern = {}
    non_funded_concern = {}

    for each in analysis_report['B - Summary of Facilities : Funded']:
        key = each['CIB Type']
        funded.setdefault(key, []).append(each)
    for each in analysis_report['B - Summary of Facilities : Non Funded']:
        key = each['CIB Type']
        non_funded.setdefault(key, []).append(each)
    for each in analysis_report['B1 - Summary of Facilities for Concerns : Funded']:
        key = each['CIB Type']
        funded_concern.setdefault(key, []).append(each)
    for each in analysis_report['B1 - Summary of Facilities for Concerns : Non Funded']:
        key = each['CIB Type']
        non_funded_concern.setdefault(key, []).append(each)


    fac_obj = {
        "B - Summary of Facilities" : {
            "Summary of funded facility" : funded,
            "Summary of non funded facility": non_funded
        },
        "B1 - Summary of Facilities for Concerns" : {
            "Summary of funded facility": funded_concern,
            "Summary of non funded facility": non_funded_concern
        }
    }
    funded_facility_table = fac_obj['B - Summary of Facilities']['Summary of funded facility']
    last_row = generateSummaryFundedFacilitiesInstallmentWorksheet(writer,workbook,funded_facility_table,False)
    funded_facility_table_concern = fac_obj['B1 - Summary of Facilities for Concerns']['Summary of funded facility']
    row = generateSummaryFundedFacilitiesInstallmentWorksheet(writer,workbook,funded_facility_table_concern,True,last_row+2)
    last_row = generateSummaryFundedFacilitiesNonInstallmentWorksheet(writer,workbook,funded_facility_table,False,row+2)
    generateSummaryFundedFacilitiesNonInstallmentWorksheet(writer,workbook,funded_facility_table_concern,True,last_row+2)
    #
    # workbook.add_worksheet("non funded facility")
    nonfunded_facility_table = fac_obj['B - Summary of Facilities']['Summary of non funded facility']
    last_row = generateSummaryNonFundedFacilitiesWorksheet(writer,workbook,nonfunded_facility_table,False)
    nonfunded_facility_table_concern = fac_obj['B1 - Summary of Facilities for Concerns']['Summary of non funded facility']
    generateSummaryNonFundedFacilitiesWorksheet(writer,workbook,nonfunded_facility_table_concern,True,last_row+2)


    reschedule_obj = {
        "C - Summary of Reschedule Loan" : {
            "Borrower" : analysis_report['C - Summary of Reschedule Loan : Borrower'],
            "Guarantor": analysis_report['C - Summary of Reschedule Loan : Guarantor']
        },
        "C1 - Summary of Reschedule Loan for Concerns" : {
            "Borrower": analysis_report['C1 - Summary of Reschedule Loan for Concerns : Borrower'],
            "Guarantor": analysis_report['C1 - Summary of Reschedule Loan for Concerns : Guarantor']
        }
    }
    # workbook.add_worksheet("Reschedule Loan")
    reschedule_loan_summary_table = reschedule_obj['C - Summary of Reschedule Loan']
    last_row = generateSummaryRescheduleLoanBorrowerWorksheet(writer,workbook,reschedule_loan_summary_table,False)
    reschedule_loan_summary_table_concern = reschedule_obj['C1 - Summary of Reschedule Loan for Concerns']
    row = generateSummaryRescheduleLoanBorrowerWorksheet(writer,workbook,reschedule_loan_summary_table_concern,True,last_row+4)
    #
    last_row = generateSummaryRescheduleLoanGuarantorWorksheet(writer,workbook,reschedule_loan_summary_table,False,row+4)
    generateSummaryRescheduleLoanGuarantorWorksheet(writer,workbook,reschedule_loan_summary_table_concern,True,last_row+4)
    #
    # workbook.add_worksheet("Requested Loan")
    requested_loan_summary_table = analysis_report['D - Summary of Requested Loan']
    last_row = generateSummaryRequestedLoanWorksheet(writer,workbook,requested_loan_summary_table,False)
    requested_loan_summary_table_concern = analysis_report['D1 - Summary of Requested Loan for Concern']
    generateSummaryRequestedLoanWorksheet(writer,workbook,requested_loan_summary_table_concern,True,last_row+2)
    # #
    # # workbook.add_worksheet("Stay Order")
    # stay_obj = {
    #     "E - Summary of Stay Order" : {
    #         "Borrower" : analysis_report['E - Summary of Stay Order : Borrower'],
    #         "Guarantor": analysis_report['E - Summary of Stay Order : Guarantor']
    #     },
    #     "E1 - Summary of Stay Order for Concern" : {
    #         "Borrower": analysis_report['E1 - Summary of Stay Order for Concern : Borrower'],
    #         "Guarantor": analysis_report['E1 - Summary of Stay Order for Concern : Guarantor']
    #     }
    # }
    # stay_order_summary_table = stay_obj['E - Summary of Stay Order']
    # row = generateSummaryStayOrderBorrowerWorksheet(writer, workbook, stay_order_summary_table)
    # generateSummaryStayOrderGuarantorWorksheet(writer, workbook, stay_order_summary_table,row)
    #
    # workbook.add_worksheet("Expired But Showing Live")

    live_obj = {
        "F - Expired Loan But Showing Live" : {
            "Summary of Funded Facility" : analysis_report['F - Expired Loan But Showing Live : Funded'],
            "Summary of Non Funded Facility": analysis_report['F - Expired Loan But Showing Live : Non Funded']
        },
        "F1 - Expired Loan But Showing Live for Concern" : {
            "Summary of Funded Facility": analysis_report['F1 - Expired Loan But Showing Live for Concern : Funded'],
            "Summary of Non Funded Facility": analysis_report['F1 - Expired Loan But Showing Live for Concern : Non Funded']
        }
    }
    expired_but_showing_live = live_obj['F - Expired Loan But Showing Live']
    last_row = generateExpiredButShowingLiveWorksheet(writer, workbook, expired_but_showing_live,False)
    expired_but_showing_live_concern = live_obj['F1 - Expired Loan But Showing Live for Concern']
    generateExpiredButShowingLiveWorksheet(writer, workbook, expired_but_showing_live_concern,True,last_row+2)
    #
    #
    # workbook.add_worksheet("Summary Table - 2")
    summary_table_2 = analysis_report["Summary Table - 2"]
    last_row = generateSummaryTableTwoWorksheet(writer, workbook, summary_table_2,False)
    summary_table_2_concern = analysis_report['Summary Table - 2 for Concern']
    if len(summary_table_2_concern)>0:

        generateSummaryTableTwoWorksheet(writer, workbook, summary_table_2_concern,True,last_row+4)
    #
    # workbook.add_worksheet("Summary Table 3 - Funded")
    # summary_3_obj = {
    #     "Summary Table - 3" : {
    #         "funded" : analysis_report['F - Expired Loan But Showing Live : Funded'],
    #         "non_funded": analysis_report['F - Expired Loan But Showing Live : Non Funded']
    #     }
        # "F1 - Expired Loan But Showing Live for Concern" : {
        #     "Summary of Funded Facility": analysis_report['F1 - Expired Loan But Showing Live for Concern : Funded'],
        #     "Summary of Non Funded Facility": analysis_report['F1 - Expired Loan But Showing Live for Concern : Non Funded']
        # }
    # }
    if analysis_report['Funded']:
        funded_summary_table_3 = analysis_report['Funded']
        generateSummaryTable3FundedWorksheet(writer,workbook,funded_summary_table_3)
    if analysis_report['Non Funded']:
        non_funded_summary_table_3 = analysis_report['Non Funded']
        generateSummaryTable3NonFundedWorksheet(writer, workbook, non_funded_summary_table_3)
