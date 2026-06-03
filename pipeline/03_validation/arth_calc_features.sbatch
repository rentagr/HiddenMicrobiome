#!/bin/bash
#SBATCH -J calc_features
#SBATCH -n 1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH -t 24:00:00
#SBATCH --error=${LOG_DIR:-.}/calc_features_arth_%j.err
#SBATCH --output=${LOG_DIR:-.}/calc_features_arth_%j.out

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "${REPO_ROOT}/config.sh"

cd "$SRR_FILES_DIR"
activate_env

"$METAFX" calc_features \
    -t $SLURM_CPUS_PER_TASK \
    -m 16G \
    -w wd_calc_features \
    -k 31 \
    -d wd_unique_bmd \
    -i $(cat files_arth_filtered.txt)
