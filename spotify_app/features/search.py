from spotify_app.authorization import get_auth_header, get_token
from requests import get
import json
import datetime

# Search for artists, tracks, or albums
def search():
    def search_for_artist(token, artist_name, limit=50, offset=0):
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(token)
        query = {"q": artist_name, "type": "artist", "limit": limit, "offset": offset}

        try:
            response = get(url, headers=headers, params=query)
            if response.status_code == 200:
                json_data = response.json()
                if "artists" in json_data and "items" in json_data["artists"]:
                    json_result = json_data["artists"]["items"]
                    if len(json_result) == 0:
                        return []
                    for artist in json_result:
                        artist['genres'] = artist.get('genres', [])
                    return json_result
                return []
            return []
        except Exception as e:
            print(f"Error in search_for_artist: {str(e)}")
            return []

    def search_for_tracks(token, track_name, limit=50, offset=0):
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(token)
        params = {"q": track_name, "type": "track", "limit": limit, "offset": offset}

        try:
            response = get(url, headers=headers, params=params)
            if response.status_code == 200:
                json_data = response.json()
                if "tracks" in json_data and "items" in json_data["tracks"]:
                    json_result = json_data["tracks"]["items"]
                    
                    # Process tracks and add additional details
                    for track in json_result:
                        duration_ms = track.get('duration_ms', 0)
                        minutes, seconds = divmod(duration_ms // 1000, 60)
                        track['formatted_duration'] = f"{minutes}:{seconds:02d}"
                        track['popularity'] = track.get('popularity', 0)
                        track['preview_url'] = track.get('preview_url')
                    return json_result
                return []
            return []
        except Exception as e:
            print(f"Error in search_for_tracks: {str(e)}")
            return []

    def search_for_albums(token, artist_name, limit=50, offset=0):
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(token)
        # Add artist: prefix to search for albums by this artist
        query = f"artist:{artist_name}"
        params = {
            "q": query,
            "type": "album",
            "limit": limit,
            "offset": offset
        }

        try:
            response = get(url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Error status code: {response.status_code}")
                return []

            json_data = response.json()
            print(f"Album search response: {json_data}")  # Debug print

            if "albums" not in json_data or "items" not in json_data["albums"]:
                return []

            albums = json_data["albums"]["items"]
            processed_albums = []

            for album in albums:
                try:
                    # Process each album
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
                        release_year = release_date.split('-')[0]
                        album_data['release_year'] = release_year
                    else:
                        album_data['release_year'] = 'Unknown'

                    processed_albums.append(album_data)
                except Exception as e:
                    print(f"Error processing album: {str(e)}")
                    continue

            return processed_albums

        except Exception as e:
            print(f"Error in search_for_albums: {str(e)}")
            return []

    return {
        "search_for_artist": search_for_artist,
        "search_for_tracks": search_for_tracks,
        "search_for_albums": search_for_albums
    }