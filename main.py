import requests
from config import ACCESS_TOKEN, INSTAGRAM_USER_ID
from analyzer import categorize_text

GRAPH_API_URL = "https://graph.facebook.com/v19.0"

def get_recent_posts():
    url = f"{GRAPH_API_URL}/{INSTAGRAM_USER_ID}/media?fields=id,caption&access_token={ACCESS_TOKEN}"
    res = requests.get(url).json()
    return res.get("data", [])

def get_likes_for_post(post_id):
    url = f"{GRAPH_API_URL}/{post_id}/likes?access_token={ACCESS_TOKEN}"
    res = requests.get(url).json()
    return [user["username"] for user in res.get("data", [])]

def get_user_profile(username):
    # Instagram Graph API does not allow full access to other users' data
    # unless they are followers or interact with your business account
    return {
        "username": username,
        "bio": "Sample bio of the user.",
        "posts": ["A post about AI", "Funny meme", "Science article"]
    }

def analyze_profile(profile):
    topics = [categorize_text(post) for post in profile["posts"]]
    return {
        "username": profile["username"],
        "bio": profile["bio"],
        "post_categories": topics
    }

def run():
    posts = get_recent_posts()
    for post in posts:
        print(f"Analyzing Post: {post['id']}")
        likers = get_likes_for_post(post["id"])
        for liker in likers:
            profile = get_user_profile(liker)
            analysis = analyze_profile(profile)
            print(analysis)

if __name__ == "__main__":
    run()
