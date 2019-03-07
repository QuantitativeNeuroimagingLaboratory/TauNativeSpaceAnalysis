#!/bin/bash
#This script registers Tau PET image to FreeSurfer image and creates masks and normalized SUVR image. Creates 4 ADNI ROIs. Applies 4 ADNI ROIs. Saves all values to a stats file

# Usage: AnalyzeTauPetImage.sh <InputDynamicPETimage> <FreeSurferDir> <OutputDir>


if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters, use following syntax"
    echo "Usage: AnalyzePetImage.sh <InputDynamicPETimage> <FreeSurferDir> <OutputDir>"
    exit 1
fi

# Set up paths
export PATH=$PATH:/bin:/usr/bin
export PATH=$PATH:/usr/local/ANTS/bin
export PATH=$PATH:/usr/local/fsl/bin
FSLDIR=/usr/local/fsl/5.0.7/
. ${FSLDIR}/etc/fslconf/fsl.sh
PATH=${FSLDIR}/bin:${PATH}
export FSLDIR PATH;
FSLOUTPUTTYPE=NIFTI_GZ
export FSLOUTPUTTYPE


echo 'Script begins here'
echo `date`

echo "This script analyzes the following PET image"
echo ${1}
echo "Using the following T1 image's FreeSurfer segmentation"
echo ${2}
echo "An the results will be saved in the following directory"
echo ${3}


SubDir=${3}
PETImage=${1} 

echo 'Creating output directory'
mkdir ${SubDir}

