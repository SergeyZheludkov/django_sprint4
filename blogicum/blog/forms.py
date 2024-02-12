from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Форма для публикации, привязанная к модели."""

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {'pub_date': forms.DateTimeInput(
            attrs={'type': 'datetime-local'}
        )}


class CommentForm(forms.ModelForm):
    """Форма для комментария, привязанная к модели."""

    class Meta:
        model = Comment
        fields = ('text',)
