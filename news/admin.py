from django.contrib import admin
from news.models import Post, Subscriber, Author, PostCategory, Category
# Register your models here.
admin.site.register(Post)
admin.site.register(Subscriber)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Category)