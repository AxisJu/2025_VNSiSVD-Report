import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_1samp
from nilearn import image
from nilearn.datasets import (
    load_mni152_brain_mask,
    load_mni152_gm_mask,
    load_mni152_wm_mask
)

import matplotlib as mpl

mpl.rcParams['pdf.fonttype'] = 42 
mpl.rcParams['ps.fonttype']  = 42
mpl.rcParams['font.family'] = 'Arial'  
mpl.rcParams['axes.unicode_minus'] = False  


# ============================================================
# 1. Load CVR data (baseline and 6m follow-up)
# ============================================================

paths = {
    "baseline": r"Z:\2023 VNSiSVD\results\20251031 CVR\MNI_rsCVR\sub-001_task-baseline_space-MNI152NLin2009cAsym_desc-preproc_bold.nii_rscvr.nii.gz",
    "6m":       r"Z:\2023 VNSiSVD\results\20251031 CVR\MNI_rsCVR\sub-001_task-6m_space-MNI152NLin2009cAsym_desc-preproc_bold.nii_rscvr.nii.gz",
    "pre": r"Z:\2023 VNSiSVD\results\20251031 CVR\MNI_rsCVR\sub-001_task-PreVNS_space-MNI152NLin2009cAsym_desc-preproc_bold.nii_rscvr.nii.gz",
    "in": r"Z:\2023 VNSiSVD\results\20251031 CVR\MNI_rsCVR\sub-001_task-InVNS_space-MNI152NLin2009cAsym_desc-preproc_bold.nii_rscvr.nii.gz",
    "post": r"Z:\2023 VNSiSVD\results\20251031 CVR\MNI_rsCVR\sub-001_task-PostVNS_space-MNI152NLin2009cAsym_desc-preproc_bold.nii_rscvr.nii.gz"
}

imgs = {k: nib.load(v) for k, v in paths.items()}
data = {k: imgs[k].get_fdata() for k in imgs}

# Compute difference map: Follow-up – Baseline
diff_followup_baseline = data["6m"] - data["baseline"]

# ============================================================
# 2. Load and resample MNI standard masks
# ============================================================

from nilearn.datasets import (
    load_mni152_brain_mask,
    load_mni152_gm_mask,
    load_mni152_wm_mask
)

ref_img = imgs['baseline']  # RSFA image = MNI152NLin6Asym_res-02

# 1) Whole brain (true MNI anatomical mask)
mni_wholebrain_mask = load_mni152_brain_mask(resolution=2,threshold=0.2)
mni_wholebrain_mask = image.resample_to_img(mni_wholebrain_mask, ref_img, interpolation="nearest")

# 2) GM mask
mni_gm_mask = load_mni152_gm_mask(resolution=2,threshold=0.7)
mni_gm_mask = image.resample_to_img(mni_gm_mask, ref_img, interpolation="nearest")

# 3) WM mask
mni_wm_mask = load_mni152_wm_mask(resolution=2,threshold=0.2)
mni_wm_mask = image.resample_to_img(mni_wm_mask, ref_img, interpolation="nearest")

# 4) WMH mask (must come from antsApplyTransforms!)
wmh_mni_baseline = image.load_img(r"Z:\2023 VNSiSVD\results\20251031 CVR\baseline_WMH_in_MNI.nii.gz")  # AFTER warp to MNI
wmh_mni_baseline = image.resample_to_img(wmh_mni_baseline, ref_img, interpolation="nearest")
wmh_mni_followup = image.load_img(r"Z:\2023 VNSiSVD\results\20251031 CVR\6m_WMH_in_MNI.nii.gz")  # AFTER warp to MNI
wmh_mni_followup = image.resample_to_img(wmh_mni_followup, ref_img, interpolation="nearest")

# 5) NAWM
nawm_mni_baseline = image.math_img("(wm > 0) * (wmh == 0)", wm=mni_wm_mask, wmh=wmh_mni_baseline)
nawm_mni_followup = image.math_img("(wm > 0) * (wmh == 0)", wm=mni_wm_mask, wmh=wmh_mni_followup)

# Baseline ROI masks
roi_masks_baseline = {
    "WholeBrain": mni_wholebrain_mask,
    "GM": mni_gm_mask,
    "NAWM": nawm_mni_baseline,
    "WMH": wmh_mni_baseline
}

