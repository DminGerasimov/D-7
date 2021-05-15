from celery import shared_task
from news.management.commands._weekly_mailing_job import weekly_mailing_subscribers
from .models import Post, Subscriber, PostCategory
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.core.mail import mail_managers
from django.core.mail import EmailMultiAlternatives
from django.template import loader


@shared_task
def weekly_mailing():
    weekly_mailing_subscribers()
    # print(f'mail sends')

@shared_task
def notify_user_post(post_id):
    subject = "Добавлена новость на портале:"
    message = "На блоге опубликована новость"
    # Создаем список категорий нового поста
    for _ in PostCategory.objects.filter(post = int(post_id)):
        # Проходимся по подписчикам из списка категорий для получения пары Подписчик: Почта
        for slist in Subscriber.get_subscribers_list(category = _):
            email = EmailAddress.objects.filter(user = User.objects.get(username=slist))[0]
            print(f'Категория {_}: подписчик: {slist} ({email})')
            
            # Получаем объект поста для передачи его содержимого в шаблон для рендеринга
            instance = Post.objects.get(id=post_id)
            # формируем html-тело и отправляем письмо
            subject=f'{subject} {instance.chapter}'
            html_content = loader.render_to_string( 
            'addnews_mail.html',
            {
                'instance': instance,
            })
            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email='',
                to=[email],
                )
            msg.attach_alternative(html_content, "text/html")

            msg.send() 
