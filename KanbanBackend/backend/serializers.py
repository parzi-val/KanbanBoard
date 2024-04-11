from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserRegistrationSerializer:
    def __init__(self, data=None):
        self.data = data

    def is_valid(self):
        self.form = UserRegistrationForm(self.data)
        return self.form.is_valid()

    def save(self):
        return self.form.save()
