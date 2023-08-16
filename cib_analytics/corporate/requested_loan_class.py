from .engine import requested_loan_summary

class requested_loan_summary_table_class:
    
    def __init__(self, cib_list):
        self.Funded_ins_bor = requested_loan_summary.requested_loan(cib_list)
        
    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])