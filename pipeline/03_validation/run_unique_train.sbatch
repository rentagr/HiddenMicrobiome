#!/bin/bash
# run_unique_train.sbatch
#SBATCH -J unique_train
#SBATCH -n 1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH -t 12:00:00
#SBATCH --output=unique_train_%j.out
#SBATCH --error=unique_train_%j.err

cd /mnt/tank/scratch/ris/SRR_files/validate
source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

# Remove old temporary directories (for restart)
rm -rf wd_unique_train/unique_kmers_* wd_unique_train/components_* wd_unique_train/contigs_* wd_unique_train/features_*
rm -f wd_unique_train/feature_table.tsv

metafx unique -t 8 -m 128G -w wd_unique_train -k 31 -i train_samples.txt --kmers-dir wd_unique_train/kmers/kmers
