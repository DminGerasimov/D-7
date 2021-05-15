from django.db import models
from django.conf import global_settings
from django.contrib.auth.models import User
# from django.urls import reverse

# Create your models here.
class Author(models.Model):
    # Поле встроенного пользователя User from django.contrib.auth.models
    user = models.OneToOneField(global_settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    
    # Поле рейтинга автора
    rating = models.IntegerField(default = 0)


    #     Метод update_rating() модели Author, который обновляет рейтинг пользователя, переданный в аргумент этого метода.
    # Он состоит из следующего:
    #     суммарный рейтинг каждой статьи автора умножается на 3;
    #     суммарный рейтинг всех комментариев автора;
    #     суммарный рейтинг всех комментариев к статьям автора
    def update_rating(self):
        sum_article_rate, sum_author_commemts_rate, sum_commemts_rate = 0, 0, 0
        
        # Статьи автора:
        for _ in Post.objects.filter(author = self.id).values('article_news_rate'):
            sum_article_rate += int(_['article_news_rate'])
        # print(sum_article_rate)
        
        # Комментарии автора
        for _ in Comment.objects.filter(user = self.id).values('comment_rate'):
            sum_author_commemts_rate += int(_['comment_rate'])
        # print(sum_author_commemts_rate)

        # Комментарии к статьям автора
        for _ in Comment.objects.filter(post__author = self.id ).values('comment_rate'):
            sum_commemts_rate += int(_['comment_rate'])
        # print(sum_commemts_rate)
        
        self.rating = sum_article_rate*3 + sum_author_commemts_rate + sum_commemts_rate
        # print(self.rating)
        self.save()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    # Категория новостей, статей - уникальная
    news_category = models.CharField(max_length = 24, unique = True)

    def __str__(self):
        return f'{self.news_category}'

class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)

    def get_absolute_url(self):
        return f'/profile/'

    # Получаем список пользователей, подписанных на данную категорию
    def get_subscribers_list(category = None):
        subscriber_list = []
        for _ in Subscriber.objects.all():
            if str(_.category).lower() == str(category).lower():
                subscriber_list.append(_.user)
        return subscriber_list

class Post(models.Model):
    # Сведения об авторе публикации: один ко многим с моделью Author
    author = models.ForeignKey('Author', on_delete = models.CASCADE)

    # Выбор вида публикации: статья, новость фиксированная двумя значениями
    news, article = 'NE', 'AR'
    POSITIONS = [(news, 'Новость'), (article,'Статья')]
    type_news_article = models.CharField(max_length = 2, choices = POSITIONS, default = 'news')

    # Дата создания публикации
    time_in = models.DateTimeField(auto_now_add = True)

    # Заголовок статьи/новости
    chapter = models.CharField(max_length = 200, unique = False)

    # Текст статьи/новости
    text = models.TextField(default = '')

    # Рейтинг статьи/новости
    article_news_rate = models.IntegerField(default=0)

    # Связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory)
    category = models.ManyToManyField(Category, through= 'PostCategory')

    def __str__(self):
        return f'{self.chapter.title()}: {self.text[0:200]}'

    def get_absolute_url(self):
        return f'/news/{self.id}'
    
    # Методы like() и dislike(), которые увеличивают/уменьшают рейтинг на единицу
    def like(self):
        self.article_news_rate += 1
        self.save

    def dislike(self):
        self.article_news_rate -= 1
        self.save

    # Метод preview() модели Post, который возвращает начало статьи 
    # (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце
    def preview(self):
        return f'{self.text[0:123]}...'


class PostCategory(models.Model):
    # Связь «один ко многим» с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # Связь «один ко многим» с моделью Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category}'


class Comment(models.Model):
    # Связь «один ко многим» с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # Связь «один ко многим» с встроенной моделью User /
    # (комментарии может оставить любой пользователь, не обязательно автор)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)

    # Текст комментария
    comment_text = models.TextField(help_text='Текст комментария', default='')

    # Дата и время создания комментария
    time_creation = models.DateTimeField(auto_now_add=True)

    # Рейтинг комментария
    comment_rate = models.IntegerField(default=0)

    # Методы like() и dislike(), которые увеличивают/уменьшают рейтинг на единицу
    def like(self):
        self.comment_rate += 1
        self.save

    def dislike(self):
        self.comment_rate -= 1
        self.save
