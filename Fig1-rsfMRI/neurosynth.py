import os

import hcp_utils as hcp
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from netneurotools import datasets as nntdata
from neuromaps import nulls, stats
from neuromaps.images import dlabel_to_gifti
from neuromaps.parcellate import Parcellater
from wordcloud import WordCloud

# --- 1. Global Setup ---
# Fetching atlas and initializing parcellater
schaefer = nntdata.fetch_schaefer2018("fslr32k")["100Parcels7Networks"]
parc_schaeffer = Parcellater(dlabel_to_gifti(schaefer), "fsLR")

# Loading Neurosynth term-based decoding data
neurosynth = pd.read_csv("F:/utils/Neurosynth/ns_scale100.csv", index_col=0)

# --- 2. Data Loading (Using Forward Slashes) ---
InVNS = np.load(
    "../output/alff/sub-001_task-InVNS_space-fsLR_den-91k_bold.dtseries.npy"
)
PreVNS = np.load(
    "../output/alff/sub-001_task-PreVNS_space-fsLR_den-91k_bold.dtseries.npy"
)
PostVNS = np.load(
    "../output/alff/sub-001_task-PostVNS_space-fsLR_den-91k_bold.dtseries.npy"
)
baseline = np.load(
    "../output/alff/sub-001_task-baseline_space-fsLR_den-91k_bold.dtseries.npy"
)
VNS_6m = np.load("../output/alff/sub-001_task-6m_space-fsLR_den-91k_bold.dtseries.npy")

# --- 3. Analysis and Visualization Functions ---


def run_neurosynth_analysis(diff_array, csv_out, img_out):
    """
    Computes spatial correlations with cognitive terms using spin-test nulls.
    """
    # Map dense surface data to parcellated space
    cortex_data = hcp.cortex_data(diff_array)
    state = parc_schaeffer.fit_transform(cortex_data, space="fsLR")

    corrs, pvals = [], []
    for col in neurosynth.columns:
        anno = neurosynth.loc[:, col]
        # Perform Alexander-Bloch spherical rotations for p-value estimation
        rotated = nulls.alexander_bloch(
            anno,
            atlas="fsLR",
            density="32k",
            n_perm=1000,
            seed=1234,
            parcellation=dlabel_to_gifti(schaefer),
        )
        corr, pval = stats.compare_images(anno, state, nulls=rotated)
        corrs.append(corr)
        pvals.append(pval)
        print(f"Analyzing {col}: r={corr:.3f}, p={pval:.3f}")

    results = pd.DataFrame(
        {"Feature": neurosynth.columns, "Correlation": corrs, "Pval": pvals}
    )
    results.to_csv(csv_out)

    # Generate visualization for significant correlations
    sig_results = results[results["Pval"] < 0.05]
    if not sig_results.empty:
        generate_wordcloud(sig_results, img_out)


def generate_wordcloud(significant_results, save_path):
    """
    Creates an elliptical word cloud colored by the sign of the correlation.
    """
    raw_weights = dict(
        zip(significant_results["Feature"], significant_results["Correlation"])
    )
    freq_weights = {k: abs(v) for k, v in raw_weights.items()}

    # Create elliptical mask
    h, w = 1200, 1800
    y, x = np.ogrid[:h, :w]
    mask = (((y - 600) ** 2 / 580**2 + (x - 900) ** 2 / 880**2) > 1).astype(
        np.uint8
    ) * 255

    colormap = cm.get_cmap("RdBu_r")
    max_abs = max(abs(min(raw_weights.values())), abs(max(raw_weights.values())))

    def color_func(word, **kwargs):
        val = raw_weights.get(word, 0)
        norm_val = 0.5 + 0.4 * val / max_abs
        r, g, b, _ = colormap(norm_val)
        return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"

    wc = WordCloud(
        background_color="white",
        width=1600,
        height=1200,
        mask=mask,
        prefer_horizontal=1.0,
    )
    wc.generate_from_frequencies(freq_weights)

    plt.figure(figsize=(8, 6))
    plt.imshow(wc.recolor(color_func=color_func), interpolation="bilinear")
    plt.axis("off")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


# --- 4. Pipeline Execution ---

# InVNS vs PreVNS
run_neurosynth_analysis(
    InVNS - PreVNS,
    "../output/alff/neurosynth_short_In_Pre.csv",
    "../output/alff/neurosynth_short_In_Pre.png",
)

# PostVNS vs PreVNS
run_neurosynth_analysis(
    PostVNS - PreVNS,
    "../output/alff/neurosynth_short_Post_Pre.csv",
    "../output/alff/neurosynth_short_Post_Pre.png",
)

# 6-Month vs Baseline
run_neurosynth_analysis(
    VNS_6m - baseline,
    "../output/alff/neurosynth_long_6m_baseline.csv",
    "../output/alff/neurosynth_long_6m_baseline.png",
)
