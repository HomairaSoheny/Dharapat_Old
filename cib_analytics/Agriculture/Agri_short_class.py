from ..cib_data_class import cib_class
from . import engine

class agri_short_class:
    def __init__(self, cib_data : cib_class):

        self.current_status = engine.current_status(cib_data)

        self.inquired_date  = engine.inquired_date(cib_data)

        self.loan_investment_request = engine.loan_investment_request(cib_data)

        self.get_sanc_limit = engine.get_sanc_limit(cib_data)
        
        self.get_outstanding = engine.get_outstanding(cib_data)

        self.get_overdue = engine.get_overdue(cib_data)

    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items()])