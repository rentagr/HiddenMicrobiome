#!/bin/bash
#SBATCH -J calc_features
#SBATCH -n 1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH -t 24:00:00
#SBATCH --error=/mnt/tank/scratch/rislamova/SRR_files/Logs/calc_features_%j.err
#SBATCH --output=/mnt/tank/scratch/rislamova/SRR_files/Logs/calc_features_%j.out

cd /mnt/tank/scratch/ris/SRR_files
source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

metafx calc_features \
    -t 8 \
    -m 16G \
    -w wd_calc_features \
    -k 31 \
    -d wd_unique_bmd \
    -i $(cat files_arth_filtered.txt)
