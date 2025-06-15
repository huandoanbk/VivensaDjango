from django.core.mail import send_mail
from django.conf import settings
import traceback

try:
    send_mail(
        subject='Test Email',
        message='This is a test message from shell.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
        fail_silently=False
    )
    print("✅ Email sent successfully.")
except Exception as e:
    print("❌ Error occurred while sending email:")
    traceback.print_exc()
