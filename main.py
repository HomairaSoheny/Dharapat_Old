import traceback
import pika
import sys
import os
import json
from utils.parsing_utils.data_preparation import process_response
from dashboard.consumer import getConsumerDashboard

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "report.settings")

import django
django.setup()


def main():
    #development_server
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-temp1.centralindia.azurecontainer.io', heartbeat=400))
    #production
    #connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-0.rabbitmq.rabbits.svc.cluster.local', heartbeat=400))
    
    channel = connection.channel()
    channel.queue_declare(queue='prime_bank_cib_response')

    def callback(ch, method, properties, body):
        try:
            metadata, req_cib, group_cib_list, error_messages = process_response(body)
            if error_messages != "":
                final = dict([
                    ('message', error_messages),
                    ('success', False),
                    ('metaData', metadata)
                ])
                print("Error")

                channel1 = connection.channel()
                channel1.queue_declare(queue='prime_bank_cib_extracted_download', durable=True)
                channel1.basic_publish(exchange='', routing_key='prime_bank_cib_extracted_download', body=json.dumps(final))

            else:
                cibs = []
                cibs.append(req_cib)

                for each in group_cib_list:
                    cibs.append(each)

                final = {}
                scorecard = []
                final['metaData'] = metadata
                # dashboard_data = get_corporate_dashboard(cib_list) if metadata['cibType'] == 'corporate' else getConsumerDashboard(cib_list)
                dashboard_data = getConsumerDashboard(cibs)
                final['score'] = scorecard
                final['dashboard'] = dashboard_data
                final['message'] = 'Ok'
                final['success'] = True
            channel1 = connection.channel()
            channel1.queue_declare(queue="prime_bank_cib_extracted_download", durable=True)
            channel1.basic_publish(exchange='', routing_key="prime_bank_cib_extracted_download", body=json.dumps(final))
            print("Analysis Report Sent")

        except Exception as exc:
            print(type(exc))
            traceback.print_exc()

            try:
                raw_json = json.loads(body, strict=False)
                metadata = raw_json['metaData']
            except:
                metadata = []
                
            final = dict([
                ('message', 'Analysis Error Found'),
                ('success', False),
                ('metaData', metadata)
            ])
            print("Exception Message: {}".format(exc))
            channel1 = connection.channel()
            channel1.queue_declare(queue='prime_bank_cib_extracted_download', durable=True)
            channel1.basic_publish(exchange='', routing_key='prime_bank_cib_extracted_download', body=json.dumps(final))

    print('[LOG] message received')

    channel.basic_consume(queue='prime_bank_cib_response', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        print("[LOG] running rabbitmq main")
        main()
        print("[LOG] success")
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
