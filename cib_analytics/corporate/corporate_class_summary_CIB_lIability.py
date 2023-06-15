from .engine import summary_engine

class corporate_class_summary_CIB_liability:
    def __init__(self, cib_data):
        self.concerns_with_pbl = {
            "funded": {
                "installment": summary_engine.funded_installment(cib_data),
                "no_installment": summary_engine.funded_no_installment(cib_data),
                "total": summary_engine.funded_total(cib_data)
            },
            "non_funded": summary_engine.non_funded_total(cib_data),
            "total": summary_engine.total(cib_data),
            "overdue": summary_engine.get_overdue(cib_data),
            "cl_status": summary_engine.get_cl_status(cib_data),
            "default": summary_engine.get_default(cib_data),
            "loan_amount": {
                "STD": summary_engine.get_std(cib_data),
                "SMA": summary_engine.get_sma(cib_data),
                "SS": summary_engine.get_ss(cib_data),
                "DF": summary_engine.get_df(cib_data),
                "BL": summary_engine.get_bl(cib_data),
                "BLW": summary_engine.get_blw(cib_data),
                "stay_order": summary_engine.get_stay_order(cib_data)
            },
            "remarks": summary_engine.get_remarks(cib_data)
        }