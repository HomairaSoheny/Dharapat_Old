from .engine import facility_summary

class Facility_summary_table_class:
    
    def __init__(self, cib_list):
        self.funded_ins_bor = facility_summary.funded_ins_borrow(cib_list)
        self.funded_nonins_bor= facility_summary.funded_nonins_borrow(cib_list)
        self.funded_ins_guran = facility_summary.funded_ins_guran(cib_list)
        self.funded_non_ins_guran =  facility_summary.funded_nonins_guran(cib_list)
        self.nonfunded_bor = facility_summary.nonfunded_borrow(cib_list)
        self.nonfund_guran =  facility_summary.nonfunded_guran(cib_list)

    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])


