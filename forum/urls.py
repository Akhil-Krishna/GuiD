from django.urls import path
from . import views

urlpatterns = [
    path('forum', views.question_list, name='question_list'),
    path('question/<int:question_id>/', views.add_answer, name='add_answer'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('upvote',views.upvote_answer,name='upvote'),
]
