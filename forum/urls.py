from django.urls import path
from . import views

app_name= 'forum'
urlpatterns = [
    
    path('', views.forum_home, name='forum_home'),
    path('add/', views.add_post, name='add_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
]
