from .engine import liability_breakdown_engine

class CorporateLiabilityBreakdownClass:
    def __init__(self, cib_list):
        self.response = {
            "A xOverdraft CC  OD Cash Credit": liability_breakdown_engine.a_overdraft(cib_list),
            "Overdue EOL of A": liability_breakdown_engine.a_overdue(cib_list),
            "B Time Loan": liability_breakdown_engine.b_time_loan(cib_list),
            "Overdue EOL of B": liability_breakdown_engine.b_overdue(cib_list),
            "C LTR": liability_breakdown_engine.c_ltr(cib_list),
            "Overdue EOL of C": liability_breakdown_engine.c_overdue(cib_list),
            "D Other Non Instalment": liability_breakdown_engine.d_other_non_installment(cib_list),
            "Overdue EOL of D": liability_breakdown_engine.d_overdue(cib_list),
            "E Term Loan": liability_breakdown_engine.e_term_loan(cib_list),
            "EMI of E": liability_breakdown_engine.e_emi(cib_list),
            "Overdue EOL of E": liability_breakdown_engine.e_overdue(cib_list),
            "F Other Installment Loan": liability_breakdown_engine.f_other_installment_loan(cib_list),
            "EMI of F": liability_breakdown_engine.f_emi(cib_list),
            "Overdue EOL of F": liability_breakdown_engine.f_overdue(cib_list),
            "Total LC": liability_breakdown_engine.total_lc(cib_list),
            "Total indirect liability (non funded)": liability_breakdown_engine.total_indirect_liability(cib_list),
            "Total BG": liability_breakdown_engine.total_bg(cib_list)
        }