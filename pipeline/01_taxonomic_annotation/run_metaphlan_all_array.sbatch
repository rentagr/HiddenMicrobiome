#!/bin/bash
#SBATCH -J metaphlan_array
#SBATCH -a 1-57        
#SBATCH -n 1
#SBATCH --cpus-per-task=8
#SBATCH --mem=60G
#SBATCH -t 04:00:00
#SBATCH --partition=main
#SBATCH --error=${LOG_DIR:-.}/metaphlan_array_%a_%j.err
#SBATCH --output=${LOG_DIR:-.}/metaphlan_array_%a_%j.out

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "${REPO_ROOT}/config.sh"

cd "$SRR_FILES_DIR"
activate_env

# Getting a list of samples
samples=($(ls *_1_trimmed_paired.fastq.gz | sed 's/_1_trimmed_paired.fastq.gz//'))
total=${#samples[@]}
idx=$((SLURM_ARRAY_TASK_ID - 1))
if [ $idx -ge $total ]; then
    echo "Task ID $SLURM_ARRAY_TASK_ID exceeds number of samples ($total), exiting."
    exit 0
fi
sample=${samples[$idx]}

"$METAPHLAN" "${sample}_1_trimmed_paired.fastq.gz,${sample}_2_trimmed_paired.fastq.gz" \
    --input_type fastq \
    --nproc $SLURM_CPUS_PER_TASK \
    --db_dir "$METAPHLAN_DB" \
    -x "$METAPHLAN_INDEX" \
    --mapout "${sample}_mapout.sam" \
    --offline \
    -o "${sample}_metaphlan.txt"

# Deleting mapout after completion (so as not to clog the disk)
rm -f "${sample}_mapout.sam"

echo "Completed: $(date)"
