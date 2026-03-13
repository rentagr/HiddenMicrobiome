
# HiddenMicrobiome

**Exploring the hidden diversity of the gut microbiome to discover diagnostic markers for disease classification using whole-genome sequencing (WGS) data.**

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Bash](https://img.shields.io/badge/bash-5.0%2B-green)](https://www.gnu.org/software/bash/)


---

##  About the Project

The human gut microbiome harbors a vast diversity of microorganisms, many of which are difficult to detect with conventional methods. This project aims to uncover **hidden microbial signatures** associated with various diseases (e.g., arthritis,osteoporosis) using whole-genome shotgun sequencing data. By integrating taxonomic, functional, and k‑mer based analyses, we try to build classification models that can differentiate between healthy and diseased individuals, ultimately leading to potential **diagnostic markers**.

The pipeline is implemented primarily in **Bash** (for workflow orchestration) and **Python** (for data processing, statistical analysis, and machine learning).

---

## Goals And Objectives

- **Goal:** Identify robust diagnostic markers from human gut WGS samples for disease classification.
- **Objectives:**
  - Literature review of existing microbiome‑disease associations.
  - Selection and preprocessing of public WGS datasets.
  - Extraction of significant features via:
    - **Taxonomic profiling** (Kraken2, MetaPhlAn)
    - **Functional profiling** 
    - **k‑mer based analysis**
  - Training and evaluation of classification models.
  - Development of a reproducible, modular analysis pipeline.
  - Annotation and biological interpretation of identified markers.

---

## Tools And Technologies

| Tool / Library      | Purpose                                      | Language   |
|---------------------|----------------------------------------------|------------|
| FastQC              | Quality control of raw reads                 | Bash       |
| Trimmomatic         | Read trimming and filtering                   | Bash       |
| Kraken2             | Taxonomic classification using k‑mers         | Bash       |
| MetaPhlAn           | Marker‑based taxonomic profiling               | Bash      |
| Python              | Data manipulation, stats, ML models           | Python     |
| - scikit‑learn      | Machine learning models                        | Python     |
| - matplotlib / seaborn| Visualisation (PCA, alpha diversity, etc.)    | Python     |

---

## Datasets

Currently, the project focuses on the following datasets:

- **Osteoporosis study**  
  - 59 human (female) gut samples from a public US database.  
  - 21 cases (with fracture), 38 healthy controls (without fracture).  
- **Arthritis study**  
    - 49 human gut samples from USA open database 
    - all ill, 20 worsened, 12 improved, 17 unclassified

---

## Pipeline Overview

1. **Quality control** – `FastQC`
2. **Trimming** – `Trimmomatic`
3. **Taxonomic profiling** – `Kraken2` (k‑mer based) and `MetaPhlAn` (marker genes)
4. **Feature extraction** – taxonomic abundances, functional profiles, k‑mer frequencies
5. **Statistical analysis & visualisation** – PCA, alpha diversity, differential abundance
6. **Machine learning** – classification models (e.g., Random Forest, SVM) with cross‑validation
7. **Marker interpretation** – annotation of top‑ranked features

---

## Getting Started

### Prerequisites

- **Python 3.8+** with packages: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, etc.
- **Bash** environment (Linux / macOS / WSL)
- External tools: `FastQC`, `Trimmomatic`, `Kraken2`, `MetaPhlAn` (see their respective installation guides)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rentagr/HiddenMicrobiome.git
   cd HiddenMicrobiome
    ```
2. in work

### Preliminary Results
 in work 

### Contributing
Contributions, issues, and feature requests are welcome! 

### Contacts
Project Link: https://github.com/rentagr/HiddenMicrobiome


