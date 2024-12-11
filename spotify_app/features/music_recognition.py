from spotify_app.authorization import get_auth_header, get_token
from requests import post, get
import os
from dotenv import load_dotenv

load_dotenv()

AUDD_API_KEY = os.getenv("AUDD_API_KEY")  # Load Audd.io API Key from environment variables

def recognize_song(audio_file_path):
    url = "https://api.audd.io/"
    data = {
        "api_token": AUDD_API_KEY,
        "return": "timecode,lyrics",
    }

    try:
        with open(audio_file_path, "rb") as audio_file:
            files = {"file": audio_file}
            response = post(url, data=data, files=files)
            if response.status_code == 200:
                return response.json()
            return {"error": f"API returned status code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def search_song_details(token, track_name, artist_name=None, limit=1):
    """
    Use Spotify API to find additional details about the identified song.
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"track:{track_name}"
    if artist_name:
        query += f" artist:{artist_name}"

    params = {"q": query, "type": "track", "limit": limit}

    try:
        response = get(url, headers=headers, params=params)
        if response.status_code == 200:
            json_data = response.json()
            tracks = json_data.get("tracks", {}).get("items", [])
            if tracks:
                return tracks[0]  # Return the most relevant track
            return {"error": "No tracks found on Spotify"}
        return {"error": f"Spotify API returned status code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def identify_and_search(audio_file_path):
    # Call Audd.io API to recognize the song
    recognition_result = recognize_song(audio_file_path)
    print("Recognition Result:", recognition_result)  # Debugging output

    # Check if the result is empty
    if recognition_result.get("result") is None:
        return {"error": "No match found. The audio could not be recognized."}

    # Extract track name and artist
    track_name = recognition_result["result"].get("title")
    artist_name = recognition_result["result"].get("artist")

    if not track_name:
        return {"error": "Recognition failed to identify the track name"}

    # Fetch additional details from Spotify
    token = get_token()
    spotify_result = search_song_details(token, track_name, artist_name)
    if "error" in spotify_result:
        return spotify_result

    return {
        "audd_result": recognition_result["result"],
        "spotify_details": spotify_result,
    }