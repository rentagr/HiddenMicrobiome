import pandas as pd
import glob
import os

# We get a list of all files with views for each sample
files = sorted(glob.glob("metaphlan_by_sample/*.csv"))
print(f"Files found: {len(files)}")

data = {}  # dictionary: {sample: DataFrame with index by type}
for f in files:
    sample = os.path.basename(f).replace(".csv", "")
    df = pd.read_csv(f)
    # Setting the view as an index
    df.set_index("species", inplace=True)
    data[sample] = df["relative_abundance"]

# Combining all the samples into one table
merged = pd.DataFrame(data).fillna(0)
# Sort the rows in descending order of average abundance (optional)
merged["mean"] = merged.mean(axis=1)
merged = merged.sort_values("mean", ascending=False).drop("mean", axis=1)

# Save it in CSV with escaping (in case of commas in names)
merged.to_csv("metaphlan_abundance_all_samples.csv", quoting=1)  # quoting=1-QUOTE_ALL
print(f"Saved types: {merged.shape[0]}, samples: {merged.shape[1]}")
