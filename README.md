Итоговое задание по модулю D-7
===============================

Зависимости: django, pymorphy2, django-filter, allauth, django-apscheduler, celery, redis

Вход в административную панель noreply@nsmnn.ru:e4DatZt3cRz7SVV


1. Установить Redis.
    - Redis установлен в облаке, пароль запикан,
     т.к. в открытом доступе в GitHub, который, кстати честно предупреждает об этом)
2. Установить Celery.
    - Установлен.
3. Произвести необходимые конфигурации Django для соединения всех компонент системы.
    - Выполнено.
    Запуск worker'a: celery -A NewsPaper worker --pool=solo --concurrency=4 -l INFO
    Запуск beat для добавки заданий в очередь: celery -A NewsPaper beat
    beat c workr'oм на Win7 работают только на 2-х консолях одновременно, 
    попытка запустить worker'a с опцией beat - провалилась: с celery V.4+ на окнах не запускаются.
4. Реализовать рассылку уведомлений подписчикам после создания новости.
    - tasks.notify_user_post(), отправка по сигналу закомментировна.
5. Реализовать еженедельную рассылку с последними новостями (каждый понедельник в 8:00 утра). 
    - tasks.weekly_mailing()
        (from news.management.commands._weekly_mailing_job import weekly_mailing_subscribers)

p.s. Пароли акаунктов почты noreply@nsmnn.ru и redis в settings сброшены с целью декомпроментации.
Для проверяющего готов предоставить в Slack