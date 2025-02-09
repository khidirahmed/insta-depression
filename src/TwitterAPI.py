import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import tweepy
import openai

load_dotenv()

app = Flask(__name__)
CORS(app)

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

@app.route("/test", methods=["GET"])
def test_env():
    return jsonify({
        "twitter_api_key": TWITTER_API_KEY[:5] + "*****",
        "openai_api_key": OPENAI_API_KEY[:5] + "*****"
    })

def fetch_liked_tweets(username, count=20):
    """Fetch the most recent liked tweets from a public Twitter account."""
    try:
        liked_tweets = api.get_favorites(screen_name=username, count=count)
        return [tweet.text for tweet in liked_tweets]
    except tweepy.errors.TweepyException as e:
        print(f"Error fetching tweets: {e}")
        return []

def analyze_sentiment_with_gpt(text):
    """Use OpenAI's GPT model to analyze sentiment of a tweet."""
    openai.api_key = OPENAI_API_KEY
    prompt = f"""
    Analyze the emotional impact of the following tweet and classify its sentiment:
    
    Tweet: "{text}"
    
    Output the sentiment (positive, neutral, negative) and whether it could contribute to anxiety, depression, or distress.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )

    return response["choices"][0]["message"]["content"]

def calculate_depression_score(tweets):
    """Calculate a depression/anxiety risk score based on analyzed sentiments."""
    negative_count = 0
    total = len(tweets)

    for tweet in tweets:
        sentiment_analysis = analyze_sentiment_with_gpt(tweet)
        print(f"Tweet: {tweet}\nAnalysis: {sentiment_analysis}\n")

        if "negative" in sentiment_analysis.lower() or "depression" in sentiment_analysis.lower():
            negative_count += 1

    if total == 0:
        return 0

    depression_score = (negative_count / total) * 100
    return round(depression_score, 2)

# Example Usage
if __name__ == "__main__":
    twitter_username = "jack"  # Replace with any public Twitter username
    liked_tweets = fetch_liked_tweets(twitter_username, count=10)

    if liked_tweets:
        risk_score = calculate_depression_score(liked_tweets)
        print(f"\nDepression/Anxiety Risk Score for @{twitter_username}: {risk_score}%")
    else:
        print("No liked tweets found or an error occurred.")

    app.run(debug=True)