from .engine import consumer_2_engine

class Consumer_2_class:
    def __init__(self, cib_data):
        self.Borrowers_name = consumer_2_engine.Borrowers_name(cib_data)
        self.Applicants_Role  = consumer_2_engine.get_Applicants_Role(cib_data)
        self.facility_name = consumer_2_engine.get_facility_name(cib_data)
        self.get_sanction_limit = consumer_2_engine.get_sanction_limit(cib_data)
        self.get_position_date = consumer_2_engine.get_position_date(cib_data)
        self.get_outstanding = consumer_2_engine.get_outstanding(cib_data)
        self.avg_get_overdue = consumer_2_engine.avg_get_overdue
        self.get_overdue = consumer_2_engine.get_overdue(cib_data)
        self.cl_status  = consumer_2_engine.cl_status(cib_data)
        self.EMI = consumer_2_engine.EMI_2(cib_data)
        self.Loan_start_date = consumer_2_engine.Loan_start_date(cib_data)
        self.Loan_expiry_date = consumer_2_engine.Loan_expiry_date(cib_data)

    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])