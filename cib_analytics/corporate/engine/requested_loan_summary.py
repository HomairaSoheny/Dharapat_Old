import pandas as pd

def requested_loan(cibs):

    req_loan = {
        "Type of Contract": ['Credit card'],
        "Facility": ["None"],
        "Role": ["None"],
        "Total Requested Amount": ["None"],
        "Request date": ["None"]}

    req_loan = pd.DataFrame(req_loan)
    columns_to_keep =["Type of Contract","Facility","Role", "Total Requested Amount", "Request date"]
    for cib in cibs:
        if isinstance(cib.req_contracts, type(None)):
            pass
        else:
            new_df = cib.req_contracts[columns_to_keep]
            req_loan = pd.concat([req_loan, new_df], ignore_index=True)
    requested_loan_res = req_loan.loc[~req_loan['Type of Contract'].str.lower().isin(['credit card'])]
    requested_loan_res = requested_loan_res.sort_values("Type of Contract")
    requested_loan_res = requested_loan_res.reset_index(drop=True)

    return requested_loan_res

