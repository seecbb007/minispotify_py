# Import the get_auth_header and get_token functions from the spotify_app.authorization module
# These functions are used to obtain the authorization header and token for Spotify API requests
from spotify_app.authorization import get_auth_header, get_token
# Import the get function from the requests module
# This function is used to make HTTP GET requests
from requests import get

import json
import datetime

# Search for artists, tracks, or albums
def search():
    # Function to search for artists on Spotify
    # limit50:  It specifies the maximum number of results to return. If not provided, the function will use the default value of 50.
    # offset0: It specifies the index of the first result to return. If not provided, the function will use the default value of 0.
    def search_for_artist(token, artist_name, limit=50, offset=0):
        # Define the URL for the Spotify search API
        url = "https://api.spotify.com/v1/search"
        # Get the authorization header using the provided token
        headers = get_auth_header(token)
        # Define the query parameters for the search request
        query = {"q": artist_name, "type": "artist", "limit": limit, "offset": offset}

        try:
            # Make the GET request to the Spotify search API
            response = get(url, headers=headers, params=query)
            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                # Parse the JSON response
                json_data = response.json()
                # Check if the response contains artist data
                if "artists" in json_data and "items" in json_data["artists"]:
                    json_result = json_data["artists"]["items"]
                    # If no artists are found, return an empty list
                    if len(json_result) == 0:
                        return []
                    # Process each artist and add additional details
                    for artist in json_result:
                        artist['genres'] = artist.get('genres', [])
                    return json_result
                # If no artist data is found, return an empty list
                return []
            # If the response status code is not 200, return an empty list
            return []
        # Handle exceptions and return an empty list
        except Exception as e:
            print(f"Error in search_for_artist: {str(e)}")
            return []
    # Function to search for tracks on Spotify
    def search_for_tracks(token, track_name, limit=50, offset=0):
        # Define the URL for the Spotify search API
        url = "https://api.spotify.com/v1/search"
        # Get the authorization header using the provided token
        headers = get_auth_header(token)
        # Define the query parameters for the search request
        params = {"q": track_name, "type": "track", "limit": limit, "offset": offset}

        try:
            # Make the GET request to the Spotify search API
            response = get(url, headers=headers, params=params)
            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                # Parse the JSON response as json_data
                json_data = response.json()
                # Check if the response contains track data
                if "tracks" in json_data and "items" in json_data["tracks"]:
                    # Get the list of tracks from the response assigned to json_result
                    json_result = json_data["tracks"]["items"]
                    
                    # Process tracks and add additional details
                    for track in json_result:
                        # Get the duration of the track in milliseconds
                        duration_ms = track.get('duration_ms', 0)
                        # Convert the duration to minutes and seconds
                        minutes, seconds = divmod(duration_ms // 1000, 60)
                        # Add formatted duration, popularity, and preview URL to the track data
                        track['formatted_duration'] = f"{minutes}:{seconds:02d}"
                        track['popularity'] = track.get('popularity', 0)
                        track['preview_url'] = track.get('preview_url')
                    # Return the list of processed tracks
                    return json_result
                # If no track data is found, return an empty list
                return []
            # If the response status code is not 200, return an empty list
            return []
        # Handle exceptions and return an empty list
        except Exception as e:
            print(f"Error in search_for_tracks: {str(e)}")
            return []
    # Function to search for albums on Spotify
    def search_for_albums(token, artist_name, limit=50, offset=0):
        # Define the URL for the Spotify search API
        url = "https://api.spotify.com/v1/search"
        # Get the authorization header using the provided token
        headers = get_auth_header(token)
        # Add artist: prefix to search for albums by this artist
        query = f"artist:{artist_name}"
        # Define the query parameters for the search request, including the artist query, type, limit, and offset
        params = {
            "q": query,
            "type": "album",
            "limit": limit,
            "offset": offset
        }

        try:
            # Make the GET request to the Spotify search API
            response = get(url, headers=headers, params=params)
            # Check if the response status code is not 200 (OK)
            if response.status_code != 200:
                # If the response status code is not 200, return an empty list
                print(f"Error status code: {response.status_code}")
                # return an empty list
                return []
            # Parse the JSON response as json_data
            json_data = response.json()
            # Check if the response contains album data,  Debug print
            print(f"Album search response: {json_data}")  
            # Check if the response contains album data
            if "albums" not in json_data or "items" not in json_data["albums"]:
                return []
            # Get the list of albums from the response
            albums = json_data["albums"]["items"]
            # Deine an empty list to store processed albums
            processed_albums = []
            # Process each album and add additional details
            for album in albums:
                try:
                    # Process each album, and get the id, name, images, artists, release date, total tracks, album type, and external URLs
                    album_data = {
                        'id': album.get('id', ''),
                        'name': album.get('name', ''),
                        'images': album.get('images', []),
                        'artists': album.get('artists', []),
                        'release_date': album.get('release_date', ''),
                        'total_tracks': album.get('total_tracks', 0),
                        'album_type': album.get('album_type', ''),
                        'external_urls': album.get('external_urls', {})
                    }

                    # Process release year
                    release_date = album.get('release_date', '')
                    if release_date:
                        # Get the release year from the release date. split() method is used to split the date string by '-',[0] is used to get the first element of the split string
                        release_year = release_date.split('-')[0]
                        # Add the release year to the album data
                        album_data['release_year'] = release_year
                    else:
                        # If the release date is not available, set the release year to 'Unknown'
                        album_data['release_year'] = 'Unknown'
                    # Append the processed album data to the list of processed albums
                    processed_albums.append(album_data)
                    # handle exceptions
                except Exception as e:
                    print(f"Error processing album: {str(e)}")
                    continue
            # Return the list of processed albums
            return processed_albums
        # Handle exceptions and return an empty list
        except Exception as e:
            print(f"Error in search_for_albums: {str(e)}")
            return []
    # Return the search functions as a dictionary
    return {
        "search_for_artist": search_for_artist,
        "search_for_tracks": search_for_tracks,
        "search_for_albums": search_for_albums
    }