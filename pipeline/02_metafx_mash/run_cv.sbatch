#!/bin/bash
#SBATCH -J rf_cv
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/rf_cv_%j.out
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/rf_cv_%j.err
#SBATCH -n 1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH -t 4:00:00

cd /mnt/tank/scratch/ris/SRR_files || exit 1
source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

metafx cv -t 16 -w wd_cv -f wd_unique/feature_table.tsv -i wd_unique/samples_categories.tsv -n 5 --grid
