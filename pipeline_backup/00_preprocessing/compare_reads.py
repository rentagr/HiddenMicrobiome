import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_rel

raw = pd.read_csv("fastqc_summary.csv")
clean = pd.read_csv("fastqc_clean_summary.csv")
raw = raw[["sample", "total_reads"]].rename(columns={"total_reads": "raw_reads"})
clean = clean[["sample", "total_reads"]].rename(columns={"total_reads": "clean_reads"})
df = pd.merge(raw, clean, on="sample")

df_melt = df.melt(id_vars="sample")
sns.boxplot(x="variable", y="value", data=df_melt)
plt.savefig("reads_boxplot.png")

df["retained"] = df["clean_reads"] / df["raw_reads"]
print(df["retained"].describe())
stat, p = ttest_rel(df["raw_reads"], df["clean_reads"])
print(f"p-value: {p}")

# In our case, the result is a boxplot graph with a p-value of ~1.56e-34 (the difference is significant, but the loss is < 0.1%)
