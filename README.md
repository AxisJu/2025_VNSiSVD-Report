# 2025_VNSiSVD-Report

Analysis pipelines and statistical code for paired vagus nerve stimulation with cognitive training (VNS-CT) in cerebral small vessel disease.

## Repository Architecture

```text
2025_VNSiSVD-Report/
├── Fig1-DTI/                                    # Diffusion tensor imaging and differential tractography
│   ├── dply_dcm2bids_dxi_250325.sh              # DICOM to BIDS conversion for diffusion MRI
│   ├── dply_qsiprep_dxi_250325.sh               # QSIPrep preprocessing pipeline
│   ├── dply_qsirecon_dxi_250407.sh              # QSIRecon with DSI Studio reconstruction
│   ├── dply_extract-dsistudio_250501.py         # Tract-level metric extraction (FA, MD, RD)
│   └── stat_dxi_250410.r                        # Statistical analysis and difference tables
├── Fig1-rsfMRI/                                 # Resting-state fMRI analysis
│   ├── ALFF.py                                  # Amplitude of low-frequency fluctuation computation
│   ├── eigenstrapping_test.py                   # Spatial autocorrelation null model testing
│   ├── neuromap.py                              # Cortical gradient projection
│   ├── neurosynth.py                            # Meta-analytic cognitive decoding
│   └── rscvr.py                                 # Resting-state CVR estimation
├── Fig2-CVR/                                    # Cerebrovascular reactivity (rs-CVR)
│   ├── dply_dcm2bids_cvr_250414.sh              # BIDS curation for BOLD CVR sequences
│   ├── dply_deepprep_cvr_250414.sh              # DeepPrep functional MRI preprocessing
│   └── analysis_rsCVRmap_251121.py              # rs-CVR mapping and regional permutation testing
├── Fig2-DCE/                                    # Dynamic contrast-enhanced MRI (BBB permeability)
│   ├── 001_dcm2nii.sh                           # DICOM to NIfTI conversion
│   ├── 002_analysis_dcemr.m                     # DCE pharmacokinetic modeling (Tofts model Ktrans)
│   ├── 003_brainmask.ipynb                      # Brain mask extraction
│   ├── dply_separate4D.py                       # 4D DCE dynamic series splitting
│   ├── dply_rearrangeT1map.py                   # Variable flip angle T1 alignment
│   ├── dply_ants_regMeanDCE.ipynb               # ANTs coregistration
│   ├── calculate_ktrans_diffrentROI.py          # ROI-wise Ktrans extraction (GM, WMH, NAWM)
│   ├── 251120_permtest.py                       # Permutation test for regional delta Ktrans
│   └── vis_ktrans.py                            # Ktrans map visualization
├── Fig2-WMH/                                    # White matter hyperintensity volumetry
│   ├── dply_deepwmh_wmhseg_250415.sh            # DeepWMH segmentation
│   ├── dlpy_freesurfer_aparc2aseg.sh            # FreeSurfer anatomical parcellation
│   ├── dply_ants_regFLAIR_250415.ipynb          # FLAIR-to-T1w registration via ANTs
│   ├── dply_ants_regFLAIR_strtnewmethods_*.ipynb# Longitudinal registration
│   ├── analysis_wmh_volume_250907.ipynb         # Lesion volume calculation (Deep vs Periventricular)
│   └── analysis_wmh_visualization.ipynb         # 3D lesion rendering
├── environment.yml                              # Conda environment configuration
├── requirements.txt                             # Python package list
├── .gitignore
└── LICENSE
```

## Prerequisites

### Software Tools
- Python >= 3.10
- R >= 4.2.0
- MATLAB (R2022b or later, for DCE Tofts modeling)
- External neuroimaging packages: QSIPrep, DSI Studio, DeepPrep / fMRIPrep, ANTs, FreeSurfer

### Python Environment
Install dependencies via Conda or pip:

```bash
conda env create -f environment.yml
conda activate vns_isvd
```

or:

```bash
pip install -r requirements.txt
```

### R Dependencies
```R
install.packages(c("tidyverse", "openxlsx", "ggplot2"))
```

## Publication

Sihan Ju, Liyi Qian, Yunqing Ying, Siheng Feng, Yutong Zhao, Yunfeng Zhang, Yulian Zhu, Xin Cheng, Qi Yue, and Liang Chen. "Paired vagus nerve stimulation for neurovascular modulation in vascular cognitive impairment: a first-in-human study." *Brain Stimulation* (2026): 103212. https://doi.org/10.1016/j.brs.2026.103212

Clinical trial registration: ChiCTR2400085374 (Chinese Clinical Trial Registry).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
