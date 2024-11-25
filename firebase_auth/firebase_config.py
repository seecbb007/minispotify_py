import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

# Get the absolute path to the service account key file
current_dir = os.path.dirname(os.path.abspath(__file__))
service_account_path = os.path.join(current_dir, '..', 'firebase', 'serviceAccountKey.json')

# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()