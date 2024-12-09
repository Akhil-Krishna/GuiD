from django.contrib import admin
from .models import CodingQuestion

admin.site.register(CodingQuestion)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import customuser
admin.site.register(customuser)


from .models import Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'link', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    
    
from .models import Course,Slide
admin.site.register(Course)
admin.site.register(Slide)



