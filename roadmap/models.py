from django.db import models
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.conf import settings
# Custom User model reference
User = settings.AUTH_USER_MODEL

# Model for each stage
class RoadmapStage(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., 'Stage 1', 'Stage 2'
    description = models.TextField(blank=True)           # Optional stage description
    badge_image = models.ImageField(upload_to='badges/', null=True, blank=True)  # Badge for the stage

    def __str__(self):
        return self.name

# Model for each course in a stage
class RoadmapCourse(models.Model):
    stage = models.ForeignKey(RoadmapStage, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)  # Course title
    description = models.TextField(blank=True)  # Course description
    order = models.PositiveIntegerField()  # Order of the course within the stage

    class Meta:
        unique_together = ('stage', 'order')
        ordering = ['order']

    def __str__(self):
        return f"{self.title} (Stage: {self.stage.name})"

# Model for slides in a course
class RoadmapSlide(models.Model):
    course = models.ForeignKey(RoadmapCourse, related_name='slides', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()  # Order of the slide within the course
    content = models.TextField()  # Content of the slide

    class Meta:
        unique_together = ('course', 'order')
        ordering = ['order']

    def __str__(self):
        return f"Slide {self.order} - {self.course.title}"

# Model for stage tests (MCQs)
class RoadmapTest(models.Model):
    stage = models.OneToOneField(RoadmapStage, related_name='test', on_delete=models.CASCADE)
    passing_score = models.PositiveIntegerField(default=50)  # Minimum score to pass the test

    def __str__(self):
        return f"Test for {self.stage.name}"

# Model for test questions
class TestQuestion(models.Model):
    test = models.ForeignKey(RoadmapTest, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1, choices=(('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')))

    def __str__(self):
        return f"Question {self.id} - {self.test.stage.name}"

# Model to track user progress big changeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='roadmap_progress', on_delete=models.CASCADE)
    stage = models.ForeignKey(RoadmapStage, related_name='user_progress', on_delete=models.CASCADE)
    current_course = models.ForeignKey(RoadmapCourse, null=True, blank=True, on_delete=models.SET_NULL)
    is_stage_completed = models.BooleanField(default=False)  # If the stage is fully completed
    badge_earned = models.BooleanField(default=False)  # If the badge is earned for this stage
    current_slide = models.ForeignKey(RoadmapSlide, null=True, blank=True, on_delete=models.SET_NULL) 
    completed_courses = models.ManyToManyField('RoadmapCourse', blank=True, related_name='completed_by_users')
  
    class Meta:
        unique_together = ('user', 'stage')

    def __str__(self):
        return f"{self.user.username} - {self.stage.name}"



# models.py additions

class TestAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(RoadmapTest, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    passed = models.BooleanField(default=False)
    attempt_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-attempt_date']

    def __str__(self):
        return f"{self.user.username} - {self.test.stage.name} - {self.score}%"

class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stage = models.ForeignKey(RoadmapStage, on_delete=models.CASCADE)
    earned_date = models.DateTimeField(auto_now_add=True)
    #user_name = models.CharField(max_length=255, blank=True)  # Add this field
    #created_at = models.DateTimeField(auto_now_add=True) #remove this and above only
    class Meta:
        unique_together = ('user', 'stage')

    def __str__(self):
        return f"{self.user.username} - {self.stage.name} Badge"