# Follow-up ROI masks
roi_masks_followup = {
    "WholeBrain": mni_wholebrain_mask,
    "GM": mni_gm_mask,
    "NAWM": nawm_mni_followup,
    "WMH": wmh_mni_followup
}

# ============================================================
# visualization of mask
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from nilearn import image
from scipy.ndimage import gaussian_filter


def plot_axial_with_contours(
    img,             # Nifti image to show (e.g., diff map or rsfa)
    gm_mask,
    wmh_mask,
    nawm_mask,
    slice_z=80,
    smooth_fwhm=0,
    title="Axial Slice with GM / WMH / NAWM Contours"
):
    """
    Plot an axial slice with GM, WMH, and NAWM contours.
    
    Parameters:
        img: Nifti1Image (the CVR or RSFA map)
        gm_mask, wmh_mask, nawm_mask: Nifti1Image (aligned masks in MNI)
        slice_z: int, slice index
        smooth_fwhm: float, smoothing FWHM in mm (0 = no smoothing)
        title: figure title
    """

    # --- Extract image data ---
    data = img.get_fdata()

    # --- Optional smoothing ---
    if smooth_fwhm > 0:
        sigma = smooth_fwhm / 2.355      # Convert FWHM → sigma for Gaussian
        data = gaussian_filter(data, sigma=sigma)

    slice_img = np.rot90(data[:, :, slice_z])

    # --- Extract masks ---
    gm = np.rot90(gm_mask.get_fdata()[:, :, slice_z] > 0)
    wmh = np.rot90(wmh_mask.get_fdata()[:, :, slice_z] > 0)
    nawm = np.rot90(nawm_mask.get_fdata()[:, :, slice_z] > 0)

    # --- Plot base image ---
    plt.figure(figsize=(8, 8))
    plt.imshow(slice_img, cmap="gray")
    
    # --- contour overlays ---
    # GM in green
    plt.contour(gm, levels=[0.5], colors="lime", linewidths=1.5, label="GM")

    # NAWM in blue
    plt.contour(nawm, levels=[0.5], colors="cyan", linewidths=1.5, label="NAWM")

    # WMH in red
    plt.contour(wmh, levels=[0.5], colors="red", linewidths=2.0, label="WMH")

    plt.title(f"{title}\nSlice z = {slice_z},  Smooth = {smooth_fwhm} mm")
    plt.axis("off")
    plt.show()


import nibabel as nib
diff_img = nib.Nifti1Image(diff_followup_baseline, imgs["baseline"].affine)

plot_axial_with_contours(
    img=diff_img,
    gm_mask=mni_gm_mask,
    wmh_mask=wmh_mni_baseline,
    nawm_mask=nawm_mni_baseline,
    slice_z=60,
    smooth_fwhm=3,
    title="CVR Diff with Mask Contours"
)

# ============================================================
# baseline CVR distribution
# ============================================================

baseline_data = data["baseline"]

def extract_roi_values(diff_data, mask_img):
    """
    Return voxel values inside ROI mask.
    """
    mask = mask_img.get_fdata() > 0
    vals = diff_data[mask]
    return vals[np.isfinite(vals)]

baseline_roi_values = {
    name: extract_roi_values(baseline_data, mask)
    for name, mask in roi_masks_baseline.items()
}

# ---- Plot ----
plt.figure(figsize=(8, 6))
roi_names = list(baseline_roi_values.keys())
plt.boxplot([baseline_roi_values[n] for n in roi_names],
            labels=roi_names, showfliers=False)
plt.ylabel("Baseline CVR value")
plt.title("Baseline CVR Distribution in ROIs")

# mean markers
for i, name in enumerate(roi_names, start=1):
    plt.scatter(i, np.mean(baseline_roi_values[name]),
                color="red", zorder=3)
plt.tight_layout()
plt.show()

# ---- Stats ----
print("\n========== Baseline CVR ROI Statistics ==========")
for name in roi_names:
    vals = baseline_roi_values[name]
    print(f"{name:10s} mean={np.mean(vals): .4f}, SD={np.std(vals,ddof=1): .4f}, n={len(vals)}")


# ============================================================
# followup CVR distribution
# ============================================================

followup_data = data["6m"]

followup_roi_values = {
    name: extract_roi_values(followup_data, mask)
    for name, mask in roi_masks_followup.items()
}

