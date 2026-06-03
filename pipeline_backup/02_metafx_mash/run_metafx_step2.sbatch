#!/bin/bash
#SBATCH -J metafx_step2
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/metafx_step2_%j.out
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/metafx_step2_%j.err
#SBATCH -n 1
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH -t 12:00:00

set -e
set -u

cd /mnt/tank/scratch/ris/SRR_files || exit 1

source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

# Deleting the old temporary folders of step 2
rm -rf wd_unique/unique_kmers_healthy wd_unique/unique_kmers_case
rm -rf wd_unique/components_healthy wd_unique/components_case
rm -rf wd_unique/contigs_healthy wd_unique/contigs_case

# Launching metafx unique with --kmers-dir
metafx unique -t 16 -m 2G -w wd_unique -k 31 -i sample_categories.txt --kmers-dir wd_unique/kmers/kmers

# After that, the final files will appear in wd_unique/: feature_table.tsv
