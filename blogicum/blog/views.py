from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)

from .forms import PostForm, CommentForm
from .models import Category, Post, Comment
from .querysets import post_query, posts_annotate_order, posts_select_related

# Число отображаемых на странице постов
POSTS_NUMBER = 10


class RedirectPostDetailMixin():
    """Возврат на страницу публикации."""

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.kwargs['pk']})


class RedirectProfileMixin():
    """Возврат на страницу профиля."""

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})


class ModelPaginateMixin():
    """Определение модели и пагинация."""

    model = Post
    paginate_by = POSTS_NUMBER


class PostListView(ModelPaginateMixin, ListView):
    """Вывод списка публикаций на главной странице."""

    queryset = post_query(Post.objects)
    template_name = 'blog/index.html'


class PostDetailView(DetailView):
    """Вывод полной информации о публикации"""

    model = Post
    template_name = 'blog/detail.html'

    def get_queryset(self):
        """Формирование необходимой выборки из БД.

        Для автора публикации информация выводится для всех его постов,
        включая снятые с публикации и с датой публикации в будущем.
        """
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.request.user == post.author:
            return posts_select_related(Post.objects)
        else:
            return post_query(Post.objects)

    def get_context_data(self, **kwargs):
        """Дополнение контекста данными по комментариям."""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CategoryPostListView(ModelPaginateMixin, ListView):
    """Вывод постов определенной категории."""

    template_name = 'blog/category.html'

    def get_queryset(self):
        """Фильтр БД постов по указанной в URL категории."""
        queryset = post_query(Post.objects).filter(
            category__slug=self.kwargs['category_slug']
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Дополнение контекста объектом  указанной в URL категории
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return context


class ProfileListView(ModelPaginateMixin, ListView):
    """Отображение страницы с профилем пользователя."""

    template_name = 'blog/profile.html'

    def get_queryset(self):
        """Формирование необходимой выборки из БД.

        Для хозяина аккаунта информация выводится для его любого поста,
        включая снятые с публикации и с датой публикации в будущем.
        """
        user = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user.id == user.pk:
            posts = posts_annotate_order(Post.objects)
            return posts.filter(author_id=user.pk)
        else:
            return post_query(Post.objects).filter(author_id=user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Дополнение контекста данными по хозяину аккаунта
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context


class UserUpdateView(UserPassesTestMixin, RedirectProfileMixin, UpdateView):
    """Редактирование профиля пользователя."""

    model = User
    fields = ['first_name', 'last_name', 'username', 'email', ]
    template_name = 'blog/user.html'

    def test_func(self):
        """Проверка соответствия пользователя хозяину аккаунта.

        Если не совпадает, то доступ запрещен - ошибка 403.
        """
        return self.request.user.id == self.kwargs['pk']


class PostUpdateView(RedirectPostDetailMixin, UpdateView):
    """Редактирование публикации."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        """Проверка соответствия пользователя автору поста.

        Если не совпадает, то переход на страницу поста.
        """
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.request.user.id != post.author_id:
            return redirect('blog:post_detail', self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, RedirectProfileMixin, CreateView):
    """Создание нового поста (только для залогиненных пользователей)."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        # Автозаполнение поля "author", которое не выводится на страницу
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(UserPassesTestMixin, RedirectProfileMixin, DeleteView):
    """Удаление публикации."""

    model = Post
    post_class = PostForm
    template_name = 'blog/create.html'

    def test_func(self):
        """Проверка соответствия пользователя автору публикации.

        Если не совпадает, то доступ запрещен - ошибка 403.
        """
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Дополнение контекста данными из публикации
        context['form'] = PostForm(instance=self.object)
        return context


class CommentCreateView(RedirectPostDetailMixin, LoginRequiredMixin,
                        CreateView):
    """Создание нового комментария (только для залогиненных пользователей)."""

    form = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Автозаполнение полей, которые не выводятся на страницу
        form.instance.author = self.request.user
        form.instance.post_id = post.pk
        return super().form_valid(form)


class CommentUpdateDeleteMixin(UserPassesTestMixin):
    """Общие инструкции для CBV редактирования и удаления комментария."""

    model = Comment
    template_name = 'blog/comment.html'

    def test_func(self):
        """Проверка соответствия пользователя автору комментария.

        Если не совпадает, то доступ запрещен - ошибка 403.
        """
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return self.request.user == comment.author

    def get_success_url(self):
        """Возврат на страницу публикации."""
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.kwargs['post_id']})


class CommentUpdateView(CommentUpdateDeleteMixin, UpdateView):
    """Редактирование комментария."""

    form_class = CommentForm


class CommentDeleteView(CommentUpdateDeleteMixin, DeleteView):
    """Удаление комментария."""

    pass
