#!/bin/bash
# run_unique_train.sbatch
#SBATCH -J unique_train
#SBATCH -n 1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH -t 12:00:00
#SBATCH --output=${LOG_DIR:-.}/unique_train_%j.out
#SBATCH --error=${LOG_DIR:-.}/unique_train_%j.err

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "${REPO_ROOT}/config.sh"

cd "$SRR_FILES_DIR/validate"
activate_env

# Remove old temporary directories (for restart)
rm -rf wd_unique_train/unique_kmers_* wd_unique_train/components_* wd_unique_train/contigs_* wd_unique_train/features_*
rm -f wd_unique_train/feature_table.tsv

"$METAFX" unique -t $SLURM_CPUS_PER_TASK -m 128G -w wd_unique_train -k 31 -i train_samples.txt --kmers-dir wd_unique_train/kmers/kmers
