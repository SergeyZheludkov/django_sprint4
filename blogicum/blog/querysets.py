import datetime as dt

from django.db.models import Count


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
    return posts_filter(selected_posts)
