import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

pred = pd.read_csv(
    "wd_predict/predictions.tsv", sep="\t", header=None, names=["sample", "predicted"]
)
true = pd.read_csv("test_samples.txt", sep="\t", header=None, names=["sample", "true"])
true["sample"] = true["sample"].str.replace("_r1.fastq.gz", "", regex=False)
merged = pd.merge(pred, true, on="sample")
acc = accuracy_score(merged["true"], merged["predicted"])
print(f"Test accuracy: {acc:.3f}")
print(classification_report(merged["true"], merged["predicted"]))
