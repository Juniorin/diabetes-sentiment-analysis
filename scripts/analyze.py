import pandas as pd
from transformers import pipeline

INPUT_FILE = "data/cleaned_posts.csv"
OUTPUT_FILE = "data/results.csv"
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# Load twitter RoBERTa's model
def load_model():
    try:
        model = pipeline("sentiment-analysis", model=MODEL_NAME)
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
