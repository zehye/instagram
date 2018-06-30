from django.urls import path
from .views import post_list, post_detail, post_create, post_delete,post_like_toggle ,comment_create

app_name = 'posts'
urlpatterns = [
    path('', post_list, name='post-list'),
    path('<int:pk>/', post_detail, name='post-detail'),
    path('create/', post_create, name='post-create'),
    path('<int:pk>/delete/', post_delete, name='post-delete'),
    path('<int:pk>/like-toggle', post_like_toggle, name='post-like-toggle'),
    path('<int:pk>/comment/create/', comment_create, name='comment-create'),
]
