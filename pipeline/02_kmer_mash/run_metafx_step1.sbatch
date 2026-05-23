#SBATCH -J metafx_step1
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/metafx_step1_%j.out
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/metafx_step1_%j.err
#SBATCH -n 1
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH -t 24:00:00

set -e
set -u

cd /mnt/tank/scratch/ris/SRR_files || exit 1

source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

# Creating links sample_r1.fastq.gz / sample_r2.fastq.gz
for r1 in *_1_trimmed_paired.fastq.gz; do
    sample_orig=$(basename "$r1" _1_trimmed_paired.fastq.gz)
    sample_lower=$(echo "$sample_orig" | tr '[:upper:]' '[:lower:]')
    r2="${sample_orig}_2_trimmed_paired.fastq.gz"
    if [ -f "$r2" ]; then
        ln -sf "$r1" "${sample_lower}_r1.fastq.gz"
        ln -sf "$r2" "${sample_lower}_r2.fastq.gz"
    else
        echo "Warning: $r2 not found for $sample_orig"
    fi
done

# Creation sample_categories.txt (approximate category)
python3 - <<EOF # the heredoc operator. It tells the shell that everything up to the EOF line is passed as standard input to the python3 command.
import pandas as pd
import os

metadata = pd.read_csv("SraRunTable.csv")
metadata.rename(columns={'Run': 'sample'}, inplace=True)
metadata['group'] = metadata['Fracture'].apply(lambda x: 'healthy' if x == 0 else 'case')

with open("sample_categories.txt", "w") as f:
    for _, row in metadata.iterrows():
        sample_lower = row['sample'].lower()
        group = row['group']
        # Check for links
        r1 = f"{sample_lower}_r1.fastq.gz"
        r2 = f"{sample_lower}_r2.fastq.gz"
        if os.path.exists(r1) and os.path.exists(r2):
            f.write(f"{sample_lower}\t{group}\n")
        else:
            print(f"Warning: {sample_lower} missing reads")
EOF

# 3. Launch metafx unique (without --kmers-dir) – it will calculate kmers by itself
metafx unique -t 16 -m 2G -w wd_unique -k 31 -i sample_categories.txt