# ---- Plot ----
plt.figure(figsize=(8, 6))
roi_names = list(followup_roi_values.keys())
plt.boxplot([followup_roi_values[n] for n in roi_names],
            labels=roi_names, showfliers=False)
plt.ylabel("Follow-up CVR value")
plt.title("Follow-up CVR Distribution in ROIs")

# mean markers
for i, name in enumerate(roi_names, start=1):
    plt.scatter(i, np.mean(followup_roi_values[name]),
                color="red", zorder=3)
plt.tight_layout()
plt.show()

# ---- Stats ----
print("\n========== Follow-up CVR ROI Statistics ==========")
for name in roi_names:
    vals = followup_roi_values[name]
    print(f"{name:10s} mean={np.mean(vals): .4f}, SD={np.std(vals,ddof=1): .4f}, n={len(vals)}")

# ============================================================
# DiffMap: multi-slice visualization (6 slices)
# ============================================================

def plot_diffmap_multi_slices(
    diff_img,
    slices=[40, 50, 60, 70, 80, 90],
    smooth_fwhm=3,
    cmap="jet",
    vmin=None,
    vmax=None,
    figsize=(14, 8),
    title="CVR DiffMap (6m - Baseline)"
):
    """
    Plot 6 axial slices of the DiffMap.

    Parameters:
        diff_img  : Nifti1Image
        slices    : list of slice indices
        smooth_fwhm : Gaussian smoothing FWHM (mm)
        cmap        : colormap
        vmin, vmax  : intensity range (default uses percentiles 2/98)
        figsize     : figure size
    """

    data = diff_img.get_fdata()

    # Optional smoothing
    if smooth_fwhm > 0:
        sigma = smooth_fwhm / 2.355
        data = gaussian_filter(data, sigma)

    # Auto intensity range if not provided
    if vmin is None or vmax is None:
        vmin = np.percentile(data, 2)
        vmax = np.percentile(data, 98)

    fig, axes = plt.subplots(1, 6, figsize=figsize)
    axes = axes.flatten()

    for ax, z in zip(axes, slices):
        slice_img = np.rot90(data[:, :, z])
        ax.imshow(slice_img, cmap=cmap, vmin=vmin, vmax=vmax)
        ax.set_title(f"Slice z = {z}", fontsize=12)
        ax.axis("off")

    plt.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


# ---- Call the function ----
plot_diffmap_multi_slices(
    diff_img=diff_img,
    slices=[10, 20, 30, 40, 50, 60],
    smooth_fwhm=3,
    cmap="jet",
    title="CVR DiffMap (6 slices)"
)

# ============================================================
# Baseline & Follow-up CVR map: 2×6 slices
# ============================================================

def plot_baseline_followup_slices(
    baseline_img,
    followup_img,
    slices=[10, 20, 30, 40, 50, 60],
    smooth_fwhm=0,
    cmap="jet",
    figsize=(18, 6),
    title="Baseline and Follow-up CVR Maps"
):
    """
    Plot 6 slices for baseline and 6 slices for follow-up CVR maps.
    Displayed in a 2×6 grid.
    
    Parameters:
        baseline_img : Nifti1Image
        followup_img : Nifti1Image
        slices       : list, slice indices to show
        smooth_fwhm  : smoothing FWHM (mm)
        cmap         : colormap
    """

    # --- Load data ---
    base = baseline_img.get_fdata()
    foll = followup_img.get_fdata()

    # --- Optional smoothing ---
    if smooth_fwhm > 0:
        sigma = smooth_fwhm / 2.355
        base = gaussian_filter(base, sigma)
        foll = gaussian_filter(foll, sigma)

    # --- Auto intensity window (same for both maps) ---
    all_vals = np.concatenate([base.flatten(), foll.flatten()])
    vmin = np.percentile(all_vals, 2)
    vmax = np.percentile(all_vals, 98)

    fig, axes = plt.subplots(2, 6, figsize=figsize)
    
    # ---- Plot baseline (top row) ----
    for i, z in enumerate(slices):
        slice_img = np.rot90(base[:, :, z])
        axes[0, i].imshow(slice_img, cmap=cmap, vmin=vmin, vmax=vmax)
        axes[0, i].set_title(f"Baseline z={z}", fontsize=11)
        axes[0, i].axis("off")

    # ---- Plot follow-up (bottom row) ----
    for i, z in enumerate(slices):
        slice_img = np.rot90(foll[:, :, z])
        axes[1, i].imshow(slice_img, cmap=cmap, vmin=vmin, vmax=vmax)
        axes[1, i].set_title(f"Follow-up z={z}", fontsize=11)
        axes[1, i].axis("off")

    plt.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


