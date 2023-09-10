from itertools import zip_longest


def isNonFunded(fac):
    if ("non funded" in fac["Ref"]["Facility"].lower() or
        "letter of credit" in fac["Ref"]["Facility"].lower() or
        "guarantee" in fac["Ref"]["Facility"].lower() or
        "other indirect facility" in fac["Ref"]["Facility"].lower() ):
        return True
    return False

def funded_installment(cib):
    try:
        response = []
        if cib.installment_facility is None:
            return []
        for facility in cib.installment_facility:
            if isNonFunded(facility) is False:
                response.append(float(facility["Ref"]['Sanction Limit']))
        return response
    except:
        return []

def funded_no_installment(cib):
    try:
        response = []
        if cib.noninstallment_facility is None:
            return []
        for facility in cib.noninstallment_facility:
            if isNonFunded(facility) is False:
                response.append(float(facility["Ref"]['SancLmt']))
        return response
    except:
        return []

def funded_total(cib):
    try:
        funded = funded_installment(cib)
        non_funded = funded_no_installment(cib)
        return [sum(n) for n in zip_longest(funded, non_funded, fillvalue=0)]
    except:
        return []
    
def non_funded(cib):
    try:
        response = []
        if cib.installment_facility is not None:
            for facility in cib.installment_facility:
                if isNonFunded(facility) is True:
                    response.append(float(facility["Ref"]["Sanction Limit"]))
        if cib.noninstallment_facility is not None:
            for facility in cib.noninstallment_facility:
                if isNonFunded(facility) is True:
                    response.append(float(facility["Ref"]["SancLmt"]))
        return response
    except:
        return []

def total(cib):
    try:
        funded = funded_total(cib)
        nonFunded = non_funded(cib)
        return [sum(n) for n in zip_longest(funded, nonFunded, fillvalue=0)]
    except:
        return []

def get_overdue(cib):
    try:
        overdue = []
        for fac_type in (cib.installment_facility, cib.credit_card_facility):
            if fac_type is not None:
                for fac in fac_type:
                    if (fac["Ref"]["Phase"]) == "Living":
                        overdue.append(float((fac["Contract History"]).sort_values("Date", ascending=False).Overdue[0]))  
        return overdue
    except:
        return []

def get_cl_status(cib):
    try:
        status = []
        for fac_type in (cib.installment_facility, cib.credit_card_facility):
            if fac_type is not None:
                for fac in fac_type:
                    if (fac["Ref"]["Phase"]) == "Living":
                        status.append(float(fac["Contract History"]).sort_values("Date", ascending=False).Status[0])
        return status
    except:
        return []

def get_default(cib):
    try:
        return []
    except:
        return []
    
def get_std(cib):
    try:
        return []
    except:
        return []

def get_sma(cib):
    try:
        response = []
        for i in cib.summary_1A["SMA_Amount"].tolist()[:3] + cib.summary_2A["SMA_Amount"].tolist()[:3]:
            response.append(str(i))
        return response
    except:
        return []

def get_ss(cib):
    try:
        response = []
        for i in cib.summary_1A["SS_Amount"].tolist()[:3] + cib.summary_2A["SS_Amount"].tolist()[:3]:
            response.append(str(i))
        return response
    except:
        return []

def get_df(cib):
    try:
        response = []
        for i in cib.summary_1A["DF_Amount"].tolist()[:3] + cib.summary_2A["DF_Amount"].tolist()[:3]:
            response.append(str(i))
        return response
    except:
        return []
    
def get_bl(cib):
    try:
        response =[]
        for i in cib.summary_1A["BL_Amount"].tolist()[:3] + cib.summary_2A["BL_Amount"].tolist()[:3]:
            response.append(str(i))
        return response
    except:
        return []

def get_blw(cib):
    try:
        response = []
        for i in cib.summary_1A["BLW_Amount"].tolist()[:3] + cib.summary_2A["BLW_Amount"].tolist()[:3]:
            response.append(str(i))
        return response
    except:
        return []

def get_stay_order(cib):
    try:
        response = []
        for i in cib.summary_1A["Stay Order_Amount"].tolist()[:3] + cib.summary_2A["Stay Order_Amount"].tolist()[:3]:
            response.append(str(i))
        return response
    except:
        return []

def get_remarks(cib):
    try:
        return str(cib.subject_info["Remarks"])
    except:
        return []
