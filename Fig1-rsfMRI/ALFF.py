import os
from pathlib import Path

import nibabel as nib
import nilearn
import nilearn.signal
import numpy as np
import pandas as pd
from data_visualization.brain_plot import surface_plot
from scipy.fft import fft, fftfreq


def compute_alff(signal, fs, low_freq=0.01, high_freq=0.08):
    N = len(signal)
    freqs = fftfreq(N, d=1 / fs)
    fft_values = np.abs(fft(signal))

    pos_mask = freqs >= 0
    freqs = freqs[pos_mask]
    fft_values = fft_values[pos_mask]

    band_mask = (freqs >= low_freq) & (freqs <= high_freq)
    alff = np.sqrt(np.mean(fft_values[band_mask] ** 2))
    return alff


bold_paths = list(Path("../data/derivatives/deepprep/BOLD/").rglob("*dtseries.nii"))


for path in bold_paths:
    print(path)
    bold = nib.load(path)
    confound, _ = nilearn.interfaces.fmriprep.load_confounds(
        str(path),
        strategy=("motion", "wm_csf", "global_signal"),
        global_signal="full",
        wm_csf="full",
    )
    data = bold.get_fdata()
    data = data[5:, :]
    confound = confound.iloc[5:, :]
    bold_clean = nilearn.signal.clean(
        data, confounds=confound, detrend=True, standardize=False
    )
    alff_results = np.apply_along_axis(compute_alff, 0, bold_clean, fs=1 / 0.7)
    alff_img_path = "../output/alff/" + path.stem + ".npy"
    np.save(alff_img_path, alff_results.squeeze())
