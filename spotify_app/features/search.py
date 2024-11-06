
from spotify_app.authorization import get_auth_header, get_token  # Import necessary functions from authorization.py
from requests import get  # Import GET request function
import json

# Search for artist
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)  # Use the imported get_auth_header function
    query = {"q": artist_name, "type": "artist", "limit": 1}  # Query parameters as a dictionary

    # Send the GET request to Spotify’s search endpoint with parameters and headers
    response = get(url, headers=headers, params=query)
    
    # Check if the request was successful
    if response.status_code == 200:
        print(response.json())
        json_result = response.json()["artists"]["items"]
        if len(json_result) == 0:
            return "No Artist Found!"  # Return message if no artists found
        return json_result[0]  # Return the first artist found
    else:
        # Return error details if the request was not successful
        return {"error": response.status_code, "message": response.reason}

# Search for Songs

def search_songs_by_artist(token, artist_id):
    # Bae URl, specific artist, pass artists id and want top tracks
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    
    json_result = json.loads(result.content)["tracks"]
    return json_result

