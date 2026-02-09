cd ~/../../mnt/z/2023\ VNSiSVD/
docker pull pbfslab/deepprep:25.1.0

docker run -it --rm -w /work \
  -v ./data/data_neuroimage_cvr/bids:/data:ro \
  -v ./data/data_neuroimage_cvr/bids/derivatives/deepprep:/out \
  -v ./data:/work \
  -v ./bin/license/freesurfer/license.txt:/opt/freesurfer/license.txt:ro \
  pbfslab/deepprep:25.1.0 \
  /data /out participant \
  --bold_task_type cvr \
  --fs_license_file /opt/freesurfer/license.txt \
  --device cpu

docker run -it --rm -w /work \
  -v ./data/tempbids:/data:ro \
  -v ./data/tempbids/derivatives/deepprep_6mT1:/out \
  -v ./data:/work \
  -v ./bin/license/freesurfer/license.txt:/opt/freesurfer/license.txt:ro \
  pbfslab/deepprep:25.1.0 \
  /data /out participant \
  --bold_task_type cvr \
  --anat_only \
  --fs_license_file /opt/freesurfer/license.txt \
  --device cpu

docker run -it --rm -w /work \
  -v ./data/tempbids:/data:ro \
  -v ./data/tempbids/derivatives/deepprep_bslT1:/out \
  -v ./data:/work \
  -v ./bin/license/freesurfer/license.txt:/opt/freesurfer/license.txt:ro \
  pbfslab/deepprep:25.1.0 \
  /data /out participant \
  --bold_task_type cvr \
  --anat_only \
  --fs_license_file /opt/freesurfer/license.txt \
  --device cpu