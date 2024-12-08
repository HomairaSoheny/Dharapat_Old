from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('basic_dashboard_report', GeneralDashboardReportApiView.as_view())
]
