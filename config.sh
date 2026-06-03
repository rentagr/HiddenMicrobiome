#!/bin/bash

# config.sh – centralized path settings for pipeline

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# The root folder for all data 
export DATA_ROOT="${DATA_ROOT:-${REPO_ROOT}/data}"

# Subfolders inside DATA_ROOT
export SRR_FILES_DIR="${SRR_FILES_DIR:-${DATA_ROOT}/SRR_files}"
export LOG_DIR="${LOG_DIR:-${REPO_ROOT}/logs}"
export KRAKEN2_DB="${KRAKEN2_DB:-${DATA_ROOT}/databases/kraken2}"
export METAPHLAN_DB="${METAPHLAN_DB:-${DATA_ROOT}/databases/metaphlan}"
export METAPHLI_INDEX="${METAPHLI_INDEX:-mpa_vJan25_CHOCOPhlAnSGB_202503}"

# Paths to executable files 
export FASTERQ_DUMP="${FASTERQ_DUMP:-fasterq-dump}"
export FASTQC="${FASTQC:-fastqc}"
export TRIMMOMATIC="${TRIMMOMATIC:-trimmomatic}"
export KRAKEN2="${KRAKEN2:-kraken2}"
export METAPHLAN="${METAPHLAN:-metaphlan}"
export METAFX="${METAFX:-metafx}"
export MASH="${MASH:-mash}"

# Name of the conda environment
export CONDA_ENV="${CONDA_ENV:-snakemake}"

# Function to activate the environment (called in each script)
# It is assumed that conda has already been initialized in the shell
activate_env() {
    eval "$(conda shell.bash hook)"
    conda activate "$CONDA_ENV"
}
