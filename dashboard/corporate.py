from dashboard.engines.corporate_engine import *

def getSummaryTable(df):
    response = []
    for category in df['CIB Category'].unique():
        cat_df = df[df['CIB Category'] == category]
        for concern_name in df['Name'].unique():
            temp_df = cat_df[cat_df['Name'] == concern_name]
            response.append(getSummaryTableFields(category, concern_name, temp_df))
        sub_total_df = pd.DataFrame(response)
        sub_total_df = sub_total_df[sub_total_df['CIB Category'] == category]
        response.append(getSummaryTableSum(category, "Sub Total", sub_total_df))
    total_df = pd.DataFrame(response)
    total_df = total_df[total_df['Name of Concern'] == "Sub Total"]
    response.append(getSummaryTableSum(category, "Grand Total", total_df))
    return response

def getSummaryOfTerminatedFacilityFunded(df):
    response = []
    return response

def getSummaryOfTerminatedFacilityNonFunded(df):
    response = []
    return response

def getSummaryOfFundedFacility(df):
    response = []
    df = df[df['Is Funded'] == 'Yes']
    installment = df[df['Installment Type'] == 'Installment']
    non_installment = df[df['Installment Type'] == 'No Installment']
    
    for i, row in installment.iterrows():
        response.append(getSummaryOfFundedFacilityFields(row, i, True))
    response.append(getSummaryOfFundedFacilitySum(installment, "Sub Total", "Installment"))

    for i, row in non_installment.iterrows():
        response.append(getSummaryOfFundedFacilityFields(row, i, False))
    response.append(getSummaryOfFundedFacilitySum(installment, "Sub Total", "No Installment"))
    
    return response

def getCorporateDashboard(cibs):
    response = {}
    df = getCorporateDataFrame(cibs)
    response['analysis type'] = "Corporate"
    response['Summary Table - 1'] = getSummaryTable(df)
    response['Summary of terminated facility (Funded)'] = getSummaryOfTerminatedFacilityFunded(df)
    response['Summary of terminated facility (Non Funded)'] = getSummaryOfTerminatedFacilityNonFunded(df)
    response['Summary of funded facility'] = getSummaryOfFundedFacility(df)
    return response