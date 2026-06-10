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
            title = title[len(flair):].strip()
    
    # Removes subreddit suffix
    if "(self." in title:
        title = title[:title.rfind("(old.")].strip()
    return title

# Grabs all the available post links from a subreddit's n pages
def get_post_links(subreddit, pages=3):
    links = []
    after = None

    session = requests.Session()
    session.headers.update(HEADERS)
    session.get("https://old.reddit.com", timeout=10)
    time.sleep(3)

    for page in range(pages):
        print(f" Fetching page {page + 1} from r/{subreddit}...")

        url = f"https://old.reddit.com/r/{subreddit}/new.json?limit=100"
        if after:
            url += f"&after={after}"
        response = session.get(url, timeout=10)

        if response.status_code != 200:
            print(f"Status Error: error code {response.status_code}")
            break

        raw_posts = response.json()
        after = raw_posts["data"]["after"]
        children = raw_posts["data"]["children"]
        for post in children:
            p = post["data"]
            permalink = p.get("permalink", "")
            if permalink:
                links.append(f"https://old.reddit.com{permalink}")

        time.sleep(3)

    return links

def scrape_post(session, url):
    try: 
        url = url.replace(".json", "")
        response = session.get(url, timeout=10)

        if response.status_code != 200:
            print(f"Post status: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        title = ""
        title_tag = soup.find("p", class_="title")
        if not title_tag:
            title_tag = soup.find("a", class_="title")
        if title_tag:
            title = clean_title(title_tag.get_text(strip=True))
        
        body = ""
        all_body_divs = soup.find_all("div", class_="usertext-body")
        for div in all_body_divs:
            md_div = div.find("div", class_="md")
            if md_div:
                text = md_div.get_text(strip=True)
                if len(text) > 10 and not is_sidebar(text):
                    body = text
                    break
        
        if not body or body in ["[deleted]", "[removed]"]:
            return None
        
        time_tag = soup.find("time")
        date = time_tag.get("datetime", "")[:10] if time_tag else ""
        
        return {
            "title": title,
            "body": body,
            "date": date,
            "url": url,
            "subreddit": url.split("/r/")[1].split("/")[0]
        }
    
    except Exception as e:
        print(f" Error: {e}")
        return None
    
if __name__ == '__main__':
    session = requests.Session()
    session.headers.update(HEADERS)
    session.get("https://old.reddit.com", timeout=10)
    time.sleep(3)

    all_posts = []

    for subreddit in SUBREDDITS:
        print(f"\nCollecting links from r/{subreddit}...")
        links = get_post_links(subreddit, pages=3)
        print(f"Found {len(links)} links...now scraping each post...")

        for i, link in enumerate(links):
            post = scrape_post(session, link)
            if post:
                all_posts.append(post)
            if i % 25 == 0 and i > 0:
                print(f"Scraped: {i} posts so far...")
                time.sleep(30)
            else:
                time.sleep(5)

        print(f"Done with r/{subreddit}...{len(all_posts)} total posts so far...")
        time.sleep(3)
    
    df = pd.DataFrame(all_posts)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"Scraping complete")
    print(f"Total posts: {len(all_posts)}")
    print(f"Saved to: {OUTPUT_FILE}")

    if len(all_posts) > 0:
        print(df["subreddit"].value_counts())
        print(f"\nSample title: {df['title'].iloc[0]}")
        print(f"Sample body: {df['body'].iloc[0]}")
