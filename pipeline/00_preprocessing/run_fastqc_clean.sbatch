#!/bin/bash
#SBATCH -J fastqc_clean
#SBATCH -n 1
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
#SBATCH -t 24:00:00
#SBATCH --error=${LOG_DIR:-.}/fastqc_clean_%j.err
#SBATCH --output=${LOG_DIR:-.}/fastqc_clean_%j.out

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "${REPO_ROOT}/config.sh"

cd "$SRR_FILES_DIR"
activate_env

"$FASTQC" --threads 2 *_trimmed_paired.fastq.gz
python "$(dirname "${BASH_SOURCE[0]}")/parse_fastqc_clean.py"

# Output file: fastqc_clean_summary.csv
