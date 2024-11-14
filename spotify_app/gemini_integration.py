import google.generativeai as genai
from django.conf import settings
import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get the API keys from the environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError("GEMINI_API_KEY not set. Please check your .env file or environment variables.")

def analyze_image_with_gemini(file_path):
    try:
        # Upload the image file using the File API
        print(f"Uploading image file: {file_path}")
        uploaded_file = genai.upload_file(file_path)

        # Check if the file was uploaded successfully
        if uploaded_file:
            print(f"Image successfully uploaded. URI: {uploaded_file}")

            # Select the generative model
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Create the prompt using the uploaded image URI
            prompt = [
                uploaded_file,
                "\n\n",
                "Identify the artist or album from the given image and provide the response as a dictionary with keys 'artist_name' and 'album_name'."
            ]

            # Generate content based on the uploaded image and the prompt
            response = model.generate_content(prompt)

            # Log and parse the response
            print(f"Gemini API Response: {response}")

            # Check if response has candidates
            if response and response.candidates:
                for candidate in response.candidates:
                    if candidate.content and hasattr(candidate.content, 'parts'):
                        content_text = candidate.content.parts[0].text

                        # Remove markdown-like code blocks (```json ... ```)
                        if content_text.startswith("```json"):
                            content_text = content_text.replace("```json\n", "").replace("\n```", "")

                        try:
                            # Attempt to parse the cleaned text as a dictionary
                            parsed_response = json.loads(content_text)
                            if isinstance(parsed_response, dict):
                                return parsed_response
                        except json.JSONDecodeError as e:
                            print(f"Failed to parse response as JSON: {e}")

                            # Return raw response if parsing as JSON fails
                            return {"additional_info": content_text}

        return {"error": "Could not parse the response"}

    except Exception as e:
        print(f"Error while calling Gemini API: {e}")
        return {"error": "Exception", "message": str(e)}
