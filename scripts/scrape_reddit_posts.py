import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Scraping from top most popular subreddits
SUBREDDITS = ["diabetes", "diabetes_t1", "diabetes_t2"]

# Output the posts in a csv file
OUTPUT_FILE = "data/raw_posts.csv"

# Site identification
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
}

# Sidebar text to avoid
SIDEBAR_MARKERS = [
    "undiagnosed? read this!",
    "ettiquette for non-diabetics",
    "discord",
    "welcome to r/diabetes",
    "please read our rules",
    "blood glucose levels conversion",
    "subreddit rules",
    "related communities r/diabetes",
    "we're a forum for the discussion",
]

# Flairs to avoid
FLAIRS = [
    "Type 1.5/LADA", "Type 1", "Type 2", "Type 3c", "MODY", "Gestational Diabetes", "CFRD", "Prediabetic", 
    "Humor", "News", "Supplies", "Healthcare", "Discussion", "Pseudoscience", "Medication", "Rant",

    "Exercise & Sport", "Nutrition & Diet", "Graphs & Data", "Meme & Humor", "T1D News", "Science & Tech", 
    "Mental Health", "Seeking Support/Advice", "Success Story",

    "Newly Diagnosed", "General Question", "Food/Diet", "Hard Work", "Joke/Meme/Satire"
]

# Returns True/False
def is_sidebar(text) -> bool:
    text_lower = text.lower()
    return any(marker in text_lower for marker in SIDEBAR_MARKERS)

def clean_title(title):
    # Removes flair prefix
    for flair in FLAIRS:
        if title.startswith(flair):
            title.title[len(flair):].strip()
    
    # Removes subreddit suffix
    if "(self." in title:
        title = title[:title.rfind("(self.")].strip()
    return title

# Grabs all the available post links from a subreddit's n pages
def get_post_links(subreddit, pages=3):
    links = []

    session = requests.Session()
    session.headers.update(HEADERS)
    session.get("https://old.reddit.com", timeout=10)
    time.sleep(3)

    for page in range(pages):
        print(f" Fetching page {page + 1} from r/{subreddit}...")

        url = f"https://old.reddit.com/r/{subreddit}/new.json?limit=100"
        response = session.get(url, timeout=10)

        if response.status_code != 200:
            print(f"Status Error: error code {response.status_code}")
            break

        raw_posts = response.json()
        children = raw_posts["data"]["children"]
        for post in children:
            p = post["data"]
            permalink = p.get("permalink", "")
            if permalink:
                links.append(f"https://old.reddit.com{permalink}")
            
        print(f"Total links found: {len(links)}")

    return links

