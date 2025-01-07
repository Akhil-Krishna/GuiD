
from django.urls import path


from roadmap.views import RoadmapStageView ,  RoadmapCourseView , RoadmapSlideView,RoadmapTestView
urlpatterns = [
    path('', RoadmapStageView.as_view(), name='roadmap_stages'),
    path('stage/<int:stage_id>/course/<int:course_order>/', RoadmapCourseView.as_view(), name='roadmap_course'),
    path('course/<int:course_id>/slide/<int:slide_order>/', RoadmapSlideView.as_view(), name='roadmap_slide'),
    #path('stage/<int:stage_id>/test/', RoadmapTestView.as_view(), name='roadmap_test'),
    path("<int:stage_id>/test/", RoadmapTestView.as_view(), name="roadmap_test"),
]
