from io import BytesIO

import pandas as pd
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

            # writer.save()

            writer.close()

            # rFile = io.getvalue()
            io.seek(0)

            response = HttpResponse(io,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
            # response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            # response['Content-Transfer-Encoding'] = 'binary'  # Add this to ensure binary content handling
            return response
        except Exception as exc:
             print(exc)
             return HttpResponse([exc])