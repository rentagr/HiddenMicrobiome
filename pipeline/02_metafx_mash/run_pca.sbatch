#!/bin/bash
#SBATCH -J pca
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/pca_%j.out
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/pca_%j.err
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH -t 1:00:00

cd /mnt/tank/scratch/ris/SRR_files # || exit 1 if the transition fails, terminate the script with error code 1. This prevents further execution of commands in the wrong place.
source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

metafx pca -w wd_pca -f wd_unique/feature_table.tsv -i wd_unique/samples_categories.tsv --show

# PCA for bone density (but everything is done in approximately the same way)
(snakemake) ris@sphinx:/mnt/tank/scratch/ris/SRR_files/wd_unique_bmd$ metafx pca \
    -w wd_pca_bmd \
    -f feature_table.tsv \
    -i samples_categories.tsv \
    --show
metafx pca -w wd_pca_bmd -f feature_table.tsv -i samples_categories.tsv --show
