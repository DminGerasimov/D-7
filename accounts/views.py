from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import Subscriber, Category 
from accounts.forms import SubscriptionForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# User page
class UserPage(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

# Добавление подпсики пользователя на странице профиля
class SubcribeAdd(LoginRequiredMixin, CreateView):
    model = Subscriber
    template_name = 'accounts/addsubscription.html'
    form_class = SubscriptionForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Ищем id текущего аутентифицированного пользователя
        user_id = User.objects.all().values().filter(username=self.request.user)[0]['id']
        # Добавляем текущего пользователя в поле user формы
        self.object.user = User.objects.get(id=user_id)

        # Проверка, есть ли уже такая подписка
        subscriber_list = Subscriber.objects.filter(user = self.object.user)
        save_flag  = True
        for item in list(subscriber_list):
            if item.category == self.object.category:
                save_flag = False
                break
        if save_flag:
            self.object.save()
            return super().form_valid(form)
        else:
            self.success_url = '/news/'
            return HttpResponseRedirect(FormMixin.get_success_url(self))


# Добавление подписки пользователя на тему текущей новости
@login_required
def fastsubscribe(request):
    category_list = []
    cat_list = []
    temp_list = []
    # Проверка, есть ли уже такая подписка
    subscriber_list = Subscriber.objects.filter(user = request.user)
    _category = str(request.GET.getlist('category'))
    while True:
        f = _category.find('PostCategory: ')
        if f == -1:
            break
        _category = _category[f+14:len(_category)]
        parse_category = ''
        for i in _category:
            if i != '>':
                parse_category = parse_category + i
            else:
                break
        cat_list.append(parse_category)
    # Если у данного пользователя отсутствуют подписки, то подписываемся
    if list(subscriber_list) == []:
        category_list = cat_list
    else:
        for item in subscriber_list:
            temp_list.append(str(item.category))
       
        for item in cat_list:
            if item not in temp_list:
                category_list.append(str(item))

    for cat in category_list:    
        Subscriber.objects.create(
            user = request.user,
            category = Category.objects.get(news_category = cat))

    return redirect('/news/')
