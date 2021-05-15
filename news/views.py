from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Author, Category, PostCategory
from .filters import NewsFilter
from .forms import NewsForm

from django.core.mail import send_mail

from django.shortcuts import redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import PermissionRequiredMixin

from .tasks import notify_user_post


class NewsList(ListView):
    model = Post
    template_name = 'news/newslist.html'
    context_object_name = 'newslist'
    ordering = ['-time_in'] # выводим первыми самые свежие новости
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/newsdetail.html'
    context_object_name = 'newsdetail'  

    def get_context_data(self, **kwargs):
        context = super(NewsDetail, self).get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        context['category'] = PostCategory.objects.filter(post = id)
        return context


class SearchNews(ListView):
    model = Post
    template_name = 'news/searchnews.html'
    context_object_name = 'searchnews'

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context["filter"] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context


class NewsAdd(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/addnews.html'
    form_class = NewsForm
    permission_required = ('news.add_post')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Ищем id текущего аутентифицированного пользователя
        user_id = User.objects.all().values().filter(username=self.request.user)[0]['id']
        # Добавляем текущего автора в поле author формы
        self.object.author = Author.objects.get_or_create(user_id=user_id)[0]
        self.object.save()

        # Создаем задачу в Celery для отправки созданной новости подписчикам
        notify_user_post.apply_async([self.object.id])

        return super().form_valid(form)




class NewsEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'news/addnews.html'
    form_class = NewsForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    context_object_name = 'newsdetail'  
    template_name = 'news/deletenews.html'
    queryset = Post.objects.all()
    success_url = '/news/'


# Добавление пользователя в группу author
@login_required
def add_to_author_group(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/news/')


# Точка входа на сайт
class Home_page(TemplateView):
    template_name = 'news/home_page.html'