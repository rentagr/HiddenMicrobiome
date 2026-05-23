import pandas as pd
import glob

# Find all the report files
reports = glob.glob("*.kraken.report")
print(f"Найдено отчётов: {len(reports)}")

# Dictionary for storing data of each sample
data = {}

for rep in reports:
    # Extract the sample name from the file name (before .kraken.report)
    sample = rep.replace(".kraken.report", "")

    # Reading the report. It has columns: percentage, number of reads in the clade, number of reads of the taxon, rank, taxid, name
    df = pd.read_csv(
        rep,
        sep="\t",
        header=None,
        names=["perc", "clade_reads", "taxon_reads", "rank", "taxid", "name"],
    )

    # Leaving only the rows with the rank 'S' (species)
    df = df[df["rank"] == "S"].copy()

    # Clearing the names of unnecessary spaces
    df["name"] = df["name"].str.strip()

    # Setting the type name as the index
    df.set_index("name", inplace=True)

    # Save a column with the number of reads for this sample
    data[sample] = df["taxon_reads"]

# Combine all the samples into one table. Fill in the gaps (species not found in the sample) with zeros.
merged = pd.DataFrame(data).fillna(0).astype(int)

# Saving the result
merged.to_csv("kraken_species_reads.csv")
print(f"Saved types: {merged.shape[0]}, samples: {merged.shape[1]}")
