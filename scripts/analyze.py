import pandas as pd
from transformers import pipeline

INPUT_FILE = "data/cleaned_posts.csv"
OUTPUT_FILE = "data/results.csv"
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

def load_model():
    try:
        model = pipeline("sentiment-analysis", model=MODEL_NAME)
    except Exception as e:
        return(f"Exception: {e}")
    
    return model
