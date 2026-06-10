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

# Shorten body to max tokens
def shorten_text(text, max_tokens=MAX_INPUT_LENGTH):
    words = text.split()
    if len(words) > max_tokens:
        words = words[:max_tokens]
    return ' '.join(words)

# Clean and shorten text body
def preprocess(df):
    df = df.dropna(subset=["title", "body"])
    df["body_cleaned"] = df["body"].apply(clean_text)
    df["body_cleaned"] = df["body_cleaned"].apply(shorten_text)
    df = df[df["body_cleaned"].str.strip() != ""]

    return df

if __name__ == "__main__":
    df = pd.read.csv(INPUT_FILE)
    print(f"Loaded {len(df)} posts from {INPUT_FILE}")

    df = preprocess(df)
    print(f"Cleaned {len(df)} posts")

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"Saved to {OUTPUT_FILE}")

    # 3 Samples of cleaned data
    print(df[["title", "body_cleaned"]].head(3))