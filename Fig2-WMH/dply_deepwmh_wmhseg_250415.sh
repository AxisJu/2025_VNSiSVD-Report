# prepare environment in WLS2 conda-env-NI
git clone https://github.com/lchdl/nnUNet_for_DeepWMH.git
cd nnUNet_for_DeepWMH/
pip install -e .

git clone https://github.com/lchdl/DeepWMH.git
cd DeepWMH/
pip install -e .

# https://www.nitrc.org/frs/download.php/5994/ROBEXv12.linux64.tar.gz
tar -xzvf ROBEXv12.linux64.tar.gz
mv ROBEX ~/bin/ROBEX
echo 'export ROBEX_DIR="/home/axis/bin/ROBEX"' >> ~/.bashrc

wget https://github.com/ANTsX/ANTs/releases/download/v2.6.0/ants-2.6.0-ubuntu-24.04-X64-gcc.zip
unzip ants-2.6.0-ubuntu-24.04-X64-gcc.zip -d ~/bin/ANTs
export PATH=~/bin/ANTs/ants-2.6.0/bin:$PATH

pip install pydicom==2.4.4
DeepWMH_predict -h

# prepare pretrained model
# https://drive.google.com/drive/folders/1CDJkY5F95sW638UGjohWDqXvPtBTI1w3
DeepWMH_install -m ./model_v1.0.tar.gz -o ~/bin/model/DeepWMH_model

# prediction
# change "\\wsl.localhost\Ubuntu\home\axis\Downloads\nnUNet_for_DeepWMH\nnunet\training\model_restore.py" line147 to "all_params = [torch.load(i, map_location=torch.device('cpu'), weights_only=False) for i in all_best_model_files]"
DeepWMH_predict \
    -i Data/ni/ANTs/reged_baselineFLAIR.nii.gz \
    -n sub001 \
    -m bin/model/DeepWMH_model \
    -o Data/ni/DeepWMH/sub001_baseline/ \
    -g 0
DeepWMH_predict \
    -i Data/ni/ANTs/reged_6mFLAIR.nii.gz \
    -n sub001 \
    -m bin/model/DeepWMH_model \
    -o Data/ni/DeepWMH/sub001_6m/ \
    -g 0

DeepWMH_predict \
    -i Data/ni/ANTs/MNI_baselineFLAIR.nii.gz \
    -n sub001 \
    -m bin/model/DeepWMH_model \
    -o Data/ni/DeepWMH/sub001_baseline_MNI/ \
    -g 0
DeepWMH_predict \
    -i Data/ni/ANTs/MNI_6mFLAIR.nii.gz \
    -n sub001 \
    -m bin/model/DeepWMH_model \
    -o Data/ni/DeepWMH/sub001_6m_MNI/ \
    -g 0
    
DeepWMH_predict \
    -i Data/ni/ANTs/reged_baselineFLAIR_DCE.nii.gz \
    -n sub001 \
    -m bin/model/DeepWMH_model \
    -o Data/ni/DeepWMH/sub001_baseline_DCE/ \
    -g 0
DeepWMH_predict \
    -i Data/ni/ANTs/reged_6mFLAIR_DCE.nii.gz \
    -n sub001 \
    -m bin/model/DeepWMH_model \
    -o Data/ni/DeepWMH/sub001_6m_DCE/ \
    -g 0
    