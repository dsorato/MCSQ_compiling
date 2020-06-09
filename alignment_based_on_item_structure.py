import pandas as pd
import numpy as np
import sys
import os
from populate_tables import *
from retrieve_from_tables import *
import math
from difflib import SequenceMatcher



def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_country_and_language(df, language):
	unique_survey_item_ids = df.survey_item_ID.unique()
	unique_country_language = []
	for u in unique_survey_item_ids:
		get_country = u.split(language+'_')[1]
		country = get_country.split('_')[0]
		country_language = language+'_'+country
		if country_language not in unique_country_language:
			unique_country_language.append(country_language)

	return unique_country_language

def filter_dataframe_by_round(df, study):
	return df[df['Study'].str.contains(study)]

def filter_eng_version(df, eng):
	return df[df['survey_item_ID'].str.contains(eng)]

def filter_by_module(df_source, df_target, module):
	df_source = df_source[df_source['module']==module]
	df_target = df_target[df_target['module']==module]

	return df_source, df_target

def filter_by_item_name(df_source, df_target):
	return pd.concat([df_source, df_target], sort=False)
	# return pd.merge(df_source, df_target, on = 'item_name')



def align_more_segments_in_source(df, df_source, df_target, target_language):
	not_appended_data = pd.DataFrame(columns=['item_name', 'item_type', 'source', 'target', 'item_value', 
	'source_survey_itemID', 'target_survey_itemID'])

	for i, irow in df_source.iterrows():
		for j, jrow in df_target.iterrows():
			if jrow[target_language] not in df['target'].unique() and irow['ENG_SOURCE'] not in df['source'].unique():
				div = len(irow['ENG_SOURCE'].split(' '))/len(jrow[target_language].split(' '))
				if div >= 0.4 and 1.5 > div :
					data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
						'source':irow['ENG_SOURCE'], 'target':jrow[target_language], 'item_value': None,
						'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': jrow['survey_item_ID']}
					df = df.append(data, ignore_index=True)
	
	for i, irow in df_source.iterrows():
		if irow['ENG_SOURCE'] not in df['source'].unique():
			data = {'item_name': irow['item_name'], 'item_type':irow['item_type'], 
			'source':irow['ENG_SOURCE'], 'target':None, 'item_value': None,
			'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': None}
			df = df.append(data, ignore_index=True)

	return df

def align_more_segments_in_target(df, df_source, df_target, target_language):
	for i, irow in df_target.iterrows():
		for j, jrow in df_source.iterrows():
			if irow[target_language] not in df['target'].unique() and jrow['ENG_SOURCE'] not in df['source'].unique():
				div = len(jrow['ENG_SOURCE'].split(' '))/len(irow[target_language].split(' '))
				if div >= 0.4 and 1.5 > div :
					data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
					'source': jrow['ENG_SOURCE'], 'target':irow[target_language], 'item_value': None,
					'source_survey_itemID': jrow['survey_item_ID'], 'target_survey_itemID': irow['survey_item_ID']}
					df = df.append(data, ignore_index=True)
	
	for i, irow in df_target.iterrows():
		if irow[target_language] not in df['target'].unique():
			data = {'item_name': irow['item_name'], 'item_type':irow['item_type'], 
			'source':None, 'target':irow[target_language], 'item_value': None,
			'source_survey_itemID': None, 'target_survey_itemID': irow['survey_item_ID']}
			df = df.append(data, ignore_index=True)


	return df
def align_responses(df_source, df_target, target_language, item_type):
	df = pd.DataFrame(columns=['item_name', 'item_type', 'source', 'target', 'item_value', 
		'source_survey_itemID', 'target_survey_itemID'])
	df_source = df_source[df_source['item_type']==item_type]
	df_target = df_target[df_target['item_type']==item_type]

	for i, irow in df_source.iterrows():
		for j, jrow in df_target.iterrows():
			if jrow['item_type'] == irow['item_type'] and jrow['item_name'] == irow['item_name']:
				if jrow['item_type'] == 'RESPONSE':
					value_i, value_j = cast_item_value(irow['item_value'], jrow['item_value'])
					if value_j == value_i and jrow[target_language] not in df['target'].unique() and irow['ENG_SOURCE'] not in df['source'].unique():
						data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
						'source':irow['ENG_SOURCE'], 'target':jrow[target_language], 'item_value': jrow['item_value'], 
						'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': jrow['survey_item_ID']}
						df = df.append(data, ignore_index=True)

	return df

