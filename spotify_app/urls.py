# Import the path function from Django's urls module to define URL patterns
from django.urls import path
# Import the views from the current directory (this app) to connect them to URLs
from . import views

urlpatterns = [
    # Maps the URL path 'search/' to the view function 'search_artist_view' in views.py
    # When a user visits '/search/', the 'search_artist_view' function will be executed
    
    path("search/", views.search_artist_view, name="search_artist"),
]
