from django.http import HttpResponse
from rest_framework.views import APIView
from report.report_download import createReportDashboard

import json
import os
abs_path = os.path.dirname(os.path.abspath(__file__))

class GeneralDashboardReportApiView(APIView):
    def post(self, request):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            raw_data = body

            cib_data_list = []
            for each in raw_data:
                cib_data_list.append(each)

            writer, io = createReportDashboard(cib_data_list)
            writer.close()
            
            rFile = io.getvalue()
            response = HttpResponse(rFile,content_type="application/ms-excel")
            response['Content-Disposition'] = f'attachment; filename=data.xlsx'

            return HttpResponse(response)
        except Exception as exc:
             print(exc)
             return HttpResponse([exc])