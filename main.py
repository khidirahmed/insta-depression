import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import numpy as np

# ✅ Spotify API Credentials (Replace with your actual credentials)
SPOTIPY_CLIENT_ID = "e0ebcf2b7946453fa93e38ef53afeab8"
SPOTIPY_CLIENT_SECRET = "eddfa6da3eb3415b9ded00a543bf926f"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

# ✅ Define Required Scopes
SCOPE = "user-library-read playlist-read-private user-read-private user-top-read user-read-recently-played"

# ✅ Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

# ✅ Fetch Access Token
token_info = sp.auth_manager.get_access_token()
access_token = token_info['access_token']
print("\n🔑 **Successfully Authenticated! Your Access Token:**")
print(token_info)


# ✅ Function to Fetch Your Top Tracks
def get_top_tracks():
    url = "https://api.spotify.com/v1/me/top/tracks?limit=20"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tracks = response.json()
        print("\n✅ **Your Top Tracks:**")
        track_ids = []
        track_names = []
        track_popularity = []
        track_explicit = []
        for i, track in enumerate(tracks['items']):
            track_ids.append(track['id'])
            track_names.append(track['name'])
            track_popularity.append(track['popularity'])
            track_explicit.append(track['explicit'])  # Explicit Content Indicator
            print(
                f"{i + 1}. {track['name']} - {track['artists'][0]['name']} {'(Explicit)' if track['explicit'] else ''}")
        return track_ids, track_names, track_popularity, track_explicit
    else:
        print(f"\n🚨 ERROR: Status {response.status_code} - {response.text}")
        return [], [], [], []


# ✅ Function to Fetch Track Tempo (BPM)
def get_track_tempo(track_ids):
    url = f"https://api.spotify.com/v1/audio-features?ids={','.join(track_ids)}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        audio_features = response.json()['audio_features']
        tempos = [track['tempo'] for track in audio_features if track and 'tempo' in track]
        return tempos
    else:
        print(f"\n🚨 ERROR: Failed to fetch tempo. Status {response.status_code} - {response.text}")
        return []


# ✅ Function to Analyze Mental Health Risks Based on Music Habits
def analyze_mental_health_risk(track_popularity, track_explicit, tempos):
    if not track_popularity:
        print("\n🚨 No track data found. Cannot analyze depression/anxiety risk.")
        return

    avg_popularity = np.mean(track_popularity)
    avg_tempo = np.mean(tempos) if tempos else 120  # Default to 120 BPM if not available
    explicit_count = sum(track_explicit)

    print("\n🧠 **Depression & Anxiety Analysis Based on Music Habits:**")
    print(f"📊 Average Track Popularity: {avg_popularity:.2f} (0 = Niche, 100 = Mainstream)")
    print(f"🎵 Average Track Tempo: {avg_tempo:.2f} BPM (Lower = More Chill, Higher = More Intense)")
    print(f"🚨 Explicit Tracks: {explicit_count}/{len(track_explicit)}")

    # 🔹 **Depression/Anxiety Indicators**
    depression_risk = False
    anxiety_risk = False

    if avg_popularity < 30 and avg_tempo < 90:
        depression_risk = True
        print("😔 **Your music suggests a tendency toward melancholic and introspective moods.**")

    if avg_tempo > 140:
        anxiety_risk = True
        print("⚡ **High-energy music may indicate stress or anxiety tendencies.**")

    if explicit_count > len(track_explicit) * 0.7:
        print("🔥 **A high percentage of explicit tracks might indicate emotional intensity or frustration.**")

    # ✅ Final Diagnosis Based on Music Patterns
    print("\n🎭 **Final Diagnosis Based on Your Music:**")
    if depression_risk and anxiety_risk:
        print("⚠️ Your playlist suggests both **depressive and anxious tendencies.**")
        print(
            "💡 You might be going through emotional distress. Consider healthy coping mechanisms like journaling, meditation, or reaching out to a friend.")
    elif depression_risk:
        print("💙 Your music suggests **a melancholic or depressive tendency**.")
        print(
            "💡 If you're feeling down often, it might help to talk to someone you trust or try engaging in activities that boost your mood.")
    elif anxiety_risk:
        print("💛 Your music suggests **anxious tendencies**, possibly linked to stress.")
        print(
            "💡 Consider relaxation techniques like deep breathing, reducing caffeine, or mindfulness practices to ease your stress.")
    else:
        print("✅ Your music taste appears **emotionally balanced!**")
        print("💡 Enjoy your music and keep discovering new tracks that uplift your mood!")


# ✅ Fetch Top Tracks, Tempo & Analyze
track_ids, track_names, track_popularity, track_explicit = get_top_tracks()
tempos = get_track_tempo(track_ids) if track_ids else []
analyze_mental_health_risk(track_popularity, track_explicit, tempos)
