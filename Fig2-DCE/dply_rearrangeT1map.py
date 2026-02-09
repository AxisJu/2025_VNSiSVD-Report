import os
import ants
import numpy as np
import nibabel as nib
from nilearn import plotting

# T1map = nib.load("Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/001_dcm2nii/baseline/t1_vibe_cor_dyn_2_waterext_7.nii")
# T1map.shape
# baseline_dce_mean = nib.load(r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/baseline/meant1_vibe_cor_dynamic_waterext_12.nii')
# baseline_dce_mean.shape
# baseline_dce_mean_mask_wb = nib.load(r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/baseline/baseline_dce_mean_mask_brain.nii')
# baseline_dce_mean_mask_wb.shape
# plotting.plot_roi(baseline_dce_mean_mask_wb, T1map, display_mode="mosaic", black_bg=True, colorbar=True, alpha=0.3)

# Baseline
T1map = ants.image_read("Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/003_rocketship_T1map/baseline/T1_map_t1_fa_fit_t1_vibe_cor_dyn_15_waterext_11.nii")
T1map.shape
arr = T1map.numpy()
arr_perm = np.transpose(arr, (0, 2, 1))
new_spacing = (T1map.spacing[0], 
               T1map.spacing[2],
               T1map.spacing[1])
T1map_R = ants.from_numpy(arr_perm,
                        spacing=new_spacing,
                        origin=T1map.origin,
                        direction=None)
T1map_R.shape
ants.image_write(T1map_R, "Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/003_rocketship_T1map/baseline/rearranged_T1_map_t1_fa_fit_t1_vibe_cor_dyn_15_waterext_11.nii")

# Followup
T1map = ants.image_read("Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/003_rocketship_T1map/followup/T1_map_t1_fa_fit_t1_vibe_cor_dyn_15_waterext_10.nii")
T1map.shape
arr = T1map.numpy()
arr_perm = np.transpose(arr, (0, 2, 1))
new_spacing = (T1map.spacing[0], 
               T1map.spacing[2],
               T1map.spacing[1])
T1map_R = ants.from_numpy(arr_perm,
                        spacing=new_spacing,
                        origin=T1map.origin,
                        direction=None)
T1map_R.shape
ants.image_write(T1map_R, "Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/003_rocketship_T1map/followup/rearranged_T1_map_t1_fa_fit_t1_vibe_cor_dyn_15_waterext_10.nii")
