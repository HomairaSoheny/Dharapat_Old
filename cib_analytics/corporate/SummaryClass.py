from .engine import corporate_summary
from ..general_helpers import get_status
class Summary():
    def __init__(self, cibs):
            
            self.concern_name = corporate_summary.get_concern_name(cibs)
            self.funded_ins_data = corporate_summary.get_outs_fund_ins(cibs)
            self.funded_non_ins_data = corporate_summary.get_outs_fund_non_ins(cibs)
            self.total_funded_amount = corporate_summary.get_total_fund_out(cibs)
            self.non_funded_amount = corporate_summary.get_outs_non_fund(cibs)
            self.total_amount = corporate_summary.get_outs_total(cibs)
            self.overdue_amount = corporate_summary.get_overdue(cibs)
            self.status = get_status(cibs)
                       
    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])