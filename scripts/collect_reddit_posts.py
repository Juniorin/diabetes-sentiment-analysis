import requests
import pandas as pd
import time

# Number of pages to scrape in a subreddit
PAGES = 5

def scrape_subreddit(subreddit, pages=PAGES):
    posts = []
    