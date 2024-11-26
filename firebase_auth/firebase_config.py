# the main Firebase Admin SDK module, 
# which provides the core functionality for interacting with Firebase services.
import firebase_admin
# credentials: This module is used to authenticate your Firebase app with a service account.
# auth: This module provides methods for managing users, such as creating, updating, and deleting users.
# firestore: This module provides methods for interacting with Cloud Firestore, such as reading and writing documents.

from firebase_admin import credentials, auth, firestore
# os module in Python provides a way of using operating system-dependent functionality. 
# It allows you to interact with the underlying operating system in a portable way.
import os

# Get the absolute path to the service account key file
current_dir = os.path.dirname(os.path.abspath(__file__))
service_account_path = os.path.join(current_dir, '..', 'firebase', 'serviceAccountKey.json')

# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()