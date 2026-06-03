sed -i 's/_r1\.fastq\.gz//' sample_categories.txt

# Create symbolic links to kmers without the _r1 suffix (so that the program can find them):

cd wd_unique/kmers/kmers
for f in *_r1.kmers.bin; do
    base=$(basename "$f" _r1.kmers.bin)
    ln -s "$f" "${base}.kmers.bin"
done
cd /mnt/tank/scratch/ris/SRR_files

# Delete the old temporary folders of the second stage to avoid the issue of overwriting, 
# which cannot be accepted or rejected interactively during the script:

rm -rf wd_unique/unique_kmers_healthy wd_unique/unique_kmers_case
rm -rf wd_unique/components_healthy wd_unique/components_case
rm -rf wd_unique/contigs_healthy wd_unique/contigs_case
