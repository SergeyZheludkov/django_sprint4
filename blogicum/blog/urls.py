# Импорт функции для связи шаблона URL-адреса и обработчика
from django.urls import path

# Импорт модуля view-функций
from . import views

# Определение namespace
app_name = 'blog'

# Формирование списка шаблонов URL-адресов и их соотнесения с view-функциями
urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('category/<slug:category_slug>/',
         views.CategoryPostListView.as_view(), name='category_posts'),
    path('profile/<username>/', views.ProfileListView.as_view(),
         name='profile'),
    path('edit_profile/<int:pk>/', views.UserUpdateView.as_view(),
         name='edit_profile'),
    path('posts/create/', views.PostCreateView.as_view(),
         name="create_post"),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<int:pk>/delete/',
         views.PostDeleteView.as_view(), name="delete_post"),
    path('posts/<int:pk>/comment/', views.CommentCreateView.as_view(),
         name="add_comment"),
    path('posts/<post_id>/edit_comment/<int:pk>/',
         views.CommentUpdateView.as_view(), name="edit_comment"),
    path('posts/<post_id>/delete_comment/<int:pk>/',
         views.CommentDeleteView.as_view(), name="delete_comment"),
]
