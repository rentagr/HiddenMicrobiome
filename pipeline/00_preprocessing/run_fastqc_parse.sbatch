#!/bin/bash
#SBATCH -J fastqc_parse
#SBATCH -n 1
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
#SBATCH -t 24:00:00
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/fastqc_parse_%j.err
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/fastqc_parse_%j.out

cd /mnt/tank/scratch/ris/SRR_files
source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

fastqc --threads 2 *.fastq.gz
python parse_fastqc.py
