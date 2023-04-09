from ..consumer.consumer_1_class import Consumer_1_class
from ..consumer.consumer_2_class import Consumer_2_class
from ..consumer.consumer_3_class import Consumer_3_class

def get_loan_table(cib):
    try:
        loan_class = Consumer_1_class(cib)
        response = []
        for i in range(len(loan_class.Borrowers_name)):
            response.append({
                    "FI Name": 'will be inputted manually',
                    "Borrower Name": str(loan_class.Borrowers_name[i]),
                    "Applicants Role": str(loan_class.Applicants_Role[i]),
                    "Nature of Facility": str(loan_class.loan_investment_request[i]),
                    "Sanctioned Limit": str(loan_class.get_sanction_limit[i]),
                    "Position Date": str(loan_class.get_position_date[i]),
                    "Outstanding": str(loan_class.get_outstanding[i]),
                    "Overdue": str(loan_class.get_overdue[i]),
                    "CL Status": str(loan_class.cl_status[i]),
                    "EMI of Term Loan or percent of Credit Card Limit Outstanding": str(loan_class.EMI[i]),
                    "Loan Start Date": str(loan_class.Loan_start_date[i]),
                    "Loan Expiry Date": str(loan_class.Loan_expiry_date[i]),
                })
        return response
    except Exception as exc:
        print("Error on consumer table 1")
        print(exc)
        return []

def get_credit_card_table(cib):
    try:
        credit_card_class = Consumer_2_class(cib)
        response = []
        for i in range(len(credit_card_class.Borrowers_name)):
            response.append({
                    "FI Name": 'will be inputted manually',
                    "Borrower Name": str(credit_card_class.Borrowers_name[i]),
                    "Applicants Role": str(credit_card_class.Applicants_Role[i]),
                    "Nature of Facility": str(credit_card_class.facility_name[i]),
                    "Sanctioned Limit": str(credit_card_class.get_sanction_limit[i]),
                    "Position Date": str(credit_card_class.get_position_date[i]),
                    "Outstanding": str(credit_card_class.get_outstanding[i]),
                    "Last 12 months Average of Credit Card Outstanding": str(credit_card_class.avg_get_overdue[i]),
                    "Overdue": str(credit_card_class.get_overdue[i]),
                    "CL Status": str(credit_card_class.cl_status[i]),
                    "EMI of Term Loan or percent of Credit Card Limit Outstanding": str(credit_card_class.EMI[i]),
                    "Loan Start Date": str(credit_card_class.Loan_start_date[i]),
                    "Loan Expiry Date": str(credit_card_class.Loan_expiry_date[i]),
                })
        return response
    except Exception as exc:
        print("Error on consumer table 2")
        print(exc)
        return []
    
def get_personal_loan_table(cib):
    try:
        personal_class = Consumer_3_class(cib)
        response = []
        for i in range(len(personal_class.Borrowers_name)):
            response.append({
                    "Borrower Name": str(personal_class.Borrowers_name[i]),
                    "Applicants Role": str(personal_class.Applicants_Role[i]),
                    "Nature of Facility": str(personal_class.facility_name[i]),
                    "Limit": str(personal_class.sanc_limit[i]),
                    "Position Date": str(personal_class.get_position_date[i]),
                    "Outstanding": str(personal_class.get_outstanding[i]),
                    "Overdue": str(personal_class.get_overdue[i]),
                    "CL Status": str(personal_class.cl_status[i]),
                    "EMI of Term Loan or percent of Credit Card Limit Outstanding": str(personal_class.EMI_3[i]),
                    "Loan Start Date": str(personal_class.Loan_start_date[i]),
                    "Loan Expiry Date": str(personal_class.Loan_expiry_date[i]),
                })
        return response
    except Exception as exc:
        print("Error on consumer table 3")
        print(exc)
        return []

def get_consumer_dashboard(cib):
    consumer_response = {
        "credit_facilities_is_the_name_of_applicant_for_personal_loan_car_loan_home_loan": get_loan_table(cib),
        "credit_facilities_in_the_name_of_applicant_for_credit_card": get_credit_card_table(cib),
        "credit_facilities_in_the_name_of_applicants_business_for_personal_loan_car_loan_home_loan_credit_card": get_personal_loan_table(cib),
    }
    
    return consumer_response
