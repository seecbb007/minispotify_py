


from dotenv import load_dotenv  # Load environment variables from a .env file
import os  # Access environment variables
import base64  # Encode the client ID and secret in base64 format
import requests  # Make HTTP requests
import json  # Parse JSON responses
from urllib.parse import urlencode  # Encode parameters into URL query strings
from django.shortcuts import redirect  # Django redirect
from django.views.decorators.csrf import csrf_exempt  # CSRF exemption for POST requests
from django.http import JsonResponse  # Django JsonResponse

load_dotenv()  # Loads environment variables from a .env file into the script
client_id = os.getenv("CLIENT_ID")  # Retrieves the CLIENT_ID environment variable
client_secret = os.getenv("CLIENT_SECRET")  # Retrieves the CLIENT_SECRET environment variable
redirect_uri = os.getenv("REDIRECT_URI")  # Retrieves the REDIRECT_URI environment variable (e.g., http://localhost:8000/callback)

# Spotify URLs
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Spotify API Scopes - for playback, user needs 'user-modify-playback-state' and 'user-read-playback-state'
scopes = "streaming user-read-email user-read-private user-read-playback-state user-modify-playback-state"


# Step 2: Start Authorization Flow
def authorize(request):
    # Redirect user to Spotify authorization page
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scopes,
        "show_dialog": True
    }
    auth_url = f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"
    return redirect(auth_url)

# Step 3: Handle Callback and Get Access Token
def callback(request):
    # Get authorization code from URL
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Authorization failed. No code provided."})

    # Exchange authorization code for access token
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    # Set up headers for token request
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    # Prepare token request data
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    response_data = response.json()
    # Handle unsuccessful token request
    if response.status_code != 200:
        return JsonResponse({'error': response_data.get('error_description', 'Unknown error')})

    # Return access and refresh tokens for further use
    access_token = response_data["access_token"]
    refresh_token = response_data.get("refresh_token")
    return JsonResponse({"access_token": access_token, "refresh_token": refresh_token})

# Function to refresh access token using refresh token
@csrf_exempt # Exempt from CSRF protection as it's an API endpoint
def refresh_token_endpoint(request):
    if request.method == "POST":
        body = json.loads(request.body)
        refresh_token = body.get("refresh_token")
        if not refresh_token:
            return JsonResponse({"error": "No refresh token provided"}, status=400)

        try:
            new_access_token = refresh_token_function(refresh_token)
            return JsonResponse({"access_token": new_access_token})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
# Token Refresh Function
def refresh_token_function(refresh_token):
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    response_data = response.json()

    if response.status_code != 200:
        raise Exception(f"Failed to refresh token: {response_data.get('error_description', 'Unknown error')}")

    return response_data["access_token"]

# Function to get authorization header
def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

# Function to get client credentials token
def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "client_credentials",
    }
    # Make token request
    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    response_data = response.json()

    if response.status_code != 200:
        raise Exception(f"Failed to get token: {response_data.get('error_description', 'Unknown error')}")

    return response_data["access_token"]