# ---- Run the function ----
plot_baseline_followup_slices(
    baseline_img=imgs["pre"],
    followup_img=imgs["in"],
    slices=list(range(31, 37)),  # Generate slices from 95 to 100 (inclusive)
    smooth_fwhm=3,
    cmap="jet",
    title="Baseline vs Follow-up CVR: 6 Slices Each (2×6)"
)

# ============================================================
# Baseline & Follow-up CVR map in White Matter only (2×6 slices)
# ============================================================

def plot_baseline_followup_WM_only(
    baseline_img,
    followup_img,
    wm_mask_img,
    slices=[40, 50, 60, 70, 80, 90],
    smooth_fwhm=3,
    cmap="jet",
    figsize=(18, 6),
    title="Baseline and Follow-up CVR (White Matter Only)"
):
    """
    Display 6 slices of baseline & follow-up CVR,
    masked by white matter only.
    """
    # ---- Load source data ----
    base = baseline_img.get_fdata()
    foll = followup_img.get_fdata()
    wm   = wm_mask_img.get_fdata() > 0

    # ---- Smoothing FIRST (avoid NaN diffusion) ----
    if smooth_fwhm > 0:
        sigma = smooth_fwhm / 2.355
        base = gaussian_filter(base, sigma)
        foll = gaussian_filter(foll, sigma)

    # ---- Apply WM mask AFTER smoothing (important!) ----
    base = np.where(wm, base, np.nan)
    foll = np.where(wm, foll, np.nan)

    # ---- Compute intensity range from WM only ----
    all_vals = np.concatenate([
        base[np.isfinite(base)],
        foll[np.isfinite(foll)]
    ])
    vmin = np.percentile(all_vals, 2)
    vmax = np.percentile(all_vals, 98)

    # ---- Plot (2×6) ----
    fig, axes = plt.subplots(2, 7, figsize=figsize)

    # ---- Baseline row ----
    for i, z in enumerate(slices):
        img_slice = np.rot90(base[:, :, z])
        im = axes[0, i].imshow(img_slice, cmap=cmap, vmin=vmin, vmax=vmax)
        axes[0, i].set_title(f"Baseline WM z={z}", fontsize=11)
        axes[0, i].axis("off")

    # ---- Follow-up row ----
    for i, z in enumerate(slices):
        img_slice = np.rot90(foll[:, :, z])
        axes[1, i].imshow(img_slice, cmap=cmap, vmin=vmin, vmax=vmax)
        axes[1, i].set_title(f"Follow-up WM z={z}", fontsize=11)
        axes[1, i].axis("off")

    # ---- Add colorbar legend ----
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(),
                        fraction=0.015, pad=0.02)
    cbar.set_label("CVR value", fontsize=12)

    plt.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# ============================================================
# Run WM-only visualization
# ============================================================

plot_baseline_followup_WM_only(
    baseline_img=imgs["baseline"],
    followup_img=imgs["6m"],
    wm_mask_img=mni_wm_mask,         # 使用你已经 resample 过的 MNI WM mask
    slices=[35,40,45,50,55,60,65],
    smooth_fwhm=8,
    cmap="coolwarm",
    title="CVR Maps in White Matter Only (Baseline vs Follow-up)"
)


