import pandas as pd
import re


INPUT_FILE = "data/raw_posts1.csv"
OUTPUT_FILE = "data/cleaned_posts.csv"

# RoBERTa's maximum input length
MAX_INPUT_LENGTH = 512

# Removes any urls, html, special characters, and whitespace
def clean_text(text):
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'&amp;|&gt;|&lt;|&nbsp;', ' ', text)
    text = re.sub(r'[^\w\s.,!?\'"-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def shorten_text(text, max_tokens=MAX_INPUT_LENGTH):
    words = text.split()
    if len(words) > max_tokens:
        words = words[:max_tokens]
    return ' '.join(words)