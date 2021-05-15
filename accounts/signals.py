from allauth.account.signals import email_confirmed
from django.dispatch import receiver # импортируем нужный декоратор
from allauth.account.models import EmailConfirmationHMAC, EmailConfirmation
from django.core.mail import EmailMultiAlternatives
from django.template import loader
import warnings
from django.core.mail import send_mail

# from django.core.mail import mail_managers

# в декоратор передаётся первым аргументом сигнал, в отправители - модель
# allauth.account.signals.email_confirmed(request, email_address)
@receiver(email_confirmed, sender=EmailConfirmationHMAC)
@receiver(email_confirmed, sender=EmailConfirmation)
def notify_user_signup(request, email_address, **kwargs):
    warnings.warn(f'{request}; email_address:{email_address}')
    print(f'EmailAddress confirmed')
    pass

    subject = f"Ваша учетная запись {email_address} активирована."
    instance = email_address
    # формируем html-тело и отправляем письмо
    html_content = loader.render_to_string( 
    'after_email_confirmation.html',
    {
        'instance': instance,
    })
    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email='',
        to=[email_address],
        )
    msg.attach_alternative(html_content, "text/html") # добавляем html
    # print(html_content)
    msg.send() 
