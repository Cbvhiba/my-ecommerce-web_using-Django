from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_email(email, email_token):
    subject = "Your account needs to be verified"
    email_from = settings.EMAIL_HOST_USER
    message = f'hi, click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}'
    
    send_mail(subject, message, email_from, [email], fail_silently=False)

def send_forget_password_mail(email, forget_password_token):
    subject = "Your forget password link"
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, you asked for reset password. click the link to reset password http://127.0.0.1:8000/accounts/reset_password/{forget_password_token}'
    
    send_mail(subject, email_from, message, [email], fail_silently=False)
    return True