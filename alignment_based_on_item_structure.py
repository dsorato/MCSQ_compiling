import pandas as pd
import numpy as np
import sys
import os
from populate_tables import *
from retrieve_from_tables import *
import math


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

def align_responses():
	df = pd.DataFrame(columns=['item_name', 'item_type', 'source', 'target', 'item_value'])
	for i, irow in df1.iterrows():
		for j, jrow in df2.iterrows():
			if jrow['item_value'] == irow['item_value']:
					data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
					'source':irow['ENG_SOURCE'], 'target':jrow['NOR_NO'], 'item_value': jrow['item_value']}
					df = df.append(data, ignore_index=True)

	return df

def align_requests(df_source, df_target):
	df = pd.DataFrame(columns=['item_name', 'item_type', 'source', 'target', 'item_value'])
	if df_source.empty():
		for i,row in df_target.iterrows():
			data = {'item_name': row['item_name'], 'item_type':row['item_type'], 
					'source':None, 'target':row['NOR_NO'], 'item_value': None}
			df = df.append(data, ignore_index=True)
	if df_target.empty():
		for i,row in df_source.iterrows():
			data = {'item_name': row['item_name'], 'item_type':row['item_type'], 
					'source':row['NOR_NO'], 'target':None, 'item_value': None}
			df = df.append(data, ignore_index=True)

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
	for i, irow in df1.iterrows():
		for j, jrow in df2.iterrows():
			if jrow['item_type'] == irow['item_type']:
				if jrow['item_type'] == 'RESPONSE':
					value_i, value_j = cast_item_value(irow['item_value'], jrow['item_value'])
					if value_j == value_i and jrow[target_language] not in df['target'].unique():
						data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
						'source':irow['ENG_SOURCE'], 'target':jrow[target_language], 'item_value': jrow['item_value'], 
						'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': jrow['survey_item_ID']}
						df = df.append(data, ignore_index=True)
					
				elif jrow['item_type'] == 'REQUEST' or jrow['item_type'] == 'INTRO' or jrow['item_type'] == 'INTRODUCTION':
					if jrow[target_language] not in df['target'].unique() and irow['ENG_SOURCE'] not in df['source'].unique():
						data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
						'source':irow['ENG_SOURCE'], 'target':jrow[target_language], 'item_value': None,
						'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': jrow['survey_item_ID']}
						df = df.append(data, ignore_index=True)

				else:
					if irow['ENG_SOURCE'] not in df['source'].unique():
						data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
						'source':irow['ENG_SOURCE'], 'target':jrow[target_language], 'item_value': None,
						'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': jrow['survey_item_ID']}
						df = df.append(data, ignore_index=True)
					else:
						if jrow[target_language] not in df['target'].unique():
							data = {'item_name':jrow['item_name'], 'item_type':jrow['item_type'], 
							'source':None, 'target':jrow[target_language], 'item_value': None,
							'source_survey_itemID': irow['survey_item_ID'], 'target_survey_itemID': jrow['survey_item_ID']}
							df = df.append(data, ignore_index=True)

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
