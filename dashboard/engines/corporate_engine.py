def getCIBCategory(cib):
    category_mapping = {
        "Type a": "Concerns of primary borrower with PBL",
        "Type b": "Other sister concerns of primary borrower",
        "Type c": "Other concerns due to common shareholdings/directorship",
        "Type d": "Directors CIB",
        "Type e": "20% plus shareholder other than director",
        "Type f": "Guarantors CIB (Personal)",
        "Type g": "Corporate Guarantor",
        "Type h": "Related party of Guarantor",
        "Type i": "Other concerns/persons not related to the company"
    }

    return category_mapping.get(cib.cib_category, None)

def getDateOfClassification(fac):
    for key in ['Date of classification']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
        
def getStartDate(fac):
    for key in ['Starting date']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
        
def getEndDateOfContract(fac):
    for key in ['End date of contract']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
        
def getRemarks(fac):
    for key in ['Remarks']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]
        
def getPaymentPeriod(fac):
    for key in ['Payments Periodicity', 'Payments periodicity',]:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]

def getTotalNumberOfInstallment(fac):
    for key in ['Total number of installments']:
        if key in fac['Ref'].keys():
            return fac['Ref'][key]