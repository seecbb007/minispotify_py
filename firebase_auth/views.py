# Import necessary modules and functions from Django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import json

# import firebase Admin SDK's auth module
from firebase_admin import auth
# Import custom forms for registration and login
from .forms import RegisterForm, LoginForm
# Import Firestore client from firebase_config
from .firebase_config import db

# Function for user registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            
            try:
                # Create user in Firebase Auth
                user = auth.create_user(
                    email=email,
                    password=password,
                    display_name=username
                )
                
                # Create user document in Firestore
                user_ref = db.collection('users').document(user.uid)
                user_ref.set({
                    'email': email,
                    'username': username,
                    # Initialize with an empty list
                    'favorite_tracks': []
                })
                # Display success message and redirect to login page
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('firebase_auth:login')
            except Exception as e:
                # Display error message if registration fails
                messages.error(request, f'Registration failed: {str(e)}')
    else:
        # If the request method is GET, create an empty form
        form = RegisterForm()
    # Render the registration page with the form
    return render(request, 'firebase_accounts/register.html', {'form': form})

# Function for user login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                # Get user by email
                user = auth.get_user_by_email(email)
                # Store user info in session
                request.session['user_id'] = user.uid
                request.session['email'] = user.email
                request.session['username'] = user.display_name
                # Display success message and redirect to main page
                messages.success(request, f'Welcome back, {user.display_name}!')
                return redirect('main_page_view')
            except Exception as e:
                # Display error message if login fails
                messages.error(request, 'Invalid email or password')
    else:
        # If the request method is GET, create an empty form
        form = LoginForm()
    # Render the login page with the form
    return render(request, 'firebase_accounts/login.html', {'form': form})

# Function for user logout
def logout_view(request):
    # Clear session data
    request.session.flush()
    # Display success message and redirect to main page
    messages.success(request, 'You have been logged out successfully.')
    return redirect('main_page_view')

# Function to like a track
def like_track(request):
    if request.method == 'POST':
        try:
            # Parse the request body
            body = json.loads(request.body)
            track_id = body.get('track_id')
            track_name = body.get('track_name')  # Track name from request
            track_artist = body.get('track_artist')  # Artist name from request

            if not track_id or not track_name or not track_artist:
                return JsonResponse({'success': False, 'error': 'Missing track details.'})

            # Get the currently logged-in user's ID from the session
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({'success': False, 'error': 'User not authenticated.'})

            # Reference the user's 'liked_songs' sub-collection
            liked_songs_ref = db.collection('users').document(user_id).collection('liked_songs')

            # Check if the track already exists in the collection
            existing_track = liked_songs_ref.where('id', '==', track_id).get()
            if existing_track:
                return JsonResponse({'success': False, 'error': 'Track already liked.'})

            # Add the track to the 'liked_songs' collection
            liked_songs_ref.add({
                'id': track_id,
                'name': track_name,
                'artist': track_artist
            })
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def liked_songs_view(request):
    if request.method == 'GET':
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                messages.error(request, 'User not authenticated.')
                return redirect('firebase_auth:login')

            liked_songs_ref = db.collection('users').document(user_id).collection('liked_songs')
            liked_songs = liked_songs_ref.stream()

            liked_songs_list = []
            for song in liked_songs:
                song_data = song.to_dict()
                song_data['embed_url'] = f"https://open.spotify.com/embed/track/{song_data['id']}" if 'id' in song_data else None
                liked_songs_list.append(song_data)

            return render(request, 'firebase_accounts/liked_songs.html', {'liked_songs': liked_songs_list})

        except Exception as e:
            messages.error(request, f'Error fetching liked songs: {str(e)}')
            return redirect('main_page_view')


#pick it for you
from django.shortcuts import render
import random
import requests
import logging
import requests
import os
import base64
import time
from dotenv import load_dotenv

# Load the .env file for API tokens
load_dotenv()

logger = logging.getLogger(__name__)


CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def get_spotify_access_token():
    """
    Get Spotify API access token.
    """
    auth_url = "https://accounts.spotify.com/api/token"
    response = requests.post(auth_url, data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    return response.json().get("access_token")

def search_spotify_track(track_name, artist_name):
    """
    Search for a track on Spotify using track name and artist name.
    """
    access_token = get_spotify_access_token()
    if not access_token:
        return None

    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "q": f"track:{track_name} artist:{artist_name}",
        "type": "track",
        "limit": 1
    }
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        tracks = response.json().get("tracks", {}).get("items", [])
        if tracks:
            return tracks[0]["id"]  # Return Spotify track ID
    return None

def pick_it_for_you(request):
    # Ensure the user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'You need to log in to access recommendations.')
        return redirect('firebase_auth:login')

    try:
        # Fetch liked songs from Firebase
        liked_songs_ref = db.collection('users').document(user_id).collection('liked_songs')
        liked_songs = liked_songs_ref.stream()

        liked_songs_list = []
        for song in liked_songs:
            song_data = song.to_dict()
            liked_songs_list.append(song_data)

        if not liked_songs_list:
            messages.warning(request, 'You have no liked songs. Like some songs to get recommendations!')
            return render(request, 'firebase_accounts/pick_it_for_you.html', {'recommendations': []})

        # Fetch similar songs using Last.fm API
        recommendations = []
        for song in liked_songs_list:
            similar_songs = fetch_similar_songs_lastfm(song['name'], song['artist'])
            if similar_songs:
                recommendations.extend(similar_songs)

        # Deduplicate and limit to 10 recommendations
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec['name'] not in seen:
                seen.add(rec['name'])
                unique_recommendations.append(rec)
        recommendations = unique_recommendations[:10]

        return render(request, 'firebase_accounts/pick_it_for_you.html', {'recommendations': recommendations})

    except Exception as e:
        logger.error(f"Error retrieving recommendations: {str(e)}")
        messages.error(request, 'An error occurred while fetching recommendations.')
        return redirect('main_page_view')


logger = logging.getLogger(__name__)

def fetch_similar_songs_lastfm(track_name, artist_name):
    """
    Fetch similar songs using the Last.fm API and enrich with Spotify embed URLs.
    """
    try:
        API_KEY = "a53a38c3f6cb64b7daadf34cc14c5796"
        endpoint = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "track.getSimilar",
            "track": track_name,
            "artist": artist_name,
            "api_key": API_KEY,
            "format": "json",
            "limit": 5
        }
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            similar_tracks = data.get('similartracks', {}).get('track', [])
            recommendations = []
            for track in similar_tracks:
                spotify_id = search_spotify_track(track['name'], track['artist']['name'])
                embed_url = f"https://open.spotify.com/embed/track/{spotify_id}" if spotify_id else None
                recommendations.append({
                    "name": track['name'],
                    "artist": track['artist']['name'],
                    "embed_url": embed_url
                })
            return recommendations
        else:
            logger.error(f"Last.fm API error: {response.status_code} {response.text}")
            return []
    except Exception as e:
        logger.error(f"Error fetching similar songs from Last.fm: {str(e)}")
        return []