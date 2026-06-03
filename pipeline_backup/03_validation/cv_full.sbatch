#!/bin/bash
#SBATCH -J cv_metafx
#SBATCH -n 1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH -t 4:00:00

cd /mnt/tank/scratch/rislamova/SRR_files
source /nfs/home/rislamova/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

metafx cv -t 16 -w wd_cv -f wd_unique_bmd/feature_table.tsv -i wd_unique_bmd/samples_categories.tsv -n 5 --grid

# The output accuracy was 0.894 ± 0.038
