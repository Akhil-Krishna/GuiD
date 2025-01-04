from django.urls import path
from .views import roadmap_home,stage_detail,course_detail,next_slide,complete_course
urlpatterns = [
    path('', roadmap_home, name='roadmap_home'),
    path('stage/<int:stage_id>/', stage_detail, name='stage_detail'),
    path('stage/<int:stage_id>/course/<int:course_id>/', course_detail, name='course_detail'),
    path('stage/<int:stage_id>/course/<int:course_id>/next/', next_slide, name='next_slide'),
    path('stage/<int:stage_id>/course/<int:course_id>/complete/', complete_course, name='complete_course'),
]