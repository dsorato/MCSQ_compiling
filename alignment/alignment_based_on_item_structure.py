import pandas as pd
import numpy as np
import sys
import os
import math
from difflib import SequenceMatcher



# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()

# def get_country_and_language(df, language):
# 	unique_survey_item_ids = df.survey_item_ID.unique()
# 	unique_country_language = []
# 	for u in unique_survey_item_ids:
# 		get_country = u.split(language+'_')[1]
# 		country = get_country.split('_')[0]
# 		country_language = language+'_'+country
# 		if country_language not in unique_country_language:
# 			unique_country_language.append(country_language)

# 	return unique_country_language

# def filter_dataframe_by_round(df, study):
# 	return df[df['Study'].str.contains(study)]

# def filter_eng_version(df, eng):
# 	return df[df['survey_item_ID'].str.contains(eng)]



# def filter_by_item_name(df_source, df_target):
# 	return pd.concat([df_source, df_target], sort=False)
# 	# return pd.merge(df_source, df_target, on = 'item_name')



# def align_more_segments_in_source(df, df_source, df_target, target_language):
# 	for i, irow in df_source.iterrows():
# 		for j, jrow in df_target.iterrows():
# 			if jrow[target_language] not in df['target'].unique() and irow['ENG_SOURCE'] not in df['source'].unique():
# 				div = len(irow['ENG_SOURCE'].split(' '))/len(jrow[target_language].split(' '))
# 				if div >= 0.5 and 1.2 > div:
# 					data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
# 						'source':irow['ENG_SOURCE'], 'target':jrow[target_language], 'item_value': None,
# 						'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': jrow['survey_item_ID']}
# 					df = df.append(data, ignore_index=True)

# 	for i, irow in df_source.iterrows():
# 		for j, jrow in df_target.iterrows():
# 			if jrow[target_language] not in df['target'].unique() and irow['ENG_SOURCE'] not in df['source'].unique():
# 				data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
# 					'source':irow['ENG_SOURCE'], 'target':jrow[target_language], 'item_value': None,
# 					'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': jrow['survey_item_ID']}
# 				df = df.append(data, ignore_index=True)
	
# 	for i, irow in df_source.iterrows():
# 		if irow['ENG_SOURCE'] not in df['source'].unique():
# 			data = {'item_name': irow['item_name'], 'item_type':irow['item_type'], 
# 			'source':irow['ENG_SOURCE'], 'target':None, 'item_value': None,
# 			'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': None}
# 			df = df.append(data, ignore_index=True)

# 	return df

# def align_more_segments_in_target(df, df_source, df_target, target_language):
# 	for i, irow in df_target.iterrows():
# 		for j, jrow in df_source.iterrows():
# 			if irow[target_language] not in df['target'].unique() and jrow['ENG_SOURCE'] not in df['source'].unique():
# 				div = len(jrow['ENG_SOURCE'].split(' '))/len(irow[target_language].split(' '))
# 				if div >= 0.5 and 1.2 > div:
# 					data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
# 					'source': jrow['ENG_SOURCE'], 'target':irow[target_language], 'item_value': None,
# 					'source_survey_itemID': jrow['survey_item_ID'], 'target_survey_itemID': irow['survey_item_ID']}
# 					df = df.append(data, ignore_index=True)

# 	for i, irow in df_target.iterrows():
# 		for j, jrow in df_source.iterrows():
# 			if irow[target_language] not in df['target'].unique() and jrow['ENG_SOURCE'] not in df['source'].unique():
# 				data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
# 				'source': jrow['ENG_SOURCE'], 'target':irow[target_language], 'item_value': None,
# 				'source_survey_itemID': jrow['survey_item_ID'], 'target_survey_itemID': irow['survey_item_ID']}
# 				df = df.append(data, ignore_index=True)
	
