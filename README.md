
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
    - **k‑mer based feature extraction** (MetaFX) 
    - **Genomic distance estimation** (Mash)
  - Training and evaluation of classification models.
  - Development of a reproducible, modular analysis pipeline.
  - Annotation and biological interpretation of identified markers.

---

# Tools And Technologies

| Tool / Library        | Purpose                                                                                | Language      |
|-----------------------|----------------------------------------------------------------------------------------|---------------|
| FastQC                | Quality control of raw reads                                                           | Bash          |
| Trimmomatic           | Read trimming and filtering                                                            | Bash          |
| Kraken2               | Taxonomic classification using k‑mers                                                  | Bash          |
| MetaPhlAn             | Marker‑based taxonomic profiling                                                       | Bash          |
| MetaFX                | k‑mer‑based feature extraction, group‑specific k‑mers, classification (Random Forest)  | Bash / Python |
| Mash                  | MinHash‑based genomic distance estimation (Jaccard index)                              | Bash          |
| Python                | Data manipulation, stats, ML models                                                    | Python        |
| - scikit‑learn        | Machine learning models                                                                | Python        |
| - matplotlib / seaborn| Visualisation (PCA, alpha diversity, etc.)                                             | Python        |

---

# Datasets

Currently, the project focuses on the following datasets:

*(more details about dataset About_dataset.md)*
- **Osteoporosis study**  
  - 56 human (female) gut microbiome samples from a public US database.  
    - 20 cases (with fracture), 37 healthy (without fracture).  
    - 20 cases (with osteoporosis or osteopinia), 37 healthy (without osteoporosis or osteopinia)
    
  *Data preprocessing and feature extraction steps are in the Jupyter notebook: Steps/Step0_data preproc.ipynb, available in this repository.*
- **Result validation**  
    - To evaluate the predictive performance of the models, the labeled cohort (56 samples) was split into *training (44 samples)* and *test (12 samples)* sets.  
       - The test set contained 4 low-BMD samples and 8 normal-BMD samples.

  **Bone Mineral Density (BMD)** – a measure of bone strength and a key indicator for diagnosing osteoporosis

    - Two approaches were compared:
        1. **Kraken2** – taxonomic profiling, filtering of taxa present in <5% of samples.
        2. **MetaFX with preprocessing** – filtering of k‑mers present in <5% of training samples.
---


# Pipeline Overview

