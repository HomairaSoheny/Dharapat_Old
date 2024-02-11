import pandas as pd
from report.excel.general_helper import align_center

def generateCorporateSpreadsheet(writer, analysis_report):
    workbook = writer.book
    
    header_format = workbook.add_format(
        {
            "bold": True,
            "text_wrap": True,
            "valign": "top",
            "fg_color": "#051094",
            "font_color": "white",
            "border": 1,
            'font_size': 14
        })
        
    title_format = workbook.add_format({
        "text_wrap": True,
        "valign": "top",
        "align": "right",
        "border": 1,
        "font_size": 12
    })
    
    bold = workbook.add_format({
        'bold': True,
        'font_size': 17
        })
    
    summary_table_1 = analysis_report['Summary Table - 1']
    summary_table_1 = pd.DataFrame(summary_table_1)
    summary_table_1.style.apply(align_center, axis=0).to_excel(writer, sheet_name="Summary Table - 1", startrow=3, index=False, header=True)
    worksheet = writer.sheets["Summary Table - 1"]
    worksheet.write("A1", "Summary Table - 1", bold)
    worksheet.write("A2", "BDT in Million")
    
    worksheet.autofit()