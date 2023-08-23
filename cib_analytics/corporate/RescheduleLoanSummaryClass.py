from .engine import reschedule_loan_summary

class RescheduleLoanSummary:
    def __init__(self, cib_list):
        self.reschedule_loan_for_borrower = reschedule_loan_summary.rescheduled_loan_borrow(cib_list)
        self.reschedule_loan_for_gurantor = reschedule_loan_summary.rescheduled_loan_guran(cib_list)
    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])
