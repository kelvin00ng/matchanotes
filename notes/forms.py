# forms.py
from django import forms
from .models import Note
from .models import Document
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'richtext'}),
        }
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file', 'youtube_url', 'processed_content']

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        youtube_url = cleaned_data.get('youtube_url')

        # Ensure that at least one field is provided
        if not file and not youtube_url:
            raise forms.ValidationError('You must upload a file or enter a YouTube URL.')

        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)