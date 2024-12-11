# spotify_app/features/topChart.py

import requests
import os
import time
import base64
from dotenv import load_dotenv

load_dotenv()

LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

LASTFM_BASE_URL = "http://ws.audioscrobbler.com/2.0/"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_BASE_URL = "https://api.spotify.com/v1/"

SPOTIFY_ACCESS_TOKEN = None
SPOTIFY_TOKEN_EXPIRES_AT = 0

def get_spotify_access_token():
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
        expires_in = token_info.get("expires_in", 3600)
        SPOTIFY_TOKEN_EXPIRES_AT = current_time + expires_in - 60
        return SPOTIFY_ACCESS_TOKEN
    else:
        print("Error obtaining Spotify token:", response.text)
        return None

def get_top_tracks_by_country(country, limit=10):
    """
    Retrieve the top 10 tracks for a specified country using the Last.fm API.
    """
    params = {
        "method": "geo.gettoptracks",
        "country": country,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }
    response = requests.get(LASTFM_BASE_URL, params=params)
    if response.status_code == 200:
        tracks = response.json().get("tracks", {}).get("track", [])
        # Return a list in the format {name, artist}
        return [{"name": t.get("name"), "artist": t.get("artist", {}).get("name", "Unknown Artist")} for t in tracks]
    else:
        print(f"Error: Failed to fetch top tracks for '{country}'. Status Code: {response.status_code}")
        return []

def get_spotify_track_details(track_name, artist_name):
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
            # Retrieve artist names
            artist_names = ", ".join([artist['name'] for artist in track['artists']])
            return {
                "id": track['id'],
                "name": track['name'],
                "artist": artist_names,
                "embed_url": f"https://open.spotify.com/embed/track/{track['id']}"
            }
    else:
        print(f"Error: Spotify API request failed for track '{track_name}' by '{artist_name}'. Status Code: {response.status_code}")
    return None

def fetch_top_tracks_with_spotify_details(country=None):
    """
    Retrieve the top 10 tracks for a country or globally and fetch detailed information using the Spotify API.
    """
    if country.lower() == "global":
        print("Fetching global top tracks...")
        top_tracks = get_global_top_tracks(limit=10)
    else:
        print(f"Fetching top tracks for country: {country}")
        top_tracks = get_top_tracks_by_country(country, limit=10)

    results = []
    for t in top_tracks:
        detail = get_spotify_track_details(t['name'], t['artist'])
        if detail:
            results.append(detail)
        else:
            # If no details are fetched from Spotify, return basic information
            results.append({
                "name": t['name'],
                "artist": t['artist'],
                "embed_url": None
            })
    return results

def get_global_top_tracks(limit=10):
    """
    Retrieve the top global tracks using the Last.fm API.
    """
    params = {
        "method": "chart.gettoptracks",  # Last.fm global top tracks API
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }
    response = requests.get(LASTFM_BASE_URL, params=params)
    if response.status_code == 200:
        tracks = response.json().get("tracks", {}).get("track", [])
        # Return a list in the format {name, artist}
        return [{"name": t.get("name"), "artist": t.get("artist", {}).get("name", "Unknown Artist")} for t in tracks]
    else:
        print(f"Error: Failed to fetch global top tracks. Status Code: {response.status_code}")
        return []