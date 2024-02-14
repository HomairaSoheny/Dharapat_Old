import pandas as pd
from io import BytesIO

from report.excel.consumer import generateConsumerSpreadsheet
from report.excel.corporate import generateCorporateSpreadsheet

def createReportDashboard(analysis_report):
    print("Entered report dashboard")
    io = BytesIO()
    writer = pd.ExcelWriter(io, engine='xlsxwriter', )
    if type(analysis_report) == list:
        print("Generating Consumer Analysis Report")
        generateConsumerSpreadsheet(writer, analysis_report)
    else:
        print("Generating Corporate Analysis Report")
        generateCorporateSpreadsheet(writer, analysis_report)
    
    return writer, io