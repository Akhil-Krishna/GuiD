from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import sign_up, sign_in, profile,notifications, mark_as_read

urlpatterns = [
    path('', views.index, name='index'),
    
   path('courses/', views.courses, name='courses'),
    path('courses/start/<int:course_id>/', views.start_course, name='start_course'),
    path('courses/<int:course_id>/<int:slide_order>/', views.course_detail, name='course_detail'),
    path('courses/complete/<int:course_id>/', views.complete_course, name='complete_course'),
    path('questions/', views.questions, name='questions'),
    path('code/<int:question_id>/', views.code, name='code'),
    path('notifications/', views.notifications, name='notifications'),
    path('profile/', views.profile, name='profile'),
    path('run_code/', views.run_code, name='run_code'),
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', profile, name='profile'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
    
]
