#!/bin/bash
#SBATCH -J fastqc_clean
#SBATCH -n 1
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
#SBATCH -t 24:00:00
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/fastqc_clean_%j.err

cd /mnt/tank/scratch/ris/SRR_files
source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

fastqc --threads 2 *_trimmed_paired.fastq.gz
python parse_fastqc_clean.py

# Output file: fastqc_clean_summary.csv
