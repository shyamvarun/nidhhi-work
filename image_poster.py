import os
import tweepy
import random
import json
from datetime import datetime

# 3 SETS OF CREDENTIALS (one per account)
ACCOUNTS = [
    {  # Account 1
        "key": os.environ["TWITTER_API_KEY_1"],
        "secret": os.environ["TWITTER_API_SECRET_KEY_1"],
        "token": os.environ["TWITTER_ACCESS_TOKEN_1"],
        "token_secret": os.environ["TWITTER_ACCESS_TOKEN_SECRET_1"],
        "bearer": os.environ["TWITTER_BEARER_TOKEN_1"],
        "handle": "@account1",
    },
    {  # Account 2
        "key": os.environ["TWITTER_API_KEY_2"],
        "secret": os.environ["TWITTER_API_SECRET_KEY_2"],
        "token": os.environ["TWITTER_ACCESS_TOKEN_2"],
        "token_secret": os.environ["TWITTER_ACCESS_TOKEN_SECRET_2"],
        "bearer": os.environ["TWITTER_BEARER_TOKEN_2"],
        "handle": "@account2",
    },
    {  # Account 3
        "key": os.environ["TWITTER_API_KEY_3"],
        "secret": os.environ["TWITTER_API_SECRET_KEY_3"],
        "token": os.environ["TWITTER_ACCESS_TOKEN_3"],
        "token_secret": os.environ["TWITTER_ACCESS_TOKEN_SECRET_3"],
        "bearer": os.environ["TWITTER_BEARER_TOKEN_3"],
        "handle": "@account3",
    },
]

CAPTIONS = [
    ".@agerwalnidhhi your beauty could stop time itself 😍 #NidhhiAgerwal",
    "Every time @agerwalnidhhi appears on my screen, the world gets softer ✨ #NidhhiAgerwal",
    ".@agerwalnidhhi you don’t just shine, you glow from within 💫 #NidhhiAgerwal",
    "How can someone look this stunning every single day? @agerwalnidhhi 🔥 #NidhhiAgerwal",
    ".@agerwalnidhhi your presence is pure magic ✨ #NidhhiAgerwal",
    "I swear even angels take notes from @agerwalnidhhi 😇 #NidhhiAgerwal",
    ".@agerwalnidhhi that smile should be declared a national treasure 😍 #NidhhiAgerwal",
    "Every picture of @agerwalnidhhi feels like poetry 💖 #NidhhiAgerwal",
    ".@agerwalnidhhi elegance flows in everything you do ✨ #NidhhiAgerwal",
    "How does @agerwalnidhhi manage to look breathtaking without even trying? 🔥 #NidhhiAgerwal",
    ".@agerwalnidhhi you're the definition of effortless beauty ✨ #NidhhiAgerwal",
    "Just seeing @agerwalnidhhi makes my day 100× better 💫 #NidhhiAgerwal",
    ".@agerwalnidhhi the glow you radiate is unreal 😍 #NidhhiAgerwal",
    "The world pauses to admire @agerwalnidhhi 🤍 #NidhhiAgerwal",
    ".@agerwalnidhhi your aura is something the universe made with extra care ✨ #NidhhiAgerwal",
    "Beauty isn’t a concept anymore; it’s @agerwalnidhhi 💋 #NidhhiAgerwal",
    ".@agerwalnidhhi you redefine charm every single time 🔥 #NidhhiAgerwal",
    "One smile from @agerwalnidhhi can fix an entire day 💫 #NidhhiAgerwal",
    ".@agerwalnidhhi your elegance is loud without saying a word ✨ #NidhhiAgerwal",
    "No filter in the world can match @agerwalnidhhi natural glow 😍 #NidhhiAgerwal",
    ".@agerwalnidhhi beauty, grace, power—everything in one 💖 #NidhhiAgerwal",
    "Every vibe from @agerwalnidhhi is pure perfection ✨ #NidhhiAgerwal",
    ".@agerwalnidhhi you turn moments into masterpieces 🔥 #NidhhiAgerwal",
    "If beauty had a face, it would look like @agerwalnidhhi 💫 #NidhhiAgerwal",
    ".@agerwalnidhhi just existing makes the world better 🤍 #NidhhiAgerwal",
    "The sparkle in @agerwalnidhhi eyes > every star in the sky ✨ #NidhhiAgerwal",
    ".@agerwalnidhhi your presence feels like art 🎨 #NidhhiAgerwal",
    "Nobody lights up a frame like @agerwalnidhhi 🔥 #NidhhiAgerwal",
    ".@agerwalnidhhi your charm is addictive 😍 #NidhhiAgerwal",
    "Perfection is just another word for @agerwalnidhhi ✨ #NidhhiAgerwal",
]

IMAGES = [
    "img (7).jpg",
    "img (8).jpg",
    "img (9).jpg",
    "img (1).png",
    "img (2).png",
    "img (10).jpg",
    "img (11).jpg",
    "img (12).jpg",
    "img (13).jpg",
    "img (14).jpg",
    "img (15).jpg",
    "img (16).jpg",
    "img (17).jpg",
    "img (18).jpg",
    "img (19).jpg",
    "img (20).jpg",
    "img (21).jpg",
    "img (22).jpg",
    "img (23).jpg",
    "img (1).jpg",
    "img (2).jpg",
    "img (3).jpg",
    "img (4).jpg",
    "img (5).jpg",
    "img (6).jpg",
]

USED_FILE = "used_captions.json"

# Load used captions (per account) as dict of lists
try:
    with open(USED_FILE, "r") as f:
        used = json.load(f)          # { "0": [...], "1": [...], "2": [...] }
except FileNotFoundError:
    used = {str(i): [] for i in range(3)}

for i, account in enumerate(ACCOUNTS):
    used_list = used.setdefault(str(i), [])

    # Pick unique caption per account
    available = [c for c in CAPTIONS if c not in used_list]
    if not available:
        print(f"❌ Account {i+1}: No captions left!")
        continue

    caption = random.choice(available)
    image = random.choice(IMAGES)

    # Track usage (as list, JSON‑safe)
    used_list.append(caption)
    used[str(i)] = used_list
    with open(USED_FILE, "w") as f:
        json.dump(used, f, indent=2)

    timestamp = datetime.now().strftime("%H:%M")
    final_caption = f"{caption} | {timestamp} #{account['handle'][1:]}"

    print(f"📸 {account['handle']}: {final_caption}")

    # Auth objects
    auth = tweepy.OAuth1UserHandler(
        account["key"], account["secret"], account["token"], account["token_secret"]
    )
    api = tweepy.API(auth)

    client = tweepy.Client(
        bearer_token=account["bearer"],
        consumer_key=account["key"],
        consumer_secret=account["secret"],
        access_token=account["token"],
        access_token_secret=account["token_secret"],
    )

    # Upload and tweet
    media = api.media_upload(image)
    response = client.create_tweet(text=final_caption, media_ids=[media.media_id])
    print(f"✅ {account['handle']} posted! ID: {response.data['id']}")

print("🎉 All 3 accounts processed!")
