# main/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CodingQuestion(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    test_cases = models.JSONField(default=list)  # Ensure this field is added

    def __str__(self):
        return self.title

# main/models.py



class customuser(AbstractUser):
    college = models.CharField(max_length=100)
    profile_pic = models.FileField(upload_to='profile_pics/', blank=True, null=True)



#notifications

from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}" 
    
    
    
    
    
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    #image = models.ImageField(upload_to='course_images/', null=True, blank=True)  # Optional course image

    def __str__(self):
        return self.title

class Slide(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='slides')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.title} - Slide {self.order}: {self.title}"
    
 
 
from django.conf import settings   
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {'Completed' if self.completed else 'In Progress'}"