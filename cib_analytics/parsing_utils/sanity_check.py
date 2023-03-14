import pandas as pd

def sanity_check(cib_obj):
    # keys that should be present in any given CIB report
    #INQUIRED
    assert len(cib_obj.inquired)  in (1,5,9,13), 'Expecting INQUIRED shape 1, 5, 9 or 13, got shape: '+str(len(cib_obj.inquired))

    #SUBJECT INFORMATION
    assert len(cib_obj.subject_info)  in (10, 13, 20), 'Expecting SUBJECT INFORMATION shape 10, 13 or 20, got shape: '+str(len(cib_obj.subject_info))

    #ADDRESS
    assert cib_obj.address.shape[1]==5, 'Expecting 5 columns in ADDRESS, got shape: '+str(cib_obj.address.shape)

    #1. SUMMARY OF FACILITY(S) AS BORROWER & CO-BORROWER
    assert len(cib_obj.summary_1)==6, 'Expecting 1. SUMMARY OF FACILITY(S) AS BORROWER & CO-BORROWER shape 6, got shape: '+str(len(cib_obj.summary_1))

    #1.(A) SUMMARY OF THE FUNDED FACILITIES AS BORROWER & CO-BORROWER
    assert cib_obj.summary_1A.shape==(4,19), 'Expecting 1.(A) SUMMARY OF THE FUNDED FACILITIES AS BORROWER & CO-BORROWER shape (4,19), got shape: '+str(cib_obj.summary_1A.shape)

    #1.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS BORROWER & CO-BORROWER
    assert cib_obj.summary_1B.shape==(4,9), 'Expecting 1.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS BORROWER & CO-BORROWER shape (4,9), got shape: '+str(cib_obj.summary_1B.shape)

    #2. SUMMARY OF FACILITY(S) AS GUARANTOR
    assert len(cib_obj.summary_2)==6, 'Expecting 2. SUMMARY OF FACILITY(S) AS GUARANTOR shape 6, got shape: '+str(len(cib_obj.summary_2))

    #2.(A) SUMMARY OF THE FUNDED FACILITIES AS GUARANTOR
    assert cib_obj.summary_2A.shape==(4,19), 'Expecting 2.(A) SUMMARY OF THE FUNDED FACILITIES AS GUARANTOR shape (4,19), got shape: '+str(cib_obj.summary_2A.shape)

    #2.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS GUARANTOR
    assert cib_obj.summary_2B.shape==(4,9), 'Expecting 2.(B) SUMMARY OF THE NON-FUNDED FACILITIES AS GUARANTOR shape (4,9), got shape: '+str(cib_obj.summary_2B.shape)



    # keys that may or may not be present in a given CIB report
    #OWNERS LIST
    if not type(cib_obj.owners_list) == type(None):
        assert cib_obj.owners_list.shape[1]==4, 'Expecting 4 columns in OWNERS LIST, got shape: '+str(cib_obj.owners_list.shape)

    #COMPANY(S) LIST
    if not type(cib_obj.company_list) == type(None):
        assert cib_obj.company_list.shape[1]==6, 'Expecting 6 columns in COMPANY(S) LIST, got shape: '+str(cib_obj.company_list.shape)

    #LINKED PROPRIETORSHIP(S) LIST
    if not type(cib_obj.linked_prop_list) == type(None):
        for i, prop in enumerate(cib_obj.linked_prop_list):
            assert len(prop['PROPRIETORSHIP CONCERN'])==6, 'Expecting shape 6 in LINKED PROPRIETORSHIP(S) LIST table '+str(i)+', got shape: '+str(len(prop['PROPRIETORSHIP CONCERN']))
            assert prop['ADDRESS'].shape[1]==5, 'Expecting 5 columns in LINKED PROPRIETORSHIP(S) LIST address '+str(i)+', got shape: '+str(prop['ADDRESS'].shape)

    #REQUESTED CONTRACT DETAILS
    if not type(cib_obj.req_contracts) == type(None):
        assert cib_obj.req_contracts.shape[1]==12, 'Expecting 12 columns in REQUESTED CONTRACT DETAILS, got shape: '+str(cib_obj.req_contracts.shape)

    #DETAILS OF INSTALLMENT FACILITY(S)
    if not type(cib_obj.installment_facility) == type(None):
        for i, fac in enumerate(cib_obj.installment_facility):
            assert len(fac['Ref'])==30, 'Expecting 30 keys in INSTALLMENT FACILITY '+str(i)+', got shape: '+str(len(fac['Ref']))
            if type(fac['Contract History']) == pd.DataFrame:
                assert fac['Contract History'].shape[1]==6, 'Expecting 6 columns in INSTALLMENT FACILITY '+str(i)+' Contract History, got shape: '+str(fac['Contract History'].shape)
            else:
                assert type(fac['Contract History'])==dict, f'INSTALLMENT FACILITY {i}, type not recognized'
            if not type(fac['Other subjects linked to the same contract']) == type(None):
                assert fac['Other subjects linked to the same contract'].shape[1]==3, 'Expecting 3 columns in INSTALLMENT FACILITY '+str(i)+' Other subjects linked to the same contract, got shape:'+str(fac['Other subjects linked to the same contract'].shape)

    #DETAILS OF NONINSTALLMENT FACILITY(S)
    if not type(cib_obj.noninstallment_facility) == type(None):
        for i, fac in enumerate(cib_obj.noninstallment_facility):
            assert len(fac['Ref'])==23, 'Expecting 23 keys in NONINSTALLMENT FACILITY '+str(i)+', got shape: '+str(len(fac['Ref']))
            if type(fac['Contract History']) == pd.DataFrame:
                assert fac['Contract History'].shape[1]==6, 'Expecting 6 columns in NONINSTALLMENT FACILITY '+str(i)+' Contract History, got shape: '+str(fac['Contract History'].shape)
            else:
                assert type(fac['Contract History'])==dict, f'NONINSTALLMENT FACILITY {i}, type not recognized'
            if not type(fac['Other subjects linked to the same contract']) == type(None):
                assert fac['Other subjects linked to the same contract'].shape[1]==3, 'Expecting 3 columns in NONINSTALLMENT FACILITY '+str(i)+' Other subjects linked to the same contract, got shape:'+str(fac['Other subjects linked to the same contract'].shape)

    #DETAILS OF DETAILS OF CREDIT CARD FACILITY(S)
    if not type(cib_obj.credit_card_facility) == type(None):
        for i, fac in enumerate(cib_obj.credit_card_facility):
            assert len(fac['Ref'])==25, 'Expecting 25 keys in CREDIT CARD FACILITY '+str(i)+', got shape: '+str(len(fac['Ref']))
            if type(fac['Contract History']) == pd.DataFrame:
                assert fac['Contract History'].shape[1]==7, 'Expecting 7 columns in CREDIT CARD FACILITY '+str(i)+' Contract History, got shape: '+str(fac['Contract History'].shape)
            else:
                assert type(fac['Contract History'])==dict, f'CREDIT CARD FACILITY {i}, type not recognized'