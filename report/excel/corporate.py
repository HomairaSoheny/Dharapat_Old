from report.excel.general_helper import *

def generateSummaryTableWorksheet(writer, workbook, summary_table):

    title_format = getTitleFormat(workbook)
    header_bold_center = getHeaderBoldCenter(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)    
    normal_format = getNormalFormat(workbook)

    worksheet = writer.sheets["Summary Table - 1"]
    worksheet.merge_range("A1:J1", "Summary Table - 1", title_format)
    worksheet.write("A2", "Position as on", header_format)
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
            worksheet.merge_range("A"+str(range_checker[0])+":A"+str(i-1), summary_table[idx-1]['CIB Category'], header_format)
        
        worksheet.write("B" + str(i), row["Name of Concern"], format)
        worksheet.write("C" + str(i), row["Funded Outstanding Installment"], format)
        worksheet.write("D" + str(i), row["Funded Outstanding Non Installment"], format)
        worksheet.write("E" + str(i), row["Funded Outstanding Total"], format)
        worksheet.write("F" + str(i), row["Non-Funded Outstanding"], format)
        worksheet.write("G" + str(i), row["Total Outstanding"], format)
        worksheet.write("H" + str(i), row["Overdue"], format)
        worksheet.write("I" + str(i), row["CL Status"], format)
        worksheet.write("J" + str(i), row["Default"], format)
        worksheet.write("K" + str(i), "N/A", format)
        worksheet.write("L" + str(i), row["Updated Overdue and CL Status"], format)

def generateSummaryTableTwoWorksheet(writer, workbook, summary_table_two):
    title_format = getTitleFormat(workbook)
    header_bold_center = getHeaderBoldCenter(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)    
    normal_format = getNormalFormat(workbook)
    
    
    worksheet = writer.sheets["Summary Table - 2"]
    worksheet.merge_range("A1:Q1", "Summary Table - 2", title_format)
    worksheet.write("A2", "Position as on", header_format)
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
            worksheet.merge_range("A"+str(range_checker[0])+":A"+str(i-1), summary_table_two[idx-1]['CIB Category'], header_format)
        
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
        
    


def generateFundedTerminatedFacilityTableWorksheet(writer, workbook, funded_terminated_facility_summary_table):
    title_format = getTitleFormat(workbook)
    header_bold_center = getHeaderBoldCenter(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)
    normal_bold_format = getNormalBoldFormat(workbook)

    
    worksheet = writer.sheets["Summary-terminated facility"]
    worksheet.set_column(0, 5, 30)
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


def generateNonFundedTerminatedFacilityTableWorksheet(writer, workbook, terminated_facility_summary_table):
    title_format = getTitleFormat(workbook)
    header_bold_center = getHeaderBoldCenter(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)
    normal_bold_format = getNormalBoldFormat(workbook)


    worksheet = writer.sheets["Summary-terminated facility"]
    worksheet.set_column(7, 13, 30)
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


def generateSummaryFundedFacilitiesInstallmentWorksheet(writer,workbook,funded_facility_table):
    title_format = getTitleFormat(workbook)
    header_bold_center = getHeaderBoldCenter(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)

    worksheet = writer.sheets["Summary- funded facility"]

    worksheet.merge_range("A1:P1", "Summary of funded facility for same type of concerns classified in summary table:1 - for individual contract: sub-total for same loan to be provided", title_format)
    worksheet.merge_range("A2:P2", "Installments", header_format)
    worksheet.set_column(0, 0, 10)
    worksheet.set_column(2, 15, 30)

    worksheet.write("A3", "Name of Concern", header_format)
    worksheet.write("B3", "B", header_format)
    worksheet.write("C3", "Summary of Funded Facility", header_format)
    worksheet.write("D3", "Limit", header_format)
    worksheet.write("E3", "Outstanding", header_format)
    worksheet.write("F3", "Overdue", header_format)
    worksheet.write("G3", "Start Date", header_format)
    worksheet.write("H3", "End Date of Contract", header_format)
    worksheet.write("I3", "Installment Amount", header_format)
    worksheet.write("J3", "Payment Period (Monthly/ Quarterly/ Half yearly/ Annually)", header_format)
    worksheet.write("K3", "Total no. of Installment", header_format)
    worksheet.write("L3", "Total no. of Installment paid", header_format)
    worksheet.write("M3", "No. of Remaining Installment", header_format)
    worksheet.write("N3", "Date of last payment", header_format)
    worksheet.write("O3", "NPI (No.)", header_format)
    worksheet.write("P3", "Default (Yes/No)", header_format)

    row = 4
    for concern_type in funded_facility_table.keys():
        if concern_type !=None:
            facility_list = [item for item in funded_facility_table[concern_type] if item['Installment Type'] == 'Installment']
            worksheet.merge_range(f"A{row}:A{row+len(facility_list)-1}",concern_type,header_format)
            for idx,item in enumerate(facility_list):
                if item["Nature of Facility"] =='Sub Total':
                    format = header_format
                else:
                    format = normal_format
                worksheet.write("B" + str(idx+row), item["SL"], format)
                worksheet.write("C" + str(idx+row), item["Nature of Facility"], format)
                worksheet.write("D" + str(idx+row), item["Limit"], format)
                worksheet.write("E" + str(idx+row), item["Outstanding"], format)
                worksheet.write("F" + str(idx+row), item["Overdue"], format)
                worksheet.write("G" + str(idx+row), item["Start Date"], format)
                worksheet.write("H" + str(idx+row), item["End Date of Contract"], format)
                worksheet.write("I" + str(idx+row), item["Installment Amount"], format)
                worksheet.write("J" + str(idx+row), item["Payment Period"], format)
                worksheet.write("K" + str(idx+row), item["Total No. of Installment"], format)
                worksheet.write("L" + str(idx+row), item["Total No. of Installment"], format)
                worksheet.write("M" + str(idx+row), item["No. of Remaining Installment"], format)
                worksheet.write("N" + str(idx+row), item["Date of Last Payment"], format)
                worksheet.write("O" + str(idx+row), item["NPI"], format)
                worksheet.write("P" + str(idx+row), item["Default"], format)
                
        
            row += len(facility_list) 
    return row