# ============================================================
# Run WholeBrain-only visualization
# ============================================================
def plot_baseline_followup_wholebrain(
    baseline_img,
    followup_img,
    whole_mask_img,
    slices=[40, 50, 60, 70, 80, 90],
    smooth_fwhm=3,
    cmap="jet",
    figsize=(18, 6),
    title="Baseline and Follow-up CVR (Whole Brain Masked)"
):
    """
    Display baseline & follow-up CVR for whole brain,
    using a user-provided whole-brain mask.
    """
    # ---- Load data ----
    base = baseline_img.get_fdata()
    foll = followup_img.get_fdata()
    mask = whole_mask_img.get_fdata() > 0

    # ---- Smoothing ----
    if smooth_fwhm > 0:
        sigma = smooth_fwhm / 2.355
        base = gaussian_filter(base, sigma)
        foll = gaussian_filter(foll, sigma)

    # ---- Apply whole-brain mask AFTER smoothing ----
    base = np.where(mask, base, np.nan)
    foll = np.where(mask, foll, np.nan)

    # ---- Compute intensity range (masked only) ----
    all_vals = np.concatenate([
        base[np.isfinite(base)],
        foll[np.isfinite(foll)]
    ])
    vmin = np.percentile(all_vals, 2)
    vmax = np.percentile(all_vals, 98)

    # ---- Plot ----
    fig, axes = plt.subplots(2, 7, figsize=figsize)

    # ---- Baseline row ----
    for i, z in enumerate(slices):
        img_slice = np.rot90(base[:, :, z])
        im = axes[0, i].imshow(img_slice, cmap=cmap, vmin=vmin, vmax=vmax)
        axes[0, i].set_title(f"Baseline z={z}", fontsize=11)
        axes[0, i].axis("off")

    # ---- Follow-up row ----
    for i, z in enumerate(slices):
        img_slice = np.rot90(foll[:, :, z])
        axes[1, i].imshow(img_slice, cmap=cmap, vmin=vmin, vmax=vmax)
        axes[1, i].set_title(f"Follow-up z={z}", fontsize=11)
        axes[1, i].axis("off")

    # ---- Colorbar ----
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(),
                        fraction=0.015, pad=0.02)
    cbar.set_label("CVR value", fontsize=12)

    plt.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

plot_baseline_followup_wholebrain(
    baseline_img=imgs["baseline"],
    followup_img=imgs["6m"],
    whole_mask_img=mni_wholebrain_mask,   # 你自己的 whole brain mask
    slices=[35,40,45,50,55,60,65],
    smooth_fwhm=8,
    cmap="coolwarm",
    title="CVR Maps (Whole Brain, Mask Applied)"
)


def plot_pre_in_post_wholebrain(
    pre_img,
    in_img,
    post_img,
    whole_mask_img,
    slices=[40, 50, 60, 70, 80, 90],
    smooth_fwhm=3,
    cmap="jet",
    figsize=(18, 9),
    title="CVR Maps (Pre / In / Post, Whole Brain Mask)"
):
    """
    Plot 3-level CVR maps: Pre, In, Post using whole-brain mask.
    """
    # ---- Load data ----
    pre  = pre_img.get_fdata()
    in_  = in_img.get_fdata()
    post = post_img.get_fdata()
    mask = whole_mask_img.get_fdata() > 0

    # ---- Smoothing ----
    if smooth_fwhm > 0:
        sigma = smooth_fwhm / 2.355
        pre  = gaussian_filter(pre,  sigma)
        in_  = gaussian_filter(in_,  sigma)
        post = gaussian_filter(post, sigma)

    # ---- Apply mask ----
    pre  = np.where(mask, pre,  np.nan)
    in_  = np.where(mask, in_,  np.nan)
    post = np.where(mask, post, np.nan)

    # ---- Intensity range ----
    all_vals = np.concatenate([
        pre[np.isfinite(pre)],
        in_[np.isfinite(in_)],
        post[np.isfinite(post)]
    ])
    vmin = np.percentile(all_vals, 2)
    vmax = np.percentile(all_vals, 98)

    # ---- Plot 3×N ----
    fig, axes = plt.subplots(3, len(slices), figsize=figsize)

    # ---- Pre row ----
    for i, z in enumerate(slices):
        img_slice = np.rot90(pre[:, :, z])
        im = axes[0, i].imshow(img_slice, cmap=cmap, vmin=vmin, vmax=vmax)
        axes[0, i].set_title(f"Pre z={z}", fontsize=11)
        axes[0, i].axis("off")

    # ---- In row ----
    for i, z in enumerate(slices):
        img_slice = np.rot90(in_[:, :, z])
        axes[1, i].imshow(img_slice, cmap=cmap, vmin=vmin, vmax=vmax)
        axes[1, i].set_title(f"In z={z}", fontsize=11)
        axes[1, i].axis("off")

    # ---- Post row ----
    for i, z in enumerate(slices):
        img_slice = np.rot90(post[:, :, z])
        axes[2, i].imshow(img_slice, cmap=cmap, vmin=vmin, vmax=vmax)
        axes[2, i].set_title(f"Post z={z}", fontsize=11)
        axes[2, i].axis("off")

    # ---- Colorbar ----
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(),
                        fraction=0.015, pad=0.03)
    cbar.set_label("CVR value", fontsize=12)

    plt.suptitle(title, fontsize=18)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
