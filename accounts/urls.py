from django.urls import path
from accounts.views import UserPage
from accounts.views import SubcribeAdd, fastsubscribe
 
urlpatterns = [
    path('', UserPage.as_view(), name = 'profile'),
    path('subscribe/', SubcribeAdd.as_view(), name = 'subscribe'),
    path('fastsubscribe/', fastsubscribe, name = 'fastsubscribe')
]