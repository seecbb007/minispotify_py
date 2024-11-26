# Import the path function from django.urls module
# This function is used to define URL patterns
from django.urls import path
# Import views from the current app
# This allows us to reference view functions in the URL patterns
from . import views
# Define the app name for namespacing
# This is useful when you have multiple apps and want to avoid naming conflicts
app_name = 'firebase_auth'
# Define the URL patterns for the app
urlpatterns = [
    # When the user visits 'register/', the register view function will be called
    path('register/', views.register, name='register'),
    # When the user visits 'login/', the login_view function will be called
    path('login/', views.login_view, name='login'),
    # When the user visits 'logout/', the logout_view function will be called
    path('logout/', views.logout_view, name='logout'),
]