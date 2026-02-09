# install dcm2bids
docker pull unfmontreal/dcm2bids:3.2.0
docker run --rm -it unfmontreal/dcm2bids:3.2.0 --help

# prepare scaffold
cd ~/../../mnt/z/2023\ VNSiSVD/
docker run --rm -it \
    --entrypoint /venv/bin/dcm2bids_scaffold \
    -v ./data/data_neuroimage_cvr:/bids \
    unfmontreal/dcm2bids:3.2.0 -o /bids/bids
# dcm2nii preview
docker run --rm -it \
    --entrypoint /venv/bin/dcm2bids_helper \
    -v ./data/data_neuroimage_cvr/raw/dicom:/dicoms:ro \
    -v ./data/data_neuroimage_cvr/bids:/bids \
    unfmontreal/dcm2bids:3.2.0 -o /bids -d /dicoms

# configuration
nano ./data/data_neuroimage_cvr/bids/code/dcm2bids_config_sub001baseline.json
nano ./data/data_neuroimage_cvr/bids/code/dcm2bids_config_sub0016m.json
### https://unfmontreal.github.io/Dcm2Bids/3.2.0/how-to/create-config-file/
### https://bids-specification.readthedocs.io/en/stable/modality-specific-files/magnetic-resonance-imaging-data.html#diffusion-imaging-data

# dcm2bids
docker run --rm -it \
    -v ./data/data_neuroimage_cvr/raw/dicom/sub001_baseline:/dicoms:ro \
    -v ./data/data_neuroimage_cvr/bids/code/dcm2bids_config_sub001baseline.json:/config.json:ro \
    -v ./data/data_neuroimage_cvr/bids:/bids \
    unfmontreal/dcm2bids:3.2.0 --bids_validate --force_dcm2bids --clobber \
    -o /bids -d /dicoms -c /config.json -p 001 -s baseline
docker run --rm -it \
    -v ./data/data_neuroimage_cvr/raw/dicom/sub001_6m:/dicoms:ro \
    -v ./data/data_neuroimage_cvr/bids/code/dcm2bids_config_sub0016m.json:/config.json:ro \
    -v ./data/data_neuroimage_cvr/bids:/bids \
    unfmontreal/dcm2bids:3.2.0 --bids_validate --force_dcm2bids --clobber \
    -o /bids -d /dicoms -c /config.json -p 001 -s 6m
