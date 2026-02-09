conda activate NI
cd 'Z:\2023 VNSiSVD\data_neuroimage_DCE\raw'
dcm2niix -z n -f %p_%s -o ../processed/001_dcm2nii/baseline -b y ./baseline
dcm2niix -z n -f %p_%s -o ../processed/001_dcm2nii/followup -b y ./followup