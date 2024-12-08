import pandas as pd
from io import BytesIO

from report.excel.consumer import generateConsumerSpreadsheet
from report.excel.corporate import generateCorporateSpreadsheet


def prepare_consumer_data_for_report(data):
    final_data = []
    for each in data['dashboardData']:
        individual = {}
        for i in each['tables']:
            a = {}
            name = i['title']
            title, loan_type = name.rsplit(" - ", 1)
            if title not in individual.keys():
                a[loan_type] = i['data']
                individual[title] = a
            else:
                individual[title][loan_type] = i['data']

        for c in each['cards']:
            for d in c['data']:
                key = d['label']
                value = d['value']
                individual[key] = value
        individual['pdf_name'] = each['tabName']
        final_data.append(individual)

    return final_data

def prepare_corporate_data_for_report(data):
    final_data = {}
    for each in data['dashboardData']:
        for i in each['tables']:
            key = i['title']
            value = i['data']
            final_data[key] = value
    return final_data


def createReportDashboard(analysis_report):
    io = BytesIO()
    writer = pd.ExcelWriter(io, engine='xlsxwriter')
    if analysis_report['clientType'] == 'Consumer':
        print("Generating Consumer Analysis Report")
        data = prepare_consumer_data_for_report(analysis_report)
        generateConsumerSpreadsheet(writer, data)
    else:
        print("Generating Corporate Analysis Report")
        data = prepare_corporate_data_for_report(analysis_report)
        generateCorporateSpreadsheet(writer, data)
    
    return writer, io