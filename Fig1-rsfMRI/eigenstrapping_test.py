import nibabel as nib
import numpy as np
from eigenstrapping import SurfaceEigenstrapping
from scipy.stats import spearmanr


def load_neuromap_pair(name, nms_dict):
    """
    Load left and right hemisphere numpy arrays for a specific neuromap.
    """
    nm_lh = np.load(nms_dict[name][0]).squeeze()
    nm_rh = np.load(nms_dict[name][1]).squeeze()
    return nm_lh, nm_rh


def load_medial_wall_mask(lh_path, rh_path):
    """
    Load and concatenate gifti medial wall masks into a single boolean array.
    """
    mw_lh = nib.load(lh_path).darrays[0].data.astype(bool)
    mw_rh = nib.load(rh_path).darrays[0].data.astype(bool)
    return np.concatenate([mw_lh, mw_rh])


def calculate_spatial_correlation(
    target_data, map_lh, map_rh, mask, surrogate_obj=None
):
    if surrogate_obj is not None:
        # Generate surrogate (symmetric assumption: LH modes used for both)
        surr_lh = surrogate_obj.generate()
        combined_map = np.concatenate([surr_lh, surr_lh])
    else:
        combined_map = np.concatenate([map_lh, map_rh])

    corr, _ = spearmanr(combined_map[mask], target_data[mask], nan_policy="omit")
    return corr


def compute_eigenstrapping_pval(corr_true, corr_surrogates):
    surrogates = np.array(corr_surrogates)
    p_upper = np.mean(surrogates >= corr_true)
    p_lower = np.mean(surrogates <= corr_true)
    return np.min([p_upper, p_lower]) * 2  # Two-tailed p-value


def initialize_eigenstrapping(data_lh, data_rh, surf_lh, surf_rh, n_modes=200):
    eigen_lh = SurfaceEigenstrapping(
        data=data_lh, surface=surf_lh, resample=True, num_modes=n_modes, n_jobs=-1
    )
    eigen_rh = SurfaceEigenstrapping(
        data=data_rh, surface=surf_rh, resample=True, num_modes=n_modes, n_jobs=-1
    )
    return eigen_lh, eigen_rh
