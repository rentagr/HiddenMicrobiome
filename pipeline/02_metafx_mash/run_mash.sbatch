#!/bin/bash
#SBATCH -J mash
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/mash_%j.out
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/mash_%j.err
#SBATCH -n 1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH -t 24:00:00

set -e
set -u

cd /mnt/tank/scratch/ris/SRR_files || exit 1

source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

echo "Mash started at $(date)"

MASH_WD="mash_output"
mkdir -p "$MASH_WD"

# Create a sketch for each sample by concatenating R1 and R2
for r1 in *_1_trimmed_paired.fastq.gz; do
    sample_orig=$(basename "$r1" _1_trimmed_paired.fastq.gz)
    r2="${sample_orig}_2_trimmed_paired.fastq.gz"
    if [ -f "$r2" ]; then
        cat "$r1" "$r2" | mash sketch -m 2 -o "$MASH_WD/${sample_orig}" -
    fi
done

# Combine all the sketches into one file
mash sketch -o "$MASH_WD/all_sketches" "$MASH_WD"/*.msh

# Building a distance matrix
mash dist "$MASH_WD/all_sketches.msh" "$MASH_WD/all_sketches.msh" > "$MASH_WD/distances.tab"
echo " Mash finished at $(date)"
