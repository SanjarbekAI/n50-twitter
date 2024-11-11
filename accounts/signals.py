import threading

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserModel, VerificationModel
from accounts.utils import get_random_verification_code
from conf import settings


def send_verification_email(email):
    try:
        code = get_random_verification_code(email=email)
        VerificationModel.objects.create(code=code, user=UserModel.objects.get(email=email))
        send_mail(
            subject="Verification Email",
            message=f"Your verification code for 2 minutes is {code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
    except Exception as e:
        print(e)


@receiver(post_save, sender=UserModel)
def send_activate_code_signal(sender, instance=None, created=False, **kwargs):
    if created:
        email_thread = threading.Thread(target=send_verification_email, args=(instance.email,))
        email_thread.start()
