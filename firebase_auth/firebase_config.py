import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
import json

# For production, get Firebase credentials from environment variable
try:
    # Try to get credentials from environment variable
    cred_dict = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', '{}'))
    cred = credentials.Certificate(cred_dict)
except Exception:
    # Fallback to local file for development
    current_dir = os.path.dirname(os.path.abspath(__file__))
    service_account_path = os.path.join(current_dir, '..', 'firebase', 'serviceAccountKey.json')
    cred = credentials.Certificate(service_account_path)

# Initialize Firebase Admin SDK
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()