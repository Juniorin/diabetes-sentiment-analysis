import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords

INPUT_FILE = "data/results.csv"
OUTPUT_FILE = "data/keyword_results.csv"
TOP_N = 50

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

# Download words that are not keywords to filter out later
nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english")).union(MANUAL_STOP_WORDS)

# Extract all keywords, filtering out any stop words
def extract_keywords(text):
    text_lower = text.lower()
    words = text_lower.split()
    words = [word for word in words if word not in STOP_WORDS and len(word) >= 3 and word.isalpha()]
    return words

# Get top n key words from every post
def get_top_keywords(df, n):
    all_words = Counter()
    for i, text in enumerate(df["body_cleaned"]):
        extracted_keywords = extract_keywords(text)
        all_words.update(extracted_keywords)
        if i % 10 == 0 and i > 0:
            print(f"{i}/{len(df)} posts counted...")

    df = pd.DataFrame(all_words.most_common(n), columns=["word", "count"])

    return df

if __name__ == '__main__':
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded input file {INPUT_FILE}...")

    top_keywords = get_top_keywords(df, TOP_N)
    print(f"Retrieved top {TOP_N} keywords...")

    top_keywords.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"Saved to {OUTPUT_FILE}")

    print(f"\n      --Top 20 Keywords--")
    print(f"{'Word':<20} | {'Count'}")
    for i in range(20):
        print(f"{top_keywords['word'].iloc[i]:<20} | {top_keywords['count'].iloc[i]}")