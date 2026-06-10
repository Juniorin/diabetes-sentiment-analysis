import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
import nltk

MANUAL_STOP_WORDS = {
    "like", "get", "know", "anyone", "also", "would", "one",
    "since", "going", "got", "really", "time", "feel", "even",
    "still", "back", "take", "go", "much", "new", "need",
    "want", "make", "good", "first", "see", "getting", "went",
    "last", "day", "two", "started", "use", "work", "every", 
    "trying", "week", "could", "think", "never", "way", 
    "something", "taking", "little", "using",
    "things", "long", "always", "around", "lot",
}

nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english")).union(MANUAL_STOP_WORDS)

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


def keyword_by_sentiment(df):
    positive_posts = df[df["sentiment"] == "positive"]
    negative_posts = df[df["sentiment"] == "negative"]
    neutral_posts = df[df["sentiment"] == "neutral"]

    for label, group in [("positive", positive_posts), ("negative", negative_posts), ("neutral", neutral_posts)]:
        all_text = " ".join(group["body_cleaned"].dropna())
        words = [word for word in all_text.lower().split() if word not in STOP_WORDS and len(word) >= 3 and word.isalpha()]
        top_words = Counter(words).most_common(10)

        print(f"\n--Top 10 words in {label} posts--")
        for word, count in top_words:
            print(f" {word:<20} | {count}")
        

if __name__ == '__main__':
    df = pd.read_csv(SENTIMENT_INPUT_FILE)
    print(f"Loaded input file {SENTIMENT_INPUT_FILE}...")

    sentiment_summary(df)
    keyword_by_sentiment(df)

    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"Saved to {OUTPUT_FILE}")