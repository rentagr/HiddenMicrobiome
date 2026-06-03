#!/bin/bash
#SBATCH -J kraken_all
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=250G
#SBATCH -t 48:00:00
#SBATCH --partition=main
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/kraken_all_%j.err
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/kraken_all_%j.out

source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh
mamba activate snakemake

cd /mnt/tank/scratch/ris/SRR_files || exit 1

KRAKEN_DB="/mnt/tank/scratch/ris/databases/kraken2"

# Getting a list of all the samples
samples=($(ls *_1_trimmed_paired.fastq.gz | sed 's/_1_trimmed_paired.fastq.gz//'))

total=${#samples[@]}
echo "Samples found: $total"
echo "General task start: $(date)"

for i in "${!samples[@]}"; do
    sample=${samples[$i]}
    echo "Sample processing $((i+1))/$total: $sample"
    echo "Start: $(date)"

    if [[ ! -f "${sample}_1_trimmed_paired.fastq.gz" ]] || [[ ! -f "${sample}_2_trimmed_paired.fastq.gz" ]]; then
        echo "ERROR: missing paired files for $sample, skipping"
        continue
    fi # closing statement

    kraken2 --db "$KRAKEN_DB" \
        --threads $SLURM_CPUS_PER_TASK \
        --paired "${sample}_1_trimmed_paired.fastq.gz" "${sample}_2_trimmed_paired.fastq.gz" \
        --output "${sample}.kraken.out" \
        --report "${sample}.kraken.report" \
         --use-names

    echo "End: $(date)"
done

echo "All samples have been processed. End time: $(date)"
