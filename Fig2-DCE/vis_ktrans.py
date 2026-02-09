import ants, numpy as np, nibabel as nib
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl

baseline_ktrans = ants.image_read("Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/004_rocketship_DCE/baseline/rt1_vibe_cor_dynamic_waterext_12_patlak_fit_Ktrans.nii")
followup_ktrans = ants.image_read("Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/004_rocketship_DCE/followup/rt1_vibe_cor_dynamic_waterext_11_patlak_fit_Ktrans.nii")

baseline_dce_mean_mask_brain = ants.image_read(r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/baseline/baseline_dce_mean_mask_brain.nii')
followup_dce_mean_mask_brain = ants.image_read(r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/followup/followup_dce_mean_mask_brain.nii')

baseline_ktrans_data = baseline_ktrans.numpy().astype(np.float32)
baseline_ktrans_data[baseline_dce_mean_mask_brain.numpy() == 0] = 0
baseline_ktrans_data[baseline_ktrans_data>0.005] = 0.005
baseline_ktrans_masked = ants.from_numpy(baseline_ktrans_data,
                            origin=baseline_ktrans.origin,
                            spacing=baseline_ktrans.spacing,
                            direction=baseline_ktrans.direction)
ants.plot(baseline_ktrans_masked, axis=1, nslices=14, ncol=7, cmap='jet', black_bg=True, vmaxol=0.005, cbar=True)

followup_ktrans_data = followup_ktrans.numpy().astype(np.float32)
followup_ktrans_data[followup_dce_mean_mask_brain.numpy() == 0] = 0
followup_ktrans_data[followup_ktrans_data>0.005] = 0.005
followup_ktrans_masked = ants.from_numpy(followup_ktrans_data,
                            origin=followup_ktrans.origin,
                            spacing=followup_ktrans.spacing,
                            direction=followup_ktrans.direction)
ants.plot(followup_ktrans_masked, axis=1, nslices=14, ncol=7, cmap='jet', black_bg=True, vmaxol=0.005, cbar=True)


### registration followup to baseline
trans = ants.registration(
    fixed=baseline_ktrans_masked,
    moving=followup_ktrans_masked, 
    type_of_transform='SyN',
    verbose=True
)
followup_ktrans_masked_reged = trans['warpedmovout']

ants.plot(baseline_ktrans_masked, axis=1, nslices=14, ncol=7, cmap='jet', black_bg=True, vmaxol=0.005, cbar=True)
ants.plot(followup_ktrans_masked, axis=1, nslices=14, ncol=7, cmap='jet', black_bg=True, vmaxol=0.005, cbar=True)
ants.plot(followup_ktrans_masked_reged, axis=1, nslices=14, ncol=7, cmap='jet', black_bg=True, vmaxol=0.005, cbar=True)

diff = followup_ktrans_masked_reged - baseline_ktrans_masked
ants.plot(diff, axis=1, nslices=14, ncol=7, cmap='jet', black_bg=True, vmaxol=0.005, cbar=True)



### Final Plotting
cols, rows = 6, 2
fig, axes = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2))
slice_list = [2,4,6,8,10,11]
for i in range(cols):
    # ---------- Baseline ----------
    slice_idx = slice_list[i]
    sl = baseline_ktrans_masked.numpy()[:, :, slice_idx]
    #sl_masked = np.ma.masked_where(sl == 0, sl)
    axes[0, i].imshow(np.rot90(sl, k=-1), cmap='jet', origin='lower')
    axes[0, i].axis('off')
slice_list = [2,4,6,8,10,11]
for i in range(cols):
    # ---------- Follow-up ----------
    slice_idx = slice_list[i]
    sl = followup_ktrans_masked_reged.numpy()[:, :, slice_idx]
    #sl_masked = np.ma.masked_where(sl == 0, sl)
    axes[1, i].imshow(np.rot90(sl, k=-1), cmap='jet', origin='lower')
    axes[1, i].axis('off')
# slice_list = [2,4,6,8,10,12]
# for i in range(cols):
#     # ---------- Diff ----------
#     slice_idx = slice_list[i]
#     sl = diff.numpy()[:, :, slice_idx]
#     #sl_masked = np.ma.masked_where(sl == 0, sl)
#     axes[2, i].imshow(np.rot90(sl, k=-1), cmap='jet', origin='lower')
#     axes[2, i].axis('off')

norm = mpl.colors.Normalize(vmin=0, vmax=0.005)
sm = plt.cm.ScalarMappable(cmap='jet', norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=axes.ravel().tolist(), fraction=0.015, pad=0.01)
cbar.set_label('Ktrans (1/min)', rotation=270, labelpad=10)

plt.tight_layout()
plt.show()
