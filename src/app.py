import spotipy
from spotipy.oauth2 import SpotifyOAuth
import openai
import os
from flask import Flask, request, redirect, session, jsonify, make_response
from dotenv import load_dotenv
from flask_cors import CORS
from flask_session import Session

# Load environment variables from .env file
load_dotenv()

# Spotify API Credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Flask App
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SESSION_COOKIE_NAME'] = "SpotifyLogin"
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Allow cross-site cookies
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True for HTTPS in production

app.config['SESSION_TYPE'] = 'filesystem'  # Store session data on disk
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = "spotify_"
app.config['SESSION_FILE_DIR'] = "./flask_session"  # Creates a directory to store sessions

Session(app)  # Initialize session

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True if using HTTPS

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-recently-played"
)

@app.route('/')
def login():
    """
    Redirects the user to Spotify's login page for authentication.
    """
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get("code")
    if not code:
        return "Authorization code not found", 400

    try:
        token_info = sp_oauth.get_access_token(code, as_dict=True)
        session["token_info"] = token_info
        print("Token retrieved and saved:", token_info)
        return redirect("http://localhost:3000/")  # Redirect back to the frontend
    except Exception as e:
        print("Error during token exchange:", str(e))
        return "Error during Spotify authentication", 500

def get_spotify_client():
    """
    Creates a Spotify client using the access token stored in the session.
    Automatically refreshes the token if expired.
    """
    token_info = session.get("token_info")
    if not token_info:
        print("Error: No token_info in session")
        return None

    try:
        if sp_oauth.is_token_expired(token_info):
            print("Token expired, refreshing...")
            token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
            session["token_info"] = token_info
            print("Token refreshed:", token_info)
        return spotipy.Spotify(auth=token_info["access_token"])
    except Exception as e:
        print("Error creating Spotify client:", str(e))
        return None

def get_recent_tracks():
    """
    Fetches the user's recently played tracks from Spotify.
    """
    sp = get_spotify_client()
    if not sp:
        print("Error: Spotify client is None (token missing or invalid)")
        return None

    try:
        results = sp.current_user_recently_played(limit=10)
        tracks = [
            f"{item['track']['name']} by {item['track']['artists'][0]['name']}"
            for item in results["items"]
        ]
        print("Tracks retrieved:", tracks)
        return tracks
    except Exception as e:
        print("Error fetching tracks:", str(e))
        return None

def analyze_mood_with_ai(tracks):
    """
    Sends the list of tracks to OpenAI's GPT model for mood analysis.
    """
    tracks_text = "\n".join(tracks)
    prompt = f"""
    Based on the following recently played songs, analyze the user's mood in terms of Depression, Anxiety, and Happiness. 
    Give three percentage scores (must add to 100%) and a brief explanation.

    Songs:
    {tracks_text}
    
    Response format:
    Depression: X%
    Anxiety: Y%
    Happiness: Z%
    
    Explanation:
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Error analyzing mood with AI:", str(e))
        return None

@app.route('/analyze')
def analyze_mood():
    """
    Endpoint to analyze the user's mood based on their recently played tracks.
    """
    print("Starting mood analysis...")
    tracks = get_recent_tracks()
    if not tracks:
        return make_response(jsonify({"error": "Please log into Spotify again to analyze your mood."}), 400)

    mood_analysis = analyze_mood_with_ai(tracks)
    if not mood_analysis:
        return make_response(jsonify({"error": "Error analyzing mood. Try again later."}), 500)

    # Parse the mood analysis result
    mood_data = {"Depression": 0, "Anxiety": 0, "Happiness": 0, "Explanation": ""}
    try:
        lines = mood_analysis.split("\n")
        for line in lines:
            if "Depression" in line:
                mood_data["Depression"] = int(line.split(":")[1].strip().replace("%", ""))
            elif "Anxiety" in line:
                mood_data["Anxiety"] = int(line.split(":")[1].strip().replace("%", ""))
            elif "Happiness" in line:
                mood_data["Happiness"] = int(line.split(":")[1].strip().replace("%", ""))
            else:
                mood_data["Explanation"] += line + " "
        print("Final mood data:", mood_data)
        return jsonify(mood_data)
    except Exception as e:
        print("Error parsing mood analysis:", str(e))
        return make_response(jsonify({"error": "Error parsing mood analysis."}), 500)

@app.route("/debug-session")
def debug_session():
    return str(session.get("token_info", "No token found"))

if __name__ == "__main__":
    app.run(debug=True)
