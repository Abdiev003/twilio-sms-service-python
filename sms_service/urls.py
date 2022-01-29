from django.urls import path

from sms_service.views import SMSAPIView

urlpatterns = [
    path('send-sms/', SMSAPIView.as_view(), name='send_sms'),
]
