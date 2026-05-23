#!/bin/bash                                                                       # shebang: the script is executed in bash
#SBATCH -J download_srr                                                           # -J: job name, will be visible in the job queue
#SBATCH -n 1                                                                      # -n: number of CPU cores/tasks. Here 1 is a single-threaded script
#SBATCH --mem=8G                                                                  # RAM request: 8 GB for the entire task
#SBATCH -t 24:00:00                                                               # -t: the maximum working time (walltime) is 24 hours, if it is not completed during this time, the process will crash
#SBATCH --error=/mnt/tank/scratch/ris/SRR_files/Logs/download_srr_%j.err          # --error: where to write stderr (errors). %j is automatically replaced by the job ID.
#SBATCH --output=/mnt/tank/scratch/ris/SRR_files/Logs/download_srr_%j.out         # --output: where to write stdout (normal program output)

cd /mnt/tank/scratch/ris/SRR_files                                                # go to the working directory, where the downloaded SRR files and the source script itself will be located  
source /nfs/home/ris/miniforge3/etc/profile.d/mamba.sh                            # loading the initialization script mamba
mamba activate snakemake                                                          # activating the environment (environment name "snakemake")

# Download (example for a single file, it is better to use --split-files for paired ends)
fasterq-dump --split-files --outdir . SRR25006867
gzip *.fastq

# Note: The SRR list loop was used for bulk upload
