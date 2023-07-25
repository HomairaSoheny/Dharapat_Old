from .consumer_dashboard import get_consumer_dashboard
from .corporate_dashboard import get_corporate_dashboard

def generate_full_response(cib_list, cib_type):
    response = []
    if cib_type == 'corporate':
        for cib in cib_list:
            response.append(get_corporate_dashboard(cib))
    else:
        for cib in cib_list:
            response.append(get_consumer_dashboard(cib))
            
    return response