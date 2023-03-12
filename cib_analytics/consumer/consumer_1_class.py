from .engine import consumer_1_engine

class Consumer_1_class:
    def __init__(self, cib_data):
        self.Borrowers_name = consumer_1_engine.Borrowers_name(cib_data)
        self.Applicants_Role  = consumer_1_engine.get_Applicants_Role(cib_data)
        self.loan_investment_request = consumer_1_engine.get_facility_name(cib_data)
        self.get_sanction_limit = consumer_1_engine.get_sanction_limit(cib_data)
        self.get_position_date = consumer_1_engine.get_position_date(cib_data)
        self.get_outstanding = consumer_1_engine.get_outstanding(cib_data)
        self.get_overdue = consumer_1_engine.get_overdue(cib_data)
        self.cl_status  = consumer_1_engine.cl_status(cib_data)
        self.EMI = consumer_1_engine.EMI_1(cib_data)
        self.Loan_start_date = consumer_1_engine.Loan_start_date(cib_data)
        self.Loan_expiry_date = consumer_1_engine.Loan_expiry_date(cib_data)

    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])