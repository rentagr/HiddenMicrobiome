import pandas as pd
import joblib
from Bio import SeqIO
import os

# Load trained model
model = joblib.load("wd_fit/rf_model.joblib")
importances = model.feature_importances_

# Load feature names (from the cleaned training feature table)
# The feature table has features as rows, samples as columns.
feature_table = pd.read_csv("feature_table_train_clean.tsv", sep="\t", index_col=0)
feature_names = feature_table.index.tolist()

# Create importance DataFrame and sort
imp_df = pd.DataFrame({"feature": feature_names, "importance": importances})
imp_df = imp_df.sort_values("importance", ascending=False)
top20 = imp_df.head(20)

# Extract sequences for each top feature
out_fasta = "top20_contigs_metafx_preproc.fasta"
with open(out_fasta, "w") as out:
    for _, row in top20.iterrows():
        feat = row["feature"]
        # Features are named as "category_index", e.g., "low_305", "normal_613"
        try:
            category, idx_str = feat.split("_")
            idx = int(idx_str)
            # Path to the contig FASTA file for that category (produced by `metafx unique`)
            fasta_file = f"wd_unique_train/contigs_{category}/components.seq.fasta"
            if not os.path.exists(fasta_file):
                print(f"Warning: {fasta_file} not found, skipping {feat}")
                continue
            # Parse FASTA and extract the sequence at position 'idx'
            records = list(SeqIO.parse(fasta_file, "fasta"))
            if idx < len(records):
                rec = records[idx]
                # Modify header to include feature name and importance
                rec.id = f"{feat}_imp_{row['importance']:.6f}"
                rec.description = ""
                SeqIO.write(rec, out, "fasta")
            else:
                print(f"Index {idx} out of range for {category} (max {len(records)-1})")
        except Exception as e:
            print(f"Error parsing {feat}: {e}")

print(f"Top‑20 contigs saved to {out_fasta}")
