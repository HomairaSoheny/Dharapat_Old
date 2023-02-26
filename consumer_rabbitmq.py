import pika, sys, os, json
from cib_analytics.api_generation.generate_full_response import generate_full_response

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-temp1.centralindia.azurecontainer.io'))
    channel = connection.channel()
    
    channel.queue_declare(queue='response')
    
    def callback(ch, method, properties, body):
        print(f"received new message: {body}")
        channel.basic_publish(exchange='', routing_key='cib_analysis_report', body=json.dumps(generate_full_response()))
    
    channel.basic_consume(queue='response', auto_ack=True, on_message_callback=callback)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        print("main")
        main()
        print("done")
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)