#!/bin/bash
#SBATCH -J copy_kmers
#SBATCH -n 1
#SBATCH --mem=8G
#SBATCH -t 0:30:00

cd /mnt/tank/scratch/ris/SRR_files/validate

# Create directory for kmers
mkdir -p wd_unique_train/kmers/kmers

# Copy kmers for all training samples (names with _r1)
cut -f1 train_samples.txt | sed 's/_r1.fastq.gz//' | while read name; do
    src="/mnt/tank/scratch/ris/SRR_files/wd_unique_bmd/kmers/kmers/${name}_r1.kmers.bin"
    dst="wd_unique_train/kmers/kmers/${name}_r1.kmers.bin"
    if [ -f "$src" ]; then
        cp -v "$src" "$dst"
    else
        echo "Skipped: $name"
    fi
done

# Create symlinks without _r1 (if needed)
cd wd_unique_train/kmers/kmers
for f in *_r1.kmers.bin; do
    ln -sf "$f" "${f/_r1./.}"
done