# 	for i, irow in df_target.iterrows():
# 		if irow[target_language] not in df['target'].unique():
# 			data = {'item_name': irow['item_name'], 'item_type':irow['item_type'], 
# 			'source':None, 'target':irow[target_language], 'item_value': None,
# 			'source_survey_itemID': None, 'target_survey_itemID': irow['survey_item_ID']}
# 			df = df.append(data, ignore_index=True)


# 	return df
# def align_responses(df_source, df_target, target_language, item_type):
# 	df = pd.DataFrame(columns=['item_name', 'item_type', 'source', 'target', 'item_value', 
# 		'source_survey_itemID', 'target_survey_itemID'])
# 	df_source = df_source[df_source['item_type']==item_type]
# 	df_target = df_target[df_target['item_type']==item_type]

# 	for i, irow in df_source.iterrows():
# 		for j, jrow in df_target.iterrows():
# 			if jrow['item_type'] == irow['item_type'] and jrow['item_name'] == irow['item_name']:
# 				if jrow['item_type'] == 'RESPONSE':
# 					value_i, value_j = cast_item_value(irow['item_value'], jrow['item_value'])
# 					if value_j == value_i and jrow[target_language] not in df['target'].unique() and irow['ENG_SOURCE'] not in df['source'].unique():
# 						data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
# 						'source':irow['ENG_SOURCE'], 'target':jrow[target_language], 'item_value': jrow['item_value'], 
# 						'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': jrow['survey_item_ID']}
# 						df = df.append(data, ignore_index=True)

# 	return df

# def align_remaining(df_source, df_target, target_language, item_type):
# 	df = pd.DataFrame(columns=['item_name', 'item_type', 'source', 'target', 'item_value', 
# 		'source_survey_itemID', 'target_survey_itemID'])
# 	df_source = df_source[df_source['item_type']==item_type]
# 	df_target = df_target[df_target['item_type']==item_type]

# 	if df_source.empty:
# 		for i,row in df_target.iterrows():
# 			data = {'item_name': row['item_name'], 'item_type':row['item_type'], 
# 					'source':None, 'target':row[target_language], 'item_value': None,
# 					'source_survey_itemID': None, 'target_survey_itemID': row['survey_item_ID']}
# 			df = df.append(data, ignore_index=True)
# 		return df
# 	if df_target.empty:
# 		for i,row in df_source.iterrows():
# 			data = {'item_name': row['item_name'], 'item_type':row['item_type'], 
# 					'source':row['ENG_SOURCE'], 'target':None, 'item_value': None,
# 					'source_survey_itemID': row['survey_item_ID'], 'target_survey_itemID': None}
# 			df = df.append(data, ignore_index=True)
# 		return df
# 	else:
# 		if len(df_source)> len(df_target):
# 			df = align_more_segments_in_source(df, df_source, df_target, target_language)

# 		elif len(df_target)> len(df_source):
# 			df = align_more_segments_in_target(df, df_source, df_target, target_language)
# 		else:
# 			for i, irow in df_source.iterrows():
# 				for j, jrow in df_target.iterrows():
# 					if  jrow['item_name'] == irow['item_name']:
# 						if jrow[target_language] not in df['target'].unique() and irow['ENG_SOURCE'] not in df['source'].unique():
# 								data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
# 								'source':irow['ENG_SOURCE'], 'target':jrow[target_language], 'item_value': None,
# 								'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': jrow['survey_item_ID']}
# 								df = df.append(data, ignore_index=True)



# 	return df


# def cast_item_value(value_i, value_j):
# 	if isinstance(value_i, float) and math.isnan(value_i) == False:
# 		value_i = int(value_i)
# 	if isinstance(value_j, float) and math.isnan(value_j) == False:
# 		value_j = int(value_j)

# 	value_i = str(value_i)
# 	value_j = str(value_j)

# 	return value_i, value_j




def align_on_metadata(df, df_source, df_target):

	df_introduction = align_remaining(df1, df2, target_language, 'INTRODUCTION')
	df = df.append(df_introduction, ignore_index=True)
	df_instruction = align_remaining(df1, df2, target_language, 'INSTRUCTION')
	df = df.append(df_instruction, ignore_index=True)
	df_request = align_remaining(df1, df2, target_language, 'REQUEST')
	df = df.append(df_request, ignore_index=True)
	df_response = align_responses(df1, df2, target_language, 'RESPONSE')
	df = df.append(df_response, ignore_index=True)

	return df


"""
Filters the source and target dataframes by the module that is being currently analyzed.

Args:
	param1 df_source (pandas dataframe): dataframe containing the data of the source questionnaire (always English).
	param2 df_target (pandas dataframe): dataframe containing the data of the target questionnaire
	param3 module (string): questionnaire module being currently analyzed in outer loop.

Returns:
	df_source (pandas dataframe) and param2 df_target (pandas dataframe). Source and target dataframes filtered
	by the module specified by parameter.
"""
def filter_by_module(df_source, df_target, module):
	df_source = df_source[df_source['module']==module]
	df_target = df_target[df_target['module']==module]

	return df_source, df_target
				
"""
Get study metadata embedded in filename. It can be retrieved either from 
the source or the target file.

Args:
	param1 filename (string): name of either source or target file.

Returns:
	study (string). Metadata that identifies the study of the questionnaires that are being aligned.
"""
def get_study_metadata(filename):
	filename = filename.split('_')
	study = filename[0]+'_'+filename[1]+'_'+filename[2]
	
	return study

"""
Get target language/country metadata embedded in filename, to name the output aligned file.

Args:
	param1 filename (string): name of target file.

Returns:
	target_language_country (string). Metadata that identifies the language/country of the target questionnaire being aligned.
"""
def get_target_language_country_metadata(filename):
	filename_without_extension = filename.replace('.csv', '')
	filename_without_extension = filename_without_extension.split('_')
	target_language_country = filename[3]+'_'+filename[4]
	
	return target_language_country

def main(folder_path, filename_source, filename_target):
	path = os.chdir(folder_path)
	df_source = pd.read_csv(filename_source)
	df_target = pd.read_csv(filename_target)

	df = pd.DataFrame(columns=['source_survey_itemID', 'target_survey_itemID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 
		'source_text', 'target_text'])

	study = get_study_metadata(filename_source)
	target_language_country = get_target_language_country_metadata(filename_target)

	if 'EVS' in study:
		source_language_country = 'ENG_GB'
	else:
		source_language_country = 'ENG_SOURCE'

	"""
	Computes the intersection between the modules of source and target questionnaires.
	We are only interested in aligning modules that are present in both files.
	"""
	intersection_modules = set(df_source.module.unique()).intersection(set(df_target.module.unique()))
	for module in sorted(intersection_modules):
		df_source_filtered, df_target_filtered = filter_by_module(df_source, df_target, module)
		
		unique_item_names_source = df_source_filtered.item_name.unique()
		unique_item_names_target = df_target_filtered.item_name.unique()
		for unique in unique_item_name_source:
			print(unique)
			"""
			Computes the intersection between the item names of source and target questionnaires.
			We are only interested in aligning questions that are present in both files.
			"""
			df_source_by_item_name = df_source_filtered[df_source_filtered['item_name'].lower()==unique.lower()]
			df_target_by_item_name = df_target_filtered[df_target_filtered['item_name'].lower()==unique.lower()]
			
			if df_target_by_item_name.empty == False and df_source_by_item_name.empty == False:
				df = align_on_metadata(df, df_source_by_item_name, df_target_by_item_name)
				
	
	df.to_csv(source_language_country+'_'+target_language_country+'_'+study+'.csv', encoding='utf-8', index=False)
	




if __name__ == "__main__":
	#Call script using the filenames of two files that should be aligned 
	#python3 alignment_based_on_item_structure.py ./test_data/ESS_R01_2002_ENG_SOURCE.csv ./test_data/ESS_R01_2002_CAT_ES.csv 
	filename_source= str(sys.argv[1])
	filename_target = str(sys.argv[2])
	main(filename_source,filename_target)
