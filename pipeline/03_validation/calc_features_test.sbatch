#!/bin/bash
# calc_features_test.sbatch
#SBATCH -J calc_test
#SBATCH -n 1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH -t 6:00:00
#SBATCH --output=${LOG_DIR:-.}/calc_test_%j.out
#SBATCH --error=${LOG_DIR:-.}/calc_test_%j.err

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "${REPO_ROOT}/config.sh"

cd "$SRR_FILES_DIR/validate"
activate_env

# Create a list of absolute paths for test samples
awk '{print "/mnt/tank/scratch/ris/SRR_files/" $1}' test_samples.txt > test_abs.txt

"$METAFX" calc_features -t $SLURM_CPUS_PER_TASK -m 16G -w wd_calc_features_test -k 31 -d wd_unique_train -i $(cat test_abs.txt)
