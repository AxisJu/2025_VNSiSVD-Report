import os
import ants
import numpy as np

output_dir = r"Z:/2023 VNSiSVD/data/Imaging/001_YJZ/DCE-MRI/baseline/corrected_separated_dce"
os.makedirs(output_dir, exist_ok=True)

baseline = ants.image_read(r"Z:/2023 VNSiSVD/data/Imaging/001_YJZ/DCE-MRI/baseline/rt1_vibe_cor_dynamic_waterext_12.nii")
baseline = ants.ndimage_to_list(baseline)

for i, img3d in enumerate(baseline):
    output_path = os.path.join(output_dir, f'frame_{i+1:03d}.nii')
    ants.image_write(img3d, output_path)

ants.list_to_ndimage(image=baseline,image_list=baseline)

T1map = ants.image_read("Z:/2023 VNSiSVD/data/Imaging/001_YJZ/DCE-MRI/baseline/sub001_baseline_T1_map_t1_fa_fit_t1_vibe_cor_dyn_15_waterext_11.nii")
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
ants.image_write(T1map_R, r"Z:/2023 VNSiSVD/data/Imaging/001_YJZ/DCE-MRI/baseline/rT1map.nii")

from nilearn import plotting
data = nib.load(r"Z:/2023 VNSiSVD/data/Imaging/001_YJZ/DCE-MRI/baseline/rt1_vibe_cor_dynamic_waterext_12_patlak_fit_Ktrans.nii")
data.shape
plotting.plot_epi(data,display_mode="mosaic")
