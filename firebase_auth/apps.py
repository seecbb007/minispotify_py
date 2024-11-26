# Import the AppConfig class from django.apps module
from django.apps import AppConfig

# Define a new AppConfig subclass for the firebase_auth app
class FirebaseAuthConfig(AppConfig):
    # Specify the default field type for auto-created primary keys
    default_auto_field = "django.db.models.BigAutoField"
    # Set the name of the app. This should match the app's directory name
    name = "firebase_auth"
