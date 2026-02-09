cd ~/../../mnt/z/2023\ VNSiSVD/
docker pull pennlinc/qsirecon
   
docker run -ti --rm -w /work \
  -v ./data/data_neuroimage_trial_processed/bids/derivatives/qsiprep:/data:ro \
  -v ./data/data_neuroimage_trial_processed/bids/derivatives/qsirecon:/out \
  -v ./data:/work \
  -v ./bin/license/freesurfer/license.txt:/opt/freesurfer/license.txt:ro \
  pennlinc/qsirecon:latest \
  /data /out participant \
  --fs-license-file /opt/freesurfer/license.txt \
  --recon-spec mrtrix_multishell_msmt_noACT \
  --atlases AAL116 \
  --output-resolution 1.3

docker run -ti --rm -w /work \
  -v ./data/data_neuroimage_trial_processed/bids/derivatives/qsiprep:/data:ro \
  -v ./data/data_neuroimage_trial_processed/bids/derivatives/qsirecon:/out \
  -v ./data:/work \
  -v ./bin/license/freesurfer/license.txt:/opt/freesurfer/license.txt:ro \
  pennlinc/qsirecon:latest \
  /data /out participant \
  --fs-license-file /opt/freesurfer/license.txt \
  --recon-spec amico_noddi \
  --atlases AAL116 \
  --output-resolution 1.3

docker run -ti --rm -w /work \
  -v ./data/data_neuroimage_trial_processed/bids/derivatives/qsiprep:/data:ro \
  -v ./data/data_neuroimage_trial_processed/bids/derivatives/qsirecon:/out \
  -v ./data:/work \
  -v ./bin/license/freesurfer/license.txt:/opt/freesurfer/license.txt:ro \
  pennlinc/qsirecon:latest \
  /data /out participant \
  --fs-license-file /opt/freesurfer/license.txt \
  --recon-spec dsi_studio_gqi \
  --atlases AAL116 \
  --output-resolution 1.3

docker run -ti --rm -w /work \
  -v ./data/data_neuroimage_trial_processed/bids/derivatives/qsiprep:/data:ro \
  -v ./data/data_neuroimage_trial_processed/bids/derivatives/qsirecon:/out \
  -v ./data:/work \
  -v ./bin/license/freesurfer/license.txt:/opt/freesurfer/license.txt:ro \
  pennlinc/qsirecon:latest \
  /data /out participant \
  --fs-license-file /opt/freesurfer/license.txt \
  --recon-spec dsi_studio_autotrack \
  --atlases AAL116 \
  --output-resolution 1.3
  