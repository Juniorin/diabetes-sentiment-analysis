import pandas as pd
from transformers import pipeline

INPUT_FILE = "data/cleaned_posts.csv"
OUTPUT_FILE = "data/results.csv"
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# Load twitter RoBERTa's model
def load_model():
    try:
        model = pipeline("sentiment-analysis", model=MODEL_NAME, truncation=True)
    except Exception as e:
        return(f"Exception: {e}")
    
    return model

# Analyze and score text
def analyze_sentiment(model, text):
    analyzed_results = model(text)

    label = analyzed_results[0]["label"]
    score = analyzed_results[0]["score"]

    return {
        "label": label,
        "score": score,
    }

# Analyze all posts and add to df
def analyze_posts(model, df):
    for i, text in enumerate(df["body_cleaned"]):
        result = analyze_sentiment(model, text)
        df.at[i, "sentiment"] = result["label"]
        df.at[i, "score"] = result["score"]
        if i % 10 == 0 and i > 0:
            print(f"{i}/{len(df)} posts analyzed...")
    return df

if __name__ == '__main__':
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded input file {INPUT_FILE}...")

    model = load_model()
    print(f"Loaded model...")

    df = analyze_posts(model, df)
    print(f"Analyzed all posts...")

    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"Saved to {OUTPUT_FILE}")

    print(f"Total posts: {len(df)}")
    print(f"\nSample title: {df['title'].iloc[0]}")
    print(f"Sample sentiment: {df['sentiment'].iloc[0]}")
    print(f"Sample score: {df['score'].iloc[0]}")

