from json import load as load_json
from os.path import isfile
from .parsing_utils import parsing_helpers
from .parsing_utils import type_converters
from .parsing_utils.sanity_check import sanity_check

class cib_class:
    """
        A data class for containing cib report data in an easily usable format

        Methods Available
        -----------------
        cib_class.get_available_keys():
            Return all keys / fields of general CIB format present in loaded json

        cib_class.perform_sanity_check():
            Perform a sanity check to see if all data variables were loaded properly.
            Useful in identifying merged keys in json, that may not have raised errors while loading.


        Data variables
        --------------
        Field                                   variable name             return type
        -----                                   -------------             -----------
        Credit Information Bureau -
        Bangladesh Bank                         cib_header                <class 'pandas.core.frame.DataFrame'>
        INQUIRED                                inquired                  <class 'dict'>
        SUBJECT INFORMATION                     subject_info              <class 'dict'>
        ADDRESS                                 address                   <class 'pandas.core.frame.DataFrame'>
        OWNERS LIST                             owners_list               <class 'pandas.core.frame.DataFrame'>
        COMPANY(S) LIST                         company_list              <class 'pandas.core.frame.DataFrame'>
        LINKED PROPRIETORSHIP(S) LIST           linked_prop_list          <class 'list'>
        1. SUMMARY OF FACILITY(S) AS
           BORROWER & CO-BORROWER               summary_1                 <class 'dict'>
        1.(A) SUMMARY OF THE FUNDED FACILITIES
           AS BORROWER & CO-BORROWER            summary_1A                <class 'pandas.core.frame.DataFrame'>
        1.(B) SUMMARY OF THE NON-FUNDED
           FACILITIES AS BORROWER & CO-BORROWER summary_1B                <class 'pandas.core.frame.DataFrame'>
        2. SUMMARY OF FACILITY(S) AS GUARANTOR  summary_2                 <class 'dict'>
        2.(A) SUMMARY OF THE FUNDED FACILITIES
           AS GUARANTOR                         summary_2A                <class 'pandas.core.frame.DataFrame'>
        2.(B) SUMMARY OF THE NON-FUNDED
           FACILITIES AS GUARANTOR              summary_2B                <class 'pandas.core.frame.DataFrame'>
        REQUESTED CONTRACT DETAILS              req_contracts             <class 'pandas.core.frame.DataFrame'>
        DETAILS OF INSTALLMENT FACILITY(S)      installment_facility      <class 'list'>
        DETAILS OF CREDIT CARD FACILITY(S)      credit_card_facility      <class 'list'>
        DETAILS OF NONINSTALLMENT FACILITY(S)   noninstallment_facility   <class 'list'>
    """

    """
    take json file as input directly as a dictionary, NOT the path
    """
    def __init__(self, cib_raw : dict):
    #    assert isfile(path), 'File "'+path+'" does not exist'

    #    with open(path) as f:
    #        cib_raw = load_json(f)


        # keys that should be present in any given CIB report
        self.cib_header = parsing_helpers.parse_cib_header(
            cib_raw['Credit Information Bureau - Bangladesh Bank']
            )
        self.cib_header = type_converters.convert_cib_header(self.cib_header)

        self.inquired = parsing_helpers.handle_inquired(cib_raw['INQUIRED'])
        self.inquired = type_converters.convert_inquired(self.inquired)

        self.subject_info = parsing_helpers.raw_to_dict(cib_raw['SUBJECT INFORMATION'])
        self.subject_info = type_converters.convert_subject_info(self.subject_info)

        self.address = parsing_helpers.parse_address(cib_raw['ADDRESS'])

        self.summary_1 = parsing_helpers.raw_to_dict(
            cib_raw['1. SUMMARY OF FACILITY(S) AS BORROWER & CO-BORROWER']
            )
        self.summary_1 = type_converters.convert_summary_1_2(self.summary_1)

        self.summary_1A = parsing_helpers.parse_facility_table(
            cib_raw['1.(A) SUMMARY OF THE FUNDED FACILITIES AS BORROWER & CO-BORROWER']
            )
        self.summary_1A = type_converters.convert_facility_table(self.summary_1A)

        self.summary_1B = parsing_helpers.parse_facility_table(
            cib_raw['1.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS BORROWER & CO-BORROWER']
            )
        self.summary_1B = type_converters.convert_facility_table(self.summary_1B)

        self.summary_2 = parsing_helpers.raw_to_dict(
            cib_raw['2. SUMMARY OF FACILITY(S) AS GUARANTOR']
            )
        self.summary_2 = type_converters.convert_summary_1_2(self.summary_2)

        self.summary_2A = parsing_helpers.parse_facility_table(
            cib_raw['2.(A) SUMMARY OF THE FUNDED FACILITIES AS GUARANTOR']
            )
        self.summary_2A = type_converters.convert_facility_table(self.summary_2A)

        self.summary_2B = parsing_helpers.parse_facility_table(
            cib_raw['2.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS GUARANTOR']
            )
        self.summary_2B = type_converters.convert_facility_table(self.summary_2B)


        # keys that may or may not be present in a given CIB report
        if 'OWNERS LIST' in cib_raw.keys():
            self.owners_list = parsing_helpers.parse_owners_list(cib_raw['OWNERS LIST'])
        else:
            self.owners_list = None

        if 'COMPANY(S) LIST' in cib_raw.keys():
            self.company_list = parsing_helpers.parse_company_list(cib_raw['COMPANY(S) LIST'])
        else:
            self.company_list = None

        if 'LINKED PROPRIETORSHIP(S) LIST' in cib_raw.keys():
            self.linked_prop_list = parsing_helpers.handle_prop_list(cib_raw['LINKED PROPRIETORSHIP(S) LIST'])
        else:
            self.linked_prop_list = None

        if 'REQUESTED CONTRACT DETAILS' in cib_raw.keys():
            self.req_contracts = parsing_helpers.parse_req_contracts(cib_raw['REQUESTED CONTRACT DETAILS'])
            self.req_contracts = type_converters.convert_req_contracts(self.req_contracts)
        else:
            self.req_contracts = None

        if 'DETAILS OF INSTALLMENT FACILITY(S)' in cib_raw.keys():
            self.installment_facility = parsing_helpers.handle_contract_facility(
                cib_raw['DETAILS OF INSTALLMENT FACILITY(S)']
                )
            self.installment_facility = type_converters.convert_installment_facility(self.installment_facility)
        else:
            self.installment_facility = None

        if 'DETAILS OF NONINSTALLMENT FACILITY(S)' in cib_raw.keys():
            self.noninstallment_facility = parsing_helpers.handle_contract_facility(
                cib_raw['DETAILS OF NONINSTALLMENT FACILITY(S)']
                )
            self.noninstallment_facility = type_converters.convert_installment_facility(self.noninstallment_facility)
        else:
            self.noninstallment_facility = None

        if 'DETAILS OF CREDIT CARD FACILITY(S)' in cib_raw.keys():
            self.credit_card_facility = parsing_helpers.handle_contract_facility(
                cib_raw['DETAILS OF CREDIT CARD FACILITY(S)']
                )
            self.credit_card_facility = type_converters.convert_credit_card_facility(self.credit_card_facility)
        else:
            self.credit_card_facility = None

        self.file_name = cib_raw.get('fileName')



    def get_UC_or_STD(self):
        """
        Return 'UC' or 'STD' based on which terminology is used in CIB
        """
        if "UC_Amount" in self.summary_1A.columns:
            return "UC"
        else:
            return "STD"



    def get_available_keys(self):
        """
        Return all keys / fields of general CIB format present in loaded json
        """
        return [k for k,v in self.__dict__.items() if not v is None]



    def perform_sanity_check(self):
        """
        Perform a sanity check to see if all data variables were loaded properly.
        Useful in identifying merged keys in json, that may not have raised errors while loading.
        """
        sanity_check(self)
