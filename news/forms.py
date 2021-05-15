from django.forms import ModelForm, TextInput, Textarea, Select, SelectMultiple
from django import forms
from .models import Post, Category
from django.contrib.auth.models import User

class NewsForm(ModelForm):
    # author =  forms.ModelChoiceField(queryset=User.objects.all(), label = 'Автор')
    # category =  forms.ModelMultipleChoiceField(queryset=.objects.all().get('category__news_category'), label = 'Категории')
    class Meta:
        model = Post
        fields = ['type_news_article', 'chapter', 'text', 'category']

        widgets = {
            'chapter': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи или новости'
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...'
            }),
            'type_news_article': Select(attrs={
                'class': 'custom-select',
                'option selected': 'Выбрать...'
            }),
            'category': SelectMultiple(attrs={
                'multiple class': 'form-control',
            }),
        }