from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import auth
from .forms import RegisterForm, LoginForm
from .firebase_config import db

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
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
                    'favorite_tracks': []
                })
                
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('firebase_auth:login')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
    else:
        form = RegisterForm()
    
    return render(request, 'firebase_accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                # Get user by email
                user = auth.get_user_by_email(email)
                
                # Store user info in session
                request.session['user_id'] = user.uid
                request.session['email'] = user.email
                request.session['username'] = user.display_name
                
                messages.success(request, f'Welcome back, {user.display_name}!')
                return redirect('main_page_view')
            except Exception as e:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    
    return render(request, 'firebase_accounts/login.html', {'form': form})

def logout_view(request):
    # Clear session data
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('main_page_view')