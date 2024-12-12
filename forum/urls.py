from django.urls import path
from . import views

urlpatterns = [
    path('question_list', views.question_list, name='question_list'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/<int:question_id>/add_answer/', views.add_answer, name='add_answer'),
    path('question/<int:question_id>/upvote/<int:answer_id>/', views.upvote_answer, name='upvote'),
    path('delete_answer/<int:answer_id>/', views.delete_answer, name='delete_answer'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
]

