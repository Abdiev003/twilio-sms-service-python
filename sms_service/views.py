import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from twilio.rest import Client


class SMSAPIView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request, format=None):
        to = request.data.get('to', False)
        body = request.data.get('body', False)

        try:
            account_sid = os.environ['TWILIO_ACCOUNT_SID']
            auth_token = os.environ['TWILIO_AUTH_TOKEN']
            client = Client(account_sid, auth_token)

            if not to or not body:
                return Response(
                    data={
                        'message': 'Missing parameters'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            message = client.messages.create(
                messaging_service_sid=os.environ['MESSAGING_SERVICE_SID'],
                body=body,
                to=to
            )

            return Response(
                data={
                    'message': 'Message sent',
                    'data': message.sid
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            pass

        return Response(
            data={'message': 'Something went wrong'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
