cd ~/../../mnt/s/2023\ VNSiSVD/
docker pull pennbbl/qsiprep
   
docker run -ti --rm -w /work \
  -v ./data/data_neuroimage_trial_processed/bids:/data:ro \
  -v ./data/data_neuroimage_trial_processed/bids/derivatives/qsiprep:/out \
  -v ./data:/work \
  -v ./bin/license/freesurfer/license.txt:/opt/freesurfer/license.txt:ro \
  pennlinc/qsiprep:latest \
  /data /out participant \
  --fs-license-file /opt/freesurfer/license.txt \
  --hmc-model 3dSHORE \
  --output-resolution 1.3