from .engine import stay_order_summary

class  StayOrderSummaryClass():

    def __init__(self, cib_list):
        self.stay_order_borrower = stay_order_summary.stay_order_borrower(cib_list)
        self.stay_order_gurantor = stay_order_summary.stay_order_gurantor(cib_list)

    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])