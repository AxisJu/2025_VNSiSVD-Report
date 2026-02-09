import numpy as np
import nibabel as nib
from tqdm import tqdm

# -------------------------------------------------------------------

baseline_ktrans = nib.load(
    r"Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/004_rocketship_DCE/baseline/rt1_vibe_cor_dynamic_waterext_12_patlak_fit_Ktrans.nii"
).get_fdata()

followup_ktrans = nib.load(
    r"Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/004_rocketship_DCE/followup/rt1_vibe_cor_dynamic_waterext_11_patlak_fit_Ktrans.nii"
).get_fdata()

# -------------------------------------------------------------------

baseline_brain_mask = nib.load(
    r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/baseline/baseline_dce_mean_mask_brain.nii'
).get_fdata() > 0

baseline_gm_mask = nib.load(
    r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/baseline/c1meant1_vibe_cor_dynamic_waterext_12.nii'
).get_fdata() > 0

baseline_wm_mask = nib.load(
    r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/baseline/c2meant1_vibe_cor_dynamic_waterext_12.nii'
).get_fdata() > 0

baseline_wmh_mask = nib.load(
    r'Z:/2023 VNSiSVD/data/data_neuroimage_trial/bids/derivatives/DeepWMH/sub001_baseline_DCE/002_Segmentations/003_postproc_fov/sub001.nii.gz'
).get_fdata() > 0

baseline_nawm_mask = baseline_wm_mask & (~baseline_wmh_mask.astype(bool))

# -------------------------------------------------------------------

followup_brain_mask = nib.load(
    r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/followup/followup_dce_mean_mask_brain.nii'
).get_fdata() > 0

followup_gm_mask = nib.load(
    r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/followup/c1meant1_vibe_cor_dynamic_waterext_11.nii'
).get_fdata() > 0

followup_wm_mask = nib.load(
    r'Z:/2023 VNSiSVD/data/data_neuroimage_DCE/processed/002_spm12_realign&seg/followup/c2meant1_vibe_cor_dynamic_waterext_11.nii'
).get_fdata() > 0

followup_wmh_mask = nib.load(
    r'Z:/2023 VNSiSVD/data/data_neuroimage_trial/bids/derivatives/DeepWMH/sub001_6m_DCE/002_Segmentations/003_postproc_fov/sub001.nii.gz'
).get_fdata() > 0

followup_nawm_mask = followup_wm_mask & (~followup_wmh_mask.astype(bool))

# -------------------------------------------------------------------

def perm_test_roi(baseline_vals, followup_vals, B=5000, two_sided=True):

    baseline_vals = baseline_vals[~np.isnan(baseline_vals)]
    followup_vals = followup_vals[~np.isnan(followup_vals)]

    n1 = len(baseline_vals)
    n2 = len(followup_vals)

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

# -------------------------------------------------------------------

baseline_wmh_vals  = baseline_ktrans[baseline_wmh_mask]
followup_wmh_vals  = followup_ktrans[followup_wmh_mask]

baseline_nawm_vals = baseline_ktrans[baseline_nawm_mask]
followup_nawm_vals = followup_ktrans[followup_nawm_mask]

baseline_gm_vals   = baseline_ktrans[baseline_gm_mask]
followup_gm_vals   = followup_ktrans[followup_gm_mask]

print("Running permutation tests (ROI-wise baseline vs follow-up)...")

B = 10000

wmh_diff,  wmh_p,  wmh_null  = perm_test_roi(baseline_wmh_vals,  followup_wmh_vals,  B=B, two_sided=True)
nawm_diff, nawm_p, nawm_null = perm_test_roi(baseline_nawm_vals, followup_nawm_vals, B=B, two_sided=True)
gm_diff,   gm_p,   gm_null   = perm_test_roi(baseline_gm_vals,   followup_gm_vals,   B=B, two_sided=True)

print("\nObserved mean Ktrans difference (follow-up - baseline):")
print(f"  WMH :  {wmh_diff}")
print(f"  NAWM:  {nawm_diff}")
print(f"  GM  :  {gm_diff}")

print("\nPermutation test (two-sided p-values):")
print(f"  WMH :  p = {wmh_p}")
print(f"  NAWM:  p = {nawm_p}")
print(f"  GM  :  p = {gm_p}")

# -------------------------------------------------------------------

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
import numpy as np

# Create figure with 3 subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Permutation Test Results: Baseline vs Follow-up Ktrans\n(Follow-up - Baseline)', 
             fontsize=16, fontweight='bold', y=1.02)

# ROI names and data
roi_names = ['WMH', 'NAWM', 'GM']
roi_diffs = [wmh_diff, nawm_diff, gm_diff]
roi_pvals = [wmh_p, nawm_p, gm_p]
roi_nulls = [wmh_null, nawm_null, gm_null]

