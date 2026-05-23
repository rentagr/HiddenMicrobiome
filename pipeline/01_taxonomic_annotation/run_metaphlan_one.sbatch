#!/bin/bash
#SBATCH -J metaphlan_one
#SBATCH -n 1
#SBATCH --cpus-per-task=8
#SBATCH --mem=60G
#SBATCH -t 04:00:00
#SBATCH --partition=main
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/metaphlan_one_%j.err
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/metaphlan_one_%j.out

source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

cd /mnt/tank/scratch/ris/SRR_files
METAPHLAN_DB="/mnt/tank/scratch/ris/databases/metaphlan"
METAPHLAN_INDEX="mpa_vJan25_CHOCOPhlAnSGB_202503"
sample=$(ls *_1_trimmed_paired.fastq.gz | head -1 | sed 's/_1_trimmed_paired.fastq.gz//')
metaphlan ${sample}_1_trimmed_paired.fastq.gz,${sample}_2_trimmed_paired.fastq.gz \
  --input_type fastq --nproc $SLURM_CPUS_PER_TASK \
  --db_dir "$METAPHLAN_DB" -x "$METAPHLAN_INDEX" \
  --mapout ${sample}_mapout.sam -o ${sample}_metaphlan_test.txt
  
# Test is successful: time ~46 min, memory ~34 GB.
