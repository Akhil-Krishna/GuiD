from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_resume, name='create_resume'),
    path('<int:resume_id>/edit/', views.edit_resume, name='edit_resume'),
     path('complete/', views.resume_complete, name='resume_complete'),
]
    