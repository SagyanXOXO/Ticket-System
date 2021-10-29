from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket

class RegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 250)
	password = forms.CharField(widget = forms.PasswordInput()) 

class TicketForm(forms.Form):
	subject = forms.CharField(max_length = 250)
	description = forms.TextInput()	