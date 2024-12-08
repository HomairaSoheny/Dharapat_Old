import pandas as pd


def rem_colon(s: str):
    if s=='':
        return s
    if s[-1] == ':':
        return s[:-1]
    else:
        return s

def raw_to_dict(raw_list: list):
    dict_form = {}
    for i in raw_list[1:]:
        if i[0].strip() == '' and i[1].strip() == '':
            pass
        else:
            dict_form[rem_colon(i[0].strip())] =  i[1].strip()
        if i[2].strip() == '' and i[3].strip() == '':
            pass
        else:
            dict_form[rem_colon(i[2].strip())] =  i[3].strip()
    return dict_form

def parse_cib_header(raw_list : list):
    return pd.DataFrame(raw_list[2:], columns=raw_list[1])

def handle_inquired(raw_list: list):
    if len(raw_list[1])==1: #check case 'Subject code:XXXXXXXXXX'
        k,v = raw_list[1][0].split(':')
        return {k:v}
    else:
        try:
          return raw_to_dict(raw_list)
        except:
            response_dict = {}
            for lst in raw_list:
                for row in lst:
                    if ":" in row:
                        response_dict[row.split(":")[0]] = row.split(":")[1]
            return response_dict
                        

def parse_address(raw_list:list):
    return pd.DataFrame(raw_list[2:], columns=raw_list[1])

def parse_company_list(raw_list:list):
    return pd.DataFrame(raw_list[2:], columns=raw_list[1])

def parse_owners_list(raw_list:list):
    return pd.DataFrame(raw_list[2:], columns=raw_list[1])

def parse_prop_concern(raw_list: list):
    dict_form = {}
    for i in raw_list[1:]:
        dict_form[i[0]] = i[1]
        dict_form[i[2]] = i[3]
        dict_form[i[4]] = i[5]

    return dict_form

def parse_prop_address(raw_list:list):
    return pd.DataFrame(raw_list[2:], columns=raw_list[1])

def handle_prop_list(raw_list:list):
    """
    Parameters
    ----------
    raw_list: list
        The value of parsed_json['LINKED PROPRIETORSHIP(S) LIST']

    Returns
    -------
    A list of dictionaries
    Each dictionary contains one proprietorship concern
    with keys ['PROPRIETORSHIP CONCERN'] and ['ADDRESS']

        Type
        ----
        'PROPRIETORSHIP CONCERN' : dictionary
        'ADDRESS' : pandas.DataFrame

    """
    prop_list = []
    for prop in raw_list:
        prop_list.append({'PROPRIETORSHIP CONCERN' : parse_prop_concern(prop['PROPRIETORSHIP CONCERN']),
                          'ADDRESS' : parse_prop_address(prop['ADDRESS'])})

    return prop_list

def parse_facility_table(raw_list:list):
    df = pd.DataFrame(raw_list[3:], columns=raw_list[2]+[' '])
    temp_cols = df.columns.tolist()
    for i, header in enumerate(temp_cols):
        if header.strip()=='':
            col_name = temp_cols[i-1]
            temp_cols[i-1] = col_name+'_No.'
            temp_cols[i] = col_name+'_Amount'
    df.columns = temp_cols
    df = df[1:]
    return df

def parse_facility_table_new(raw_list:list):
    header1 = [h.strip() for h in raw_list[2] if len(h.strip()) > 1]

    columns = []
    columns.append(header1[0])

    for category in header1[1:]:
        columns.append(category + "_No.")
        columns.append(category + "_Amount")

    data_rows = raw_list[4:]
    df = pd.DataFrame(data_rows, columns=columns)
    df_melted = df.melt(id_vars=['Contract Category'], var_name='Product_Measure', value_name='Value')

    df_melted['Product_Measure'] = df_melted['Product_Measure'].str.replace('.', '', regex=False)
    df_melted[['Product', 'Measure']] = df_melted['Product_Measure'].str.rsplit('_', n=1, expand=True)
    df_melted['Contract_Category_Clean'] = df_melted['Contract Category'].str.replace(r'[^\w\s]', '', regex=True)
    df_melted['Contract_Category_Clean'] = df_melted['Contract_Category_Clean'].str.replace(' ', '_')
    df_melted['Product'] = df_melted['Product'].str.replace(' ', '_')

    df_melted['Contract_Measure'] = df_melted['Contract_Category_Clean'] + '_' + df_melted['Measure']
    df_melted['Value'] = df_melted['Value'].replace({',': ''}, regex=True)
    df_melted['Value'] = pd.to_numeric(df_melted['Value'], errors='coerce')

    # Pivot the DataFrame
    df_pivot = df_melted.pivot_table(
        index='Product',
        columns='Contract_Measure',
        values='Value',
        aggfunc='first'
    )

    df_pivot.columns = df_pivot.columns.get_level_values(0)
    df_pivot = df_pivot.reset_index()

    desired_products = ['Installments', 'Non-Installments', 'Credit_Cards', 'Total']
    df_pivot = df_pivot[df_pivot['Product'].isin(desired_products)]

    return df_pivot

