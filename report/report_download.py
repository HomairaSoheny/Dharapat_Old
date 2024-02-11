import pandas as pd
from io import BytesIO

from report.excel.consumer import generateConsumerSpreadsheet

def createReportDashboard(cib_datas):
    io = BytesIO()
    writer = pd.ExcelWriter(io, engine='xlsxwriter', )
    generateConsumerSpreadsheet(writer, cib_datas)
    
    return writer, io