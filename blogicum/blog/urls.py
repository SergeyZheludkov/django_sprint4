# Импорт функции для связи шаблона URL-адреса и обработчика
from django.urls import include, path

# Импорт модуля view-функций
from . import views

# Определение namespace
app_name = 'blog'

# Формирование списка шаблонов URL-адресов и их соотнесения с view-функциями
extra_patterns_posts_pk = [
    path('', views.PostDetailView.as_view(), name='post_detail'),
    path('edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path('comment/', views.CommentCreateView.as_view(), name='add_comment'),
]

extra_patterns_post_id = [
    path('edit_comment/<int:comment_id>/', views.CommentUpdateView.as_view(),
         name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.CommentDeleteView.as_view(),
         name='delete_comment'),
]

extra_patterns_posts = [
    path('<int:pk>/', include(extra_patterns_posts_pk)),
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('<int:pk>/', include(extra_patterns_post_id)),
]

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/', include(extra_patterns_posts)),
    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(), name='category_posts'),
    path('profile/<username>/', views.ProfileListView.as_view(),
         name='profile'),
    path('edit_profile/<int:pk>/', views.UserUpdateView.as_view(),
         name='edit_profile'),
]
