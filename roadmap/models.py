









# # models.py
# from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings

# class Stage(models.Model):
#     number = models.IntegerField(unique=True)
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     is_active = models.BooleanField(default=True)
    
#     class Meta:
#         ordering = ['number']
    
#     def __str__(self):
#         return f"S{self.number}"
# class Course(models.Model):
#     stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='courses')
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     is_active = models.BooleanField(default=True)
#     #image = models.ImageField(upload_to='course_images/', null=True, blank=True)  # Optional course image
#     class Meta:
#         ordering = ['order_number']
#         unique_together = ['stage', 'order_number']
#     def __str__(self):
#         return self.title
    
# class Slide(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='slides')
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     order = models.PositiveIntegerField()

#     def __str__(self):
#         return f"{self.course.title} - Slide {self.order}: {self.title}"
    
 

# # class Test(models.Model):
# #     stage = models.OneToOneField(Stage, on_delete=models.CASCADE, related_name='test')
# #     title = models.CharField(max_length=200)
# #     description = models.TextField()
# #     passing_score = models.IntegerField(default=70)
# #     duration_minutes = models.IntegerField(default=60)
    
# #     def __str__(self):
# #         return f"Test for Stage {self.stage.number}"
    
#  # class Slide(models.Model):
# #     SLIDE_TYPES = (
# #         ('TEXT', 'Text Content'),
# #         ('VIDEO', 'Video Content'),
# #         ('CODE', 'Code Example'),
# #         ('QUIZ', 'Quick Quiz'),
# #     )
    
# #     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='slides')
# #     title = models.CharField(max_length=200)
# #     content = models.TextField()
# #     slide_type = models.CharField(max_length=10, choices=SLIDE_TYPES)
# #     order_number = models.IntegerField()
# #     created_at = models.DateTimeField(auto_now_add=True)
    
# #     class Meta:
# #         ordering = ['order_number']
# #         unique_together = ['course', 'order_number']
    
# #     def __str__(self):
# #         return f"Slide {self.order_number}: {self.title}"

# # class Test(models.Model):
# #     stage = models.OneToOneField(Stage, on_delete=models.CASCADE, related_name='test')
# #     title = models.CharField(max_length=200)
# #     description = models.TextField()
# #     passing_score = models.IntegerField(default=70)
# #     duration_minutes = models.IntegerField(default=60)
# #     is_active = models.BooleanField(default=True)
# #     created_at = models.DateTimeField(auto_now_add=True)
    
# #     def __str__(self):
# #         return f"Test for Stage {self.stage.number}"

# # class Question(models.Model):
# #     test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
# #     question_text = models.TextField()
# #     order_number = models.IntegerField()
# #     points = models.IntegerField(default=1)
    
# #     class Meta:
# #         ordering = ['order_number']
    
# #     def __str__(self):
# #         return f"Question {self.order_number} for {self.test}"

# # class Choice(models.Model):
# #     question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
# #     choice_text = models.CharField(max_length=200)
# #     is_correct = models.BooleanField(default=False)
    
# #     def __str__(self):
# #         return self.choice_text

# # class UserProgress(models.Model):
# #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# #     stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
# #     course = models.ForeignKey(Course, on_delete=models.CASCADE)
# #     last_slide = models.ForeignKey(Slide, on_delete=models.SET_NULL, null=True)
# #     completed = models.BooleanField(default=False)
# #     test_score = models.IntegerField(null=True, blank=True)
# #     updated_at = models.DateTimeField(auto_now=True)
    
# #     class Meta:
# #         unique_together = ['user', 'stage', 'course']