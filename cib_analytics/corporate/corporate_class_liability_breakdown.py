from .engine import liability_breakdown_engine

class CorporateLiabilityBreakdownClass:
    def __init__(self, cib_data):
        self.a = {
            "company or person": liability_breakdown_engine.company_or_person(cib_data),
            "A Overdraft CC  OD Cash Credit": liability_breakdown_engine.a_overdraft(cib_data),
            "Overdue EOL of A": liability_breakdown_engine.a_overdue(cib_data),
            "B Time Loan": liability_breakdown_engine.b_time_loan(cib_data),
            "Overdue EOL of B": liability_breakdown_engine.b_overdue(cib_data),
            "C LTR": liability_breakdown_engine.c_ltr(cib_data),
            "Overdue EOL of C": liability_breakdown_engine.c_overdue(cib_data),
            "D Other Non Instalment": liability_breakdown_engine.d_other_non_installment(cib_data),
            "Overdue EOL of D": liability_breakdown_engine.d_overdue(cib_data),
            "E Term Loan": liability_breakdown_engine.e_term_loan(cib_data),
            "EMI of E": liability_breakdown_engine.e_emi(cib_data),
            "Overdue EOL of E": liability_breakdown_engine.e_overdue(cib_data),
            "F Other Installment Loan": liability_breakdown_engine.f_other_installment_loan(cib_data),
            "EMI of F": liability_breakdown_engine.f_emi(cib_data),
            "Overdue EOL of F": liability_breakdown_engine.f_overdue(cib_data),
            "Total LC": liability_breakdown_engine.total_lc(cib_data),
            "Total indirect liability (non funded)": liability_breakdown_engine.total_indirect_liability(cib_data),
            "Total BG": liability_breakdown_engine.total_bg(cib_data)
        }