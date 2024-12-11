from django.urls import path
from . import views
from . import authorization  


urlpatterns = [
    # " " is the main page
    path('', views.main_page_view, name='main_page_view'),
    # "dashboard/" is the dashboard page
    path('dashboard/', views.main_page_view, name='dashboard'),
    # "analyze/" is the image analysis page
    path('analyze/', views.analyze_image_view, name='analyze_image'),
    
    # Spotify Authorization Routes
    path('authorize/', views.authorize, name='authorize'),  # For initiating Spotify auth
    path('callback/', views.callback, name='callback'),    # For handling Spotify's response
    path('refresh_token/', views.refresh_token, name='refresh_token'),   # Token Refresh Route
]