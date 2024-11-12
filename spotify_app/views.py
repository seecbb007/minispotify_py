

# from django.shortcuts import render
# from .authorization import get_token
# from .features.search import search
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
#             artist_paginator = Paginator(artist_results, 20)  # 20 artists per page
#             artist_page = request.POST.get("artist_page", 1)

#             try:
#                 artists = artist_paginator.page(artist_page)
#             except PageNotAnInteger:
#                 artists = artist_paginator.page(1)
#             except EmptyPage:
#                 artists = artist_paginator.page(artist_paginator.num_pages)

#             context['artists'] = artists if not isinstance(artist_results, dict) or "error" not in artist_results else None

#         if active_tab == "all_results" or active_tab == "tracks":
#             track_results = search_functions["search_for_tracks"](token, search_query)
#             track_paginator = Paginator(track_results, 20)  # 20 tracks per page
#             track_page = request.POST.get("track_page", 1)

#             try:
#                 tracks = track_paginator.page(track_page)
#             except PageNotAnInteger:
#                 tracks = track_paginator.page(1)
#             except EmptyPage:
#                 tracks = track_paginator.page(track_paginator.num_pages)

#             context['tracks'] = tracks if not isinstance(track_results, dict) or "error" not in track_results else None

#         if active_tab == "all_results" or active_tab == "albums":
#             album_results = search_functions["search_for_albums"](token, search_query)
#             album_paginator = Paginator(album_results, 20)  # 20 albums per page
#             album_page = request.POST.get("album_page", 1)

#             try:
#                 albums = album_paginator.page(album_page)
#             except PageNotAnInteger:
#                 albums = album_paginator.page(1)
#             except EmptyPage:
#                 albums = album_paginator.page(album_paginator.num_pages)

#             context['albums'] = albums if not isinstance(album_results, dict) or "error" not in album_results else None
#     else:
#         # Default context when no search has been made
#         context["default_landing"] = True

#     return render(request, "main_page.html", context)

from django.shortcuts import render
from .authorization import get_token
from .features.search import search
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Main page view function
def main_page_view(request):
    context = {}
    search_functions = search()

    active_tab = request.POST.get("active_tab", "all_results")  # Default to 'all_results' if no tab is clicked
    context["active_tab"] = active_tab

    # Handle search if the form is submitted
    if request.method == "POST" and "search_query" in request.POST:
        search_query = request.POST.get("search_query")
        token = get_token()

        # Artists pagination
        if active_tab == "all_results" or active_tab == "artists":
            artist_results = search_functions["search_for_artist"](token, search_query)
            artist_paginator = Paginator(artist_results, 20)  # 20 artists per page
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
            track_paginator = Paginator(track_results, 20)  # 20 tracks per page
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
            album_results = search_functions["search_for_albums"](token, search_query)
            album_paginator = Paginator(album_results, 20)  # 20 albums per page
            album_page = request.POST.get("album_page", 1)

            try:
                albums = album_paginator.page(album_page)
            except PageNotAnInteger:
                albums = album_paginator.page(1)
            except EmptyPage:
                albums = album_paginator.page(album_paginator.num_pages)

            context['albums'] = albums
            context['album_paginator'] = album_paginator
    else:
        # Default context when no search has been made
        context["default_landing"] = True

    return render(request, "main_page.html", context)
