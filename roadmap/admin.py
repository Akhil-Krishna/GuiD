from django.contrib import admin

from .models import UserProgress,TestQuestion,RoadmapCourse,RoadmapSlide,RoadmapStage,RoadmapTest
# Register your models here.
admin.site.register(UserProgress)
admin.site.register(TestQuestion)
admin.site.register(RoadmapTest)
admin.site.register(RoadmapSlide)
admin.site.register(RoadmapCourse)
admin.site.register(RoadmapStage)
