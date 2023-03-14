import json
import time
from ..cib_data_class import cib_class

def process_response(body):
    raw_json = json.loads(body)
    metadata = raw_json['metaData']
    default_cib = metadata['defaultCib']
    error_message = ''
    a = []
    if 'success' not in raw_json.keys():
        raw_json['success'] = True
    if raw_json['success'] == False:
        files =  ", ".join([str(elem) for elem in raw_json['Falied_files']])
        error_message = "Can not able to parse pdf file. File Name - {}. Please try to run the analysis again by excluding the mentioned files.".format(files)
        req_cib = []
        return metadata,req_cib,a,error_message
    a = []
    for k,v in raw_json.items():
        if k == 'cibs':
            cib_list = raw_json[k]
    total_time = 0
    for each in cib_list:
        if  each['id'] == default_cib:
            start = time.time()
            req_cib = cib_class(each)
            total_time+=(time.time())-start
            print("cib processed in : {}".format((time.time())-start))
        else:
            start = time.time()
            a.append(cib_class(each))
            total_time+=(time.time())-start
            print("cib processed in : {}".format((time.time())-start))
    print('total time for cib processing: {}'.format(total_time))
    return metadata,req_cib,a, error_message