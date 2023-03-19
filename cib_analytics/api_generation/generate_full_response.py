from .consumer_dashboard import get_consumer_dashboard

def generate_full_response(cib_list):
    response = []
    for cib in cib_list:
        response.append(get_consumer_dashboard(cib))
    return response