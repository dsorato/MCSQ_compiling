import pandas as pd
import numpy as np
import sys
import os
from countryspecificrequest import *
import math
from difflib import SequenceMatcher



# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()


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
#  	return df



"""
Aligns introduction, instruction and requests segments. Differently from response segments, these other item types can't be
merged. There are five distinct cases to consider: 1) only source segments (df_target is empty), 2) only target segments (df_source is empty),
3) df_source has more segments than df_target 4) df_target has more segments than df_source and, 5) df_source and df_target have the 
same number of segments.

Args:
	param1 df (pandas dataframe): dataframe to store the questionnaire alignment
	param2 df_source (pandas dataframe): dataframe containing the data of the source questionnaire (always English).
	param3 df_target (pandas dataframe): dataframe containing the data of the target questionnaire
	param4 item_type (string): metadata that indicates if the dataframes contain introductions, instructions or requests.

Returns:
	df (pandas dataframe) with newly aligned survey item segments.
"""
def align_introduction_instruction_request(df, df_source, df_target, item_type):
	df_source = df_source[df_source['item_type']==item_type]
	df_target = df_target[df_target['item_type']==item_type]

	if df_source.empty:
		for i,row in df_target.iterrows():
			data = {'source_survey_itemID': None, 'target_survey_itemID': row['survey_item_ID'], 'Study': row['Study'], 
			'module': row['module'], 'item_type': item_type, 'item_name':row['item_name'], 'item_value': None, 
			'source_text': None, 'target_text': row['text']}
			df = df.append(data, ignore_index=True)
		return df

	if df_target.empty:
		for i,row in df_source.iterrows():
			data = {'source_survey_itemID': row['survey_item_ID'], 'target_survey_itemID': None , 'Study': row['Study'], 
			'module': row['module'], 'item_type': item_type, 'item_name':row['item_name'], 'item_value': None, 
			'source_text': row['text'], 'target_text': None}
			df = df.append(data, ignore_index=True)
		return df
	else:
		list_target = df_target.values.tolist()
		list_source = df_source.values.tolist()

		if len(list_source) > len(df_target):
			pass
			# df = align_more_segments_in_source(df, df_source, df_target, target_language)

		elif len(list_target) > len(list_source):
			pass
			# df = align_more_segments_in_target(df, df_source, df_target, target_language)
		elif len(list_target) == len(list_source):
			
			for i, item in enumerate(list_source):
				print(item, item[0],  list_target[i][0])
				data = {'source_survey_itemID': item[0], 'target_survey_itemID': list_target[i][0] , 'Study': item[1], 
				'module': item[2], 'item_type': item_type, 'item_name':item[4], 'item_value': None, 
				'source_text': item[6], 'target_text':  list_target[i][6]}
				df = df.append(data, ignore_index=True)

						


	return df

"""
Aligns response segments by merging them on item_value metadata.
Args:
	param1 df (pandas dataframe): dataframe to store the questionnaire alignment
	param2 df_source (pandas dataframe): dataframe containing the data of the source questionnaire (always English).
	param3 df_target (pandas dataframe): dataframe containing the data of the target questionnaire

Returns:
	df (pandas dataframe) with newly aligned response segments.
"""
def align_responses(df, df_source, df_target):
	df_source = df_source[df_source['item_type']=='RESPONSE']
	df_target = df_target[df_target['item_type']=='RESPONSE']

	df_merge = pd.merge(df_source, df_target, on='item_value')

	for i, row in df_merge.iterrows():
		data = {'source_survey_itemID': row['survey_item_ID_x'], 'target_survey_itemID':  row['survey_item_ID_y'], 'Study': row['Study_x'], 
		'module': row['module_x'], 'item_type': 'RESPONSE', 'item_name':row['item_name_x'], 'item_value': row['item_value'], 
		'source_text': row['text_x'], 'target_text': row['text_y']}
		df = df.append(data, ignore_index=True)

	return df

"""
Calls the appropriate method for alignment based on metadata.
Responses are aligned separately of other item types because answers are merged using the item value.
Args:
	param1 df (pandas dataframe): dataframe to store the questionnaire alignment
	param2 df_source (pandas dataframe): dataframe containing the data of the source questionnaire (always English).
	param3 df_target (pandas dataframe): dataframe containing the data of the target questionnaire
	param4 process_responses (boolean): indicates if the response segments should be processed, country-specific answers are excluded by design. 

Returns:
	df (pandas dataframe) with newly aligned survey items.
"""
def align_on_metadata(df, df_source, df_target, process_responses):

	df = align_introduction_instruction_request(df, df_source, df_target, 'INTRODUCTION')
	df = align_introduction_instruction_request(df, df_source, df_target, 'INSTRUCTION')
	df = align_introduction_instruction_request(df, df_source, df_target, 'REQUEST')
	if process_responses:
		df = align_responses(df, df_source, df_target)
	

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
	target_language_country = filename_without_extension[3]+'_'+filename_without_extension[4]
	
	return target_language_country

"""
Instantiates the appropriate set of country-specific requests according to the study.
Country-specific requests are deleted from alignment by design because the answer categories
frequently change from country to country.

Args:
	param1 study (string): study metadata, embedded in filenames.

Returns:
	country_specific_requests (Python object). Instance of python object that encapsulates the item names of 
	teh country specific questions.
"""
def instantiate_country_specific_request_object(study):
	if 'ESS_R01' in study:
		country_specific_requests = ESSCountrySpecificR01()

	return country_specific_requests



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


	country_specific_requests = instantiate_country_specific_request_object(study)

	"""
	Computes the intersection between the modules of source and target questionnaires.
	We are only interested in aligning modules that are present in both files.
	"""
	intersection_modules = set(df_source.module.unique()).intersection(set(df_target.module.unique()))
	for module in sorted(intersection_modules):
		df_source_filtered, df_target_filtered = filter_by_module(df_source, df_target, module)
		
		unique_item_names_source = df_source_filtered.item_name.unique()
		unique_item_names_target = df_target_filtered.item_name.unique()
		
		for unique_item_name in unique_item_names_source:
			process_responses = True
			if unique_item_name.lower() in country_specific_requests.item_names:
				process_responses = False
			"""
			Computes the intersection between the item names of source and target questionnaires.
			We are only interested in aligning questions that are present in both files.
			"""
			df_source_by_item_name = df_source_filtered[df_source_filtered['item_name'].str.lower()==unique_item_name.lower()]
			df_target_by_item_name = df_target_filtered[df_target_filtered['item_name'].str.lower()==unique_item_name.lower()]
			
			if df_target_by_item_name.empty == False and df_source_by_item_name.empty == False:
				df = align_on_metadata(df, df_source_by_item_name, df_target_by_item_name, process_responses)
				
	
	df.to_csv(source_language_country+'_'+target_language_country+'_'+study+'.csv', encoding='utf-8', index=False)
	




if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	filename_source = str(sys.argv[2])
	filename_target = str(sys.argv[3])
	main(folder_path, filename_source,filename_target)
