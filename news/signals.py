from django.db.models.signals import m2m_changed
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Post, Subscriber, PostCategory
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
# from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import loader

# в декоратор передаётся первым аргументом сигнал, в отправители - модель
# @receiver(m2m_changed, sender=PostCategory)
# def notify_user_post(sender, instance, **kwargs):
#     subject = "Добавлена новость на портале:"
#     message = "На блоге опубликована новость"
#     # Создаем список категорий нового поста
#     for _ in PostCategory.objects.filter(post = int(instance.id)):
#         # Проходимся по подписчикам из списка категорий
#         for slist in Subscriber.get_subscribers_list(category = _):
#             email = EmailAddress.objects.filter(user = User.objects.get(username=slist))[0]
#             # print(f'Категория {_}: подписчик: {slist} ({email})')
            
#             # формируем html-тело и отправляем письмо
#             subject=f'{subject} {instance.chapter}'
#             html_content = loader.render_to_string( 
#             'addnews_mail.html',
#             {
#                 'instance': instance,
#             })
#             msg = EmailMultiAlternatives(
#                 subject=subject,
#                 body='',
#                 from_email='',
#                 to=[email],
#                 )
#             msg.attach_alternative(html_content, "text/html") # добавляем html

#             msg.send() 
