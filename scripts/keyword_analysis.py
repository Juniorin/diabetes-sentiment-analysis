import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords

INPUT_FILE = "data/results.csv"
OUTPUT_FILE = "data/keyword_results.csv"
TOP_N = 50

# Download words that are not keywords to filter out later
nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))

# Extract all keywords, filtering out any stop words
def extract_keywords(text):
    text_lower = text.lower()
    words = text_lower.split()
    words = [word for word in words if word not in STOP_WORDS]
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
