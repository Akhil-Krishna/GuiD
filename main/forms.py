# main/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import customuser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    college = forms.CharField(required=True)
    profile_pic = forms.FileField(required=False)

    class Meta:
        model = customuser
        fields = ('username', 'email', 'college', 'profile_pic', 'password1', 'password2')



class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
    
    
from .models import Notification
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'message', 'link']
