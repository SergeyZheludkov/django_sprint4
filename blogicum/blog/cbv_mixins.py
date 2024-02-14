from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse

from .forms import PostForm
from .models import Comment, Post


class RedirectProfileMixin():
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


class CommentUpdateDeleteMixin(UserPassesTestMixin):
    """Общие инструкции для CBV редактирования и удаления комментария."""

    model = Comment
    template_name = 'blog/comment.html'

    def test_func(self):
        """Проверка соответствия пользователя автору комментария."""
        self.object = self.get_object(Comment.objects)
        return self.request.user == self.object.author

    def get_success_url(self):
        """Возврат на страницу публикации."""
        return reverse('blog:post_detail',
                       kwargs={'pk': self.kwargs['post_id']})
