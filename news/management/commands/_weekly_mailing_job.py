from news.models import Post, Subscriber, PostCategory
from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.template import loader
from django.core.mail import EmailMultiAlternatives


def weekly_mailing_subscribers():
    # Настраиваем зону времени, чтобы база данных не руглась на запросы без TimeZone
    tz = timezone(timedelta(hours=3), name='MSK')
    dt= datetime.now(tz=tz) - timedelta(weeks = 1)
    dt.utcoffset()

    # Список статей за последнюю неделю
    lastweek_postlist = Post.objects.filter(time_in__gte = dt)
    
    # Формирование словаря категорий статей за прошедшую неделю
    category_lastweekposts = {}
    for _ in lastweek_postlist:
        for pc in PostCategory.objects.filter(post = int(_.id)):
            category_lastweekposts[_.id] = str(pc)
    # print(category_lastweekposts)

    # Формирование словаря {почта подписчика:[новость,новость,]}
    mailing_list = {}
    for slist in Subscriber.objects.all():
        email = str(EmailAddress.objects.filter(user = User.objects.get(username=slist.user))[0])
        for k, v in category_lastweekposts.items():
            if str(v) == str(slist.category):
                if email not in mailing_list.keys():
                    mailing_list[email] = []
                mailing_list[email].append(k)
    # print(mailing_list)

    # формируем html-тело для каждого подписчика и отправляем письмо
    subject=f'Новости на портале за прошедшую неделю.'
    for email in mailing_list.keys():
        # Формируем список новостей для подписчика
        instance = []
        for _ in mailing_list[email]:
            instance.append(Post.objects.get(id  = int(_)))
        
        html_content = loader.render_to_string( 
        'weekly_mailing.html',
        {
            'instance': instance,
        })
        print("sending message...")

        msg = EmailMultiAlternatives(
            subject=subject,
            body=f'Уважаемый подписчик {slist.user}, за прошедшую неделю на портале появились следующие новости:',
            from_email='',
            to=[email],
            )
        msg.attach_alternative(html_content, "text/html") # добавляем html

        msg.send() 
        print("OK___")
