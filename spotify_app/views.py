

import os
from django.shortcuts import render, redirect
from .authorization import get_token
from .features.search import search
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .gemini_integration import analyze_image_with_gemini
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

from django.conf import settings
from django.contrib import messages
from urllib.parse import urlencode
import base64
import requests



# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/callback"  # Update with your redirect URI

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Main page view function

def main_page_view(request):
    context = {}
    search_functions = search()

    # Get active tab with default to 'all_results'
    active_tab = request.POST.get("active_tab", "all_results")
    context["active_tab"] = active_tab

    # Handle search if the form is submitted
    if request.method == "POST" and "search_query" in request.POST:
        search_query = request.POST.get("search_query")
        token = get_token()

        try:
            # Artists pagination
            if active_tab == "all_results" or active_tab == "artists":
                artist_results = search_functions["search_for_artist"](token, search_query)
                if isinstance(artist_results, list):  # Check if we got a valid result
                    artist_paginator = Paginator(artist_results, 10)
                    artist_page = request.POST.get("artist_page", 1)

                    try:
                        artists = artist_paginator.page(artist_page)
                    except PageNotAnInteger:
                        artists = artist_paginator.page(1)
                    except EmptyPage:
                        artists = artist_paginator.page(artist_paginator.num_pages)

                    context['artists'] = artists
                    context['artist_paginator'] = artist_paginator

            # Tracks pagination
            if active_tab == "all_results" or active_tab == "tracks":
                track_results = search_functions["search_for_tracks"](token, search_query)
                if isinstance(track_results, list):  # Check if we got a valid result
                    track_paginator = Paginator(track_results, 10)
                    track_page = request.POST.get("track_page", 1)

                    try:
                        tracks = track_paginator.page(track_page)
                    except PageNotAnInteger:
                        tracks = track_paginator.page(1)
                    except EmptyPage:
                        tracks = track_paginator.page(track_paginator.num_pages)

                    context['tracks'] = tracks
                    context['track_paginator'] = track_paginator

            # Albums pagination
            if active_tab == "all_results" or active_tab == "albums":
                # Add debug print
                print(f"Searching for albums with query: {search_query}")
                album_results = search_functions["search_for_albums"](token, search_query)
                print(f"Album results count: {len(album_results) if album_results else 0}")

                if isinstance(album_results, list):  # Check if we got a valid result
                    album_paginator = Paginator(album_results, 10)
                    album_page = request.POST.get("album_page", 1)

                    try:
                        albums = album_paginator.page(album_page)
                    except PageNotAnInteger:
                        albums = album_paginator.page(1)
                    except EmptyPage:
                        albums = album_paginator.page(album_paginator.num_pages)

                    context['albums'] = albums
                    context['album_paginator'] = album_paginator

            # Add search query to context for form persistence
            context['search_query'] = search_query

        except Exception as e:
            print(f"Error in search: {str(e)}")
            messages.error(request, "An error occurred while searching. Please try again.")
    else:
        # Default context when no search has been made
        context["default_landing"] = True

    # Pass tokens to the context
    access_token = request.session.get("access_token")
    refresh_token = request.session.get("refresh_token")
    context['access_token'] = access_token
    context['refresh_token'] = refresh_token

    # Debug prints
    print(f"Context keys: {context.keys()}")
    print(f"Albums in context: {'albums' in context}")
    if 'albums' in context:
        print(f"Number of albums: {len(context['albums'])}")

    return render(request, "main_page.html", context)
# Step 2: Start Authorization Flow
def authorize(request):
    # Redirect user to Spotify authorization page
    scopes = " ".join([
        "streaming",                # Required for playback
        "user-read-email",         # Required for user info
        "user-read-private",       # Required for user info
        "user-read-playback-state",     # Required to check playback state
        "user-modify-playback-state",   # Required to control playback
        "user-read-currently-playing",  # Required to check what's playing
        "app-remote-control"            # Required for remote control
    ])
    
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scopes,
        "show_dialog": True  # Forces the authorization dialog to show
    }
    # constructs a URL for Spotify authentication by combining a base URL with encoded query parameters.
    auth_url = f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"
    return redirect(auth_url)

# Step 3: Handle Callback and Get Access Token
def callback(request):
    code = request.GET.get("code")

    if not code:
        return JsonResponse({'error': 'No code provided'})

    # Exchange authorization code for access token
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    response_data = response.json()

    if response.status_code != 200:
        return JsonResponse({'error': response_data.get('error', 'Unknown error')})

    # Save the access token and refresh token in the session
    request.session['access_token'] = response_data['access_token']
    if 'refresh_token' in response_data:
        request.session['refresh_token'] = response_data['refresh_token']

    # Redirect to main page
    return redirect('main_page_view')

