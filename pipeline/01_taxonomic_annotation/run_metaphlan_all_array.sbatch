#!/bin/bash
#SBATCH -J metaphlan_array
#SBATCH -a 1-57        
#SBATCH -n 1
#SBATCH --cpus-per-task=8
#SBATCH --mem=60G
#SBATCH -t 04:00:00
#SBATCH --partition=main
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/metaphlan_array_%a_%j.err
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/metaphlan_array_%a_%j.out

source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

cd /mnt/tank/scratch/ris/SRR_files || exit 1

METAPHLAN_DB="/mnt/tank/scratch/ris/databases/metaphlan"
METAPHLAN_INDEX="mpa_vJan25_CHOCOPhlAnSGB_202503"

# Getting a list of samples
# mapfile -t samples < <(ls *_1_trimmed_paired.fastq.gz | sed 's/_1_trimmed_paired.fastq.gz//')
# total=${#samples[@]}

# idx=$((SLURM_ARRAY_TASK_ID - 1))
# sample=${samples[$idx]}

# echo "Sample processing $SLURM_ARRAY_TASK_ID/$total: $sample"
# echo "Start: $(date)"

# if [[ ! -f "${sample}_1_trimmed_paired.fastq.gz" ]] || [[ ! -f "${sample}_2_trimmed_paired.fastq.gz" ]]; then
#     echo "ERROR: missing paired files for $sample"
#     exit 1
# fi
# Delete the old mapout, if any (when restarting)
# rm -f "${sample}_mapout.sam"

metaphlan "${sample}_1_trimmed_paired.fastq.gz,${sample}_2_trimmed_paired.fastq.gz" \
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
