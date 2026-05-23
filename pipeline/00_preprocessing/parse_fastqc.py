#!/usr/bin/env python
import os
import glob
import pandas as pd
import zipfile
import io

fastq_files = glob.glob("*.fastq.gz")
sample_set = set()
for f in fastq_files:
    if f.endswith("_1.fastq.gz"):
        sample_set.add(f[:-11])
    elif f.endswith("_2.fastq.gz"):
        sample_set.add(f[:-11])

samples = sorted(sample_set)
print(f"Found {len(samples)} samples: {samples}")

results = []
missing = []

for sample in samples:
    r1_zip = f"{sample}_1_fastqc.zip"
    r2_zip = f"{sample}_2_fastqc.zip"

    if not os.path.isfile(r1_zip):
        missing.append(r1_zip)
        continue
    if not os.path.isfile(r2_zip):
        missing.append(r2_zip)
        continue

    reads = 0
    lengths = []

    def read_fastqc_data(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as z:
            base = os.path.basename(zip_path).replace('.zip', '')
            data_file = f"{base}/fastqc_data.txt"
            with z.open(data_file) as f:
                return io.TextIOWrapper(f).readlines()

    lines = read_fastqc_data(r1_zip)
    for line in lines:
        if "Total Sequences" in line:
            reads += int(line.split()[-1])
        if "Sequence length" in line:
            lengths.append(line.split()[-1].strip())

    lines = read_fastqc_data(r2_zip)
    for line in lines:
        if "Total Sequences" in line:
            reads += int(line.split()[-1])
        if "Sequence length" in line:
            lengths.append(line.split()[-1].strip())

    results.append({
        "sample": sample,
        "total_reads": reads,
        "read1_length": lengths[0] if len(lengths) > 0 else "NA",
        "read2_length": lengths[1] if len(lengths) > 1 else "NA"
    })

    print(sample, reads, lengths)

if results:
    pd.DataFrame(results).to_csv("fastqc_summary.csv", index=False)
    print("\nSummary saved to fastqc_summary.csv")
else:
    print("No results collected.")

if missing:
    print("\nWarning: missing FastQC zip files:")
    for m in missing:
        print("  ", m)
