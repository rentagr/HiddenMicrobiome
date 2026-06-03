#!/bin/bash
#SBATCH -J metaphlan_one
#SBATCH -n 1
#SBATCH --cpus-per-task=8
#SBATCH --mem=60G
#SBATCH -t 04:00:00
#SBATCH --partition=main
#SBATCH --error=${LOG_DIR:-.}/metaphlan_one_%j.err
#SBATCH --output=${LOG_DIR:-.}/metaphlan_one_%j.out

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "${REPO_ROOT}/config.sh"

cd "$SRR_FILES_DIR"
activate_env

sample=$(ls *_1_trimmed_paired.fastq.gz | head -1 | sed 's/_1_trimmed_paired.fastq.gz//')
"$METAPHLAN" ${sample}_1_trimmed_paired.fastq.gz,${sample}_2_trimmed_paired.fastq.gz \
  --input_type fastq --nproc $SLURM_CPUS_PER_TASK \
  --db_dir "$METAPHLAN_DB" -x "$METAPHLAN_INDEX" \
  --mapout ${sample}_mapout.sam -o ${sample}_metaphlan_test.txt
  
# Test is successful: time ~46 min, memory ~34 GB.
