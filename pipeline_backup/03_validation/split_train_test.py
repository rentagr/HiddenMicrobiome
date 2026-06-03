import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv(
    "sample_categories_bmd.txt", sep="\t", header=None, names=["sample", "category"]
)
train, test = train_test_split(
    df, test_size=12 / 56, random_state=42, stratify=df["category"]
)
train.to_csv("train_samples.txt", sep="\t", index=False, header=False)
test.to_csv("test_samples.txt", sep="\t", index=False, header=False)
print(f"Train: {len(train)}, Test: {len(test)}")
