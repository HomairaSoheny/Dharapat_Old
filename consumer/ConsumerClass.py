from consumer.engine import consumer_engine

class Consumer:
    def __init__(self, cib_data):
        self.borrowers_name = consumer_engine.getBorrowersName(cib_data)
        self.facility_type = consumer_engine.getFacilityType(cib_data)
        self.sanctioned_limit = consumer_engine.getSanctionedLimit(cib_data)
        self.facility_start_date = consumer_engine.getFacilityStartDate(cib_data)
        self.loan_expiry_date = consumer_engine.getLoanExpiryDate(cib_data)
        self.outstanding = consumer_engine.getOutstanding(cib_data)
        self.emi = consumer_engine.getEMI(cib_data)
        self.total_emi = consumer_engine.getTotalEMI(cib_data)
        self.remaining_emi = consumer_engine.getRemainingEMI(cib_data)
        self.avg_outstandint_last_12_months = consumer_engine.getAvgOutstandingLast12Months(cib_data)
        self.overdue = consumer_engine.getOverdue(cib_data)
        self.current_cl_status = consumer_engine.getCurrentCLStatus(cib_data)
        self.percent_of_credit_card_limit_outstanding = consumer_engine.percentOfCreditCardLimit12Outstanding(cib_data)
        self.worst_cl_status_in_last_12_months = consumer_engine.getWorstCLStatusInLast12Months(cib_data)
        self.current_NPI = consumer_engine.getCurrentNPI(cib_data)
        self.no_of_NPI_in_last_3_months = consumer_engine.getNoOfNPI(cib_data, 3)
        self.no_of_NPI_in_last_6_months = consumer_engine.getNoOfNPI(cib_data, 6)
        self.no_of_NPI_in_last_12_months = consumer_engine.getNoOfNPI(cib_data, 12)

    def __repr__(self):
        return '\n'.join([(str(k)+' : '+str(v)) for k,v in self.__dict__.items() if k!='config'])