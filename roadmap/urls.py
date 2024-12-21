from django.urls import path
from . import views

urlpatterns=[
    path("",views.road,name='road'),
    path("road/<int:id>",views.stage,name="stage")
]