# Step 4: Refresh Access Token.
# OAuth for authentication (such as with Spotify), access tokens have a limited lifespan and need to be refreshed periodically to maintain access without requiring the user to re-authenticate.
def refresh_token(request):
    refresh_token = request.session.get('refresh_token')
    if not refresh_token:
        return JsonResponse({'error': 'No refresh token available'}, status=400)

    try:
        # Combines the client ID and client secret into a single string separated by a colon.
        auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
        # Encodes the combined string into bytes using UTF-8 encoding.
        auth_bytes = auth_string.encode("utf-8")
        #  Encodes the bytes object into a Base64-encoded string.
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
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx, is used to raise an exception if the HTTP request returned an unsuccessful status code. 
        # is used to parse the JSON content of an HTTP response and store it in the variable response_data.
        response_data = response.json()

        # Update the session with new tokens
        request.session['access_token'] = response_data['access_token']
        if 'refresh_token' in response_data:
            request.session['refresh_token'] = response_data['refresh_token']

        return JsonResponse({
            'access_token': response_data['access_token']
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)
# View function for analyzing image


def analyze_image_view(request):
    context = {'image_uploaded': False}  # Initialize context with default values

    if request.method == 'POST':
        # File presence validation
        if 'image_file' not in request.FILES and not request.POST.get('current_image'):
            messages.error(request, "Please upload an image file.")
            return render(request, 'main_page.html', context)
        
        # Handle pagination request
        current_image = request.POST.get('current_image')
        if current_image:
            file_url = current_image
            filename = os.path.basename(current_image)
            analysis_result = request.session.get('analysis_result')
        else:
            # File extension validation
            image_file = request.FILES['image_file']
            if not image_file.name.lower().endswith('.png'):
                messages.error(request, "Only PNG files are allowed.")
                return render(request, 'main_page.html', context)
            
            # Save the uploaded file
            # Creates an instance of FileSystemStorage that will store files in the directory specified by settings.MEDIA_ROOT.
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            #  This method saves the uploaded file to the storage system.
            filename = fs.save(image_file.name, image_file)
            # This method returns the URL to access the file.
            file_url = fs.url(filename)

            # Debug: Log the image upload information
            print(f"Image saved at: {file_url}")

            try:
                # Call Gemini API to analyze the image, This combines the MEDIA_ROOT directory and the filename to create the full path to the image file.
                analysis_result = analyze_image_with_gemini(os.path.join(settings.MEDIA_ROOT, filename))
                # Store analysis result in session for pagination,save the analysis result in the user's session so that it can be accessed later, even across different requests. 
                # This is useful for persisting data that needs to be available throughout the user's sessio
                request.session['analysis_result'] = analysis_result
            except Exception as e:
                print(f"Error in image analysis: {str(e)}")
                messages.error(request, "Error analyzing the image. Please try again.")
                return render(request, 'main_page.html', context)

        # Debug: Log the Gemini API response
        print(f"Gemini API Response: {analysis_result}")

        # Prepare context with analysis result, artist name, and album name for display
        artist_name = None
        album_name = None
        additional_info = analysis_result.get('additional_info', "N/A")

        if 'artist_name' in analysis_result:
            artist_name = analysis_result['artist_name']
        if 'album_name' in analysis_result and analysis_result['album_name'] and analysis_result['album_name'].strip() != '-':
            album_name = analysis_result['album_name']

        # Update context with basic analysis
        context.update({
            'image_url': file_url,
            'analysis_result': {
                'artist': artist_name if artist_name else "N/A",
                'album': album_name if album_name else None,
                'additional_info': additional_info
            },
            'image_uploaded': True,
        })

        # If Gemini found an artist, use Spotify API to search
        if artist_name:
            token = get_token()
            search_functions = search()
            
            # Get artists with pagination
            artist_results = search_functions['search_for_artist'](token, artist_name)
            
            if isinstance(artist_results, list):
                # Paginate the artist results with 10 artists per page
                artist_paginator = Paginator(artist_results, 10)  # 10 artists per page
                artist_page = request.POST.get('artist_page', 1)

                try:
                    artists = artist_paginator.page(artist_page)
                except PageNotAnInteger:
                    artists = artist_paginator.page(1)
                except EmptyPage:
                    artists = artist_paginator.page(artist_paginator.num_pages)

                context['artists'] = artists
                context['artist_paginator'] = artist_paginator
                print(f"Artists pagination - Total: {artist_paginator.count}, Pages: {artist_paginator.num_pages}")

            # Get tracks related to the artist with pagination
            track_results = search_functions['search_for_tracks'](token, f"artist:{artist_name}")
            if isinstance(track_results, list):
                track_paginator = Paginator(track_results, 10)  # 10 tracks per page
                track_page = request.POST.get('track_page', 1)

                try:
                    tracks = track_paginator.page(track_page)
                except PageNotAnInteger:
                    tracks = track_paginator.page(1)
                except EmptyPage:
                    tracks = track_paginator.page(track_paginator.num_pages)

                context['tracks'] = tracks
                context['track_paginator'] = track_paginator
                print(f"Tracks pagination - Total: {track_paginator.count}, Pages: {track_paginator.num_pages}")

            # Get access token for playback
            access_token = request.session.get('access_token', token)
            refresh_token = request.session.get('refresh_token')

            # Update context with remaining data
            context.update({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'active_tab': 'all_results',
                'current_image': file_url  # Add this for pagination form
            })

            # Debug logging
            print(f"Context keys: {context.keys()}")
            print(f"Artists in context: {'artists' in context}")
            print(f"Tracks in context: {'tracks' in context}")
            if 'artists' in context:
                print(f"Number of artists per page: {len(context['artists'])}")
            if 'tracks' in context:
                print(f"Number of tracks per page: {len(context['tracks'])}")

    return render(request, 'image_analysis.html', context)