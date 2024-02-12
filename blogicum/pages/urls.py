# Импорт функции для связи шаблона URL-адреса и обработчика
from django.urls import path

# Импорт модуля view-функций
from . import views

# Определение namespace
app_name = 'pages'

# Формирование списка шаблонов URL-адресов и их соотнесения с view-функциями
urlpatterns = [
    path('about/', views.AboutPage.as_view(), name='about'),
    path('rules/', views.RulesPage.as_view(), name='rules'),
]
