from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'title', 'name', 'email', 'phone', 
            'summary', 'education', 'experience', 'skills'
        ]
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3}),
            'education': forms.Textarea(attrs={'rows': 4}),
            'experience': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 3}),
        }
