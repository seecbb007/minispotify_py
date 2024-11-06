# from pj5001_dj.spotify_app.authorization import get_token, get_auth_header
# from features.search import search_for_artist, search_songs_by_artist

# def main():
#     token = get_token() 
#     print("token:", token)  # Displays the access token

#     # Search for an artist
#     # artist_name = "ACDC"  # Example artist name
#     artist_name = ""
#     search_artist_result = search_for_artist(token, artist_name)
    
#     # Check if the result is valid before accessing it
#     if isinstance(search_artist_result, dict) and "id" in search_artist_result:
#         print("Artist Name:", search_artist_result["name"])
#         artist_id = search_artist_result["id"]

#         # Search songs by the artist
#         search_songs_by_artist_result = search_songs_by_artist(token, artist_id)
#         print("Songs by Artist:", search_songs_by_artist_result)
#     else:
#         print("No artist found or there was an error:", search_artist_result)

#     for idx, song in enumerate(search_songs_by_artist_result):
#         print(f"{idx + 1}. {song["name"]}")    

# if __name__ == "__main__":
#     main()
