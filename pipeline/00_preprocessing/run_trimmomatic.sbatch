#!/bin/bash
#SBATCH -J trimmomatic
#SBATCH -n 1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH -t 06:00:00
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/trimmomatic_%j_%a.err
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/trimmomatic_%j_%a.out

cd /mnt/tank/scratch/ris/SRR_files
source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

samples=($(ls *_1.fastq.gz | sed 's/_1.fastq.gz//'))
sample=${samples[$SLURM_ARRAY_TASK_ID-1]}

trimmomatic PE -threads 2 \
  ${sample}_1.fastq.gz ${sample}_2.fastq.gz \
  ${sample}_1_trimmed_paired.fastq.gz ${sample}_1_trimmed_unpaired.fastq.gz \
  ${sample}_2_trimmed_paired.fastq.gz ${sample}_2_trimmed_unpaired.fastq.gz \
  ILLUMINACLIP:/path/to/adapters.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
  
# After trimming, files with the suffix _trimmed_paired appear.fastq.gz.
