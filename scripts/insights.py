import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
import nltk
import webbrowser

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

SENTIMENT_INPUT_FILE = "data/sentiment_results.csv"
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
            print(f" {word:<15} | {count} | {count/len(group)*100:.1f}% posts")
        

def explore_posts(df):
    print(f"\n-- Post Explorer --")
    print(f"Enter a keyword and sentiment to see random matching posts.")
    print(f"Sentiments: positive, negative, neutral")
    print(f"Type 'quit' to exit\n")

    while True:
        keyword = input("Keyword: ").strip().lower()
        if keyword == "quit":
            break

        sentiment = input("Sentiment (positive/negative/neutral): ").strip().lower()
        if sentiment not in ["positive", "negative", "neutral"]:
            print(f"Invalid sentiment. Choose positive, negative, or neutral.\n")
            continue

        filtered = df[
            df["body_cleaned"].str.contains(keyword, case=False, na=False) &
            (df["sentiment"] == sentiment)
        ]

        if len(filtered) == 0:
            print(f"No {sentiment} posts found containing '{keyword}'\n")
            continue

        post = filtered.sample(1).iloc[0]

        print(f"\n{'='*50}")
        print(f"Title:     {post['title']}")
        print(f"Subreddit: r/{post['subreddit']}")
        print(f"Date:      {post['date']}")
        print(f"Sentiment: {post['sentiment']} | Score: {post['score']:.2f}")
        print(f"\nBody:\n{post['body_cleaned'][:1000]}")
        print(f"{'='*50}")

        view_full = input(f"\nView full post? (y/n): ").strip().lower()
        if view_full != "n":
            webbrowser.open(post["url"])

        another = input("\nSee another post? (y/n): ").strip().lower()
        if another != "y":
            print("\nThanks!")
            break

if __name__ == '__main__':
    df = pd.read_csv(SENTIMENT_INPUT_FILE)
    print(f"Loaded input file {SENTIMENT_INPUT_FILE}...")

    sentiment_summary(df)
    keyword_by_sentiment(df)

    explore_posts(df)