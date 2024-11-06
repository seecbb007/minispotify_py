# Import the render function to render templates with context data
from django.shortcuts import render
# Import authorization functions to get a Spotify access token
from .authorization import get_token
# Import functions to search for artists and songs from the Spotify API
from .features.search import search_for_artist,search_songs_by_artist

# Define the main view function to handle displaying the main page and searching for artists
def main_page_view(request):
    # Create an empty context dictionary to store data that will be passed to the template
    context = {}
    
    # Check if the request method is POST, indicating that the form was submitted
    if request.method == "POST":
        # Get the artist name submitted in the form
        artist_name = request.POST.get("artist_name")
        # Get an access token for Spotify API authorization
        token = get_token()
        # Search for the artist using the Spotify API
        artist_info = search_for_artist(token, artist_name)
         # Check if the artist was found and if the response contains an 'id'
        if isinstance(artist_info, dict) and "id" in artist_info:
            # Add artist information to the context dictionary
            context['artist_name'] = artist_info["name"]
            context['artist_info'] = artist_info

            # Search for sogs by the artist
            # Search for songs by the artist using the artist ID
            artist_id = artist_info['id']
            songs = search_songs_by_artist(token, artist_id)
            # Add the list of songs to the context dictionary
            context['songs'] = songs
        else:
            # If no artist is found, add an error message to the context dictionary
            context['error'] = "No artist found!"
    
    # Render the main page with or without search results
    return render(request, "main_page.html", context)
