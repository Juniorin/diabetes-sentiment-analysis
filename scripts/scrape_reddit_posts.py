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
