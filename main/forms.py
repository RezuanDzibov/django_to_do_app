from django import forms
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ('name', 'description', 'image', 'status')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'exampleFormControlInput1'
            }),
            'text_body': forms.Textarea(attrs={'class': 'form-control', 'id': 'exampleFormControlTextarea1'}),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'type': 'file',
                'id': 'formFile'
            })
        }


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'text'}),
        }

    def clean(self):
        cd = super().clean()
        if cd['email']:
            email = cd.get('email')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('An account with the same email address already exists.')