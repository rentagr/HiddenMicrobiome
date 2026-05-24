import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt

# Uploading data
X = pd.read_csv("feature_table.tsv", sep="\t", index_col=0).T.fillna(0)
y_df = pd.read_csv(
    "samples_categories.tsv", sep="\t", header=None, names=["sample", "group"]
)
X.index = X.index.str.lower()
y_df["sample"] = y_df["sample"].str.lower()
common = X.index.intersection(y_df["sample"])
X = X.loc[common]
y = y_df.set_index("sample").loc[common, "group"]

# Separation and training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)

# Rating
y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred))

# Importance of signs
importances = rf.feature_importances_
imp_df = pd.DataFrame({"feature": X.columns, "importance": importances}).sort_values(
    "importance", ascending=False
)
imp_df.to_csv("feature_importance.csv", index=False)

# Chart of the top 20
top = imp_df.head(20)
plt.figure(figsize=(10, 8))
plt.barh(top["feature"], top["importance"], color="skyblue")
plt.savefig("top20_features.png", dpi=300)
