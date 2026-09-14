# 🧠 2025_VNSiSVD-Report: Paired Vagus Nerve Stimulation for Neurovascular Modulation in Vascular Cognitive Impairment

**Official Analysis Pipeline and Codebase for the First-in-Human Study**

[![Brain Stimulation](https://img.shields.io/badge/Journal-Brain%20Stimulation-red.svg)](https://doi.org/10.1016/j.brs.2026.103212)
[![DOI: 10.1016/j.brs.2026.103212](https://img.shields.io/badge/DOI-10.1016%2Fj.brs.2026.103212-blue.svg)](https://doi.org/10.1016/j.brs.2026.103212)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Trial: ChiCTR2400085374](https://img.shields.io/badge/Clinical%20Trial-ChiCTR2400085374-success.svg)](https://www.chictr.org.cn/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://www.python.org/)
[![R 4.2+](https://img.shields.io/badge/R-4.2+-blue.svg)](https://www.r-project.org/)

---

## 📖 Paper Information & Citation

This repository provides the computational pipelines, preprocessing workflows, and statistical analyses accompanying:

> **Ju, Sihan†, Liyi Qian†, Yunqing Ying†, Siheng Feng, Yutong Zhao, Yunfeng Zhang, Yulian Zhu, Xin Cheng\*, Qi Yue\*, and Liang Chen\*.**  
> *"Paired vagus nerve stimulation for neurovascular modulation in vascular cognitive impairment: a first-in-human study."*  
> **Brain Stimulation** (2026): 103212.  
> 🔗 **DOI**: [https://doi.org/10.1016/j.brs.2026.103212](https://doi.org/10.1016/j.brs.2026.103212)  
> *†These authors contributed equally to this work. \*Corresponding authors.*

```bibtex
@article{ju2026paired,
  title={Paired vagus nerve stimulation for neurovascular modulation in vascular cognitive impairment: a first-in-human study},
  author={Ju, Sihan and Qian, Liyi and Ying, Yunqing and Feng, Siheng and Zhao, Yutong and Zhang, Yunfeng and Zhu, Yulian and Cheng, Xin and Yue, Qi and Chen, Liang},
  journal={Brain Stimulation},
  pages={103212},
  year={2026},
  publisher={Elsevier},
  doi={10.1016/j.brs.2026.103212}
}
```

---

## 🌟 Clinical Background & Study Highlights

Cerebral small vessel disease (cSVD) is a principal driver of vascular cognitive impairment (VCI), primarily orchestrated by dysfunction across the **neurovascular unit (NVU)**. Conventional pharmacological strategies target vascular risk factors without directly restoring NVU integrity.

In this first-in-human case study, we implemented a 6-month protocol combining **Vagus Nerve Stimulation paired with Cognitive Training (VNS-CT)** in a 54-year-old female patient with symptomatic sporadic cSVD (3 hours daily VNS paired with structured cognitive exercises).

By integrating acute within-subject stimulation-locked experiments with 6-month longitudinal multimodal magnetic resonance imaging (MRI), this codebase reproduces four core neurovascular dimensions:

```
[ Paired VNS-CT Intervention (6 Months) ]
  ├── Acute Stimulus-Locked Protocol (Pre-VNS ──> VNS ──> Post-VNS)
  └── Longitudinal Follow-up (Baseline ──> 6-Month Post-Intervention)
                   │
                   ▼
┌──────────────────────────────────────┬──────────────────────────────────────┐
│        Neural Modulation             │        Vascular & NVU Plasticity     │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ 1. Cortical Function (rs-fMRI ALFF)  │ 3. Cerebrovascular Reactivity (CVR)  │
│    • Acute dorsolateral-ventromedial │    • Gas-free resting-state BOLD     │
│      activation gradient             │    • Significant elevation in left   │
│    • Longitudinal consolidation in   │      frontal and temporal cortex     │
│      dorsal attention & somatomotor  │                                      │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ 2. Microstructure (DTI Differential) │ 4. BBB & White Matter Hyperintensity │
│    • Tractography via DSI Studio     │    • DCE-MRI Tofts modeling (Ktrans) │
│    • Concomitant FA increase &       │    • Pronounced BBB leakage drop     │
│      MD/RD decrease in association   │    • 657 mm³ (9.64%) reduction in    │
│      and motor projection fibers     │      deep WMH volume (DeepWMH)       │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 🏗️ Repository Architecture

The codebase is organized into modules corresponding to the published figures:

```text
2025_VNSiSVD-Report/
├── Fig1-DTI/                                    # Diffusion Tensor Imaging & Differential Tractography
│   ├── dply_dcm2bids_dxi_250325.sh              # BIDS formatting for diffusion sequences
│   ├── dply_qsiprep_dxi_250325.sh               # QSIprep preprocessing container workflow
│   ├── dply_qsirecon_dxi_250407.sh              # QSIRecon with DSI Studio GQI reconstruction
│   ├── dply_extract-dsistudio_250501.py         # Tract bundle metric extraction (FA, MD, RD)
│   └── stat_dxi_250410.r                        # Statistical comparison & ternary change tables
│
├── Fig1-rsfMRI/                                 # Resting-State fMRI & Functional Gradient Mapping
│   ├── ALFF.py                                  # Amplitude of Low-Frequency Fluctuations computation
│   ├── eigenstrapping_test.py                   # Spatial autocorrelation-preserving null tests
│   ├── neuromap.py                              # Neuromaps cortical gradient & hierarchical mapping
│   ├── neurosynth.py                            # Meta-analytic cognitive decoding via NeuroSynth
│   └── rscvr.py                                 # Resting-state fMRI CVR signal extraction
│
├── Fig2-CVR/                                    # Cerebrovascular Reactivity (rs-CVR) Modeling
│   ├── dply_dcm2bids_cvr_250414.sh              # BIDS curation for BOLD CVR data
│   ├── dply_deepprep_cvr_250414.sh              # DeepPrep / fMRIPrep BOLD preprocessing pipeline
│   └── analysis_rsCVRmap_251121.py              # rs-CVR map generation, cortical ROI permutation test
│
├── Fig2-DCE/                                    # Dynamic Contrast-Enhanced MRI & BBB Permeability
│   ├── 001_dcm2nii.sh                           # DICOM to NIfTI conversion
│   ├── 002_analysis_dcemr.m                     # MATLAB DCE pharmacokinetic modeling (Tofts model Ktrans)
│   ├── 003_brainmask.ipynb                      # Brain masking and parenchymal tissue extraction
│   ├── dply_separate4D.py                       # 4D dynamic series decomposition
│   ├── dply_rearrangeT1map.py                   # Variable Flip Angle T1 mapping alignment
│   ├── dply_ants_regMeanDCE.ipynb               # ANTs rigid + deformable co-registration
│   ├── calculate_ktrans_diffrentROI.py          # ROI-wise Ktrans extraction (GM, WMH, NAWM)
│   ├── 251120_permtest.py                       # Permutation test for regional delta Ktrans
│   └── vis_ktrans.py                            # Ktrans parametric map visualization
│
├── Fig2-WMH/                                    # White Matter Hyperintensity Volumetry & Lesion Profiling
│   ├── dply_deepwmh_wmhseg_250415.sh            # Deep learning WMH segmentation (DeepWMH)
│   ├── dlpy_freesurfer_aparc2aseg.sh            # FreeSurfer aparc+aseg anatomical parcellation
│   ├── dply_ants_regFLAIR_250415.ipynb          # 3D FLAIR to T1w co-registration via ANTs
│   ├── dply_ants_regFLAIR_strtnewmethods_*.ipynb# Longitudinal symmetric registration
│   ├── analysis_wmh_volume_250907.ipynb         # Quantitative lesion volume (Deep vs Periventricular WMH)
│   └── analysis_wmh_visualization.ipynb         # 3D lesion rendering & surface mapping
│
├── environment.yml                              # Conda environment definition
├── requirements.txt                             # Python package dependencies
├── .gitignore                                   # Ignore rules for MRI binaries & caches
├── LICENSE                                      # MIT Open Source License
└── README.md                                    # Project documentation (this file)
```

---

## ⚡ Getting Started & Prerequisites

### 1. Environment Setup

#### Python Environment (via Conda)
```bash
conda env create -f environment.yml
conda activate vns_isvd
```

Or via `pip`:
```bash
pip install -r requirements.txt
```

#### R Dependencies (for DTI statistical summaries)
```R
install.packages(c("tidyverse", "openxlsx", "ggplot2"))
```

### 2. External Neuroimaging Software
The pipeline leverages industry-standard neuroimaging engines (recommended to run via Singularity or Docker):
- **BIDS Converter**: `dcm2bids` (v2.1.6+) / `dcm2niix`
- **Diffusion MRI**: [QSIprep](https://qsiprep.readthedocs.io/) (v0.19+) & [DSI Studio](https://dsi-studio.labsolver.org/) (GQI reconstruction)
- **Functional MRI**: [DeepPrep](https://github.com/pku-brain-net/DeepPrep) / [fMRIPrep](https://fmriprep.org/)
- **Coregistration & Parcellation**: [ANTs](http://stnava.github.io/ANTs/) (v2.4+) & [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/) (v7.3+)
- **Pharmacokinetics**: MATLAB (R2022b+) for DCE-MRI extended Tofts modeling

---

## 🔬 Figure-by-Figure Reproduction Guide

### Figure 1: Functional & Structural Plasticity

#### 1. rs-fMRI ALFF & Cortical Hierarchy (`Fig1-rsfMRI/`)
- Preprocess BOLD data and compute Amplitude of Low-Frequency Fluctuations (ALFF, 0.01–0.08 Hz):
  ```bash
  python Fig1-rsfMRI/ALFF.py
  ```
- Assess spatial alignment with canonical molecular-psychological cortical gradients using eigenstrapping:
  ```bash
  python Fig1-rsfMRI/neuromap.py
  python Fig1-rsfMRI/eigenstrapping_test.py
  ```
- Meta-analytic cognitive decoding with NeuroSynth:
  ```bash
  python Fig1-rsfMRI/neurosynth.py
  ```

#### 2. DTI Differential Tractography (`Fig1-DTI/`)
- Execute BIDS curation and QSIprep diffusion preprocessing:
  ```bash
  bash Fig1-DTI/dply_dcm2bids_dxi_250325.sh
  bash Fig1-DTI/dply_qsiprep_dxi_250325.sh
  bash Fig1-DTI/dply_qsirecon_dxi_250407.sh
  ```
- Extract tractography metrics (FA, MD, RD) and run ternary statistics:
  ```bash
  python Fig1-DTI/dply_extract-dsistudio_250501.py
  Rscript Fig1-DTI/stat_dxi_250410.r
  ```

---

### Figure 2: Neurovascular Unit & Parenchymal Integrity

#### 1. Resting-State Cerebrovascular Reactivity (`Fig2-CVR/`)
- Preprocess BOLD series with DeepPrep:
  ```bash
  bash Fig2-CVR/dply_deepprep_cvr_250414.sh
  ```
- Model voxel-wise rs-CVR and perform non-parametric lobe-level permutation testing:
  ```bash
  python Fig2-CVR/analysis_rsCVRmap_251121.py
  ```

#### 2. Blood-Brain Barrier Permeability by DCE-MRI (`Fig2-DCE/`)
- Decompose 4D dynamic contrast-enhanced scans and coregister via ANTs:
  ```bash
  python Fig2-DCE/dply_separate4D.py
  python Fig2-DCE/dply_rearrangeT1map.py
  ```
- Run pharmacokinetic modeling in MATLAB (`002_analysis_dcemr.m`), then compute tissue-specific $K^{trans}$ across GM, WMHs, and NAWM:
  ```bash
  python Fig2-DCE/calculate_ktrans_diffrentROI.py
  python Fig2-DCE/251120_permtest.py
  python Fig2-DCE/vis_ktrans.py
  ```

#### 3. White Matter Hyperintensity Volume Quantification (`Fig2-WMH/`)
- Segment WMH with DeepWMH and parcellate anatomical structures with FreeSurfer:
  ```bash
  bash Fig2-WMH/dply_deepwmh_wmhseg_250415.sh
  bash Fig2-WMH/dlpy_freesurfer_aparc2aseg.sh
  ```
- Compute volume shrinkage in deep vs periventricular WMH:
  ```bash
  jupyter notebook Fig2-WMH/analysis_wmh_volume_250907.ipynb
  ```

---

## ⚖️ Ethics & Clinical Trial Registration

- **Trial Registration**: Registered with the Chinese Clinical Trial Registry ([ChiCTR2400085374](https://www.chictr.org.cn/showproj.html?proj=233481)).
- **Ethics Approval**: Approved by the Institutional Review Board / Ethics Committee of Huashan Hospital, Fudan University (Approval No. **KY2024-594**).
- **Guidelines**: Compliant with the Declaration of Helsinki and CARE guidelines for clinical case reports. Written informed consent was obtained from the patient.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🤝 Acknowledgments

This work was supported by the **National Natural Science Foundation of China** (Grant Nos. 82272063, 82127801, and 82227806), the **Noncommunicable Chronic Diseases-National Science and Technology Major Project** (2023ZD0504903), and the **Medical Science Data Center in Shanghai Medical College of Fudan University**.
