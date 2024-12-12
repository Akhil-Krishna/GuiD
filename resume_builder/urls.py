from django.urls import path
from . import views

urlpatterns = [
    path('resumes/', views.resume_list, name='resume_list'),
    path('resumes/create/', views.create_resume, name='create_resume'),
    path('resumes/<int:resume_id>/edit/', views.edit_resume, name='edit_resume'),
    path('resumes/<int:resume_id>/delete/', views.delete_resume, name='delete_resume'),
    path('resumes/<int:resume_id>/view/', views.view_resume, name='view_resume'),
]
