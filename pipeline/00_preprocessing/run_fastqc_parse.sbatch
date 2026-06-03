#!/bin/bash
#SBATCH -J fastqc_parse
#SBATCH -n 1
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
#SBATCH -t 24:00:00
#SBATCH --error=${LOG_DIR:-.}/fastqc_parse_%j.err
#SBATCH --output=${LOG_DIR:-.}/fastqc_parse_%j.out

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "${REPO_ROOT}/config.sh"

cd "$SRR_FILES_DIR"
activate_env

"$FASTQC" --threads 2 *.fastq.gz
python "$(dirname "${BASH_SOURCE[0]}")/parse_fastqc.py"