def parse_facility_table_B(raw_list:list):
    df = pd.DataFrame(raw_list[3:], columns=raw_list[2]+[' '])
    temp_cols = df.columns.tolist()
    for i, header in enumerate(temp_cols):
        if header.strip()=='':
            col_name = temp_cols[i-1]
            temp_cols[i-1] = col_name+'_No.'
            temp_cols[i] = col_name+'_Amount'
    df.columns = temp_cols
    df = df[1:]
    return df

def parse_req_contracts(raw_list:list):
    return pd.DataFrame(raw_list[2:], columns=raw_list[1])

def identify_header_col_idx(raw_table : list):
    for e, row in enumerate(raw_table):
        if ('Date' in row) or ('Outstanding' in row) or ('Overdue' in row): # checking for one of first 3 expected columns for header row
            return e
    
    raise ValueError(f'No header columns could be found: \n{raw_table}')

def parse_contract_history(table:list):
    """
    Returns
    -------
    Case-1: If there is a Stay Order, returns a dictionary with a single key
    'Stay Order' and the Stay Order note as the value
    Case-2: Returns the table of the contract history
        Type
        ----
        Case-1: dict
        Case-2: pandas.DataFrame
    """
    if (len(table[-1])==3 or len(table[-1])==2) and table[-1][0].strip()=='Stay Order:':
        return {rem_colon(table[-1][0].strip()) : table[-1][1]}

    header_col_idx = identify_header_col_idx(raw_table=table)
    return pd.DataFrame(table[header_col_idx + 1: ], columns=table[header_col_idx])

def parse_other_subjects_linked(table:list):
    if len(table) <= 1:
        return None

    return pd.DataFrame(table[2:], columns=table[1])

def parse_contract_facility_info(list_input : list):
    parsed_dict = {}
    for k, v in zip(list_input[0], list_input[1]):
        parsed_dict[k] = v
    parsed_dict.update(raw_to_dict(list_input[1:]))

    return parsed_dict

def handle_contract_facility(raw_list:list):
    """
    Parameters
    ----------
    raw_list: list
        Expecting input keys:
            -> 'DETAILS OF INSTALLMENT FACILITY(S)'
            -> 'DETAILS OF NONINSTALLMENT FACILITY(S)'
            -> 'DETAILS OF CREDIT CARD FACILITY(S)'

    Returns
    -------
    A list of dictionaries
    Each dictionary contains one contract facility
    with keys ['Ref'], ['Other subjects linked to the same contract']
          and ['Contract History']

        Type
        ----
        'Ref' : dictionary
        'Other subjects linked to the same contract' : pandas.DataFrame
        'Contract History' : pandas.DataFrame

    """
    facility_list = []
    for i, fac in enumerate(raw_list):
        facility = {}
        if i==0:
            facility['Ref'] = parse_contract_facility_info(raw_list[i]['Ref'][1:])
        else:
            facility['Ref'] = parse_contract_facility_info(raw_list[i]['Ref'][:])

        facility['Other subjects linked to the same contract'] = parse_other_subjects_linked(
                                    raw_list[i]['Other subjects linked to the same contract'])

        facility['Contract History'] = parse_contract_history(raw_list[i]['Contract History'])


        facility_list.append(facility)

    return facility_list


