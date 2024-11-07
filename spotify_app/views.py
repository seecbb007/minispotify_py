from django.shortcuts import render
from .authorization import get_token
from .features.search import search

# Main page view function
def main_page_view(request):
    context = {}
    search_functions = search()
    
    # Handle search if the form is submitted
    if request.method == "POST":
        search_query = request.POST.get("search_query")
        token = get_token()
        
        # Perform searches for artists, tracks, and albums
        artist_results = search_functions["search_for_artist"](token, search_query)
        track_results = search_functions["search_for_tracks"](token, search_query)
        album_results = search_functions["search_for_albums"](token, search_query)

        # Add the results to the context
        if isinstance(artist_results, dict) and "error" in artist_results:
            context['artist_error'] = "No artists found!"
        else:
            context['artists'] = artist_results

        if isinstance(track_results, dict) and "error" in track_results:
            context['track_error'] = "No tracks found!"
        else:
            context['tracks'] = track_results

        if isinstance(album_results, dict) and "error" in album_results:
            context['album_error'] = "No albums found!"
        else:
            context['albums'] = album_results

    # Render the main page with or without search results
    return render(request, "main_page.html", context)
