import pandas as pd

feat = pd.read_csv("wd_unique/feature_table.tsv", sep="\t", index_col=0)
# Remove the suffix _r1 from the column names
feat.columns = [col.replace("_r1", "") for col in feat.columns]
# Removing duplicates (leaving the first column for each sample)
feat = feat.loc[:, ~feat.columns.duplicated()]
feat.to_csv("wd_unique/feature_table.tsv", sep="\t")
print(
    f"There were columns: {pd.read_csv('wd_unique/feature_table_original.tsv', sep='\t', index_col=0).shape[1]}"
)
print(f"Become columns{feat.shape[1]}")
