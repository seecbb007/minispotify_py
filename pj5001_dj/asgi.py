"""
ASGI config for pj5001_dj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
# Import the os module to interact with the operating system
import os
# Import the ASGI application function from Django
from django.core.asgi import get_asgi_application

# Sets the default settings module for the ASGI application.
# This specifies which settings file should be used for the Django project (pj5001_dj.settings).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pj5001_dj.settings")

# Create an ASGI application instance
# This callable will be used by ASGI servers to communicate with the Django application
application = get_asgi_application()
