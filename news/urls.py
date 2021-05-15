from django.urls import path
from .views import NewsList, NewsDetail, SearchNews, NewsAdd, NewsEdit, NewsDelete
from .views import add_to_author_group
 
 
urlpatterns = [
    path('', NewsList.as_view(), name = 'news_list'),
    path('<int:pk>', NewsDetail.as_view()),  # pk — это первичный ключ, который будет выводиться у нас в шаблон
    path('search/', SearchNews.as_view(), name = 'search_news'),
    path('search/<int:pk>', NewsDetail.as_view()),
    path('add/', NewsAdd.as_view(), name = 'add_news'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name = 'edit_news'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name = 'delete_news'),
    path('accounts/add_author/', add_to_author_group, name = 'add_to_author_group')
]