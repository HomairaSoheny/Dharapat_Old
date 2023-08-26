import pandas as pd
from io import BytesIO
import datetime
from .consumer_spreadsheet import generate_consumer_spreadsheet
from .corporate_spreadsheet import generate_corporate_spreadsheet

def create_report_dashboard(cib_datas, output_dir: str):
    Output = output_dir + f'\\filename dashboard {datetime.datetime.now().strftime("%d-%m-%Y %Hh%Mm%Ss")}.xlsx'
    io = BytesIO()
    writer = pd.ExcelWriter(io, engine='xlsxwriter', )

    if "summary of cib liability" in cib_datas[0]:
        generate_corporate_spreadsheet(writer, cib_datas[0])
    else:
        for cib in cib_datas:
            generate_consumer_spreadsheet(writer, cib)
    
    return writer, io