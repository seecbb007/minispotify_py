"""
URL configuration for pj5001_dj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Import the admin module to include Django's built-in admin site
from django.contrib import admin
# Import path to define URL patterns and views for the project
from django.urls import path
# Import the views from spotify_app to connect them to URLs
from spotify_app import views

urlpatterns = [
    # Path to the Django admin site. Typically used for site management by administrators
    path('admin/', admin.site.urls),
    # Path for the root URL ('/') to display the main page view
    # When the user accesses the root URL, it will render the main page view from spotify_app
    path('', views.main_page_view, name='home'),  # Set root URL to the main page
]