1. **Quality control** – `FastQC`
2. **Trimming** – `Trimmomatic`
3. **Taxonomic profiling** – `Kraken2` (k‑mer based) and `MetaPhlAn` (marker genes) –> *Steps/Step1_annotation.ipunb*
4. **Feature extraction**
      - taxonomic abundances (`Kraken2`, `MetaPhlAn` –> *Steps/Step1_annotation.ipunb/substeps 1.5 and 1.6*
5. **Genomic distance estimation** – `Mash` (MinHash‑based Jaccard index) –> *Steps/Step2_MetaFX_Mash.ipunb/substep 2.2*
6. **Statistical analysis & visualisation** – PCA, alpha diversity (Shannon index), beta diversity (`Mash` distances tab), mean relative abundance –> *Steps/Step1_annotation.ipunb/substeps from 1.7 and /Step2_MetaFX_Mash.ipunb/substeps from 2.2*
7. **Machine learning** –> *Steps/Step3_validation.ipunb*
      - Random Forest (`scikit‑learn`) on taxonomic profiles
      - Random Forest (`MetaFX`) on k‑mer features
      - 5‑fold cross‑validation and train/test split

8. **Marker interpretation** – annotation of top‑ranked features using NCBI (blastn, blastx) and leterature

---

# Prerequisites

- **Python 3.8+** with packages: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, etc.
- **Bash** environment (Linux / macOS / WSL)
- External tools: `FastQC`, `Trimmomatic`, `Kraken2`, `MetaPhlAn`, `MetaFX`, `Mash` (see their respective installation guides)

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

---
*For a complete list of top‑20 contigs, please refer to [top20_bmd.fasta](https://github.com/rentagr/HiddenMicrobiome/releases/download/v1.0/top20_bmd.fasta) in the repository.*

## Fracture
**Mean relative abundance**
![Mean relative abundance](./images/Fracture/Pasted%20image.png)

**Table: Top discriminatory contigs between normal and low bone density groups identified by Random Forest (MetaFX results)**

| Sequence ID | Predicted bacterium | Predicted gene/protein | Function / role | Reference |
|-------------|---------------------|------------------------|----------------|-----------|
| `case_474` | *Mediterraneibacter massiliensis* | GTPase ObgE (WP_117993920.1) | P-loop GTPase involved in ribosome assembly, cell cycle, cell wall synthesis, and stress response. Isolated from faeces of an obese patient. No direct link to bone pathology. | [PMID 29855844](https://pubmed.ncbi.nlm.nih.gov/29855844/) |
| `case_263` | *Bacteroides luhongzhouii* and *Bacteroides zhangwenhongii* (two novel species) | not specified (16S rRNA identification) | New species of genus *Bacteroides* isolated from faeces of healthy humans. Typical gut commensals, no signs of pathogenicity. | [CP182860](https://www.ncbi.nlm.nih.gov/nucleotide/CP182860.1) (species description) |
| `case_90` | *Bacteroides* sp. A1C1 (species not determined) | not specified | Gram-negative anaerobic rod isolated from cat faeces. Likely incidental detection; clinical significance for humans unclear. | [PRJNA522935](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA522935) |
| `case_108` | *Bacteroides thetaiotaomicron* | ATP-dependent zinc metalloprotease FtsH (CAK7001341.1) | Universal protease essential for cell division, stress resistance, and membrane homeostasis. Key gut commensal, beneficial for polysaccharide breakdown. | none (protein link available) |
| `case_22` | *Phocaeicola vulgatus* (formerly *Bacteroides vulgatus*) | not specified | Candidate strain NB1000S for treatment of hyperoxaluria (oxalate reduction). May indirectly affect calcium metabolism, but no direct bone link proven. | [PRJNA1211572](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1211572) |
| `case_16` | *Bacteroides ovatus* | not specified | Typical gut commensal involved in dietary fibre fermentation. Neutral microorganism, not associated with bone pathology. | [CP134818](https://www.ncbi.nlm.nih.gov/nucleotide/CP134818.1) |

*Note*: In the case (fracture) group, no bacterium with a proven direct link to osteomyelitis or bone resorption was found, in contrast to the low bone density group where Ruthenibacterium lactatiformans was present. The dominant bacteria are common commensals of the genus Bacteroides.

---
*For a complete list of top‑20 contigs, please refer to [top20_fracture.fasta](https://github.com/rentagr/HiddenMicrobiome/releases/download/v1.0/top20_fracture.fasta) in the repository.*

## Validation results 

| Method | Accuracy | Recall (low) | Precision (low) | Correct low (out of 4) | Correct normal (out of 8) |
|--------|----------|--------------|----------------|------------------------|---------------------------|
| Kraken2 | **0.833** (10/12) | 0.50 | 1.00 | 2 | 8 |
| MetaFX + preprocessing | 0.750 (9/12) | 0.25 | 1.00 | 1 | 8 |

### Detailed error analysis

- **Kraken2** misclassified two low‑BMD samples as normal: `SRR25006884` and `SRR25006909`. It correctly predicted `SRR25006887` and `SRR25006893`.
- **MetaFX + preprocessing** misclassified three low‑BMD samples (`SRR25006884`, `SRR25006887`, `SRR25006909`) and correctly predicted only `SRR25006893`.
- **Both methods** made identical errors on `SRR25006884` and `SRR25006909`, and both correctly identified `SRR25006893`.
- All normal samples were correctly predicted by every method.

Given the small test set (only 4 low‑BMD samples), the difference of 1–2 correctly predicted samples is not statistically significant.  
Thus, the performance of **Kraken2** and **MetaFX with preprocessing** is **comparable**, and the preprocessing step substantially improved MetaFX (accuracy rose from 66.7% to 75%, enabling detection of at least one low‑BMD sample).

The consistently misclassified low‑BMD samples (`SRR25006884` and `SRR25006909`) might have bone density reduction driven by non‑microbiome factors (e.g., genetic connective tissue disorders), which warrants further clinical investigation.

## Top‑20 contigs discriminating low/normal groups (trained on the training set)

Using the Random Forest model from **MetaFX with preprocessing**, the most important features (k‑mers assembled into contigs) were extracted and annotated via BLAST. Selected results are shown below; the full list of 20 contigs is available in Supplementary Materials.

| Sequence ID | Predicted taxon | Predicted gene/protein | Function / role | Reference |
|-------------|----------------|------------------------|----------------|-----------|
| `low_305` | *Ruthenibacterium lactatiformans* | not specified | Cleavage of sulfated compounds; potential pathogen associated with vertebral osteomyelitis and bacteremia | [PMC11247725](https://pmc.ncbi.nlm.nih.gov/articles/PMC11247725/) |
| `low_27` | *Bacteroides ovatus* (chromosome CP103080.1) | LTA synthase family protein | Commensal with immunomodulatory properties; role in bone density unclear | [BLAST](https://www.ncbi.nlm.nih.gov/nucleotide/CP103080.1) |
| `low_701` | *Pilosibacter sp.* (CP175657.1) | AEC family transporter | Gut commensal; no direct bone link | [BLAST](https://www.ncbi.nlm.nih.gov/nucleotide/CP175657.1) |
| `low_87` | *Dorea longicatena* | MptD family putative ECF transporter S component [Dorea]| Ferments carbohydrates → short‑chain fatty acids; associated with increased muscle mass and bone mineral density in the HUNT cohort (2023) | [MDPI Nutrients 13(6):2032](https://www.mdpi.com/2072-6643/13/6/2032); [Nat Commun 14, 2250 (2023)](https://www.nature.com/articles/s41467-023-37978-9) |
| `normal_613` | *Bacteroides finegoldii* | translocation/assembly module TamB domain-containing protein, partial| Commensal with anti‑inflammatory properties; strengthens intestinal barrier, reduces pro‑inflammatory cytokines (IL‑6, TNF‑α, IL‑1β), and suppresses NF‑κB and MAPK pathways; may contribute to normal bone density via systemic anti‑inflammatory effects| [PMC12442397](https://pmc.ncbi.nlm.nih.gov/articles/PMC12442397/); [AEM.00891-25](https://journals.asm.org/doi/full/10.1128/aem.00891-25) |

### Biological interpretation

The presence of *Dorea longicatena* (contig `low_87`) is particularly interesting because this species shows a **paradoxical role**: it has been positively associated with bone mineral density and muscle mass, but also linked to obesity and colorectal cancer.  
This suggests that the low‑BMD patient group is microbially heterogeneous, which could explain why some low‑BMD samples were misclassified by both methods.

---
*For a complete list of top‑20 contigs, please refer to [top20_contigs_metafx_preproc.fasta]() in the repository.*

## Contributing
Contributions, issues, and feature requests are welcome! 

## Contacts
Project Link: https://github.com/rentagr/HiddenMicrobiome


