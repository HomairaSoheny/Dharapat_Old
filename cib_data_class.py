from datetime import datetime

import numpy as np
import pandas as pd

from utils.parsing_utils import parsing_helpers
from utils.parsing_utils import type_converters
from utils.parsing_utils.sanity_check import sanityCheck

class CIB:

    def __init__(self, json_obj):
        self.cib_raw = json_obj
        # keys that should be present in any given CIB report
        try:
            self.pdf_name = self.cib_raw["fileName"]
            self.cib_id = self.cib_raw["id"]
            self.cib_category = self.cib_raw["catagory"]
        except:
            self.pdf_name = "fileName"
            self.cib_id = "id"
            self.cib_category = str(np.random.choice(["Type a", "Type b", "Type c", "Type d", "Type e", "Type f", "Type g", "Type h", "Type i", "Type j", "Type k"]))
        try:
            self.cib_header = parsing_helpers.parse_cib_header(self.cib_raw['Credit Information Bureau - Bangladesh Bank'])
        except:
            self.cib_header = parsing_helpers.parse_cib_header(self.cib_raw['Credit Information Report'])
        self.cib_header = type_converters.convert_cib_header(self.cib_header)

        self.inquired = parsing_helpers.handle_inquired(self.cib_raw['INQUIRED'])
        self.inquired = type_converters.convert_inquired(self.inquired)

        #self.subject_info = parsing_helpers.raw_to_dict(self.cib_raw['SUBJECT INFORMATION'])
        #self.subject_info = type_converters.convert_subject_info(self.subject_info)

        if 'SUBJECT INFORMATION' in self.cib_raw:
            self.subject_info = parsing_helpers.raw_to_dict(self.cib_raw['SUBJECT INFORMATION'])
            self.subject_info = type_converters.convert_subject_info(self.subject_info)
            
        #else:
        #    print(f"Warning: 'SUBJECT INFORMATION' is missing for CIB ID: {self.cib_id}")
        #    self.subject_info = {"message": "No subject information available"}


        self.address=pd.DataFrame()
        if 'ADDRESS' in self.cib_raw.keys():
            self.address = parsing_helpers.parse_address(self.cib_raw['ADDRESS'])

        self.summary_1 = {}
        if '1. SUMMARY OF FACILITY(S) AS BORROWER & CO-BORROWER' in self.cib_raw.keys():
            self.summary_1 = parsing_helpers.raw_to_dict(self.cib_raw['1. SUMMARY OF FACILITY(S) AS BORROWER & CO-BORROWER'])
            self.summary_1 = type_converters.convert_summary_1_2(self.summary_1)

        self.summary_1A = pd.DataFrame()
        if '1.(A) SUMMARY OF THE FUNDED FACILITIES AS BORROWER & CO-BORROWER' in self.cib_raw.keys():
            if pd.to_datetime(self.cib_header['Date of Inquiry']).dt.date[0] < pd.to_datetime('2024-06-15').date():
                self.summary_1A = parsing_helpers.parse_facility_table(self.cib_raw['1.(A) SUMMARY OF THE FUNDED FACILITIES AS BORROWER & CO-BORROWER'])
            else:
                self.summary_1A = parsing_helpers.parse_facility_table_new(self.cib_raw['1.(A) SUMMARY OF THE FUNDED FACILITIES AS BORROWER & CO-BORROWER'])
        # self.summary_1A = type_converters.convert_facility_table(self.summary_1A)
        self.summary_1B = pd.DataFrame()
        if '1.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS BORROWER & CO-BORROWER' in self.cib_raw.keys():
            self.summary_1B = parsing_helpers.parse_facility_table_B(self.cib_raw['1.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS BORROWER & CO-BORROWER'])
            self.summary_1B = type_converters.convert_facility_table(self.summary_1B)

        self.summary_2 = {}
        if '2. SUMMARY OF FACILITY(S) AS GUARANTOR' in self.cib_raw.keys():
            self.summary_2 = parsing_helpers.raw_to_dict(self.cib_raw['2. SUMMARY OF FACILITY(S) AS GUARANTOR'])
            self.summary_2 = type_converters.convert_summary_1_2(self.summary_2)

        self.summary_2A = pd.DataFrame()
        if '2.(A) SUMMARY OF THE FUNDED FACILITIES AS GUARANTOR' in self.cib_raw.keys():
            if pd.to_datetime(self.cib_header['Date of Inquiry']).dt.date[0] < pd.to_datetime('2024-06-15').date():
                self.summary_2A = parsing_helpers.parse_facility_table(self.cib_raw['2.(A) SUMMARY OF THE FUNDED FACILITIES AS GUARANTOR'])
            # self.summary_2A = type_converters.convert_facility_table(self.summary_2A)
            else:
                self.summary_2A = parsing_helpers.parse_facility_table_new(self.cib_raw['2.(A) SUMMARY OF THE FUNDED FACILITIES AS GUARANTOR'])

        self.summary_2B = pd.DataFrame()
        if '2.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS GUARANTOR' in self.cib_raw.keys():
            self.summary_2B = parsing_helpers.parse_facility_table_B(self.cib_raw['2.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS GUARANTOR'])
            self.summary_2B = type_converters.convert_facility_table(self.summary_2B)

        #keys that will come from metadata
        self.id = ""
        self.file_name = ""
        if 'id' in self.cib_raw.keys():
            self.id = self.cib_raw['id']
        if 'fileName' in self.cib_raw.keys():
            self.file_name = self.cib_raw['fileName']
        # keys that may or may not be present in a given CIB report
        if 'OWNERS LIST' in self.cib_raw.keys():
            self.owners_list = parsing_helpers.parse_owners_list(self.cib_raw['OWNERS LIST'])
        else:
            self.owners_list = None

        if 'COMPANY(S) LIST' in self.cib_raw.keys():
            self.company_list = parsing_helpers.parse_company_list(self.cib_raw['COMPANY(S) LIST'])
        else:
            self.company_list = None

        if 'LINKED PROPRIETORSHIP(S) LIST' in self.cib_raw.keys():
            self.linked_prop_list = parsing_helpers.handle_prop_list(self.cib_raw['LINKED PROPRIETORSHIP(S) LIST'])
        else:
            self.linked_prop_list = None

        if 'REQUESTED CONTRACT DETAILS' in self.cib_raw.keys():
            self.req_contracts = parsing_helpers.parse_req_contracts(self.cib_raw['REQUESTED CONTRACT DETAILS'])
            self.req_contracts = type_converters.convert_req_contracts(self.req_contracts)
        else:
            self.req_contracts = None
        
        if 'DETAILS OF INSTALLMENT FACILITY(S)' in self.cib_raw.keys():
            self.installment_facility = parsing_helpers.handle_contract_facility(self.cib_raw['DETAILS OF INSTALLMENT FACILITY(S)'])
            self.installment_facility = type_converters.convert_installment_facility(self.installment_facility)
        else:
            self.installment_facility = None
        if 'DETAILS OF NONINSTALLMENT FACILITY(S)' in self.cib_raw.keys():
            self.noninstallment_facility = parsing_helpers.handle_contract_facility(self.cib_raw['DETAILS OF NONINSTALLMENT FACILITY(S)'])
            self.noninstallment_facility = type_converters.convert_installment_facility(self.noninstallment_facility)
        else:
            self.noninstallment_facility = None

        if 'DETAILS OF CREDIT CARD FACILITY(S)' in self.cib_raw.keys():
            self.credit_card_facility = parsing_helpers.handle_contract_facility(self.cib_raw['DETAILS OF CREDIT CARD FACILITY(S)'])
            self.credit_card_facility = type_converters.convert_credit_card_facility(self.credit_card_facility)
        else:
            self.credit_card_facility = None


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
        return list(self.cib_raw.keys()).copy()



    def perform_sanity_check(self):
        """
        Perform a sanity check to see if all data variables were loaded properly.
        Useful in identifying merged keys in json, that may not have raised errors while loading.
        """
        sanityCheck(self)



        
