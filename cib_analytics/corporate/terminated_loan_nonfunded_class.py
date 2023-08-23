from .engine import terminated_loan_summary

class TerminatedLoanNonfundedTableClass():

    def __init__(self, cib_list):

        self.total_nonfunded_terminated_loan = terminated_loan_summary.term_total_nonfunded_loan(cib_list)
        self.non_funded_ins_limit = terminated_loan_summary.nonfunded_worse_cl_status(cib_list)
        self.non_funded_facility_name = terminated_loan_summary.nonfunded_facility_name(cib_list)
        self.non_funded_ins_worse_cl_status = terminated_loan_summary.nonfunded_worse_cl_status(cib_list)
        self.non_Funded_date_of_classification = terminated_loan_summary.nonfunded_date_of_class(cib_list)

    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])