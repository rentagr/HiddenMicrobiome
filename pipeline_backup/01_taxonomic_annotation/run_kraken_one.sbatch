#!/bin/bash
#SBATCH -J kraken_one
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=250G
#SBATCH -t 04:00:00
#SBATCH --partition=main
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/kraken_one_%j.err
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/kraken_one_%j.out

source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

cd /mnt/tank/scratch/ris/SRR_files
KRAKEN_DB="/mnt/tank/scratch/ris/databases/kraken2"
sample=$(ls *_1_trimmed_paired.fastq.gz | head -1 | sed 's/_1_trimmed_paired.fastq.gz//')
kraken2 --db "$KRAKEN_DB" --threads $SLURM_CPUS_PER_TASK --paired \
  ${sample}_1_trimmed_paired.fastq.gz ${sample}_2_trimmed_paired.fastq.gz \
  --output ${sample}_kraken_test.out --report ${sample}_kraken_test.report --use-names
  
# Test is successful: time ~22 min, memory ~228 GB
