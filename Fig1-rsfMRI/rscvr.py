import os
import nibabel as nib
import numpy as np
from nilearn import datasets, signal
from nilearn.image import resample_to_img
from nilearn.maskers import NiftiMasker
from nilearn.interfaces import fmriprep


def bold_process(img, confounds):
    """
    Performs signal cleaning and regresses voxel-wise data against the global mean.
    The resulting beta weights represent the resting-state Cerebrovascular Reactivity (rsCVR).
    """
    n_scans = img.shape[-1]
    # Skip the first 5 scans to ensure T1-equilibration
    sample_mask = np.arange(5, n_scans)

    # Standard MNI152 brain mask (2mm resolution)
    mni_template_mask = datasets.load_mni152_brain_mask(resolution=2)

    # Resample mask to match the input image geometry
    final_mask = resample_to_img(
        source_img=mni_template_mask,
        target_img=img,
        interpolation="nearest",
    )

    # Initialize NiftiMasker with band-pass filtering and spatial smoothing
    masker = NiftiMasker(
        mask_img=final_mask,
        detrend=True,
        standardize=False,
        low_pass=0.04,
        high_pass=0.02,
        t_r=0.7,
        smoothing_fwhm=8,
    )

    # Clean the BOLD signal: regressing out motion confounds and band-pass filtering
    cleaned = masker.fit_transform(
        img, confounds=confounds, sample_mask=sample_mask
    )  # Result shape: (Timepoints, Voxels)

    # Extract Global Signal (GS) as the reference regressor
    ref = cleaned.mean(axis=1)  # (T,)
    X = ref.reshape(-1, 1)  # (T, 1)

    # Compute Voxel-wise Beta weights using Ordinary Least Squares (OLS)
    # Equation: beta = (X'X)^-1 X'Y
    beta = (X.T @ cleaned) / (X.T @ X)  # (1, V)

    # Map the 1D array back to 3D NIfTI image space
    beta_img = masker.inverse_transform(beta.ravel())

    return beta_img


def create_rscvr(path):
    """
    Main execution pipeline for rsCVR estimation per subject/session.
    """
    print(f"Processing: {path}")

    # Load BOLD image and generate motion confounds via fMRIPrep strategy
    img = nib.load(path)
    confounds, _ = fmriprep.load_confounds(str(path), strategy=["motion"])

    # Estimate rsCVR image
    beta_img = bold_process(img, confounds)

    # Define output path using forward-slash convention
    output_filename = path.name.replace(
        "_space-MNI152NLin6Asym_res-02_desc-preproc_bold.nii.gz", "_rscvr.nii.gz"
    )
    rsfa_img_path = f"../output/cvr/{output_filename}"

    # Ensure directory exists and save the resulting NIfTI
    os.makedirs(os.path.dirname(rsfa_img_path), exist_ok=True)
    nib.save(beta_img, rsfa_img_path)

    print(f"Saved: {rsfa_img_path}")
