from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ContactFormSerializer


class ContactFormView(APIView):
    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']

            full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            try:
                send_mail(
                    subject=subject,
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
                    fail_silently=False
                )
                return Response({ "success": True }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    { "success": False, "error": "email_send_failed", "details": str(e) },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
