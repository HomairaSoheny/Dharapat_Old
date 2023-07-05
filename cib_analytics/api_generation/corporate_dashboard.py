from ..corporate.corporate_class_liability_breakdown import corporate_class_liability_breakdown
from ..corporate.corporate_class_summary_CIB_lIability import corporate_class_summary_CIB_liability

def summary_of_cib_liability(cib):
    try:
        summary = corporate_class_summary_CIB_liability(cib)
        return {
            "funded": summary.funded,
            "non_funded": summary.non_funded,
            "total": summary.total,
            "overdue": summary.overdue,
            "cl status": summary.cl_status,
            "default": summary.default,
            "loan amount": summary.loan_amount,
            "remarks": summary.remarks
        }
    except Exception as exc:
        print("Error on consumer table 2")
        print(exc)
        return {}

def liability_type_wise_breakup(cib):
    return cib

def get_corporate_dashboard(cib):
    corporate_response = {
        "summary of cib liability": summary_of_cib_liability(cib),
        "liability type wise break up": liability_type_wise_breakup(cib)
    }
    
    return corporate_response