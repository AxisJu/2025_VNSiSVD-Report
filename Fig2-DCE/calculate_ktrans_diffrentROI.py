import ants, numpy as np, nibabel as nib
import matplotlib.pyplot as plt

baseline_ktrans = nib.load("Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/004_rocketship_DCE/baseline/rt1_vibe_cor_dynamic_waterext_12_patlak_fit_Ktrans.nii").get_fdata()
followup_ktrans = nib.load("Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/004_rocketship_DCE/followup/rt1_vibe_cor_dynamic_waterext_11_patlak_fit_Ktrans.nii").get_fdata()

baseline_dce_mean_mask_brain = nib.load(r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/baseline/baseline_dce_mean_mask_brain.nii').get_fdata()
baseline_dce_mean_mask_brain = baseline_dce_mean_mask_brain > 0
baseline_dce_mean_mask_gm = nib.load(r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/baseline/c1meant1_vibe_cor_dynamic_waterext_12.nii').get_fdata()
baseline_dce_mean_mask_gm = baseline_dce_mean_mask_gm > 0
baseline_dce_mean_mask_wm = nib.load(r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/baseline/c2meant1_vibe_cor_dynamic_waterext_12.nii').get_fdata()
baseline_dce_mean_mask_wm = baseline_dce_mean_mask_wm > 0
baseline_dce_mean_mask_wmh = nib.load(r'Z:/2023 VNSiSVD/data/data_neuroimage_trial/bids/derivatives/DeepWMH/sub001_baseline_DCE/002_Segmentations/003_postproc_fov/sub001.nii.gz').get_fdata()
baseline_dce_mean_mask_wmh = baseline_dce_mean_mask_wmh > 0
baseline_dce_mean_mask_nawm = baseline_dce_mean_mask_wm & (~baseline_dce_mean_mask_wmh.astype(bool))

followup_dce_mean_mask_brain = nib.load(r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/followup/followup_dce_mean_mask_brain.nii').get_fdata()
followup_dce_mean_mask_brain = followup_dce_mean_mask_brain > 0
followup_dce_mean_mask_gm = nib.load(r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/followup/c1meant1_vibe_cor_dynamic_waterext_11.nii').get_fdata()
followup_dce_mean_mask_gm = followup_dce_mean_mask_gm > 0
followup_dce_mean_mask_wm = nib.load(r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/followup/c2meant1_vibe_cor_dynamic_waterext_11.nii').get_fdata()
followup_dce_mean_mask_wm = followup_dce_mean_mask_wm > 0
followup_dce_mean_mask_wmh = nib.load(r'Z:/2023 VNSiSVD/data/data_neuroimage_trial/bids/derivatives/DeepWMH/sub001_6m_DCE/002_Segmentations/003_postproc_fov/sub001.nii.gz').get_fdata()
followup_dce_mean_mask_wmh = followup_dce_mean_mask_wmh > 0
followup_dce_mean_mask_nawm = followup_dce_mean_mask_wm & (~followup_dce_mean_mask_wmh.astype(bool))

mean_wb       = np.nanmean(baseline_ktrans[baseline_dce_mean_mask_brain])
mean_gm       = np.nanmean(baseline_ktrans[baseline_dce_mean_mask_gm])
mean_wm       = np.nanmean(baseline_ktrans[baseline_dce_mean_mask_wm])
mean_wmh      = np.nanmean(baseline_ktrans[baseline_dce_mean_mask_wmh])
mean_nawm     = np.nanmean(baseline_ktrans[baseline_dce_mean_mask_nawm])

mean_wb       = np.nanmean(followup_ktrans[followup_dce_mean_mask_brain])
mean_gm       = np.nanmean(followup_ktrans[followup_dce_mean_mask_gm])
mean_wm       = np.nanmean(followup_ktrans[followup_dce_mean_mask_wm])
mean_wmh      = np.nanmean(followup_ktrans[followup_dce_mean_mask_wmh])
mean_nawm     = np.nanmean(followup_ktrans[followup_dce_mean_mask_nawm])
