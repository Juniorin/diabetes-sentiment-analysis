import pandas as pd
df = pd.read_csv("data/results.csv")
print(df["sentiment"].value_counts())
print(df["sentiment"].value_counts(normalize=True).round(2))