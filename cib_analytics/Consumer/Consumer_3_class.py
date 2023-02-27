
from .engine import Consumer_3_engine
class Consumer_3_class:
    
    def __init__(self, cib_data):
        

        self.Borrowers_name = Consumer_3_engine.Borrowers_name(cib_data)

        self.Applicants_Role  = Consumer_3_engine.get_Applicants_Role(cib_data)

        self.facility_name = Consumer_3_engine.get_facility_name(cib_data)
        
        self.sanc_limit    = Consumer_3_engine.sanc_limit(cib_data)
        
        self.get_position_date = Consumer_3_engine.get_position_date(cib_data)
        
        self.get_outstanding  = Consumer_3_engine.get_outstanding(cib_data)
        
        self.get_overdue = Consumer_3_engine.get_overdue(cib_data)
        
        self.cl_status = Consumer_3_engine.cl_status(cib_data)
        
        self.EMI_3  = Consumer_3_engine.EMI_3(cib_data)
        
        self.Loan_start_date = Consumer_3_engine.Loan_start_date(cib_data)
        
        self.Loan_expiry_date = Consumer_3_engine.Loan_expiry_date(cib_data)
