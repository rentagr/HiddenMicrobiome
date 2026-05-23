import os
import zipfile
import io
import glob
import pandas as pd


def read_fastqc_data(zip_path):
    """
    Extracts the contents fastqc_data.txt from the FastQC zip archive.
    Returns a list of rows.
    """
    with zipfile.ZipFile(zip_path, "r") as z:
        # File name inside the archive: <archive_name without_zip>/fastqc_data.txt
        base = os.path.basename(zip_path).replace(".zip", "")
        data_file = f"{base}/fastqc_data.txt"
        with z.open(data_file) as f:
            return io.TextIOWrapper(
                f
            ).readlines()  # wraps a binary stream into a text stream (using UTF‑8 encoding) to read strings


def main():
    # Finding all R1 files for pure data - suffix _1_trimmed_paired.fastq.gz
    r1_files = glob.glob("*_1_trimmed_paired.fastq.gz")
    if not r1_files:
        print("No files with the suffix '_1_trimmed_paired were found.fastq.gz'")
        return

    # Extract the names of the samples-remove the suffix
    samples = set()
    for f in r1_files:
        # Expected format: <sample>_1_trimmed_paired.fastq.gz
        sample = f.replace("_1_trimmed_paired.fastq.gz", "")
        samples.add(sample)
    samples = sorted(samples)
    print(f"Found {len(samples)} samples: {samples}")

    results = []
    missing = []

    for sample in samples:
        # Forming the expected names of FastQC zip archives
        r1_zip = f"{sample}_1_trimmed_paired_fastqc.zip"
        r2_zip = f"{sample}_2_trimmed_paired_fastqc.zip"

        # Check for both zip files
        if not os.path.isfile(r1_zip):
            missing.append(r1_zip)
            continue
        if not os.path.isfile(r2_zip):
            missing.append(r2_zip)
            continue

        total_reads = 0
        lengths = []

        # R1 parsing
        lines = read_fastqc_data(r1_zip)
        for line in lines:
            if "Total Sequences" in line:
                total_reads += int(line.split()[-1])
            if "Sequence length" in line:
                lengths.append(line.split()[-1].strip())

        # R2 parsing
        lines = read_fastqc_data(r2_zip)
        for line in lines:
            if "Total Sequences" in line:
                total_reads += int(line.split()[-1])
            if "Sequence length" in line:
                lengths.append(line.split()[-1].strip())

        results.append(
            {
                "sample": sample,
                "total_reads": total_reads,
                "read1_length": lengths[0] if len(lengths) > 0 else "NA",
                "read2_length": lengths[1] if len(lengths) > 1 else "NA",
            }
        )

        print(sample, total_reads, lengths)

    # Results saving
    if results:
        df = pd.DataFrame(results)
        df.to_csv("fastqc_clean_summary.csv", index=False)
        print("\nThe result is saved in fastqc_clean_summary.csv")
    else:
        print("There is no data collected")

    if missing:
        print("\nThe following FastQC zip files are missing:")
        for m in missing:
            print("  ", m)


if __name__ == "__main__":
    main()
