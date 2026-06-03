#!/bin/bash
#SBATCH -J cv_metafx
#SBATCH -n 1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH -t 4:00:00
#SBATCH --output=${LOG_DIR:-.}/cv_full_%j.out
#SBATCH --error=${LOG_DIR:-.}/cv_full_%j.err

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "${REPO_ROOT}/config.sh"

cd "$SRR_FILES_DIR/wd_unique_bmd"   # или другая папка с feature_table.tsv
activate_env


"$METAFX" cv -t $SLURM_CPUS_PER_TASK -w wd_cv -f wd_unique_bmd/feature_table.tsv -i wd_unique_bmd/samples_categories.tsv -n 5 --grid

# The output accuracy was 0.894 ± 0.038
