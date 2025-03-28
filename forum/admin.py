from django.contrib import admin

# Register your models here.
from .models import Vote,Comment,Answer,Question

admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(Answer)
admin.site.register(Question)