def align_remaining(df_source, df_target, target_language, item_type):
	df = pd.DataFrame(columns=['item_name', 'item_type', 'source', 'target', 'item_value', 
		'source_survey_itemID', 'target_survey_itemID'])
	df_source = df_source[df_source['item_type']==item_type]
	df_target = df_target[df_target['item_type']==item_type]

	if df_source.empty:
		for i,row in df_target.iterrows():
			data = {'item_name': row['item_name'], 'item_type':row['item_type'], 
					'source':None, 'target':row[target_language], 'item_value': None,
					'source_survey_itemID': None, 'target_survey_itemID': row['survey_item_ID']}
			df = df.append(data, ignore_index=True)
		return df
	if df_target.empty:
		for i,row in df_source.iterrows():
			data = {'item_name': row['item_name'], 'item_type':row['item_type'], 
					'source':row['ENG_SOURCE'], 'target':None, 'item_value': None,
					'source_survey_itemID': row['survey_item_ID'], 'target_survey_itemID': None}
			df = df.append(data, ignore_index=True)
		return df
	else:
		if len(df_source)> len(df_target):
			df = align_more_segments_in_source(df, df_source, df_target, target_language)

		elif len(df_target)> len(df_source):
			df = align_more_segments_in_target(df, df_source, df_target, target_language)
		else:
			for i, irow in df_source.iterrows():
				for j, jrow in df_target.iterrows():
					if  jrow['item_name'] == irow['item_name']:
						if jrow[target_language] not in df['target'].unique() and irow['ENG_SOURCE'] not in df['source'].unique():
							div = len(irow['ENG_SOURCE'].split(' '))/len(jrow[target_language].split(' '))
							if div >= 0.6 and 1.5 > div :
								data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
								'source':irow['ENG_SOURCE'], 'target':jrow[target_language], 'item_value': None,
								'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': jrow['survey_item_ID']}
								df = df.append(data, ignore_index=True)

			# if jrow[target_language] not in df['target'].unique():
			# 	data = {'item_name': jrow['item_name'], 'item_type':jrow['item_type'], 
			# 	'source':None, 'target':jrow[target_language], 'item_value': None,
			# 	'source_survey_itemID': None, 'target_survey_itemID': jrow['survey_item_ID']}
			# 	df = df.append(data, ignore_index=True)
			# if irow['ENG_SOURCE'] not in df['source'].unique():
			# 	# if len(irow['ENG_SOURCE'].split(' '))> len(jrow[target_language].split(' ')):
			# 	data = {'item_name': irow['item_name'], 'item_type':irow['item_type'], 
			# 	'source':irow['ENG_SOURCE'], 'target':None, 'item_value': None,
			# 	'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': None}
			# 	df = df.append(data, ignore_index=True)



	return df




def cast_item_value(value_i, value_j):
	if isinstance(value_i, float) and math.isnan(value_i) == False:
		value_i = int(value_i)
	if isinstance(value_j, float) and math.isnan(value_j) == False:
		value_j = int(value_j)

	value_i = str(value_i)
	value_j = str(value_j)

	return value_i, value_j


def align_on_meta(df1, df2, target_language):
	df = pd.DataFrame(columns=['item_name', 'item_type', 'source', 'target', 'item_value', 
		'source_survey_itemID', 'target_survey_itemID'])

	df_introduction = align_remaining(df1, df2, target_language, 'INTRODUCTION')
	df = df.append(df_introduction, ignore_index=True)
	df_instruction = align_remaining(df1, df2, target_language, 'INSTRUCTION')
	df = df.append(df_instruction, ignore_index=True)
	df_request = align_remaining(df1, df2, target_language, 'REQUEST')
	df = df.append(df_request, ignore_index=True)
	df_response = align_responses(df1, df2, target_language, 'RESPONSE')
	df = df.append(df_response, ignore_index=True)

	return df
				


def main(filename_source, filename_target, study_round, target_country_language):
	df_source = pd.read_csv(filename_source)
	df_target = pd.read_csv(filename_target)

	target_language = filename_target.replace('.csv', '')
	target_language = target_language.split('/')[-1]

	filtered_df_source = filter_dataframe_by_round(df_source, study_round) 
	filtered_df_target = filter_dataframe_by_round(df_target, study_round) 
	filtered_df_eng_source = filter_eng_version(filtered_df_source, 'ENG_SOURCE')
	if target_language == 'GER':
		filtered_df_target = filter_eng_version(filtered_df_target, target_country_language)
	if target_language == 'FRE':
		filtered_df_target = filter_eng_version(filtered_df_target, target_country_language)
	if target_language == 'RUS':
		filtered_df_target = filter_eng_version(filtered_df_target, target_country_language)
	if target_language == 'ENG':
		filtered_df_target = filter_eng_version(filtered_df_target, target_country_language)

	intersection_modules = set(filtered_df_eng_source.module.unique()).intersection(set(filtered_df_target.module.unique()))

	df = pd.DataFrame(columns=['item_name', 'item_type', 'source', 'target', 'item_value'])
	for module in intersection_modules:
		df_source, df_target = filter_by_module(filtered_df_eng_source, filtered_df_target, module)
		unique_item_name_source = df_source.item_name.unique()
		unique_item_name_target = df_target.item_name.unique()
		for unique in unique_item_name_source:
			df_source_by_item_name = df_source[df_source['item_name']==unique]
			df_target_by_item_name = df_target[df_target['item_name']==unique]
			if df_target_by_item_name.empty == False and df_source_by_item_name.empty == False:
				alignment = align_on_meta(df_source_by_item_name, df_target_by_item_name, target_language)
				df = df.append(alignment, ignore_index=True)
	
	df.to_csv('ENG-'+target_country_language+'_'+study_round+'.csv', encoding='utf-8', index=False)
	




if __name__ == "__main__":
	#Call script using the filenames of two files that should be aligned 
	#python3 alignment_based_on_item_structure.py ./test_data/ENG.csv ./test_data/ENG.csv R01 ENG_GB
	filename_source= str(sys.argv[1])
	filename_target = str(sys.argv[2])
	study_round = str(sys.argv[3])
	target_country_language = str(sys.argv[4])
	main(filename_source,filename_target, study_round, target_country_language)
