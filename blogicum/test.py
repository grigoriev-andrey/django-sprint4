from django.core.mail import send_mail

send_mail(
    subject='Test',
    message='Test',
    from_email='admin@yandex.ru',
    recipient_list=['request.user.email'],
    fail_silently=False,
)