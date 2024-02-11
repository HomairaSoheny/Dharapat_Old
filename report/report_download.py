import pandas as pd
from io import BytesIO

from report.excel.consumer import generateConsumerSpreadsheet
from report.excel.corporate import generateCorporateSpreadsheet

def createReportDashboard(analysis_report):
    io = BytesIO()
    writer = pd.ExcelWriter(io, engine='xlsxwriter', )
    if type(analysis_report) == list:
        generateConsumerSpreadsheet(writer, analysis_report)
    else:
        generateCorporateSpreadsheet(writer, analysis_report)
    
    return writer, io