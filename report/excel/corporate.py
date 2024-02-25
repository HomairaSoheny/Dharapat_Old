def generateSummaryTableWorksheet(writer, workbook, summary_table):

    title_format = workbook.add_format(
        {
            "bold": True,
            "border": 2,
            "align": "center",
            "valign": "vcenter",
            # "fg_color": "#051094",
            "font_size": 17,
            # "font_color": "white",
            # "border_color": "white",
        }
    )
    
    header_bold_center = workbook.add_format(
        {
            "bold": True,
            "align": 'center',
            "valign": 'vcenter',
            "font_size": 12,
            "border": 1,
            # "fg_color": "#051094",
            # "font_color": "white",
            # "border_color": "white",
        }
    )
    
    header_non_bold = workbook.add_format(
        {
            "align": 'center',
            "font_size": 12,
            "border": 1,
            "valign": 'vcenter',
            # "fg_color": "#051094",
            # "font_color": "white",
            # "border_color": "white",
        }
    )

    header_format = workbook.add_format(
        {
            "bold": True,
            "font_size": 12,
            "border": 1,
            "valign": 'vcenter',
            # "fg_color": "#051094",
            # "font_color": "white",
            # "border_color": "white",
        }
    )
    
    normal_format = workbook.add_format(
        {
            "font_size": 12,
        }
    )

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


def generateFundedTerminatedFacilityTableWorksheet(writer, workbook, funded_terminated_facility_summary_table):
    title_format = workbook.add_format(
        {
            "bold": True,
            "border": 2,
            "align": "center",
            "valign": "vcenter",
            # "fg_color": "#051094",
            "font_size": 17,
            # "font_color": "white",
            # "border_color": "white",
            'text_wrap':True
        }
    )
    
    header_bold_center = workbook.add_format(
        {
            "bold": True,
            "align": 'center',
            "valign": 'vcenter',
            "font_size": 12,
            "border": 1,
            'text_wrap':True
            # "fg_color": "#051094",
            # "font_color": "white",
            # "border_color": "white",
        }
    )

    header_non_bold = workbook.add_format(
        {
            "align": 'center',
            "font_size": 12,
            "border": 1,
            "valign": 'vcenter',
            'text_wrap':True
            # "fg_color": "#051094",
            # "font_color": "white",
            # "border_color": "white",
        }
    )

    header_format = workbook.add_format(
        {
            "bold": True,
            "font_size": 12,
            "border": 1,
            "valign": 'vcenter',
            'text_wrap':True
            # "fg_color": "#051094",
            # "font_color": "white",
            # "border_color": "white",
        }
    )

    normal_format = workbook.add_format(
        {
            "font_size": 12,
            "text_wrap": True
        }
    )
    normal_bold_format = workbook.add_format(
        {
            "bold": True,
            "font_size": 12,
        }
    )

    
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
    title_format = workbook.add_format(
        {
            "bold": True,
            "border": 2,
            "align": "center",
            "valign": "vcenter",
            # "fg_color": "#051094",
            "font_size": 17,
            # "font_color": "white",
            # "border_color": "white",
            'text_wrap':True
        }
    )
    
    header_bold_center = workbook.add_format(
        {
            "bold": True,
            "align": 'center',
            "valign": 'vcenter',
            "font_size": 12,
            "border": 1,
            'text_wrap':True
            # "fg_color": "#051094",
            # "font_color": "white",
            # "border_color": "white",
        }
    )

    header_non_bold = workbook.add_format(
        {
            "align": 'center',
            "font_size": 12,
            "border": 1,
            "valign": 'vcenter',
            'text_wrap':True
            # "fg_color": "#051094",
            # "font_color": "white",
            # "border_color": "white",
        }
    )

    header_format = workbook.add_format(
        {
            "bold": True,
            "font_size": 12,
            "border": 1,
            "valign": 'vcenter',
            'text_wrap':True
            # "fg_color": "#051094",
            # "font_color": "white",
            # "border_color": "white",
        }
    )

    normal_format = workbook.add_format(
        {
            "font_size": 12,
        }
    )
    normal_bold_format = workbook.add_format(
        {
            "bold": True,
            "font_size": 12,
        }
    )


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


def generateCorporateSpreadsheet(writer, analysis_report):
    workbook = writer.book

    worksheet = workbook.add_worksheet("Summary Table - 1")
    summary_table_1 = analysis_report["Summary Table - 1"]
    generateSummaryTableWorksheet(writer, workbook, summary_table_1)
    worksheet = workbook.add_worksheet("Summary-terminated facility")
    funded_terminated_facility_summary_table = analysis_report["A - Summary of Terminated Facilities"]
    generateFundedTerminatedFacilityTableWorksheet(writer,workbook,funded_terminated_facility_summary_table)
    generateNonFundedTerminatedFacilityTableWorksheet(writer,workbook,funded_terminated_facility_summary_table)

    worksheet.autofit()
