# Project 5001 - AI-Powered Music Discovery Platform

This project combines Spotify's music library with AI image analysis to create an innovative music discovery experience. Users can search for music traditionally or upload images for AI-powered music suggestions.

## Features

### Music Search and Playback
- Search for artists, tracks, and albums
- Real-time music playback with Spotify Web Playback SDK
- Paginated search results
- Detailed music information display

### AI Image Analysis
- Upload images of artists or album covers
- AI-powered recognition using Google's Gemini API
- Automatic music suggestions based on image content

### User Authentication
- Secure login and registration with Firebase
- User session management
- Profile customization options

## Prerequisites

- **Python 3.9+**: Required for running the application
- **Spotify Premium Account**: Required for playback functionality
- **Firebase Account**: For user authentication
- **Google Cloud Account**: For Gemini AI API access
- **Git LFS**: For handling large files

## Installation

### Clone the Repository
```bash
git clone https://github.com/FinalProject5001/project5001.git
cd project5001
# 11/24

install python
pip install django
pip install python-dotenv
pip install requests
pip install google-generativeai
pip install firebase-admin

# Group Music App 🎵

A web application that combines Spotify API integration with AI-powered image analysis to provide a unique music discovery experience.

## Features 🚀

### Core Functionality
- **Spotify Integration**
  - Search for artists, tracks, and albums
  - Play music directly in the browser
  - Paginated search results for better user experience
  - Real-time music playback controls

- **AI Image Analysis**
  - Upload artist/album images for analysis
  - AI-powered recognition using Google's Gemini API
  - Automatic music suggestions based on image content

- **User Authentication**
  - Firebase-based user management
  - Secure login and registration
  - Session management

### User Interface
- **Modern, Responsive Design**
  - Clean and intuitive interface
  - Mobile-friendly layout
  - Tailwind CSS styling

- **Advanced Search**
  - Tabbed interface for different content types
  - Real-time results
  - Filterable content

## Technical Stack 💻

### Frontend
- HTML5
- Tailwind CSS
- JavaScript
- Spotify Web Playback SDK

### Backend
- Django (Python)
- Firebase Authentication
- Google Gemini AI
- Spotify API

### Database
- Firebase Firestore (for user data)
- Django's session management

## Setup and Installation 🛠️

1. **Clone the Repository**
```bash
git clone [repository-url]
cd [project-directory]

2. Environment Setup
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
brew install git-lfs  # For macOS

git lfs install
3. Environment Variables
Create a .env file in the root directory with:

# Spotify API Credentials
# Ask in GROUP CHAT, I will send it to you
CLIENT_ID = "your_spotify_client_id" 
CLIENT_SECRET = "your_spotify_client_secret"

# Google Gemini API Key
GEMINI_API_KEY = "your_gemini_api_key"
4.Tailwind CSS Setup
# Install Tailwind CSS
npm install -D tailwindcss

# Initialize Tailwind CSS
npx tailwindcss init

# Compile CSS
npx tailwindcss -i ./static/css/tailwind.css -o ./static/css/output.css --watch
5. Run Development Server

python manage.py runserver

Project Structure 📁
project_root/
├── spotify_app/               # Main Django app
│   ├── templates/            # HTML templates
│   ├── static/               # Static files (CSS, JS)
│   ├── features/            # Core features
│   │   └── search.py        # Search functionality
│   ├── authorization.py     # Spotify auth
│   └── views.py            # View functions
├── firebase_auth/           # Firebase authentication app
├── static/                  # Global static files
├── templates/              # Global templates
└── manage.py              # Django management


{
  "devDependencies": {
    "tailwindcss": "^3.3.5",
    "@tailwindcss/forms": "^0.5.7"
  },
  "dependencies": {
    "firebase": "^10.7.1"
  }
}

### Frontend Dependencies Installation

1. **Install Node.js Dependencies**
```bash
# Install Tailwind CSS and its forms plugin
npm install -D tailwindcss @tailwindcss/forms

# Install Firebase
npm install firebase