# Import necessary modules and functions from Django
from django.shortcuts import render, redirect
from django.contrib import messages
# import firebase Admin SDK's auth module
from firebase_admin import auth
# Import custom forms for registration and login
from .forms import RegisterForm, LoginForm
# Import Firestore client from firebase_config
from .firebase_config import db

# Function for user registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            
            try:
                # Create user in Firebase Auth
                user = auth.create_user(
                    email=email,
                    password=password,
                    display_name=username
                )
                
                # Create user document in Firestore
                user_ref = db.collection('users').document(user.uid)
                user_ref.set({
                    'email': email,
                    'username': username,
                    # Initialize with an empty list
                    'favorite_tracks': []
                })
                # Display success message and redirect to login page
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('firebase_auth:login')
            except Exception as e:
                 # Display error message if registration fails
                messages.error(request, f'Registration failed: {str(e)}')
    else:
        # If the request method is GET, create an empty form
        #  This allows the user to fill out the form and submit it, which will then be handled by the POST request logic.
        form = RegisterForm()
    #  Render the registration page with the form
    return render(request, 'firebase_accounts/register.html', {'form': form})

# function for user login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # is_valid() is a default method provided by Django's Form class. It is used to validate form data.
        if form.is_valid():
            # Get cleaned data from the form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                # Get user by email
                user = auth.get_user_by_email(email)
                # Store user info in session
                request.session['user_id'] = user.uid
                request.session['email'] = user.email
                request.session['username'] = user.display_name
                # Display success message and redirect to main page
                messages.success(request, f'Welcome back, {user.display_name}!')
                return redirect('main_page_view')
            except Exception as e:
                # Display error message if login fails
                messages.error(request, 'Invalid email or password')
    else:
        # If the request method is GET, create an empty form
        form = LoginForm()
    #  Render the login page with the form
    return render(request, 'firebase_accounts/login.html', {'form': form})

def logout_view(request):
    # Clear session data
    request.session.flush()
    # Display success message and redirect to main page
    messages.success(request, 'You have been logged out successfully.')
    return redirect('main_page_view')