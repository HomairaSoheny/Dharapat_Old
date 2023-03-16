import traceback
import pika, sys, os, json
from cib_analytics.parsing_utils.data_preparation import process_response
from cib_analytics.api_generation.generate_full_response import generate_full_response

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-temp1.centralindia.azurecontainer.io', heartbeat=400))
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
                print(final)
                
                channel1 = connection.channel()
                channel1.queue_declare(queue='prime_bank_cib_extracted_download', durable=True)
                channel1.basic_publish(exchange='', routing_key='prime_bank_cib_extracted_download', body=json.dumps(final))
            
            else:
                cib_list = []
                cib_list.append(req_cib)
                
                for each in group_cib_list:
                    cib_list.append(each)
                    
                if metadata['cibType'] in ('cd', 'sme'):
                    final = {}
                    scorecard = []
                    dashboard_data = []
                    final['metaData'] = metadata
                    final['score'] = scorecard
                    final['dashboard'] = dashboard_data
                    # final['dashboard']['total_score'] = []
                    # final['dashboard']['group_score'] = []
                    # final['dashboard']['dashboard_objects'] = []
                    # final['score']['score_objects'] = []
                    final['message'] = 'Ok'
                    final['success'] = True
                    print('in if......')
                else:
                    scorecard = []
                    dashboard_data = []
                    detail_dashboard_data = []
                    final = {}
                    final['metaData'] = metadata
                    final['score'] = scorecard
                    final['dashboard'] = dashboard_data
                    # final['dashboard']['total_score'] = []
                    # final['dashboard']['group_score'] = []
                    # final['dashboard']['corporate_detail_dashboard'] = detail_dashboard_data
                    # final['dashboard']['dashboard_objects'] = []
                    # final['score']['score_objects'] = []
                    final['message'] = 'Ok'
                    final['success'] = True
                    print('detailed ............')
            print("Analysis Report")
            print(".................................")
            print(final)
            channel1 = connection.channel()
            channel1.queue_declare(queue='prime_bank_cib_extracted_download', durable=True)
            channel1.basic_publish(exchange='', routing_key='prime_bank_cib_extracted_download', body=json.dumps(final))
            print("Analysis Report Sent")
        
        except Exception as exc:
            print(type(exc))
            traceback.print_exc()
            
            raw_json = json.loads(body, strict=False)
                
            metadata = raw_json['metaData']
            final = dict([
                ('message', 'Analysis Error Found'),
                ('success', False),
                ('metaData', metadata)
            ])
            print("Exception Message: {}".format(exc))
            channel1 = connection.channel()
            channel1.queue_declare(queue='prime_bank_cib_extracted_download',durable=True)
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