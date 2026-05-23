import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load Kraken data
df = pd.read_csv("kraken_species_reads.csv", index_col=0)
# Transpose: samples -> rows, taxa -> columns
df_T = df.T
print(f"Original table: {df_T.shape[0]} samples, {df_T.shape[1]} taxa")

# Original table: 57 samples, 16,873 taxa

train_samples_raw = [
    "SRR25006915",
    "SRR25006904",
    "SRR25006916",
    "SRR25006888",
    "SRR25006874",
    "SRR25006889",
    "SRR25006912",
    "SRR25006894",
    "SRR25006905",
    "SRR25006869",
    "SRR25006920",
    "SRR25006881",
    "SRR25006922",
    "SRR25006876",
    "SRR25006880",
    "SRR25006891",
    "SRR25006883",
    "SRR25006878",
    "SRR25006892",
    "SRR25006896",
    "SRR25006923",
    "SRR25006907",
    "SRR25006903",
    "SRR25006910",
    "SRR25006875",
    "SRR25006900",
    "SRR25006890",
    "SRR25006882",
    "SRR25006917",
    "SRR25006913",
    "SRR25006871",
    "SRR25006886",
    "SRR25006877",
    "SRR25006924",
    "SRR25006897",
    "SRR25006879",
    "SRR25006921",
    "SRR25006870",
    "SRR25006898",
    "SRR25006867",
    "SRR25006925",
    "SRR25006873",
    "SRR25006872",
    "SRR25006908",
    "SRR25006895",
]

train_labels = [
    "normal",
    "normal",
    "low",
    "normal",
    "normal",
    "normal",
    "normal",
    "normal",
    "low",
    "low",
    "normal",
    "normal",
    "low",
    "normal",
    "normal",
    "low",
    "normal",
    "normal",
    "low",
    "normal",
    "normal",
    "normal",
    "normal",
    "normal",
    "low",
    "low",
    "normal",
    "normal",
    "low",
    "normal",
    "low",
    "normal",
    "normal",
    "normal",
    "normal",
    "low",
    "low",
    "low",
    "normal",
    "normal",
    "low",
    "normal",
    "low",
    "normal",
    "low",
]

# Ensure all samples exist in the data
train_samples = [s for s in train_samples_raw if s in df_T.index]
train_labels = train_labels[: len(train_samples)]

test_true = {}
with open("test_BMD_samples.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) == 2:
            sample_name = parts[0].replace("_r1.fastq.gz", "").upper()
            label = parts[1]
            test_true[sample_name] = label

# Feature preprocessing
# Remove taxa present in less than 5% of samples
min_samples_frac = 0.05
taxa_to_keep = (df_T > 0).sum(axis=0) >= len(df_T) * min_samples_frac
X_filtered = df_T.loc[:, taxa_to_keep]

# Normalization: relative abundances
X_norm = X_filtered.div(X_filtered.sum(axis=1), axis=0).fillna(0)

# Split into train / test
X_train = X_norm.loc[train_samples]
y_train = pd.Series(train_labels, index=train_samples)

# Test samples – all not in train
X_test = X_norm.loc[~X_norm.index.isin(train_samples)]
# Keep only samples with true labels
X_test = X_test.loc[X_test.index.isin(test_true.keys())]
y_test = pd.Series({s: test_true[s] for s in X_test.index})

model = RandomForestClassifier(
    n_estimators=100, class_weight="balanced", random_state=42, n_jobs=-1
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_pred_prob = model.predict_proba(X_test)[:, 1]  # probability of class "low"

# Metrics
accuracy = accuracy_score(y_test, y_pred)
print(f"\nTest set accuracy: {accuracy:.3f}")
print("\nClassification report:")
print(classification_report(y_test, y_pred))
print("\nConfusion matrix:")
cm = confusion_matrix(y_test, y_pred, labels=["normal", "low"])
print(cm)

# Visualize confusion matrix
plt.figure(figsize=(5, 4))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["normal", "low"],
    yticklabels=["normal", "low"],
)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("Step3_kraken_confusion_matrix.png")
plt.show()
