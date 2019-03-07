#!/bin/bash
# This scripts transfers the pre-analized/normalized PET images to standard space (MNI152)

# Usage : TransferingPetImagesToStandardSpace.sh <PET_AnalyzedDir>

echo 'Generating a dilated brain mask using the aparc+aseg file in the directory and the multiplying to existing nu.nii file to extract the brain'
fslmaths ${1}/aparc+aseg.nii.gz -bin -dilM -mul ${1}/nu.nii.gz ${1}/brain.nii.gz

echo 'Non-linear registration of the extracted brain to MNI brain using ANTS'
ANTS 3 -m MI[/usr/local/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz, ${1}/brain.nii.gz,1,64] -i 100x100x100 -o ${1}/Brain2standard.nii  -t SyN[0.25] -r Gauss[3,0] 

echo 'Transfering the PET image in nu space to MNI space'
WarpImageMultiTransform 3 ${1}/PET_RegisteredSatatic_NuSpace_SUVR.nii.gz  ${1}/PET_RegisteredSatatic_MNI152Space_SUVR.nii.gz -R /usr/local/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz ${1}/Brain2standardWarp.nii ${1}/Brain2standardAffine.txt

echo 'Transfering the brain image to MNI space for sanity check'
WarpImageMultiTransform 3 ${1}/brain.nii.gz  ${1}/brain_MNI152Space.nii.gz -R /usr/local/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz ${1}/Brain2standardWarp.nii ${1}/Brain2standardAffine.txt

	







