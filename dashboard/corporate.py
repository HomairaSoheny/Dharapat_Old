from dashboard.engines.corporate_engine import getCorporateDataFrame

def summaryTable1(df):
    return df

def getCorporateDashboard(cibs):
    response = {}
    df = getCorporateDataFrame(cibs)