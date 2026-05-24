import pandas as pd
from Bio import SeqIO

imp = pd.read_csv("rf_results/feature_importance.csv")
top20 = imp.head(20)["feature"].tolist()
with open("top20_features.fasta", "w") as out:
    for feat in top20:
        group, idx = feat.split("_")
        idx = int(idx)
        fasta_file = f"contigs_{group}/components.seq.fasta"
        records = list(SeqIO.parse(fasta_file, "fasta"))
        if idx < len(records):
            rec = records[idx]
            out.write(f">{feat} ({rec.id})\n{rec.seq}\n")
