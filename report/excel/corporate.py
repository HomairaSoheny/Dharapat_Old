import pandas as pd
from report.excel.general_helper import align_center


def generateSummaryTableWorksheet(writer, workbook, summary_table):

    title_format = workbook.add_format(
        {
            "bold": True,
            "border": 6,
            "align": "center",
            "valign": "vcenter",
            # "fg_color": "#051094",
            "font_size": 17,
            # "font_color": "white",
            # "border_color": "white",
        }
    )
    
    header_non_bold = workbook.add_format(
        {
            "bold": True,
            "font_size": 12,
            "border": 2,
            # "fg_color": "#051094",
            # "font_color": "white",
            # "border_color": "white",
        }
    )

    header_format = workbook.add_format(
        {
            "bold": True,
            "font_size": 12,
            "border": 2,
            # "fg_color": "#051094",
            # "font_color": "white",
            # "border_color": "white",
        }
    )
    
    normal_format = workbook.add_format(
        {
            "font_size": 12
        }
    )

    worksheet = writer.sheets["Summary Table - 1"]
    worksheet.merge_range("A1:I1", "Summary Table - 1", title_format)
    worksheet.write("A2", "Position as on", header_format)
    worksheet.merge_range("B2:I2", "BDT in Million", header_non_bold)
    worksheet.merge_range("A3:A4", "Name of Concern", header_format)
    worksheet.merge_range("B3:D3", "Funded Outstanding", header_format)
    worksheet.write("B4", "Installment", header_format)
    worksheet.write("C4", "Non Installment", header_format)
    worksheet.write("D4", "Total", header_format)
    worksheet.merge_range("E3:E4", "Non-Funded Outstanding", header_format)
    worksheet.merge_range("F3:F4", "Total Outstanding", header_format)
    worksheet.merge_range("G3:G4", "Overdue", header_format)
    worksheet.merge_range("H3:H4", "CL Status", header_format)
    worksheet.merge_range("I3:I4", "Default", header_format)
    worksheet.merge_range("J1:J4", "CIB PDF View", header_format)
    worksheet.merge_range(
        "K1:K4",
        "Updated Overdue and CL status (as per detail report) based on new inclusion of BB for real time CIB",
        header_format,
    )

    for idx, row in enumerate(summary_table):
        format = header_format if row["Name of Concern"] in ("Sub Total", "Grand Total") else normal_format
        i = idx + 5
        worksheet.write("A" + str(i), row["Name of Concern"], format)
        worksheet.write("B" + str(i), row["Funded Outstanding Installment"], format)
        worksheet.write("C" + str(i), row["Funded Outstanding Non Installment"], format)
        worksheet.write("D" + str(i), row["Funded Outstanding Total"], format)
        worksheet.write("E" + str(i), row["Non-Funded Outstanding"], format)
        worksheet.write("F" + str(i), row["Total Outstanding"], format)
        worksheet.write("G" + str(i), row["Overdue"], format)
        worksheet.write("H" + str(i), row["CL Status"], format)
        worksheet.write("I" + str(i), row["Default"], format)
        worksheet.write("J" + str(i), "N/A", format)
        worksheet.write("K" + str(i), row["Updated Overdue and CL Status"], format)


def generateCorporateSpreadsheet(writer, analysis_report):
    workbook = writer.book

    worksheet = workbook.add_worksheet("Summary Table - 1")
    summary_table_1 = analysis_report["Summary Table - 1"]
    generateSummaryTableWorksheet(writer, workbook, summary_table_1)

    worksheet.autofit()
