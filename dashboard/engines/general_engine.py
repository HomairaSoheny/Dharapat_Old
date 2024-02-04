def isNonFunded(fac):
    keywords = ['non funded', 'letter of credit', 'gurantee', 'other indirect facility']
    for key in keywords:
        if key in fac["Ref"]["Facility"].lower():
            return True
    return False

def getBorrowersName(subject_info):
    keys = ['Title', 'Name', 'Title, Name', 'Trade Name']
    for key in keys:
        if key in subject_info.keys():
            if len(subject_info[key]) == 0:
                continue
            return subject_info[key]