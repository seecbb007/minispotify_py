from django.urls import path
from . import views
from . import authorization  
from django.urls import path
from .views import recommendation_view
from .views import audio_recognition_view


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
        path('audio-recognition/', audio_recognition_view, name='audio_recognition_view'), # For audio recognition
    path('song-recognition/', views.song_recognition_view, name='song_recognition_view'), # For song recognition
    path('recommendation/', views.recommendation_view, name='recommendation_view'), # For recommendation
    path('top-charts/', views.top_charts_view, name='top_charts_view'), # For top charts
]