plot_pre_in_post_wholebrain(
    pre_img=imgs["pre"],
    in_img=imgs["in"],
    post_img=imgs["post"],
    whole_mask_img=mni_wholebrain_mask,
    slices=[35,40,45,50,55,60,65],
    smooth_fwhm=5,
    cmap="coolwarm",
    title="CVR (Pre / In / Post, Whole Brain)"
)


# ============================================================
# ROI voxel extraction for CVR baseline & follow-up
# ============================================================

baseline_cvr = data["baseline"]
followup_cvr = data["6m"]

# Baseline ROI masks
baseline_gm_mask   = mni_gm_mask.get_fdata() > 0
baseline_wm_mask   = mni_wm_mask.get_fdata() > 0
baseline_nawm_mask = nawm_mni_baseline.get_fdata() > 0
baseline_wmh_mask  = wmh_mni_baseline.get_fdata()  > 0

# Follow-up ROI masks
followup_gm_mask   = mni_gm_mask.get_fdata()       > 0
followup_wm_mask = mni_wm_mask.get_fdata() > 0
followup_nawm_mask = nawm_mni_followup.get_fdata() > 0
followup_wmh_mask  = wmh_mni_followup.get_fdata()  > 0

# Extract values
baseline_vals = {
    "GM":   baseline_cvr[baseline_gm_mask],
    "WM": baseline_cvr[baseline_wm_mask],
    "NAWM": baseline_cvr[baseline_nawm_mask],
    "WMH":  baseline_cvr[baseline_wmh_mask],
}

followup_vals = {
    "GM":   followup_cvr[followup_gm_mask],
    "WM": followup_cvr[followup_wm_mask],
    "NAWM": followup_cvr[followup_nawm_mask],
    "WMH":  followup_cvr[followup_wmh_mask],
}

# ============================================================
# Permutation test
# ============================================================

def perm_test_roi(baseline_vals, followup_vals, B=5000, two_sided=True):

    baseline_vals = baseline_vals[np.isfinite(baseline_vals)]
    followup_vals = followup_vals[np.isfinite(followup_vals)]

    n1, n2 = len(baseline_vals), len(followup_vals)
    if n1 == 0 or n2 == 0:
        return np.nan, np.nan, None

    obs_diff = np.mean(followup_vals) - np.mean(baseline_vals)

    pooled = np.concatenate([baseline_vals, followup_vals])
    null_dist = np.zeros(B)

    for b in range(B):
        perm = np.random.permutation(pooled)
        grp1 = perm[:n1]
        grp2 = perm[n1:]
        null_dist[b] = np.mean(grp2) - np.mean(grp1)

    if two_sided:
        p = (1 + np.sum(np.abs(null_dist) >= np.abs(obs_diff))) / (B + 1)
    else:
        p = (1 + np.sum(null_dist >= obs_diff)) / (B + 1)

    return obs_diff, p, null_dist

# ============================================================
# Run permutation tests for GM / NAWM / WMH CVR
# ============================================================

roi_names = ["GM", "WM"]
B = 10000

cvr_results = {}

for roi in roi_names:
    diff, pval, null = perm_test_roi(baseline_vals[roi], followup_vals[roi], B)
    cvr_results[roi] = {
        "diff": diff,
        "pval": pval,
        "null": null,
        "baseline": baseline_vals[roi],
        "followup": followup_vals[roi]
    }

print("\nObserved CVR difference (follow-up − baseline):")
for roi in roi_names:
    print(f"{roi:5s} {cvr_results[roi]['diff']:.6f}")

print("\nPermutation test p-values:")
for roi in roi_names:
    print(f"{roi:5s} p = {cvr_results[roi]['pval']:.6f}")

# ============================================================
# Visualization: Null distributions of permutation tests
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(16, 5))
fig.suptitle("Permutation Test of CVR Change (Follow-up − Baseline)", fontsize=16)

