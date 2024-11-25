# Project 5001 - Spotify Search Feature

This project is a Spotify search application that allows users to search for artists, songs, and albums using the Spotify API. It is built using Django for the backend, React for the frontend, and styled with Tailwind CSS.

## Prerequisites

- **Python 3.9+**: Make sure you have Python installed.
- **Node.js and npm**: Required for managing frontend packages.
- **Git LFS**: Needed to handle large files in your repository.
- **Django 4.x**: Backend framework.
## Installation

### Clone the Repository
```bash
git clone https://github.com/FinalProject5001/project5001.git
cd project5001

### Set Up Python Virtual Environment

To create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # For Windows use: venv\Scripts\activate
### Install Python Dependencies

Install all necessary Python packages with:
```bash
pip install -r requirements.txt
### Install Node.js Dependencies

To install all necessary Node.js packages, run:
```bash
npm install
### Database Setup

Apply Django migrations to set up the database:
```bash
python manage.py migrate
### Install Git LFS

To install Git LFS, run:
```bash
brew install git-lfs
git lfs install
### Environment Variables

Create a `.env` file in the root directory of the project with the following content:
```bash
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
## Running the Project

### Run the Django Server
Start the server with:
```bash
python manage.py runserver
### Compile Tailwind CSS

To compile Tailwind CSS, use the following command:
```bash
npx tailwindcss -i ./static/css/tailwind.css -o ./static/css/output.css --watch
### Compile Tailwind CSS

To compile Tailwind CSS, use the following command:
```bash
npx tailwindcss -i ./static/css/tailwind.css -o ./static/css/output.css --watch
## Project Structure

- `pj5001_dj/`: Contains the main Django project settings and URLs.
- `spotify_app/`: The main app containing views, models, templates, etc.
- `static/`: Holds all static files including CSS, JavaScript, and images.

Set Up Python Virtual Environment
bash

python3 -m venv venv
source venv/bin/activate  # For Windows use: venv\Scripts\activate

Install Python Dependencies
bash

pip install -r requirements.txt
Install Node.js Dependencies
bash

npm install
Database Setup
bash

python manage.py migrate

Install Git LFS
To install Git LFS, run:

bash

brew install git-lfs
git lfs install

Run the Django Server
Start the server with:


python manage.py runserver

# 11/24

install python
pip install django
pip install python-dotenv
pip install requests
pip install google-generativeai
pip install firebase-admin