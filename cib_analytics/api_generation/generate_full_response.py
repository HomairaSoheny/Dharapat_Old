from .consumer_dashboard import get_consumer_dashboard

def generate_full_response():
    
    response = []
    response.append(get_consumer_dashboard())
    
    return response