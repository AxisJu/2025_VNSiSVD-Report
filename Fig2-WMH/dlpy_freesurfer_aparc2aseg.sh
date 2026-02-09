cd ~/../../mnt/z/2023\ VNSiSVD/
docker pull freesurfer/freesurfer:7.1.1

# baseline
docker run -it --rm \
  -v ./bin/license/freesurfer/license.txt:/opt/freesurfer/license.txt:ro \
  -v ./data/data_neuroimage_trial/bids/derivatives/freesurfer:/output \
  -v ./data/data_neuroimage_CVR/bids/derivatives/deepprep_baselineT1/Recon:/subjects \
  -e SUBJECTS_DIR=/subjects \
  -e FS_LICENSE=/opt/freesurfer/license.txt \
  freesurfer/freesurfer:7.1.1 /bin/bash

mri_aparc2aseg --s sub-001 --o /output/baseline_aparc+aseg_labelwm.mgz --new-ribbon --labelwm --wmparc-dmax 10 --rip-unknown --hypo-as-wm
mri_convert /output/baseline_aparc+aseg_labelwm.mgz /output/baseline_aparc+aseg_labelwm.nii.gz

# followup
docker run -it --rm \
  -v ./bin/license/freesurfer/license.txt:/opt/freesurfer/license.txt:ro \
  -v ./data/data_neuroimage_trial/bids/derivatives/freesurfer:/output \
  -v ./data/data_neuroimage_CVR/bids/derivatives/deepprep_6mT1/Recon:/subjects \
  -e SUBJECTS_DIR=/subjects \
  -e FS_LICENSE=/opt/freesurfer/license.txt \
  freesurfer/freesurfer:7.1.1 /bin/bash

mri_aparc2aseg --s sub-001 --o /output/followup_aparc+aseg_labelwm.mgz --new-ribbon --labelwm --wmparc-dmax 10 --rip-unknown --hypo-as-wm
mri_convert /output/followup_aparc+aseg_labelwm.mgz /output/followup_aparc+aseg_labelwm.nii.gz