echo 'Empty directory if it is already exist'
rm -rf ${SubDir}/*.*

echo 'Converting Freesurfer format files to nifti and store them in the output directory'
mri_convert ${2}/mri/nu.mgz ${SubDir}/nu.nii.gz
if [ $? -ne 0 ]; then
    echo "The T1 image in FreeSurfer space is missing"
    exit 2
fi
mri_convert ${2}/mri/aparc+aseg.mgz ${SubDir}/aparc+aseg.nii.gz
if [ $? -ne 0 ]; then
    echo "The FreeSurfer segmentation image is missing"
    exit 3
fi


FSImage=${SubDir}/nu.nii.gz
FSLabel=${SubDir}/aparc+aseg.nii.gz


echo 'Split the dynamic PET image into 6 static images'
fslsplit ${PETImage} ${SubDir}/PET_DynamicSplit
if [ $? -ne 0 ]; then
    echo "The input dynamic PET image is missing"
    exit 4
fi


echo 'Register PET dynamic volumes to the first volume'
flirt -in ${SubDir}/PET_DynamicSplit0001.nii.gz -ref ${SubDir}/PET_DynamicSplit0000.nii.gz -out ${SubDir}/PET_DynamicSplit0001_Registered.nii.gz -omat ${SubDir}/PET_DynamicSplit0001_Registered.mat -bins 256 -cost normmi -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6  -interp trilinear

flirt -in ${SubDir}/PET_DynamicSplit0002.nii.gz -ref ${SubDir}/PET_DynamicSplit0000.nii.gz -out ${SubDir}/PET_DynamicSplit0002_Registered.nii.gz -omat ${SubDir}/PET_DynamicSplit0002_Registered.mat -bins 256 -cost normmi -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6  -interp trilinear

flirt -in ${SubDir}/PET_DynamicSplit0003.nii.gz -ref ${SubDir}/PET_DynamicSplit0000.nii.gz -out ${SubDir}/PET_DynamicSplit0003_Registered.nii.gz -omat ${SubDir}/PET_DynamicSplit0003_Registered.mat -bins 256 -cost normmi -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6  -interp trilinear

flirt -in ${SubDir}/PET_DynamicSplit0004.nii.gz -ref ${SubDir}/PET_DynamicSplit0000.nii.gz -out ${SubDir}/PET_DynamicSplit0004_Registered.nii.gz -omat ${SubDir}/PET_DynamicSplit0004_Registered.mat -bins 256 -cost normmi -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6  -interp trilinear

flirt -in ${SubDir}/PET_DynamicSplit0005.nii.gz -ref ${SubDir}/PET_DynamicSplit0000.nii.gz -out ${SubDir}/PET_DynamicSplit0005_Registered.nii.gz -omat ${SubDir}/PET_DynamicSplit0005_Registered.mat -bins 256 -cost normmi -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6  -interp trilinear

echo 'Add the registered volumes to generate a newly registered static PET image'
fslmaths ${SubDir}/PET_DynamicSplit0000.nii.gz -add ${SubDir}/PET_DynamicSplit0001_Registered.nii.gz -add ${SubDir}/PET_DynamicSplit0002_Registered.nii.gz -add ${SubDir}/PET_DynamicSplit0003_Registered.nii.gz -add ${SubDir}/PET_DynamicSplit0004_Registered.nii.gz -add ${SubDir}/PET_DynamicSplit0005_Registered.nii.gz ${SubDir}/PET_RegisteredSatatic.nii.gz 


echo 'Directly registering the PET image to the Freesurfer space'
flirt -in ${SubDir}/PET_RegisteredSatatic.nii.gz -ref ${FSImage} -out ${SubDir}/PET_RegisteredSatatic_NuSpace.nii.gz -omat ${SubDir}/PET_RegisteredSatatic_NuSpace.mat -bins 256 -cost normmi -searchrx -180 180 -searchry -180 180 -searchrz -180 180 -dof 6  -interp trilinear

echo 'Making a mask image of the cerebellum gray and white matter'
fslmaths ${FSLabel} -thr 7 -uthr 7 -bin ${SubDir}/CerebellumWhiteMatterMask.nii.gz
fslmaths ${FSLabel} -thr 46 -uthr 46 -bin -add ${SubDir}/CerebellumWhiteMatterMask.nii.gz ${SubDir}/CerebellumWhiteMatterMask.nii.gz

fslmaths ${FSLabel} -thr 8 -uthr 8 -bin ${SubDir}/CerebellumGrayMatterMask.nii.gz
fslmaths ${FSLabel} -thr 47 -uthr 47 -bin -add ${SubDir}/CerebellumGrayMatterMask.nii.gz ${SubDir}/CerebellumGrayMatterMask.nii.gz

echo 'Dialate cerebellum white matetr mask by 2 voxel'
fslmaths ${SubDir}/CerebellumWhiteMatterMask.nii.gz -kernel box 5 -dilM  ${SubDir}/CerebellumWhiteMatterMaskDialated.nii.gz

echo 'Subtract the Dialate cerebelum white matter mask from Gray matter mask to make sure no white matter voxels are considered for suv computation'
fslmaths ${SubDir}/CerebellumGrayMatterMask.nii.gz -sub ${SubDir}/CerebellumWhiteMatterMaskDialated.nii.gz -thr 0 -bin ${SubDir}/CerebellumGrayMatterMaskNoWhite.nii.gz;     

echo 'Mask PET image with the generated gray matter mask to compute the average uptake in cerebelum gray matter' 
fslmaths ${SubDir}/PET_RegisteredSatatic_NuSpace.nii.gz -mas ${SubDir}/CerebellumGrayMatterMaskNoWhite.nii.gz ${SubDir}/PET_RegisteredSatatic_NuSpace_CerebellumGrayMatter.nii.gz; 


echo 'Obtain cerebral white matter mask'
fslmaths ${FSLabel} -thr 2 -uthr 2 -bin ${SubDir}/CerebralWhiteMatterMask.nii.gz
fslmaths ${FSLabel} -thr 41 -uthr 41 -bin -add ${SubDir}/CerebralWhiteMatterMask.nii.gz ${SubDir}/CerebralWhiteMatterMask.nii.gz

echo 'Dialate cerebral white matetr mask by 1 voxel'
fslmaths ${SubDir}/CerebralWhiteMatterMask.nii.gz -kernel box 3 -dilM  ${SubDir}/CerebralWhiteMatterMaskDialated.nii.gz



ExtractRegionalTauPETUptake.py ${SubDir}
TransferingTauPetImagesToStandardSpace.sh ${SubDir}

echo "Well...I finished...";
echo `date`





