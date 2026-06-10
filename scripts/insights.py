import pandas as pd

SENTIMENT_INPUT_FILE = "data/results.csv"
KEYWORD_INPUT_FILE = "data/keyword_results.csv"
OUTPUT_FILE = "data/insights_results.csv"

# Creates a sentiment summary based off data
def sentiment_summary(df):
    counts = df["sentiment"].value_counts()
    percentages = df["sentiment"].value_counts(normalize=True).round(2) * 100

    print(f"--Sentiment Summary--")
    for sentiment in counts.index:
        print(f"{sentiment:<12} | {counts[sentiment]} posts | {percentages[sentiment]}%")