from dotenv import load_dotenv  # Imports load_dotenv to load environment variables from a .env file
import os  # Imports os module to access environment variables
import base64  # Imports base64 to encode the client ID and secret in base64 format
from requests import post  # Imports the post function from requests to make HTTP POST requests
import json  # Imports json to parse JSON responses

load_dotenv()  # Loads environment variables from a .env file into the script
client_id = os.getenv("CLIENT_ID")  # Retrieves the CLIENT_ID environment variable
client_secret = os.getenv("CLIENT_SECRET")  # Retrieves the CLIENT_SECRET environment variable

def get_token():
    # Combines client_id and client_secret with a colon in between for Basic Auth
    auth_string = client_id + ":" + client_secret
    # Encodes the combined string to bytes using UTF-8 encoding for security
    auth_bytes = auth_string.encode("utf-8")
    # Encodes the byte string in base64 format and converts it back to a UTF-8 string for security
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # Sets the URL for Spotify's token request endpoint
    url = "https://accounts.spotify.com/api/token"
    # Prepares the headers with the base64-encoded authorization and content type
    headers = {
        "Authorization": "Basic " + auth_base64,  # Sets the authorization header with Basic Auth
        "Content-Type": "application/x-www-form-urlencoded"  # Sets content type for form data
    }
    # Prepares the data for the POST request, specifying the client credentials grant type
    data = {
        "grant_type": "client_credentials"  # Specifies the type of OAuth token grant
    }
    # Sends a POST request to Spotify’s token endpoint with headers and data
    result = post(url, headers=headers, data=data)
    # Parses the response content as JSON to extract the access token
    json_result = json.loads(result.content)
    token = json_result["access_token"]  # Retrieves the access token from the JSON response
    return token  # Returns the access token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}