for idx, roi in enumerate(roi_names):

    diff = cvr_results[roi]["diff"]
    pval = cvr_results[roi]["pval"]
    null = cvr_results[roi]["null"]

    baseline_vals_roi = cvr_results[roi]["baseline"]
    followup_vals_roi = cvr_results[roi]["followup"]

    ax = axes[idx]

    # null distribution
    ax.hist(null, bins=50, alpha=0.7, color="#CCCCCC", edgecolor="black")

    # observed diff
    ax.axvline(diff, color="red" if pval < 0.05 else "blue",
               linestyle="--", linewidth=3)

    # critical region lines
    lower = np.percentile(null, 2.5)
    upper = np.percentile(null, 97.5)
    ax.axvline(lower, color="red", linestyle=":", linewidth=1)
    ax.axvline(upper, color="red", linestyle=":", linewidth=1)

    ax.set_title(f"{roi}\np={pval:.4f}", fontsize=12)
    ax.set_xlabel("Mean CVR Difference")
    ax.set_ylabel("Frequency")

plt.tight_layout()
plt.show()

# ============================================================
# Bar plot: null mean ± 95% CI + observed diff
# ============================================================

null_means = [np.mean(cvr_results[roi]["null"]) for roi in roi_names]
null_lower = [np.percentile(cvr_results[roi]["null"], 2.5) for roi in roi_names]
null_upper = [np.percentile(cvr_results[roi]["null"], 97.5) for roi in roi_names]
obs_diffs  = [cvr_results[roi]["diff"] for roi in roi_names]
colors     = ["#E31A1C" if cvr_results[roi]["pval"] < 0.05 else "#1F78B4"
              for roi in roi_names]

error_bars = [[null_means[i] - null_lower[i], null_upper[i] - null_means[i]]
              for i in range(2)]

fig, ax = plt.subplots(figsize=(8, 6))

x = np.arange(2)

ax.bar(x, null_means, yerr=np.array(error_bars).T, capsize=8,
       color="#CCCCCC", edgecolor="black", linewidth=1.0,
       label="Null Mean ± 95% CI")

for i in range(2):
    ax.scatter(i, obs_diffs[i], color=colors[i], s=120, zorder=5)

ax.axhline(0, linestyle="--", color="black", linewidth=1)
ax.set_xticks(x)
ax.set_xticklabels(roi_names, fontsize=12)
ax.set_ylabel("Mean CVR Difference (Follow-up − Baseline)", fontsize=12)
ax.set_title("Observed CVR Change vs Null Distribution", fontsize=15)
ax.grid(axis="y", alpha=0.3)
ax.legend()

plt.tight_layout()
plt.show()

# ============================================================
# Cohen's d function (independent groups)
# ============================================================

def cohens_d_independent(baseline_vals, followup_vals):
    """
    Independent groups Cohen’s d:
        d = (mean2 - mean1) / pooled_std
    """

    baseline_vals = baseline_vals[np.isfinite(baseline_vals)]
    followup_vals = followup_vals[np.isfinite(followup_vals)]

    mean1 = np.mean(baseline_vals)
    mean2 = np.mean(followup_vals)

    sd1 = np.std(baseline_vals, ddof=1)
    sd2 = np.std(followup_vals, ddof=1)

    pooled_std = np.sqrt((sd1**2 + sd2**2) / 2)

    if pooled_std == 0:
        return np.nan

    return (mean2 - mean1) / pooled_std

# ============================================================
# Run permutation tests for GM / NAWM / WMH CVR + Cohen’s d
# ============================================================

roi_names = ["GM", "WM"]
B = 10000

cvr_results = {}

for roi in roi_names:
    diff, pval, null = perm_test_roi(baseline_vals[roi], followup_vals[roi], B)

    d = cohens_d_independent(baseline_vals[roi], followup_vals[roi])

    cvr_results[roi] = {
        "diff": diff,
        "pval": pval,
        "null": null,
        "cohend": d,
        "baseline": baseline_vals[roi],
        "followup": followup_vals[roi]
    }

print("\nObserved CVR difference (follow-up − baseline):")
for roi in roi_names:
    print(f"{roi:5s}  Diff = {cvr_results[roi]['diff']:.6f}")

print("\nPermutation p-values:")
for roi in roi_names:
    print(f"{roi:5s}  p = {cvr_results[roi]['pval']:.6f}")

print("\nCohen's d:")
for roi in roi_names:
    print(f"{roi:5s}  d = {cvr_results[roi]['cohend']:.4f}")

































