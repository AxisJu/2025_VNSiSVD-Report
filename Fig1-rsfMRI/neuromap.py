import os

import hcp_utils as hcp

# Neuroimaging tools
import nilearn.datasets
import numpy as np
import pandas as pd

# Visualization
from data_visualization.stats_plot import scatter_lineplot
from joblib import Parallel, delayed
from netneurotools import datasets as nntdata
from neuromaps import datasets, nulls, stats, transforms
from neuromaps.datasets import available_annotations, fetch_annotation
from neuromaps.images import dlabel_to_gifti
from neuromaps.parcellate import Parcellater
from tqdm import tqdm

# --- 1. Configuration & Paths ---
PATHS = {
    "invns": "../output/alff/sub-001_task-InVNS_space-fsLR_den-91k_bold.dtseries.npy",
    "prevns": "../output/alff/sub-001_task-PreVNS_space-fsLR_den-91k_bold.dtseries.npy",
    "output_dir": "../output/alff/output/neuromaps",
}

# --- 2. Atlas & Parcellater Setup ---
# Setup Surface Parcellater (fsLR 32k)
schaefer_fslr_file = nntdata.fetch_schaefer2018("fslr32k")["100Parcels7Networks"]
fslr_parc = Parcellater(dlabel_to_gifti(schaefer_fslr_file), "fsLR")

# Setup Volumetric Parcellater (MNI152)
schaefer_mni = nilearn.datasets.fetch_atlas_schaefer_2018(
    n_rois=100, yeo_networks=7, resolution_mm=2
)
mni_parc = Parcellater(schaefer_mni["maps"], "mni152")

# --- 3. Process Target Data ---
# Load and calculate delta (ALFF difference)
invns_data = np.load(PATHS["invns"])
prevns_data = np.load(PATHS["prevns"])
diff_data = hcp.cortex_data(invns_data - prevns_data)
diff_parc = fslr_parc.fit_transform(diff_data, space="fsLR")


# --- 4. Define Processing Function ---
def process_anno(annotation):
    """Fetch, transform, and parcellate brain annotations."""
    source, desc, space, den = annotation
    try:
        anno = fetch_annotation(source=source, desc=desc, space=space, den=den)

        # Handle single hemisphere files
        if isinstance(anno, str) or len(anno) != 2:
            hemi = "R" if "hemi-R" in str(anno) else "L"
            if space == "fsaverage":
                xfm = transforms.fsaverage_to_fslr(anno, "32k", hemi=hemi)
            elif space == "civet":
                xfm = transforms.civet_to_fslr(anno, "32k", hemi=hemi)
            else:
                xfm = transforms.fslr_to_fslr(anno, "32k", hemi=hemi)

            p_data = fslr_parc.fit_transform(xfm, "fsLR", hemi=hemi)
            # Duplicate to match parcel count if necessary
            return np.concatenate([p_data.squeeze(), p_data.squeeze()]), annotation

        # Handle standard bilateral files
        if space == "fsaverage":
            xfm = transforms.fsaverage_to_fslr(anno, "32k")
            p_data = fslr_parc.fit_transform(xfm, "fsLR")
        elif space == "MNI152":
            p_data = mni_parc.fit_transform(anno, "MNI152")
        elif space == "civet":
            xfm = transforms.civet_to_fslr(anno, "32k")
            p_data = fslr_parc.fit_transform(xfm, "fsLR")
        else:
            xfm = transforms.fslr_to_fslr(anno, "32k")
            p_data = fslr_parc.fit_transform(xfm, "fsLR")

        return p_data.squeeze(), annotation
    except Exception:
        return None, None


# --- 5. Execution & Statistical Analysis ---
# Parallel parcellation
all_annos = available_annotations()
results = Parallel(n_jobs=-1)(
    delayed(process_anno)(a) for a in tqdm(all_annos, desc="Parcellating")
)

stats_list = []

# Loop through valid annotations for correlation & null testing
for data_par, info in tqdm([r for r in results if r[0] is not None], desc="Testing"):
    src, dsc, spc, dn = info

    # Generate null distributions (Spin Test)
    null_dist = nulls.alexander_bloch(
        data_par,
        atlas="fsLR",
        density="32k",
        n_perm=5000,
        seed=1234,
        parcellation=dlabel_to_gifti(schaefer_fslr_file),
    )

    # Calculate correlation and p-value
    r_val, p_val = stats.compare_images(data_par, diff_parc, nulls=null_dist)

    # Save visualization
    plot_df = pd.DataFrame({"Annotation": data_par, "Difference": diff_parc})
    save_name = f"InVNS-PreVNS_{src}_{dsc}.pdf"

    scatter_lineplot(
        plot_df,
        x="Annotation",
        y="Difference",
        xlabel=f"{src}_{dsc}",
        ylabel="ALFF Diff",
        save_path=os.path.join(PATHS["output_dir"], save_name),
        r=r_val,
        p=p_val,
    )

    stats_list.append({"Source": src, "Desc": dsc, "Corr": r_val, "Pval": p_val})

# --- 6. Final Export ---
final_df = pd.DataFrame(stats_list).sort_values("Pval")
final_df.to_csv(
    os.path.join(PATHS["output_dir"], "InVNS-PreVNS_Summary.csv"), index=False
)
print("Processing complete.")
