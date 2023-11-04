from ..consumer.LoanClass import Loan
from ..consumer.CreditCardClass import CreditCard
from ..consumer.PersonalLoanClass import PersonalLoan
from ..general_helpers import get_worst_status

def get_loan_table(cib):
    try:
        loan_class = Loan(cib)
        response = []
        for i in range(len(loan_class.borrowers_name)):
            response.append({
                    "FI Name": 'Prime Bank Limited',
                    "Borrower Name": str(loan_class.borrowers_name[i]),
                    "Applicants Role": str(loan_class.applicants_role[i]),
                    "Nature of Facility": str(loan_class.loan_investment_request[i]),
                    "Sanctioned Limit": str(loan_class.get_sanction_limit[i]),
                    "Position Date": str(loan_class.get_position_date[i]),
                    "Outstanding": str(loan_class.get_outstanding[i]),
                    "Overdue": str(loan_class.get_overdue[i]),
                    "CL Status": str(loan_class.cl_status[i]),
                    "EMI of Term Loan or percent of Credit Card Limit Outstanding": str(loan_class.EMI[i]),
                    "Loan Start Date": str(loan_class.loan_start_date[i]),
                    "Loan Expiry Date": str(loan_class.loan_expiry_date[i]),
                })
        return response
    except Exception as exc:
        print("Error on loan table")
        print(exc)
        return []

def get_credit_card_table(cib):
    try:
        credit_card_class = CreditCard(cib)
        response = []
        for i in range(len(credit_card_class.borrowers_name)):
            response.append({
                    "FI Name": 'Prime Bank Limited',
                    "Borrower Name": str(credit_card_class.borrowers_name[i]),
                    "Applicants Role": str(credit_card_class.applicants_Role[i]),
                    "Nature of Facility": str(credit_card_class.facility_name[i]),
                    "Sanctioned Limit": str(credit_card_class.get_sanction_limit[i]),
                    "Position Date": str(credit_card_class.get_position_date[i]),
                    "Outstanding": str(credit_card_class.get_outstanding[i]),
                    "Last 12 months Average of Credit Card Outstanding": str(credit_card_class.avg_get_overdue[i]),
                    "Overdue": str(credit_card_class.get_overdue[i]),
                    "CL Status": str(credit_card_class.cl_status[i]),
                    "EMI of Term Loan or percent of Credit Card Limit Outstanding": str(credit_card_class.EMI[i]),
                    "Loan Start Date": str(credit_card_class.loan_start_date[i]),
                    "Loan Expiry Date": str(credit_card_class.loan_expiry_date[i]),
                })
        return response
    except Exception as exc:
        print("Error on credit card table")
        print(exc)
        return []
    
def get_personal_loan_table(cib):
    try:
        personal_class = PersonalLoan(cib)
        response = []
        for i in range(len(personal_class.borrowers_name)):
            response.append({
                    "Borrower Name": str(personal_class.borrowers_name[i]),
                    "Applicants Role": str(personal_class.applicants_role[i]),
                    "Nature of Facility": str(personal_class.facility_name[i]),
                    "Limit": str(personal_class.sanc_limit[i]),
                    "Position Date": str(personal_class.get_position_date[i]),
                    "Outstanding": str(personal_class.get_outstanding[i]),
                    "Overdue": str(personal_class.get_overdue[i]),
                    "CL Status": str(personal_class.cl_status[i]),
                    "EMI of Term Loan or percent of Credit Card Limit Outstanding": str(personal_class.EMI_3[i]),
                    "Loan Start Date": str(personal_class.loan_start_date[i]),
                    "Loan Expiry Date": str(personal_class.loan_expiry_date[i]),
                })
        return response
    except Exception as exc:
        print("Error on personal loan table")
        print(exc)
        return []

def get_cib_owner_info(cib):
    cib_report_of = "None"
    nid = "None"
    current_status = "None"
    try:
        for key in ['Title, Name', 'Title', 'Name', 'name']:
            if key in cib.subject_info.keys():
                cib_report_of = cib.subject_info[key]
                break
            else:
                cib_report_of = "Couldn't read the name"
                # print(cib.subject_info.keys())
    except:
        cib_report_of = "Couldn't read the name"
    
    try:
        for key in ['NID', 'NID (10 Digit)', 'NID (17 Digit)']:
            if key in cib.subject_info.keys():
                nid = cib.subject_info[key]
                break
            else:
                nid = "Couldn't read the NID"
                # print(cib.subject_info.keys())
    except:
        nid = "-"
        
    try:
        current_status = []
        if cib.installment_facility != None:
            current_status.append(get_worst_status(cib.installment_facility[-1]))
        if cib.credit_card_facility != None:
            current_status.append(get_worst_status(cib.credit_card_facility[-1]))
        if cib.noninstallment_facility != None:
            current_status.append(get_worst_status(cib.noninstallment_facility[-1]))
        current_status = get_class_from_set(set(current_status))
    except:
        current_status = "-"
        
        
    return {
        "CIB Report of": cib_report_of,
        "NID Number": nid,
        "Current Status": current_status
    }
    
def get_consumer_dashboard(cib):
    consumer_response = {
        
        "basic_info": get_cib_owner_info(cib),
        "credit_facilities_is_the_name_of_applicant_for_personal_loan_car_loan_home_loan": get_loan_table(cib),
        "credit_facilities_in_the_name_of_applicant_for_credit_card": get_credit_card_table(cib),
        "credit_facilities_in_the_name_of_applicants_business_for_personal_loan_car_loan_home_loan_credit_card": get_personal_loan_table(cib),
    }
    print("___________________________________________")
    print(consumer_response["basic_info"])
    print("___________________________________________")
    
    return consumer_response
