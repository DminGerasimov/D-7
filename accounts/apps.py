from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'


 # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        import accounts.signals