def generateSummaryFundedFacilitiesNonInstallmentWorksheet(writer,workbook,funded_facility_table, starting_row):
    title_format = getTitleFormat(workbook)
    header_bold_center = getHeaderBoldCenter(workbook)
    header_non_bold = headerNonBold(workbook)
    header_format = getHeaderFormat(workbook)
    normal_format = getNormalFormat(workbook)
    normal_bold_format = getNormalBoldFormat(workbook)

    worksheet = writer.sheets["Summary- funded facility"]

    starting_row+=1

    worksheet.merge_range(f"A{starting_row}:P{starting_row}", "Summary of funded facility for same type of concerns classified in summary table:1 - for individual contract: sub-total for same loan to be provided", title_format)
    worksheet.merge_range(f"A{starting_row+1}:P{starting_row+1}", "Non Installments", title_format)
    

    worksheet.write(f"A{starting_row+2}", "Name of Concern", header_format)
    worksheet.write(f"B{starting_row+2}", "B", header_format)
    worksheet.write(f"C{starting_row+2}", "Summary of Funded Facility", header_format)
    worksheet.write(f"D{starting_row+2}", "Limit", header_format)
    worksheet.write(f"E{starting_row+2}", "Outstanding", header_format)
    worksheet.write(f"F{starting_row+2}", "Overdue", header_format)
    worksheet.write(f"G{starting_row+2}", "Start Date", header_format)
    worksheet.write(f"H{starting_row+2}", "End Date of Contract", header_format)
    worksheet.write(f"I{starting_row+2}", "Installment Amount", header_format)
    worksheet.write(f"J{starting_row+2}", "Payment Period (Monthly/ Quarterly/ Half yearly/ Annually)", header_format)
    worksheet.write(f"K{starting_row+2}", "Total no. of Installment", header_format)
    worksheet.write(f"L{starting_row+2}", "Total no. of Installment paid", header_format)
    worksheet.write(f"M{starting_row+2}", "No. of Remaining Installment", header_format)
    worksheet.write(f"N{starting_row+2}", "Date of last payment", header_format)
    worksheet.write(f"O{starting_row+2}", "NPI (No.)", header_format)
    worksheet.write(f"P{starting_row+2}", "Default (Yes/No)", header_format)

    row = starting_row + 3
    
    for concern_type in funded_facility_table.keys():
        if concern_type !=None:
            facility_list = [item for item in funded_facility_table[concern_type] if item['Installment Type'] == 'No Installment']
            worksheet.merge_range(f"A{row}:A{row+len(facility_list)-1}",concern_type,header_format)
            for idx,item in enumerate(facility_list):
                if item["Nature of Facility"] =='Sub Total':
                    format = header_format
                else:
                    format = normal_format
                worksheet.write("B" + str(idx+row), item["SL"], format)
                worksheet.write("C" + str(idx+row), item["Nature of Facility"], format)
                worksheet.write("D" + str(idx+row), item["Limit"], format)
                worksheet.write("E" + str(idx+row), item["Outstanding"], format)
                worksheet.write("F" + str(idx+row), item["Overdue"], format)
                worksheet.write("G" + str(idx+row), item["Start Date"], format)
                worksheet.write("H" + str(idx+row), item["End Date of Contract"], format)
                worksheet.write("I" + str(idx+row), item["Installment Amount"], format)
                worksheet.write("J" + str(idx+row), item["Payment Period"], format)
                worksheet.write("K" + str(idx+row), item["Total No. of Installment"], format)
                worksheet.write("L" + str(idx+row), item["Total No. of Installment"], format)
                worksheet.write("M" + str(idx+row), item["No. of Remaining Installment"], format)
                worksheet.write("N" + str(idx+row), item["Date of Last Payment"], format)
                worksheet.write("O" + str(idx+row), item["NPI"], format)
                worksheet.write("P" + str(idx+row), item["Default"], format)
        
            row += len(facility_list) 
    

    


    



def generateCorporateSpreadsheet(writer, analysis_report):
    workbook = writer.book

    worksheet = workbook.add_worksheet("Summary Table - 1")
    summary_table_1 = analysis_report["Summary Table - 1"]
    generateSummaryTableWorksheet(writer, workbook, summary_table_1)
    
    worksheet = workbook.add_worksheet("Summary-terminated facility")
    funded_terminated_facility_summary_table = analysis_report["A - Summary of Terminated Facilities"]
    generateFundedTerminatedFacilityTableWorksheet(writer,workbook,funded_terminated_facility_summary_table)
    generateNonFundedTerminatedFacilityTableWorksheet(writer,workbook,funded_terminated_facility_summary_table)
    
    worksheet = workbook.add_worksheet("Summary- funded facility")
    funded_facility_table = analysis_report['B - Summary of Facilities']['Summary of funded facility']
    row = generateSummaryFundedFacilitiesInstallmentWorksheet(writer,workbook,funded_facility_table)
    generateSummaryFundedFacilitiesNonInstallmentWorksheet(writer,workbook,funded_facility_table,row+1)
    
    worksheet = workbook.add_worksheet("Summary Table - 2")
    summary_table_2 = analysis_report["Summary Table - 2"]
    generateSummaryTableTwoWorksheet(writer, workbook, summary_table_2)

    worksheet.autofit()
