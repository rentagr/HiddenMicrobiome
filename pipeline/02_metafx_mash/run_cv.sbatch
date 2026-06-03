#!/bin/bash
#SBATCH -J rf_cv
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/rf_cv_%j.out
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/rf_cv_%j.err
#SBATCH -n 1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH -t 4:00:00

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "${REPO_ROOT}/config.sh"

cd "$SRR_FILES_DIR"
activate_env

"$METAFX" cv -t $SLURM_CPUS_PER_TASK  -w wd_cv -f wd_unique/feature_table.tsv -i wd_unique/samples_categories.tsv -n 5 --grid
