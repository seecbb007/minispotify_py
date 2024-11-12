

# from django.shortcuts import render
# from .authorization import get_token
# from .features.search import search

# # Main page view function
# def main_page_view(request):
#     context = {}
#     search_functions = search()

#     active_tab = request.POST.get("active_tab", "all_results")  # Default to 'all_results' if no tab is clicked
#     context["active_tab"] = active_tab

#     # Handle search if the form is submitted
#     if request.method == "POST" and "search_query" in request.POST:
#         search_query = request.POST.get("search_query")
#         token = get_token()

#         # Perform searches for artists, tracks, and albums if 'all_results' or specific tab
#         if active_tab == "all_results" or active_tab == "artists":
#             artist_results = search_functions["search_for_artist"](token, search_query)
#             context['artists'] = artist_results if not isinstance(artist_results, dict) or "error" not in artist_results else None
        
#         if active_tab == "all_results" or active_tab == "tracks":
#             track_results = search_functions["search_for_tracks"](token, search_query)
#             context['tracks'] = track_results if not isinstance(track_results, dict) or "error" not in track_results else None
        
#         if active_tab == "all_results" or active_tab == "albums":
#             album_results = search_functions["search_for_albums"](token, search_query)
#             context['albums'] = album_results if not isinstance(album_results, dict) or "error" not in album_results else None

#     return render(request, "main_page.html", context)

# from django.shortcuts import render
# from django.core.paginator import Paginator
# from .authorization import get_token
# from .features.search import search

# # Main page view function
# def main_page_view(request):
#     context = {}
#     search_functions = search()

#     active_tab = request.POST.get("active_tab", "all_results")  # Default to 'all_results' if no tab is clicked
#     context["active_tab"] = active_tab

#     # Handle search if the form is submitted
#     if request.method == "POST" and "search_query" in request.POST:
#         search_query = request.POST.get("search_query")
#         token = get_token()

#         # Perform searches for artists, tracks, and albums if 'all_results' or specific tab
#         if active_tab == "all_results" or active_tab == "artists":
#             artist_results = search_functions["search_for_artist"](token, search_query, limit=50)
#             if not isinstance(artist_results, dict) or "error" not in artist_results:
#                 artist_paginator = Paginator(artist_results, 20)  # Show 20 artists per page
#                 artist_page_number = request.POST.get("artist_page") or 1
#                 context['artists'] = artist_paginator.get_page(artist_page_number)
#             else:
#                 context['artists'] = None

#         if active_tab == "all_results" or active_tab == "tracks":
#             track_results = search_functions["search_for_tracks"](token, search_query, limit=50)
#             if not isinstance(track_results, dict) or "error" not in track_results:
#                 track_paginator = Paginator(track_results, 20)  # Show 20 tracks per page
#                 track_page_number = request.POST.get("track_page") or 1
#                 context['tracks'] = track_paginator.get_page(track_page_number)
#             else:
#                 context['tracks'] = None

#         if active_tab == "all_results" or active_tab == "albums":
#             album_results = search_functions["search_for_albums"](token, search_query, limit=50)
#             if not isinstance(album_results, dict) or "error" not in album_results:
#                 album_paginator = Paginator(album_results, 20)  # Show 20 albums per page
#                 album_page_number = request.POST.get("album_page") or 1
#                 context['albums'] = album_paginator.get_page(album_page_number)
#             else:
#                 context['albums'] = None

#     return render(request, "main_page.html", context)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .authorization import get_token
from .features.search import search

# Main page view function
def main_page_view(request):
    context = {}
    search_functions = search()

    active_tab = request.POST.get("active_tab", "all_results")  # Default to 'all_results' if no tab is clicked
    context["active_tab"] = active_tab

  
    if request.method == "POST" and "search_query" in request.POST:
        search_query = request.POST.get("search_query")
        token = get_token()

        # Set up pagination page number
        artist_page = request.POST.get("artist_page", 1)
        track_page = request.POST.get("track_page", 1)
        album_page = request.POST.get("album_page", 1)

        # Perform searches for artists, tracks, and albums if 'all_results' or specific tab
        if active_tab == "all_results" or active_tab == "artists":
            artist_results = search_functions["search_for_artist"](token, search_query)
            paginator = Paginator(artist_results, 20)  # 20 artists per page
            try:
                artists = paginator.page(artist_page)
            except PageNotAnInteger:
                artists = paginator.page(1)
            except EmptyPage:
                artists = paginator.page(paginator.num_pages)
            context['artists'] = artists
            context['artist_paginator'] = paginator

        if active_tab == "all_results" or active_tab == "tracks":
            track_results = search_functions["search_for_tracks"](token, search_query)
            paginator = Paginator(track_results, 10)  # 10 tracks per page
            try:
                tracks = paginator.page(track_page)
            except PageNotAnInteger:
                tracks = paginator.page(1)
            except EmptyPage:
                tracks = paginator.page(paginator.num_pages)
            context['tracks'] = tracks
            context['track_paginator'] = paginator

        if active_tab == "all_results" or active_tab == "albums":
            album_results = search_functions["search_for_albums"](token, search_query)
            paginator = Paginator(album_results, 10)  # 10 albums per page
            try:
                albums = paginator.page(album_page)
            except PageNotAnInteger:
                albums = paginator.page(1)
            except EmptyPage:
                albums = paginator.page(paginator.num_pages)
            context['albums'] = albums
            context['album_paginator'] = paginator

    return render(request, "main_page.html", context)
