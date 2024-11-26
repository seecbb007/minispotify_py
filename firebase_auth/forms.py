# Import the forms module from Django
from django import forms
# Define a form for user registration
class RegisterForm(forms.Form):
    # Email field with label and widget customization
    email = forms.EmailField(
        label='Email', # Label for the email field
        # Use EmailInput widget with custom attributes
        # Add css class for styling
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    # Password field with label and widget customization
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    # Username field with label and widget customization
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )
# Define a form for user login
class LoginForm(forms.Form):
    # Email field with label and widget customization
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    # Password field with label and widget customization
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )