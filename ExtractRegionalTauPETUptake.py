#!/usr/bin/env python
# encoding: utf-8
"""
ExtractRegionalPETUptake.py
This scripts extract the regional Amloyd PET uptake

Created by Ray Razlighi on 2010-09-08.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
import sys
import csv
import nibabel as nb
import numpy as np

ReD = "\033[91m"
YelloW = "\033[93m"
EndC = "\033[0m"


Regions=[2,4,5,7,8,10,11,12,13,14,15,16,17,18,24,26,28,30,31,41,43,44,46,47,49,50,51,52,53,54,58,60,62,63,72,77,78,79,80,81,82,85,251,252,253,254,255]+range(1000,1036)+range(2000,2036); 

if __name__ == '__main__':
	

	
	if len(sys.argv)<2:
		print 'Usage: ExtractRegionalPETUptake.py <OutputDirectory> ' 
		sys.exit(0)

	OutputDir = sys.argv[1]
	
	#OutputDir = '/share/studies/WHICAP_PET/Quarantine/Subjects/W43680/V2/PETAnalyzed/'
	InputFileName = OutputDir + '/PET_RegisteredSatatic_NuSpace.nii.gz'	
	InputRoIImage = OutputDir + '/aparc+aseg.nii.gz'
	
	
	# load the Input PET image
	InputPetFileHandle = nb.load(InputFileName)
	PET_Data = InputPetFileHandle.get_data()
	
	
	# load FreeSurfer Segmantation image
	InputRoiFileHandle = nb.load(InputRoIImage)
	ROI_Data = InputRoiFileHandle.get_data()
	
	# load cerebelum gray matter uptake
	SUVFileHandle = nb.load(OutputDir + '/PET_RegisteredSatatic_NuSpace_CerebellumGrayMatter.nii.gz')
	SUV_Data = SUVFileHandle.get_data()
	
	
	# load dialted cerebral white matter mask
	WMFileHandle = nb.load(OutputDir + '/CerebralWhiteMatterMask.nii.gz')
	WM_Data = WMFileHandle.get_data()

		
	SUV = SUV_Data.sum() / (SUV_Data!=0).sum()
	
	PET_Data_SUVR = PET_Data / SUV
	
	
	RegionalPetUptake = np.zeros((len(Regions)+20, 4))
	for Reg in Regions:
		RegionalPetUptake[Regions.index(Reg), 0] = Reg
		RegionalPetUptake[Regions.index(Reg), 1] = (ROI_Data==Reg).sum()
		RegionalPetUptake[Regions.index(Reg), 2] = PET_Data_SUVR[((ROI_Data==Reg)  & (WM_Data==0)).nonzero()].mean()
		RegionalPetUptake[Regions.index(Reg), 3] = PET_Data_SUVR[((ROI_Data==Reg)  & (WM_Data==0)).nonzero()].std()
	
	RegionalPetUptake[119,0] = 119
	RegionalPetUptake[119,1] = ((ROI_Data==1015) | (ROI_Data==1030)).sum()
	RegionalPetUptake[119,2] = PET_Data_SUVR[(((ROI_Data==1015) | (ROI_Data==1030)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[119,3] = PET_Data_SUVR[(((ROI_Data==1015) | (ROI_Data==1030)) & (WM_Data==0)).nonzero()].std()
		
	RegionalPetUptake[120,0] = 120
	RegionalPetUptake[120,1] = ((ROI_Data==2015) | (ROI_Data==2030)).sum()
	RegionalPetUptake[120,2] = PET_Data_SUVR[(((ROI_Data==2015) | (ROI_Data==2030)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[120,3] = PET_Data_SUVR[(((ROI_Data==2015) | (ROI_Data==2030)) & (WM_Data==0)).nonzero()].std()

	RegionalPetUptake[121,0] = 121
	RegionalPetUptake[121,1] = ((ROI_Data==1008) | (ROI_Data==1025) | (ROI_Data==1029) | (ROI_Data==1031)).sum()
	RegionalPetUptake[121,2] = PET_Data_SUVR[(((ROI_Data==1008) | (ROI_Data==1025) | (ROI_Data==1029) | (ROI_Data==1031)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[121,3] = PET_Data_SUVR[(((ROI_Data==1008) | (ROI_Data==1025) | (ROI_Data==1029) | (ROI_Data==1031)) & (WM_Data==0)).nonzero()].std()

	RegionalPetUptake[122,0] = 122
	RegionalPetUptake[122,1] = ((ROI_Data==2008) | (ROI_Data==2025) | (ROI_Data==2029) | (ROI_Data==2031)).sum()
	RegionalPetUptake[122,2] = PET_Data_SUVR[(((ROI_Data==2008) | (ROI_Data==2025) | (ROI_Data==2029) | (ROI_Data==2031)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[122,3] = PET_Data_SUVR[(((ROI_Data==2008) | (ROI_Data==2025) | (ROI_Data==2029) | (ROI_Data==2031)) & (WM_Data==0)).nonzero()].std()

	RegionalPetUptake[123,0] = 123
	RegionalPetUptake[123,1] = ((ROI_Data==1002) | (ROI_Data==1010) | (ROI_Data==1023) | (ROI_Data==1026)).sum()
	RegionalPetUptake[123,2] = PET_Data_SUVR[(((ROI_Data==1002) | (ROI_Data==1010) | (ROI_Data==1023) | (ROI_Data==1026)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[123,3] = PET_Data_SUVR[(((ROI_Data==1002) | (ROI_Data==1010) | (ROI_Data==1023) | (ROI_Data==1026)) & (WM_Data==0)).nonzero()].std()

	RegionalPetUptake[124,0] = 124
	RegionalPetUptake[124,1] = ((ROI_Data==2002) | (ROI_Data==2010) | (ROI_Data==2023) | (ROI_Data==2026)).sum()
	RegionalPetUptake[124,2] = PET_Data_SUVR[(((ROI_Data==2002) | (ROI_Data==2010) | (ROI_Data==2023) | (ROI_Data==2026)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[124,3] = PET_Data_SUVR[(((ROI_Data==2002) | (ROI_Data==2010) | (ROI_Data==2023) | (ROI_Data==2026)) & (WM_Data==0)).nonzero()].std()

	RegionalPetUptake[125,0] = 125
	RegionalPetUptake[125,1] = ((ROI_Data==1003) | (ROI_Data==1012) | (ROI_Data==1014) | (ROI_Data==1018) |(ROI_Data==1019) | (ROI_Data==1020) | (ROI_Data==1027) | (ROI_Data==1028) | (ROI_Data==1032)).sum()
	RegionalPetUptake[125,2] = PET_Data_SUVR[(((ROI_Data==1003) | (ROI_Data==1012) | (ROI_Data==1014) | (ROI_Data==1018) |(ROI_Data==1019) | (ROI_Data==1020) | (ROI_Data==1027) | (ROI_Data==1028) | (ROI_Data==1032)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[125,3] = PET_Data_SUVR[(((ROI_Data==1003) | (ROI_Data==1012) | (ROI_Data==1014) | (ROI_Data==1018) |(ROI_Data==1019) | (ROI_Data==1020) | (ROI_Data==1027) | (ROI_Data==1028) | (ROI_Data==1032)) & (WM_Data==0)).nonzero()].std()

	RegionalPetUptake[126,0] = 126
	RegionalPetUptake[126,1] = ((ROI_Data==2003) | (ROI_Data==2012) | (ROI_Data==2014) | (ROI_Data==2018) |(ROI_Data==2019) | (ROI_Data==2020) | (ROI_Data==2027) | (ROI_Data==2028) | (ROI_Data==2032)).sum()
	RegionalPetUptake[126,2] = PET_Data_SUVR[(((ROI_Data==2003) | (ROI_Data==2012) | (ROI_Data==2014) | (ROI_Data==2018) |(ROI_Data==2019) | (ROI_Data==2020) | (ROI_Data==2027) | (ROI_Data==2028) | (ROI_Data==2032)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[126,3] = PET_Data_SUVR[(((ROI_Data==2003) | (ROI_Data==2012) | (ROI_Data==2014) | (ROI_Data==2018) |(ROI_Data==2019) | (ROI_Data==2020) | (ROI_Data==2027) | (ROI_Data==2028) | (ROI_Data==2032)) & (WM_Data==0)).nonzero()].std()

	RegionalPetUptake[127,0] = 127
	RegionalPetUptake[127,1] = (ROI_Data==1006).sum()
	RegionalPetUptake[127,2] = PET_Data_SUVR[((ROI_Data==1006) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[127,3] = PET_Data_SUVR[((ROI_Data==1006) & (WM_Data==0)).nonzero()].std()
	
	RegionalPetUptake[128,0] = 128
	RegionalPetUptake[128,1] = (ROI_Data==2006).sum()
	RegionalPetUptake[128,2] = PET_Data_SUVR[((ROI_Data==2006) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[128,3] = PET_Data_SUVR[((ROI_Data==2006) & (WM_Data==0)).nonzero()].std()
	
	RegionalPetUptake[129,0] = 129
	RegionalPetUptake[129,1] = (ROI_Data==17).sum()
	RegionalPetUptake[129,2] = PET_Data_SUVR[((ROI_Data==17) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[129,3] = PET_Data_SUVR[((ROI_Data==17) & (WM_Data==0)).nonzero()].std()
	
	RegionalPetUptake[130,0] = 130
	RegionalPetUptake[130,1] = (ROI_Data==53).sum()
	RegionalPetUptake[130,2] = PET_Data_SUVR[((ROI_Data==53) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[130,3] = PET_Data_SUVR[((ROI_Data==53) & (WM_Data==0)).nonzero()].std()
		
	RegionalPetUptake[131,0] = 131
	RegionalPetUptake[131,1] = ((ROI_Data==1016) | (ROI_Data==1007) | (ROI_Data==1013) | (ROI_Data==18)).sum()
	RegionalPetUptake[131,2] = PET_Data_SUVR[(((ROI_Data==1016) | (ROI_Data==1007) | (ROI_Data==1013) | (ROI_Data==18)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[131,3] = PET_Data_SUVR[(((ROI_Data==1016) | (ROI_Data==1007) | (ROI_Data==1013) | (ROI_Data==18)) & (WM_Data==0)).nonzero()].std()
	
	RegionalPetUptake[132,0] = 132
	RegionalPetUptake[132,1] = ((ROI_Data==2016) | (ROI_Data==2007) | (ROI_Data==2013) | (ROI_Data==54)).sum()
	RegionalPetUptake[132,2] = PET_Data_SUVR[(((ROI_Data==2016) | (ROI_Data==2007) | (ROI_Data==2013) | (ROI_Data==54)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[132,3] = PET_Data_SUVR[(((ROI_Data==2016) | (ROI_Data==2007) | (ROI_Data==2013) | (ROI_Data==54)) & (WM_Data==0)).nonzero()].std()

	RegionalPetUptake[133,0] = 133
	RegionalPetUptake[133,1] = ((ROI_Data==1009) | (ROI_Data==1015) | (ROI_Data==1033) | (ROI_Data==10) | (ROI_Data==1002) | (ROI_Data==1026) | (ROI_Data==1010) | (ROI_Data==1023) | (ROI_Data==1035)).sum()
	RegionalPetUptake[133,2] = PET_Data_SUVR[(((ROI_Data==1009) | (ROI_Data==1015) | (ROI_Data==1033) | (ROI_Data==10) | (ROI_Data==1002) | (ROI_Data==1026) | (ROI_Data==1010) | (ROI_Data==1023) | (ROI_Data==1035)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[133,3] = PET_Data_SUVR[(((ROI_Data==1009) | (ROI_Data==1015) | (ROI_Data==1033) | (ROI_Data==10) | (ROI_Data==1002) | (ROI_Data==1026) | (ROI_Data==1010) | (ROI_Data==1023) | (ROI_Data==1035)) & (WM_Data==0)).nonzero()].std()
	
	RegionalPetUptake[134,0] = 134
	RegionalPetUptake[134,1] = ((ROI_Data==2009) | (ROI_Data==2015) | (ROI_Data==2033) | (ROI_Data==49) | (ROI_Data==2002) | (ROI_Data==2026) | (ROI_Data==2010) | (ROI_Data==2023) | (ROI_Data==2035)).sum()
	RegionalPetUptake[134,2] = PET_Data_SUVR[(((ROI_Data==2009) | (ROI_Data==2015) | (ROI_Data==2033) | (ROI_Data==49) | (ROI_Data==2002) | (ROI_Data==2026) | (ROI_Data==2010) | (ROI_Data==2023) | (ROI_Data==2035)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[134,3] = PET_Data_SUVR[(((ROI_Data==2009) | (ROI_Data==2015) | (ROI_Data==2033) | (ROI_Data==49) | (ROI_Data==2002) | (ROI_Data==2026) | (ROI_Data==2010) | (ROI_Data==2023) | (ROI_Data==2035)) & (WM_Data==0)).nonzero()].std()


	RegionalPetUptake[135,0] = 135
	RegionalPetUptake[135,1] = ((ROI_Data==1028) | (ROI_Data==1029) | (ROI_Data==1008) | (ROI_Data==1011) | (ROI_Data==1034) | (ROI_Data==1030) | (ROI_Data==1025) | (ROI_Data==26) | (ROI_Data==11) | (ROI_Data==12)).sum()
	RegionalPetUptake[135,2] = PET_Data_SUVR[(((ROI_Data==1028) | (ROI_Data==1029) | (ROI_Data==1008) | (ROI_Data==1011) | (ROI_Data==1034) | (ROI_Data==1030) | (ROI_Data==1025) | (ROI_Data==26) | (ROI_Data==11) | (ROI_Data==12)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[135,3] = PET_Data_SUVR[(((ROI_Data==1028) | (ROI_Data==1029) | (ROI_Data==1008) | (ROI_Data==1011) | (ROI_Data==1034) | (ROI_Data==1030) | (ROI_Data==1025) | (ROI_Data==26) | (ROI_Data==11) | (ROI_Data==12)) & (WM_Data==0)).nonzero()].std()
	
	RegionalPetUptake[136,0] = 136
	RegionalPetUptake[136,1] = ((ROI_Data==2028) | (ROI_Data==2029) | (ROI_Data==2008) | (ROI_Data==2011) | (ROI_Data==2034) | (ROI_Data==2030) | (ROI_Data==2025) | (ROI_Data==58) | (ROI_Data==50) | (ROI_Data==51)).sum()
	RegionalPetUptake[136,2] = PET_Data_SUVR[(((ROI_Data==2028) | (ROI_Data==2029) | (ROI_Data==2008) | (ROI_Data==2011) | (ROI_Data==2034) | (ROI_Data==2030) | (ROI_Data==2025) | (ROI_Data==58) | (ROI_Data==50) | (ROI_Data==51)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[136,3] = PET_Data_SUVR[(((ROI_Data==2028) | (ROI_Data==2029) | (ROI_Data==2008) | (ROI_Data==2011) | (ROI_Data==2034) | (ROI_Data==2030) | (ROI_Data==2025) | (ROI_Data==58) | (ROI_Data==50) | (ROI_Data==51)) & (WM_Data==0)).nonzero()].std()

	RegionalPetUptake[137,0] = 137
	RegionalPetUptake[137,1] = ((ROI_Data==1024) | (ROI_Data==1022) | (ROI_Data==1017) | (ROI_Data==1005) | (ROI_Data==1021)).sum()
	RegionalPetUptake[137,2] = PET_Data_SUVR[(((ROI_Data==1024) | (ROI_Data==1022) | (ROI_Data==1017) | (ROI_Data==1005) | (ROI_Data==1021)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[137,3] = PET_Data_SUVR[(((ROI_Data==1024) | (ROI_Data==1022) | (ROI_Data==1017) | (ROI_Data==1005) | (ROI_Data==1021)) & (WM_Data==0)).nonzero()].std()
	
	RegionalPetUptake[138,0] = 138
	RegionalPetUptake[138,1] = ((ROI_Data==2024) | (ROI_Data==2022) | (ROI_Data==2017) | (ROI_Data==2005) | (ROI_Data==2021)).sum()
	RegionalPetUptake[138,2] = PET_Data_SUVR[(((ROI_Data==2024) | (ROI_Data==2022) | (ROI_Data==2017) | (ROI_Data==2005) | (ROI_Data==2021)) & (WM_Data==0)).nonzero()].mean()
	RegionalPetUptake[138,3] = PET_Data_SUVR[(((ROI_Data==2024) | (ROI_Data==2022) | (ROI_Data==2017) | (ROI_Data==2005) | (ROI_Data==2021)) & (WM_Data==0)).nonzero()].std()





	RegionNames=['lh-Cerebral-White-Matter',	'lh-Lateral-Ventricle',	'lh-Inf-Lat-Vent',	'lh-Cerebellum-White-Matter',
	'lh-Cerebellum-Cortex', 	'lh-Thalamus-Proper',	'lh-Caudate', 	'lh-Putamen',
	'lh-Pallidum',	'3rd-Ventricle',	'4rd-Ventricle',	'Brain-Stem',
	'lh-Hippocampus',	'lh-Amygdala',	'CSF',	'lh-Accumbens-area',
	'lh-VentralDC',	'lh-vessel',	'lh-choroid-plexus',	'rh-Cerebral-White-Matter',
	'rh-Lateral-Ventricle',	'rh-Inf-Lat-Vent',	'rh-Cerebellum-White-Matter',	'rh-Cerebellum-Cortex',
	'rh-Thalamus-Proper',	'rh-Caudate',	'rh-Putamen',	'rh-Pallidum',
	'rh-Hippocampus',	'rh-Amygdala',	'rh-Accumbens-area',	'rh-VentralDC',
	'rh-vessel',	'rh-choroid-plexus',	'5th-Ventricle',	'WM-hypointensities',
	'lh-WM-hypointensities',	'rh-WM-hypointensities',	'non-WM-hypointensities',	'lh-non-WM-hypointensities',
	'rh-non-WM-hypointensities',	'Optic-Chiasm',	'CC_Posterior',		'CC_Mid_Posterior',             
	'CC_Central',	'CC_Mid_Anterior',	'CC_Anterior', 'lh-unkownn',	'lh-bankssts',
	'lh-caudalanteriorcingulate',	'lh-caudalmiddlefrontal',	'lh-corpuscallosum',	'lh-cuneus',
	'lh-entorhinal',	'lh-fusiform',	'lh-inferiorparietal',	'lh-inferiortemporal',
	'lh-isthmuscingulate',	'lh-lateraloccipital',	'lh-lateralorbitofrontal',	'lh-lingual',
	'lh-medialorbitofrontal',	'lh-middletemporal',	'lh-parahippocampal',	'lh-paracentral',
	'lh-parsopercularis',	'lh-parsorbitalis',	'lh-parstriangularis',	'lh-pericalcarine',
	'lh-postcentral',	'lh-posteriorcingulate',	'lh-precentral',	'lh-precuneus',
	'lh-rostralanteriorcingulate',	'lh-rostralmiddlefrontal',	'lh-superiorfrontal',	'lh-superiorparietal',
	'lh-superiortemporal',	'lh-supramarginal',	'lh-frontalpole',	'lh-temporalpole',
	'lh-transversetemporal',	'lh-insula', 'rh-unkownn',	'rh-bankssts', 	'rh-caudalanteriorcingulate',
	'rh-caudalmiddlefrontal',	'rh-corpuscallosum',	'rh-cuneus',	'rh-entorhinal',
	'rh-fusiform',	'rh-inferiorparietal',	'rh-inferiortemporal',	'rh-isthmuscingulate',
	'rh-lateraloccipital',	'rh-lateralorbitofrontal',	'rh-lingual',	'rh-medialorbitofrontal',
	'rh-middletemporal',	'rh-parahippocampal',	'rh-paracentral',	'rh-parsopercularis',
	'rh-parsorbitalis',	'rh-parstriangularis',	'rh-pericalcarine',	'rh-postcentral',
	'rh-posteriorcingulate',	'rh-precentral',	'rh-precuneus',	'rh-rostralanteriorcingulate',
	'rh-rostralmiddlefrontal',	'rh-superiorfrontal',	'rh-superiorparietal',	'rh-superiortemporal',
	'rh-supramarginal',	'rh-frontalpole',	'rh-temporalpole',	'rh-transversetemporal',
	'rh-insula',	'temporal_l_lobe',	'temporal_r_lobe',	'parietal_l_lobe', 
	'parietal_r_lobe', 	'cingulate_l_lobe', 	'cingulate_r_lobe', 	'frontal_l_lobe', 	'frontal_r_lobe',
	'lh_BraakStage1', 'rh_BraakStage1', 'lh_BraakStage2', 'rh_BraakStage2', 'lh_BraakStage3', 'rh_BraakStage3', 
	'lh_BraakStage4', 'rh_BraakStage4', 'lh_BraakStage5', 'rh_BraakStage5', 'lh_BraakStage6', 'rh_BraakStage6']
	
	# Convert the numpy array to list to insert the name strings
	ListOfRegionalPetUptake = RegionalPetUptake.tolist()
	for i in range(len(ListOfRegionalPetUptake)):
		ListOfRegionalPetUptake[i][0] = RegionNames[i]
	
	# Add a first line as the header of the columns
	ListOfRegionalPetUptake.insert(0,['RegionName', 'Volume', 'MeanUptake', 'StdUptake'])
	
	
	with open(OutputDir + '/RegionalVolumeAndTauUptakeStats.csv', "wb") as f:
		writer = csv.writer(f)
		writer.writerows(ListOfRegionalPetUptake)
    
    
    
	#np.save(OutputDir + '/RegionalVolumeAndAmyloidAndUptakeStats.csv')


