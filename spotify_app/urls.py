from django.urls import path
from . import views
from . import authorization  # If you've kept the authorization functions in authorization.py
# If you've moved the authorization functions to views.py, you don't need this import

urlpatterns = [
    path('', views.main_page_view, name='main_page_view'),
    path('dashboard/', views.main_page_view, name='dashboard'),
    path('analyze/', views.analyze_image_view, name='analyze_image'),
    
    # Add these new authorization-related URLs
    path('authorize/', views.authorize, name='authorize'),  # For initiating Spotify auth
    path('callback/', views.callback, name='callback'),    # For handling Spotify's response
    path('refresh_token/', views.refresh_token, name='refresh_token'),  # You already have this
]