from .engine import summary

class SummaryCIBLiability:
    def __init__(self, cib_data):
        self.funded = {
                "installment": summary.funded_installment(cib_data),
                "no_installment": summary.funded_no_installment(cib_data),
                "total": summary.funded_total(cib_data)
            }
        self.non_funded = summary.non_funded(cib_data)
        self.total = summary.total(cib_data)
        self.overdue = summary.get_overdue(cib_data)
        self.cl_status = summary.get_cl_status(cib_data)
        self.default = summary.get_default(cib_data)
        self.loan_amount = {
                "STD": summary.get_std(cib_data),
                "SMA": summary.get_sma(cib_data),
                "SS": summary.get_ss(cib_data),
                "DF": summary.get_df(cib_data),
                "BL": summary.get_bl(cib_data),
                "BLW": summary.get_blw(cib_data),
                "stay_order": summary.get_stay_order(cib_data)
            }
        self.remarks = summary.get_remarks(cib_data)