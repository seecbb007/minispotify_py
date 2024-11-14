
import os
from django.shortcuts import render
from .authorization import get_token
from .features.search import search
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .gemini_integration import analyze_image_with_gemini
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

from django.conf import settings
from django.contrib import messages

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
            artist_paginator = Paginator(artist_results, 10)  # 10 artists per page
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
            track_paginator = Paginator(track_results, 10)  # 10 tracks per page
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
            album_paginator = Paginator(album_results, 10)  # 10 albums per page
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





# View function for analyzing image


def analyze_image_view(request):
    context = {'image_uploaded': False}  # Initialize context with default values

    if request.method == 'POST':
        # File presence validation
        if 'image_file' not in request.FILES:
            messages.error(request, "Please upload an image file.")
            return render(request, 'main_page.html', context)
        
        # File extension validation
        image_file = request.FILES['image_file']
        if not image_file.name.lower().endswith('.png'):
            messages.error(request, "Only PNG files are allowed.")
            return render(request, 'main_page.html', context)
        
        # Save the uploaded file
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(image_file.name, image_file)
        file_url = fs.url(filename)

        # Debug: Log the image upload information
        print(f"Image saved at: {file_url}")

        # Call Gemini API to analyze the image
        analysis_result = analyze_image_with_gemini(os.path.join(settings.MEDIA_ROOT, filename))

        # Debug: Log the Gemini API response
        print(f"Gemini API Response: {analysis_result}")

        # Prepare context with analysis result
        artist_name = album_name = None  # Initialize as None to handle later conditions
        additional_info = analysis_result.get('additional_info', "N/A")

        if 'artist_name' in analysis_result:
            artist_name = analysis_result['artist_name']
        if 'album_name' in analysis_result and analysis_result['album_name']:
            album_name = analysis_result['album_name']

        # Update context, including artist and album only if they exist
        context.update({
            'image_url': file_url,
            'analysis_result': {
                'artist': artist_name if artist_name else "N/A",
                'album': album_name if album_name else None,  # Only include album if it's not None
                'additional_info': additional_info
            },
            'image_uploaded': True,
        })

        # If Gemini found an artist, use Spotify API to search
        if artist_name:
            token = get_token()
            search_functions = search()
            artist_results = search_functions['search_for_artist'](token, artist_name)

            context.update({
                'artists': artist_results,
            })

    return render(request, 'image_analysis.html', context)
