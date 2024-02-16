from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .forms import PostForm
from .models import Comment, Post
from .querysets import post_query, posts_select_related


class CheckAuthorshipMixin:
    """Формирование необходимой выборки из БД.

    Для автора публикации информация доступна для всех его постов,
    включая снятые с публикации и с датой публикации в будущем.
    """

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs[self.pk_url_kwarg])
        if post.author != self.request.user:
            return post_query(Post.objects)
        return posts_select_related(Post.objects)


class RedirectProfileMixin:
    """Возврат на страницу профиля."""

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


class PostUpdateDeleteViewMixin(UserPassesTestMixin):
    """Общие инструкции для CBV редактирования и удаления публикации."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def test_func(self):
        """Проверка соответствия пользователя автору поста."""
        self.object = self.get_object(Post.objects.all())
        return self.request.user == self.object.author

    def handle_no_permission(self):
        """Переход в случае провала проверки UserPassesTestMixin.test_func."""
        return redirect('blog:post_detail', self.object.pk)


class CommentUpdateDeleteMixin(UserPassesTestMixin):
    """Общие инструкции для CBV редактирования и удаления комментария."""

    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def test_func(self):
        """Проверка соответствия пользователя автору комментария."""
        self.object = self.get_object()
        return self.request.user == self.object.author

    def get_success_url(self):
        """Возврат на страницу публикации."""
        return reverse('blog:post_detail',
                       kwargs={'pk': self.kwargs['pk']})
