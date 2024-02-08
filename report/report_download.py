import pandas as pd
from io import BytesIO

from report.excel.consumer import generateConsumerSpreadsheet

def createReportDashboard(cib_datas):
    io = BytesIO()
    writer = pd.ExcelWriter(io, engine='xlsxwriter', )

    # if "summary of cib liability" in cib_datas[0]:
    #     generate_corporate_spreadsheet(writer, cib_datas[0])
    # else:
    generateConsumerSpreadsheet(writer, cib_datas[0])
    
    return writer, io