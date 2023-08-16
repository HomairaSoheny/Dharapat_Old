from .engine import terminated_loan_summary

class TerminatedLoanFundedTableClass():

    def __init__(self, cib_list):
        self.number_of_funded_terminated_loan = terminated_loan_summary.term_total_funded_loan(cib_list)
        self.Funded_ins_limit = terminated_loan_summary.funded_ins_limit(cib_list)
        self.Funded_facility_name = terminated_loan_summary.funded_ins_facility_name(cib_list)
        self.Funded_ins_worse_cl_status = terminated_loan_summary.funded_ins_worse_cl_status(cib_list)
        self.Funded_date_of_classification = terminated_loan_summary.funded_ins_date_of_class(cib_list)

        self.Funded_nonins_limit = terminated_loan_summary.funded_non_ins(cib_list)
        self.Funded_nonins_facility_name = terminated_loan_summary.funded_non_ins_facility_name(cib_list)
        self.Funded_nonins_worse_cl_status = terminated_loan_summary.funded_non_ins_worse_cl_status(cib_list)
        self.Funded_nonins_date_of_classification = terminated_loan_summary.funded_non_ins_date_of_class(cib_list)
    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])