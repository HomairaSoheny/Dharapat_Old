from django.http import HttpResponse
from rest_framework.views import APIView
# from settings import abs_path
from cib_analytics.cib_data_class import cib_class
from cib_analytics.spreadsheet_generation.consumer_spreadsheet import create_report_dashboard

import json
import os
abs_path = os.path.dirname(os.path.abspath(__file__))

class GeneralDashboardReportApiView(APIView):
    def post(self, request):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            raw_data = body['data']

            cib_data_list = []
            for each in raw_data:
                cib_data_list.append(cib_class(each))
                
            path = os.path.join(abs_path)

            writer, io = create_report_dashboard(cib_data_list, path)
            writer.close()
            
            rFile = io.getvalue()
            response = HttpResponse(rFile,content_type="application/ms-excel")
            response['Content-Disposition'] = f'attachment; filename=data.xlsx'

            return response
        except Exception as exc:
            print(exc)
            return exc