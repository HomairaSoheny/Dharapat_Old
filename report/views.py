from django.http import HttpResponse
from rest_framework.views import APIView
from report.report_download import createReportDashboard
from beeprint import pp
import json
import os
abs_path = os.path.dirname(os.path.abspath(__file__))

class GeneralDashboardReportApiView(APIView):
    def post(self, request):
        try:
            print("Analysis report received")
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            print("\n\n___________________________________________________\n\n")
            pp(body)
            print("\n\n___________________________________________________\n\n")
            writer, io = createReportDashboard(body)
            writer.close()
            
            rFile = io.getvalue()
            response = HttpResponse(rFile,content_type="application/ms-excel")
            response['Content-Disposition'] = f'attachment; filename=data.xlsx'

            return HttpResponse(response)
        except Exception as exc:
             print(exc)
             return HttpResponse([exc])