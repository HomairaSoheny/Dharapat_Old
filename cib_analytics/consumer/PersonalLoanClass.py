from .engine import personal_loan

class PersonalLoan:
    def __init__(self, cib_data):
        self.borrowers_name = personal_loan.Borrowers_name(cib_data)
        self.applicants_role  = personal_loan.get_Applicants_Role(cib_data)
        self.facility_name = personal_loan.get_facility_name(cib_data)
        self.sanc_limit    = personal_loan.sanc_limit(cib_data)
        self.get_position_date = personal_loan.get_position_date(cib_data)
        self.get_outstanding  = personal_loan.get_outstanding(cib_data)
        self.get_overdue = personal_loan.get_overdue(cib_data)
        self.cl_status = personal_loan.cl_status(cib_data)
        self.EMI_3  = personal_loan.EMI_3(cib_data)
        self.loan_start_date = personal_loan.Loan_start_date(cib_data)
        self.loan_expiry_date = personal_loan.Loan_expiry_date(cib_data)

def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])