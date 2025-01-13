#myupdate
from django.urls import path
from . import views

from roadmap.views import RoadmapStageView ,  RoadmapCourseView , RoadmapSlideView,RoadmapTestView ,RoadmapCourseList,StageCourseListView
urlpatterns = [
    path('', RoadmapStageView.as_view(), name='roadmap_stages'),
    path('stage/<int:stage_id>/course/<int:course_order>/', RoadmapCourseView.as_view(), name='roadmap_course'),
    path('course/<int:course_id>/slide/<int:slide_order>/', RoadmapSlideView.as_view(), name='roadmap_slide'),
    #path('stage/<int:stage_id>/test/', RoadmapTestView.as_view(), name='roadmap_test'),
    path("<int:stage_id>/test/", RoadmapTestView.as_view(), name="roadmap_test"),
    #path('stage/<int:stage_id>/courselist',RoadmapCourseList.as_view(),name="course_list"),
    path('stage/<int:stage_id>/courses/', StageCourseListView.as_view(), name='stage_courses'),
    path('chat/', views.chat_with_llama, name='chat_with_llama'),
    # In urls.py
    #path('stage/<int:stage_id>/course/', RoadmapCourseView.as_view(), name='roadmap_course'),
    
]
