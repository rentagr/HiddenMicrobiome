import pandas as pd
import glob
import os

files = sorted(glob.glob("*_metaphlan.txt"))
print(f"Found files: {len(files)}")
os.makedirs("metaphlan_by_sample", exist_ok=True)

for f in files:
    sample = f.replace("_metaphlan.txt", "")
    print(f"Processing {sample}...")
    df = pd.read_csv(
        f,
        sep="\t",
        comment="#",
        header=None,
        names=["clade_name", "NCBI_tax_id", "relative_abundance", "additional_species"],
    )
    # Leaving only the lines where there are 's__' (types)
    species = df[df["clade_name"].str.contains("s__", na=False)].copy()
    if len(species) == 0:
        print(f"There are no views in the {f} file")
        continue
    # Extract the short name of the type (the last element after the '|')
    species["species"] = species["clade_name"].apply(lambda x: x.split("|")[-1])
    result = species[["species", "relative_abundance"]].sort_values(
        "relative_abundance", ascending=False
    )
    result.to_csv(f"metaphlan_by_sample/{sample}.csv", index=False)
    print(f" Saved file with {len(result)} views")
