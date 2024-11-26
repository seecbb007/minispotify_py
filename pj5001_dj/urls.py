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
# Import the admin module to include the admin site URLs
from django.contrib import admin
# Import the path and include functions from django.urls
# path is used to define individual URL patterns
# include is used to include other URL configurations
from django.urls import path, include  
# Import settings and static functions to serve media files during development
from django.conf import settings
from django.conf.urls.static import static
# Define the URL patterns for the project
urlpatterns = [
    # URL pattern for the admin site
    path('admin/', admin.site.urls),
    # Include the URLs from the spotify_app application
    path('', include('spotify_app.urls')), 
    # Include the URLs from the firebase_auth application 
    path('auth/', include('firebase_auth.urls')),  
    # is used to serve media files during development in a Django project.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files during development
# This is only done when DEBUG is True in settings
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)