# Original data for Cohen's d calculation
roi_baseline = [baseline_wmh_vals, baseline_nawm_vals, baseline_gm_vals]
roi_followup = [followup_wmh_vals, followup_nawm_vals, followup_gm_vals]

# Colors
color_significant = '#E31A1C'  # Red for significant
color_nonsignif = '#1F78B4'    # Blue for non-significant
color_null = '#CCCCCC'         # Gray for null distribution

# Plot each ROI
for idx, (ax, roi, diff, pval, null, baseline_vals, followup_vals) in enumerate(
    zip(axes, roi_names, roi_diffs, roi_pvals, roi_nulls, roi_baseline, roi_followup)):
    
    # Determine if significant (p < 0.05)
    is_significant = pval < 0.05
    obs_color = color_significant if is_significant else color_nonsignif
    
    # Calculate Cohen's d
    pooled_std = np.sqrt((np.std(baseline_vals, ddof=1)**2 + np.std(followup_vals, ddof=1)**2) / 2)
    cohens_d = diff / pooled_std if pooled_std > 0 else 0
    
    # Plot null distribution histogram
    n, bins, patches = ax.hist(null, bins=50, alpha=0.7, color=color_null, 
                                edgecolor='black', linewidth=0.5,
                                label='Null Distribution')
    
    # Plot observed difference as vertical line
    ax.axvline(diff, color=obs_color, linewidth=3, linestyle='--',
               label=f'Observed Diff\n({diff:.6f})', zorder=5)
    
    # Add shaded regions for critical values (alpha = 0.05, two-tailed)
    alpha = 0.05
    lower_crit = np.percentile(null, alpha/2 * 100)
    upper_crit = np.percentile(null, (1 - alpha/2) * 100)
    
    ax.axvline(lower_crit, color='red', linewidth=1, linestyle=':', alpha=0.5)
    ax.axvline(upper_crit, color='red', linewidth=1, linestyle=':', alpha=0.5)
    
    # Determine significance marker
    if pval < 0.001:
        sig_marker = '***'
    elif pval < 0.01:
        sig_marker = '**'
    elif pval < 0.05:
        sig_marker = '*'
    else:
        sig_marker = 'n.s.'
    
    # Styling
    title_color = obs_color
    ax.set_title(f'{roi}\np = {pval:.4f} ({sig_marker})', 
                 fontsize=12, fontweight='bold', color=title_color)
    ax.set_xlabel('Mean Difference (min/mL)', fontsize=10)
    ax.set_ylabel('Frequency', fontsize=10)
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
    
    # Add stats text box with Cohen's d and absolute difference
    stats_text = f"Mean Diff: {diff:.6f}\nAbs Diff: {abs(diff):.6f}\nCohen's d: {cohens_d:.4f}\np-value: {pval:.4f}\nPermutations: {B}"
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
            fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Rotate x-axis labels by 45 degrees for all subplots
for ax in axes:
    ax.tick_params(axis='x', rotation=45)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the plot
plt.show()

# ============================================================

import matplotlib.pyplot as plt
import numpy as np

roi_names = ['WMH', 'NAWM', 'GM']
roi_nulls = [wmh_null, nawm_null, gm_null]
roi_diffs = [wmh_diff, nawm_diff, gm_diff]
roi_pvals = [wmh_p, nawm_p, gm_p]

null_means = [np.mean(n) for n in roi_nulls]
null_lower = [np.percentile(n, 2.5) for n in roi_nulls]
null_upper = [np.percentile(n, 97.5) for n in roi_nulls]

error_bars = [
    [null_means[i] - null_lower[i], 
     null_upper[i] - null_means[i]]  
    for i in range(3)
]

colors = ['#E31A1C' if p < 0.05 else '#1F78B4' for p in roi_pvals]

fig, ax = plt.subplots(figsize=(8, 6))

x = np.arange(3)

bars = ax.bar(
    x,
    null_means,
    yerr=np.array(error_bars).T,
    capsize=8,
    color='#CCCCCC',
    edgecolor='black',
    linewidth=1.0,
    label='Null mean ± 95% CI'
)

for i, (obs, color) in enumerate(zip(roi_diffs, colors)):
    ax.scatter(i, obs, color=color, s=120, zorder=5, label='Observed Diff' if i == 0 else None)

# Add horizontal zero line
ax.axhline(0, color='black', linewidth=1, linestyle='--')

# Styling
ax.set_xticks(x)
ax.set_xticklabels(roi_names, fontsize=12)
ax.set_ylabel('Mean Difference (Follow-up - Baseline)', fontsize=12)
ax.set_title('Observed Ktrans Change vs Null Distribution (95% CI)', fontsize=15, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Add legend
ax.legend(framealpha=0.9)

plt.tight_layout()
plt.show()