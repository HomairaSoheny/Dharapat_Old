from .engine import liability_breakdown

class LiabilityBreakdown:
    def __init__(self, cib_list):
        self.response = {
            "A Overdraft CC  OD Cash Credit": liability_breakdown.a_overdraft(cib_list),
            "Overdue EOL of A": liability_breakdown.a_overdue(cib_list),
            "B Time Loan": liability_breakdown.b_time_loan(cib_list),
            "Overdue EOL of B": liability_breakdown.b_overdue(cib_list),
            "C LTR": liability_breakdown.c_ltr(cib_list),
            "Overdue EOL of C": liability_breakdown.c_overdue(cib_list),
            "D Other Non Instalment": liability_breakdown.d_other_non_installment(cib_list),
            "Overdue EOL of D": liability_breakdown.d_overdue(cib_list),
            "E Term Loan": liability_breakdown.e_term_loan(cib_list),
            "EMI of E": liability_breakdown.e_emi(cib_list),
            "Overdue EOL of E": liability_breakdown.e_overdue(cib_list),
            "F Other Installment Loan": liability_breakdown.f_other_installment_loan(cib_list),
            "EMI of F": liability_breakdown.f_emi(cib_list),
            "Overdue EOL of F": liability_breakdown.f_overdue(cib_list),
            "Total LC": liability_breakdown.total_lc(cib_list),
            "Total indirect liability (non funded)": liability_breakdown.total_indirect_liability(cib_list),
            "Total BG": liability_breakdown.total_bg(cib_list)
        }