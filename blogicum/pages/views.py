# Импорт функции для формирования ответа view-функций
from django.shortcuts import render
# Импорт CBV для статичных страниц
from django.views.generic import TemplateView


class AboutPage(TemplateView):
    """CBV для страницы с описанием проекта."""

    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    """CBV для страницы с описанием правил сообщества."""

    template_name = 'pages/rules.html'


def csrf_failure(request, reason=''):
    """View-функция вызова кастомной страницы для ошибки 403."""
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    """View-функция вызова кастомной страницы для ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def internal_server_error(request):
    """View-функция вызова кастомной страницы для ошибки 500."""
    return render(request, 'pages/500.html', status=500)
