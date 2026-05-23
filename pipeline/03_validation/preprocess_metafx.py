import pandas as pd


def clean_names(s):
    return s.str.replace("_r1", "", regex=False).str.replace(
        ".fastq.gz", "", regex=False
    )


# Train
train_raw = pd.read_csv("wd_unique_train/feature_table.tsv", sep="\t", index_col=0).T
train_raw.index = clean_names(train_raw.index)
train_labels = pd.read_csv(
    "train_samples.txt", sep="\t", header=None, names=["sample", "category"]
)
train_labels["sample"] = clean_names(train_labels["sample"])
common = train_raw.index.intersection(train_labels["sample"])
X_train = train_raw.loc[common]
y_train = train_labels.set_index("sample").loc[common]

# Filter features (>=5% of train samples)
min_frac = 0.05
keep = (X_train > 0).sum(axis=0) >= (len(X_train) * min_frac)
keep_cols = keep[keep].index
X_train_filt = X_train[keep_cols]
X_train_norm = X_train_filt.div(X_train_filt.sum(axis=1), axis=0).fillna(0)

# Test
test_raw = pd.read_csv(
    "wd_calc_features_test/feature_table.tsv", sep="\t", index_col=0
).T
test_raw.index = clean_names(test_raw.index)
X_test = test_raw[keep_cols]
X_test_norm = X_test.div(X_test.sum(axis=1), axis=0).fillna(0)

# Save cleaned tables (transposed back to features × samples)
X_train_norm.T.to_csv("feature_table_train_clean.tsv", sep="\t")
X_test_norm.T.to_csv("feature_table_test_clean.tsv", sep="\t")

# Save labels for fit
y_train.to_csv("train_categories_clean.tsv", sep="\t", header=False)
print("Preprocessing done. Files saved.")
