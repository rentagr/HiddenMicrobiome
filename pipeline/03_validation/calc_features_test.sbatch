#!/bin/bash
# calc_features_test.sbatch
#SBATCH -J calc_test
#SBATCH -n 1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH -t 6:00:00
#SBATCH --output=calc_test_%j.out
#SBATCH --error=calc_test_%j.err

cd /mnt/tank/scratch/ris/SRR_files/validate
source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

# Create a list of absolute paths for test samples
awk '{print "/mnt/tank/scratch/ris/SRR_files/" $1}' test_samples.txt > test_abs.txt

metafx calc_features -t 8 -m 16G -w wd_calc_features_test -k 31 -d wd_unique_train -i $(cat test_abs.txt)
