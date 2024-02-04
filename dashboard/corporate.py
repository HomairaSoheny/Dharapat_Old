from dashboard.engines.corporate_engine import getCorporateDataFrame

def getCorporateDashboard(cibs):
    response = {}
    df = getCorporateDataFrame(cibs)