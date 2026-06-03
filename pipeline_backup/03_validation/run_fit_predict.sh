#!/bin/bash
set -euo pipefail

cd /mnt/tank/scratch/ris/SRR_files/validate
source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

# Fit model
metafx fit -w wd_fit -f feature_table_train_clean.tsv -i train_categories_clean.tsv --name rf_model

# Predict on test
metafx predict -w wd_predict -f feature_table_test_clean.tsv --model wd_fit/rf_model.joblib --name predictions
