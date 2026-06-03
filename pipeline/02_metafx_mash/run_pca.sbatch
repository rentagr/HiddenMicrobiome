#!/bin/bash
#SBATCH -J pca
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/pca_%j.out
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/pca_%j.err
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH -t 1:00:00

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "${REPO_ROOT}/config.sh"

cd "$SRR_FILES_DIR"
activate_env

"$METAFX" pca -w wd_pca -f wd_unique/feature_table.tsv -i wd_unique/samples_categories.tsv --show

