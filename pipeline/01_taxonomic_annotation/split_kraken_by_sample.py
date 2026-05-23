import pandas as pd
import os

df = pd.read_csv("kraken_species_reads.csv", index_col=0)
os.makedirs("kraken_by_sample", exist_ok=True)

for sample in df.columns:
    series = df[sample][df[sample] > 0]
    sample_df = pd.DataFrame({"species": series.index, "reads": series.values})
    sample_df = sample_df.sort_values("reads", ascending=False)
    sample_df.to_csv(f"kraken_by_sample/{sample}.csv", index=False)
    print(f"Saved {sample}.csv with {len(sample_df)} views")
