import nibabel as nib
import numpy as np
from dipy.io import save_nifti

dwi_img = nib.load('Z:/2023 VNSiSVD/data/data_neuroimage_trial/bids/sub-001/ses-baseline/dwi/sub-001_ses-baseline_acq-dxi_dwi.nii.gz')
dwi_data = dwi_img.get_fdata()
affine = dwi_img.affine

bvals = np.loadtxt('Z:/2023 VNSiSVD/data/data_neuroimage_trial/bids/sub-001/ses-baseline/dwi/sub-001_ses-baseline_acq-dxi_dwi.bval')
bvecs = np.loadtxt('Z:/2023 VNSiSVD/data/data_neuroimage_trial/bids/sub-001/ses-baseline/dwi/sub-001_ses-baseline_acq-dxi_dwi.bvec')

b0_idx = np.where(bvals < 50)[0][0].ravel()
target_b = 1000
tolerance = 100
b_dti_idx = np.where((bvals > target_b - tolerance) & (bvals < target_b + tolerance))[0][0].ravel()
selected_idx = np.concatenate([b0_idx, b_dti_idx])
selected_idx.sort()

dwi_selected = dwi_data[..., selected_idx]
bvals_selected = bvals[selected_idx]
bvecs_selected = bvecs[:, selected_idx]

prefix = 'Z:/2023 VNSiSVD/data/'

nib.save(nib.Nifti1Image(dwi_selected, affine), f'{prefix}sub-001_ses-baseline_DTI.nii.gz')
np.savetxt(f'{prefix}sub-001_ses-baseline_DTI.bval', bvals_selected, fmt='%.1f')
np.savetxt(f'{prefix}sub-001_ses-baseline_DTI.bvec', bvecs_selected, fmt='%.6f')
