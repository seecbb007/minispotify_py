import requests
import os
import base64
import time
from dotenv import load_dotenv

# Load the .env file for API tokens
load_dotenv()

LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

LASTFM_BASE_URL = "http://ws.audioscrobbler.com/2.0/"

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_BASE_URL = "https://api.spotify.com/v1/"

# Global variables to cache the Spotify access token
SPOTIFY_ACCESS_TOKEN = None
SPOTIFY_TOKEN_EXPIRES_AT = 0

def get_spotify_access_token():
    """
    Obtain the Spotify API access token using Client Credentials Flow
    and cache it to reduce the number of requests.
    """
    global SPOTIFY_ACCESS_TOKEN, SPOTIFY_TOKEN_EXPIRES_AT
    current_time = time.time()
    
    if SPOTIFY_ACCESS_TOKEN and current_time < SPOTIFY_TOKEN_EXPIRES_AT:
        return SPOTIFY_ACCESS_TOKEN
    
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    
    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        token_info = response.json()
        SPOTIFY_ACCESS_TOKEN = token_info.get("access_token")
        expires_in = token_info.get("expires_in", 3600)  # Default 1 hour
        SPOTIFY_TOKEN_EXPIRES_AT = current_time + expires_in - 60  # Expires 60 seconds early
        return SPOTIFY_ACCESS_TOKEN
    else:
        print(f"Error: Failed to obtain Spotify access token. Status Code: {response.status_code}")
        return None

def get_similar_songs(artist, track, limit=5):
    """
    Retrieve similar songs using the Last.fm API.
    :param artist: Name of the artist
    :param track: Name of the track
    :param limit: Number of results to return
    :return: List of similar songs [{"name": track name, "artist": artist name}, ...]
    """
    params = {
        "method": "track.getsimilar",
        "artist": artist,
        "track": track,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }
    response = requests.get(LASTFM_BASE_URL, params=params)

    if response.status_code == 200:
        tracks = response.json().get("similartracks", {}).get("track", [])
        # Ensure each returned song contains both "name" and "artist"
        return [
            {"name": track.get("name"), "artist": track.get("artist", {}).get("name", "Unknown Artist")}
            for track in tracks
        ]
    else:
        print(f"Error: Failed to fetch similar songs for '{track}' by '{artist}'. Status Code: {response.status_code}")
        return []

def get_spotify_track_details(track_name, artist_name):
    """
    Use the Spotify API to search for a track and retrieve detailed information.
    :param track_name: Name of the track
    :param artist_name: Name of the artist
    :return: Detailed track information or None
    """
    access_token = get_spotify_access_token()
    if not access_token:
        return None

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    query = f"track:{track_name} artist:{artist_name}"
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }
    response = requests.get(f"{SPOTIFY_BASE_URL}search", headers=headers, params=params)
    if response.status_code == 200:
        tracks = response.json().get("tracks", {}).get("items", [])
        if tracks:
            track = tracks[0]
            # Get release_year
            release_date = track['album']['release_date']
            release_year = release_date.split('-')[0] if release_date else "Unknown"

            # Retrieve artist names (combine multiple artist names into one string)
            artist_names = ", ".join([artist['name'] for artist in track['artists']])

            return {
                "id": track['id'],
                "name": track['name'],
                "artist": artist_names,  # Modified to a single string
                "album": {
                    "name": track['album']['name'],
                    "images": [{"url": img['url']} for img in track['album']['images']],
                    "release_year": release_year
                },
                "popularity": track['popularity'],
                "spotify_url": track['external_urls']['spotify'],
                "embed_url": f"https://open.spotify.com/embed/track/{track['id']}"
            }
    else:
        print(f"Error: Spotify API request failed for track '{track_name}' by '{artist_name}'. Status Code: {response.status_code}")
    return None

def recommend_songs(user_favorites, limit=5):
    """
    Recommend similar songs based on a list of user-provided tracks
    and retrieve Spotify details for each recommended track.
    :param user_favorites: List of user-provided tracks [{"name": track name, "artist": artist name}]
    :param limit: Number of similar songs to return per track
    :return: List of recommended tracks with Spotify details
    """
    recommendations = []
    for song in user_favorites:
        print(f"Fetching similar songs for: {song['name']} by {song['artist']}")
        similar_songs = get_similar_songs(song['artist'], song['name'], limit=limit)
        for similar_song in similar_songs:
            spotify_track = get_spotify_track_details(similar_song['name'], similar_song['artist'])
            if spotify_track:
                recommendations.append(spotify_track)
            else:
                # If Spotify API details are unavailable, return basic information
                recommendations.append({
                    "name": similar_song['name'],
                    "artist": similar_song['artist'],
                    "spotify_url": None,
                    "embed_url": None
                })
    return recommendations