import datetime as dt

from django.db.models import Count, Q

from .models import Post


def posts_select_related(posts):
    """Объединение связанных баз данных."""
    return posts.select_related(
        'author', 'category', 'location'
    )


def posts_filter(posts):
    """Фильтрация данных по дате публикации и флажкам публичности."""
    return posts.filter(
        pub_date__lte=dt.datetime.now(),
        is_published=True,
        category__is_published=True
    )


def posts_annotate_order(posts):
    """Аннотация счетчика комментариев и упорядочивание по дате публикации."""
    return posts.annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


def post_query(posts):
    """Обобщенный запрос к базам данных, повторяющийся в CBV."""
    selected_posts = posts_annotate_order(posts)
    selected_posts = posts_select_related(selected_posts)
    selected_posts = posts_filter(selected_posts)
    return selected_posts


def check_authorship(self):
    """Формирование необходимой выборки из БД.

    Для автора публикации информация доступна для всех его постов,
    включая снятые с публикации и с датой публикации в будущем.
    """
    try:
        Post.objects.get(Q(pk=self.kwargs[self.pk_url_kwarg]) & Q(
                         author__id=self.request.user.pk))
        return posts_select_related(Post.objects)
    except Post.DoesNotExist:
        return post_query(Post.objects)
