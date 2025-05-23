# main/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CodingQuestion(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    test_cases = models.JSONField(default=list)  # Ensure this field is added
    solution=models.TextField(default="Def func():")

    def __str__(self):
        return self.title

# main/models.py chang

#big changeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
from django.utils import timezone
class customuser(AbstractUser):
    Name=models.CharField(max_length =255,default="Guid User")
    college = models.CharField(max_length=100)
    profile_pic = models.FileField(upload_to='profile_pics/', blank=True, null=True)
    xp=models.IntegerField(default=0)
    
    stage1_time = models.DurationField(default=timezone.timedelta)
    stage2_time = models.DurationField(default=timezone.timedelta)
    stage3_time = models.DurationField(default=timezone.timedelta)
    stage4_time = models.DurationField(default=timezone.timedelta)
    stage5_time = models.DurationField(default=timezone.timedelta)
    stage6_time = models.DurationField(default=timezone.timedelta)
    stage7_time = models.DurationField(default=timezone.timedelta)
    stage8_time = models.DurationField(default=timezone.timedelta)
    
    stage1_attempt=models.PositiveIntegerField(default=0)
    stage2_attempt=models.PositiveIntegerField(default=0)
    stage3_attempt=models.PositiveIntegerField(default=0)
    stage4_attempt=models.PositiveIntegerField(default=0)
    stage5_attempt=models.PositiveIntegerField(default=0)
    stage6_attempt=models.PositiveIntegerField(default=0)
    stage7_attempt=models.PositiveIntegerField(default=0)
    stage8_attempt=models.PositiveIntegerField(default=0)
    
    stage1_score=models.PositiveIntegerField(default=0)
    stage2_score=models.PositiveIntegerField(default=0)
    stage3_score=models.PositiveIntegerField(default=0)
    stage4_score=models.PositiveIntegerField(default=0)
    stage5_score=models.PositiveIntegerField(default=0)
    stage6_score=models.PositiveIntegerField(default=0)
    stage7_score=models.PositiveIntegerField(default=0)
    stage8_score=models.PositiveIntegerField(default=0)
    


#notifications

from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    send_to_all = models.BooleanField(default=False)  # New field to send to all users

    def save(self, *args, **kwargs):
        """
        Override save() to send notification to all users when `send_to_all` is True.
        """
        if self.send_to_all:
            users = customuser.objects.all()  # Get all users
            notifications = [Notification(user=user, message=self.message,link=self.link,created_at=self.created_at,is_read=False) for user in users]
            Notification.objects.bulk_create(notifications)  # Bulk insert for efficiency
        else:
            super().save(*args, **kwargs)  # Save normally if send_to_all is False

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}" 
    
    
    
    
    
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
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