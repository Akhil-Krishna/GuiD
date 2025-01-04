from django.db import models
from django.conf import settings

# Models

class Stage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    stage = models.ForeignKey(Stage, related_name="courses1", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Slide(models.Model):
    course = models.ForeignKey(Course, related_name="slides", on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    content = models.TextField()

    class Meta:
        unique_together = ('course', 'order')
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - Slide {self.order}"


class UserProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    current_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    current_slide = models.PositiveIntegerField(default=1)

    def move_to_next_slide(self):
        slides = self.current_course.slides.all()
        if self.current_slide < slides.count():
            self.current_slide += 1
        else:
            self.move_to_next_course()

    def move_to_next_course(self):
        courses = self.current_stage.courses.all()
        current_course_index = list(courses).index(self.current_course)
        if current_course_index + 1 < len(courses):
            self.current_course = courses[current_course_index + 1]
            self.current_slide = 1
        else:
            self.move_to_next_stage()

    def move_to_next_stage(self):
        stages = Stage.objects.all()
        current_stage_index = list(stages).index(self.current_stage)
        if current_stage_index + 1 < len(stages):
            self.current_stage = stages[current_stage_index + 1]
            self.current_course = self.current_stage.courses.first()
            self.current_slide = 1
        else:
            self.current_stage = None  # User has completed all stages

    def __str__(self):
        return f"{self.user} Progress"


# Admin Registration

from django.contrib import admin

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'stage')


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('course', 'order')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_stage', 'current_course', 'current_slide')
