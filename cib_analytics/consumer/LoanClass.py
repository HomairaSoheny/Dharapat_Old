from .engine import loan
from .engine import general_engine

class Loan:
    def __init__(self, cib_data):
        self.borrowers_name = general_engine.borrowers_name(cib_data)
        self.applicants_role  = general_engine.get_applicants_role(cib_data)
        self.loan_investment_request = general_engine.get_facility_name(cib_data)
        self.get_sanction_limit = general_engine.get_sanction_limit(cib_data)
        self.get_position_date = general_engine.get_position_date(cib_data)
        self.get_outstanding = general_engine.get_outstanding(cib_data)
        self.get_overdue = general_engine.get_overdue(cib_data)
        self.cl_status  = general_engine.cl_status(cib_data)
        self.EMI = loan.EMI_1(cib_data)
        self.loan_start_date = general_engine.loan_start_date(cib_data)
        self.loan_expiry_date = general_engine.loan_expiry_date(cib_data)

    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])