
# HiddenMicrobiome

**Exploring the hidden diversity of the gut microbiome to discover diagnostic markers for osteoporosis disease classification using whole-genome sequencing (WGS) data.**

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Bash](https://img.shields.io/badge/bash-5.0%2B-green)](https://www.gnu.org/software/bash/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20130730.svg)](https://doi.org/10.5281/zenodo.20130730)

---

#  About the Project

The human gut microbiome harbors a vast diversity of microorganisms, many of which are difficult to detect with conventional methods. This project aims to uncover **hidden microbial signatures** associated with various diseases (e.g. osteoporosis) using whole-genome shotgun sequencing data. 

By integrating taxonomic, functional, and k‑mer‑based analyses, we attempt to identify subtle patterns that can robustly differentiate between healthy and diseased individuals. The ultimate goal is to discover potential diagnostic markers for human diseases.

The pipeline is implemented primarily in **Bash** and **Python** (for data processing, statistical analysis, and machine learning).

---

# Goals And Objectives

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

# Tools And Technologies

| Tool / Library      | Purpose                                      | Language   |
|---------------------|----------------------------------------------|------------|
| FastQC              | Quality control of raw reads                 | Bash       |
| Trimmomatic         | Read trimming and filtering                  | Bash       |
| Kraken2             | Taxonomic classification using k‑mers        | Bash       |
| MetaPhlAn           | Marker‑based taxonomic profiling             | Bash       |
| Python              | Data manipulation, stats, ML models          | Python     |
| - scikit‑learn        | Machine learning models                    | Python     |
| - matplotlib / seaborn| Visualisation (PCA, alpha diversity, etc.) | Python     |

---

# Datasets

Currently, the project focuses on the following datasets:

- **Osteoporosis study**  
  - 59 human (female) gut samples from a public US database.  
    - 21 cases (with fracture), 38 healthy controls (without fracture).  
    - xx cases (with osteoporosis or osteopinia), xx healthy controls (without fracture)
- **Result validation**  
    - 50 human gut samples from Chinise open database 
    - xxxx

---

# Pipeline Overview

1. **Quality control** – `FastQC`
2. **Trimming** – `Trimmomatic`
3. **Taxonomic profiling** – `Kraken2` (k‑mer based) and `MetaPhlAn` (marker genes)
4. **Feature extraction** – taxonomic abundances, functional profiles, k‑mer frequencies
5. **Statistical analysis & visualisation** – PCA, alpha diversity, differential abundance
6. **Machine learning** – classification models (e.g., Random Forest, SVM) with cross‑validation
7. **Marker interpretation** – annotation of top‑ranked features using NCBI (blastn, blastx) and leterature

---

# Getting Started

## Prerequisites

- **Python 3.8+** with packages: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, etc.
- **Bash** environment (Linux / macOS / WSL)
- External tools: `FastQC`, `Trimmomatic`, `Kraken2`, `MetaPhlAn` (see their respective installation guides)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rentagr/HiddenMicrobiome.git
   cd HiddenMicrobiome
    ```
2. in work

# Results

## BMD
**Mean relative abundance'**
![Mean relative abundance'](./images/BMD/Pasted%20image.png)

**Table: Top discriminatory contigs between normal and low bone density groups identified by Random Forest (MetaFX results)**

| Sequence ID | Predicted bacterium | Predicted gene/protein | Function / role | Reference (article) |
|-------------|---------------------|------------------------|----------------|---------------------|
| `low_238` | *Ruthenibacterium lactatiformans* | Sulfatase-like hydrolase/transferase (WP_288694885.1) | Cleavage of sulfated compounds; potential pathogen associated with vertebral osteomyelitis and bacteremia (first human case reported in 2024) | [PMC11247725](https://pmc.ncbi.nlm.nih.gov/articles/PMC11247725/) |
| `low_340` | *Caproiciproducens lactatisolvens* | Not specified (16S rRNA) | Caproic acid production; no established link to bone pathology (found in a patient with low bone density) | none |
| `normal_602` | *Bacteroides finegoldii* | Transmembrane permease (DMT family); putative transmembrane permease (CDA85058.1) | Hyaluronic acid degradation to oligosaccharides, potentially beneficial for joint and skin health; normal commensal | [PMID 36586473](https://pubmed.ncbi.nlm.nih.gov/36586473/) |
| `low_605` | *[Clostridium] leptum* (metagenome-assembled) | Histidine kinase sensor (MFQ9845483.1) | Two-component signal transduction system, adaptation to stress/nutrients; role in bone density unclear | none |



## Fracture
**Mean relative abundance'**
![Mean relative abundance'](./images/Fracture/Pasted%20image.png)

**Table: Top discriminatory contigs between normal and low bone density groups identified by Random Forest (MetaFX results)**

| Sequence ID | Predicted bacterium | Predicted gene/protein | Function / role | Reference |
|-------------|---------------------|------------------------|----------------|-----------|
| `case_474` (465_1) | *Mediterraneibacter massiliensis* | GTPase ObgE (WP_117993920.1) | P-loop GTPase involved in ribosome assembly, cell cycle, cell wall synthesis, and stress response. Isolated from faeces of an obese patient. No direct link to bone pathology. | [PMID 29855844](https://pubmed.ncbi.nlm.nih.gov/29855844/) |
| `case_263` (254_1) | *Bacteroides luhongzhouii* and *Bacteroides zhangwenhongii* (two novel species) | not specified (16S rRNA identification) | New species of genus *Bacteroides* isolated from faeces of healthy humans. Typical gut commensals, no signs of pathogenicity. | [CP182860](https://www.ncbi.nlm.nih.gov/nucleotide/CP182860.1) (species description) |
| `case_90` (84_1) | *Bacteroides* sp. A1C1 (species not determined) | not specified | Gram-negative anaerobic rod isolated from cat faeces. Likely incidental detection; clinical significance for humans unclear. | [PRJNA522935](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA522935) |
| `case_108` (102_1) | *Bacteroides thetaiotaomicron* | ATP-dependent zinc metalloprotease FtsH (CAK7001341.1) | Universal protease essential for cell division, stress resistance, and membrane homeostasis. Key gut commensal, beneficial for polysaccharide breakdown. | none (protein link available) |
| `case_22` (19_1) | *Phocaeicola vulgatus* (formerly *Bacteroides vulgatus*) | not specified | Candidate strain NB1000S for treatment of hyperoxaluria (oxalate reduction). May indirectly affect calcium metabolism, but no direct bone link proven. | [PRJNA1211572](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1211572) |
| `case_16` (13_1) | *Bacteroides ovatus* | not specified | Typical gut commensal involved in dietary fibre fermentation. Neutral microorganism, not associated with bone pathology. | [CP134818](https://www.ncbi.nlm.nih.gov/nucleotide/CP134818.1) |

*Note*: In the case (fracture) group, no bacterium with a proven direct link to osteomyelitis or bone resorption was found, in contrast to the low bone density group where Ruthenibacterium lactatiformans was present. The dominant bacteria are common commensals of the genus Bacteroides.

## Contributing
Contributions, issues, and feature requests are welcome! 

## Contacts
Project Link: https://github.com/rentagr/HiddenMicrobiome


