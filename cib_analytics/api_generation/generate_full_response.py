from .consumer_dashboard import get_consumer_dashboard
from .sme_dashboard import get_sme_dashboard

def generate_full_response(cib_list, cib_type):
    response = []
    if cib_type == 'corporate':
        for cib in cib_list:
            response.append(get_sme_dashboard())
    else:
        for cib in cib_list:
            response.append(get_consumer_dashboard(cib))
    return response