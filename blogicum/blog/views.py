from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)
from django.views.generic.detail import SingleObjectMixin

from .cbv_mixins import (CheckAuthorshipMixin, CommentUpdateDeleteMixin,
                         PostUpdateDeleteViewMixin, RedirectProfileMixin)
from .forms import PostForm, CommentForm
from .models import Category, Post, Comment
from .querysets import post_query, posts_annotate_order, posts_filter

# Число отображаемых на странице постов
POSTS_NUMBER = 10


class PostListView(ListView):
    """Вывод списка публикаций на главной странице."""

    model = Post
    paginate_by = POSTS_NUMBER
    queryset = post_query(Post.objects)
    template_name = 'blog/index.html'


class PostDetailView(CheckAuthorshipMixin, DetailView):
    """Вывод полной информации о публикации."""

    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        """Дополнение контекста данными по комментариям."""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CategoryListView(SingleObjectMixin, ListView):
    """Вывод постов определенной категории."""

    paginate_by = POSTS_NUMBER
    slug_url_kwarg = 'category_slug'
    template_name = 'blog/category.html'

    def get(self, request, *args, **kwargs):
        """Выбор необходимого объекта модели Category."""
        self.object = self.get_object(
            Category.objects.filter(is_published=True))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Дополнение контекста объектом модели Category."""
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        return context

    def get_queryset(self):
        return posts_filter(self.object.posts)


class ProfileListView(SingleObjectMixin, ListView):
    """Отображение страницы с профилем пользователя."""

    paginate_by = POSTS_NUMBER
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'blog/profile.html'

    def get(self, request, *args, **kwargs):
        """Выбор необходимого объекта модели User."""
        self.object = self.get_object(User.objects)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Дополнение контекста объектом модели User."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context

    def get_queryset(self):
        """Формирование необходимой выборки из БД.

        Для хозяина аккаунта информация выводится для его любого поста,
        включая снятые с публикации и с датой публикации в будущем.
        """
        if self.request.user != self.object:
            return post_query(self.object.posts)
        return posts_annotate_order(self.object.posts)


class UserUpdateView(UserPassesTestMixin, RedirectProfileMixin, UpdateView):
    """Редактирование профиля пользователя."""

    model = User
    fields = ('first_name', 'last_name', 'username', 'email',)
    template_name = 'blog/user.html'

    def test_func(self):
        """Проверка соответствия пользователя хозяину аккаунта."""
        return self.request.user == self.get_object(User.objects)


class PostCreateView(LoginRequiredMixin, RedirectProfileMixin, CreateView):
    """Создание нового поста (только для залогиненных пользователей)."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        # Автозаполнение поля "author", которое не выводится на страницу
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PostUpdateDeleteViewMixin, UpdateView):
    """Редактирование публикации."""

    def get_success_url(self):
        """Возврат на страницу публикации."""
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(PostUpdateDeleteViewMixin, RedirectProfileMixin,
                     DeleteView):
    """Удаление публикации."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Дополнение контекста данными из публикации
        context['form'] = PostForm(instance=self.object)
        return context


class CommentCreateView(LoginRequiredMixin, CheckAuthorshipMixin, CreateView):
    """Создание нового комментария (только для залогиненных пользователей)."""

    form = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        # Автозаполнение полей, которые не выводятся на страницу
        form.instance.author = self.request.user
        form.instance.post_id = post.pk
        return super().form_valid(form)

    def get_success_url(self):
        """Возврат на страницу публикации."""
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(CommentUpdateDeleteMixin, UpdateView):
    """Редактирование комментария."""

    form_class = CommentForm


class CommentDeleteView(CommentUpdateDeleteMixin, DeleteView):
    """Удаление комментария."""
