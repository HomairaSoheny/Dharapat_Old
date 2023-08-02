from .engine import facility_summary

class facility_summary_table_class:
    
    def __init__(self, cib_list):
        self.Funded_ins_bor = facility_summary.funded_ins_borrow(cib_list)
        self.Funded_nonins_bor= facility_summary.funded_nonins_borrow(cib_list)
        self.Funded_ins_guran = facility_summary.funded_ins_guran(cib_list)
        self.Funded_non_ins_guran =  facility_summary.funded_nonins_guran(cib_list)
        self.Nonfunded_bor = facility_summary.Nonfunded_borrow(cib_list)
        self.Nonfund_guran =  facility_summary.Nonfunded_guran(cib_list)

    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])


