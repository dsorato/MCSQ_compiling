"""
Python3 script for dataset inclusion in the MCSQ database
Before running the script, install requirements: pandas, numpy, SQLAlchemy, psycopg2
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 
import pandas as pd
import numpy as np
import sys
import os
import re
from populate_tables import *
from retrieve_from_tables import *

"""
Gets surveyid, study, wave_round, year and country_language metadata, contained in survey_item_ID values.

Args:
	param1 survey_item_id (string): survey_item_id from survey_item_ID column contained in input csv file.

Returns: 
	surveyid (string), study (string), wave_round (string), year (string) and country_language (string) metadata.
"""
def get_metadata_from_survey_item_id(survey_item_id):
	survey_item_id_split = survey_item_id.split('_')
	surveyid = survey_item_id_split[0]+'_'+survey_item_id_split[1]+'_'+survey_item_id_split[2]+'_'+survey_item_id_split[3]+'_'+survey_item_id_split[4]
	study = survey_item_id_split[0]
	if study == 'SHA':
		study = 'SHARE'
	wave_round = survey_item_id_split[1]
	year = survey_item_id_split[2]
	country_language = survey_item_id_split[3]+'_'+survey_item_id_split[4]

	return surveyid, study, wave_round, year, country_language

"""
Prepares the data and calls write_survey_item_table() function to populate survey_item table.

Args:
	param1 df (pandas dataframe): input csv file.
	param2 df (pandas dataframe): input csv file.

"""
def populate_survey_item(df, d_surveys, d_modules, d_introductions, d_instructions, d_requests, d_responses):
	for i, row in df.iterrows():
		surveyid, study, wave_round, year, country_language = get_metadata_from_survey_item_id(row['survey_item_ID'])

		survey_id = d_surveys[surveyid]
		module_id = d_modules[row['module']]

		request_id = None
		response_id = None
		instruction_id = None
		introduction_id = None

		item_value = row['item_value']

		if row['item_type'] == 'INTRODUCTION':
			introduction_id = d_introductions[row['text']]
		elif row['item_type'] == 'INSTRUCTION':
			instruction_id = d_instructions[row['text']]
		elif row['item_type'] == 'REQUEST':
			request_id = d_requests[row['text']]
		elif row['item_type'] == 'RESPONSE':
			if isinstance(row['item_value'], str):
				if str(row['item_value'])[-2:] == '.0':
					item_value = row['item_value'][:-2]					

				response_id = d_responses[row['text']+item_value]
			else:
				response_id = d_responses[row['text']+'None']

		if country_language == 'ENG_SOURCE':
			item_is_source = True
		else:
			item_is_source = False

		write_survey_item_table(row['survey_item_ID'], surveyid, row['text'], item_value, module_id, request_id, response_id, 
			instruction_id, introduction_id, country_language, item_is_source, row['item_name'], row['item_type'])



def populate_introduction_table(df):
	df_introduction = df[df['item_type']=='INTRODUCTION']
	df_introduction = df_introduction.drop_duplicates('text')

	dictionary_introductions = dict()
	for i, row in df_introduction.iterrows(): 
		write_introduction_table(row['text'])
		introduction_id = get_introduction_id(row['text'])
		dictionary_introductions[row['text']] = introduction_id

	return dictionary_introductions

def populate_instruction_table(df):
	df_instructions = df[df['item_type']=='INSTRUCTION']
	df_instructions = df_instructions.drop_duplicates('text')

	dictionary_instructions = dict()
	for i, row in df_instructions.iterrows(): 
		write_instruction_table(row['text'])
		instruction_id = get_instruction_id(row['text'])
		dictionary_instructions[row['text']] = instruction_id

	return dictionary_instructions

def populate_request_table(df):
	df_request = df[df['item_type']=='REQUEST']
	df_request = df_request.drop_duplicates('text')

	dictionary_requests = dict()
	for i, row in df_request.iterrows(): 
		write_request_table(row['text'])
		request_id = get_request_id(row['text'])
		dictionary_requests[row['text']] = request_id

	return dictionary_requests

def populate_response_table(df):
	df_response = df[df['item_type']=='RESPONSE']

	dictionary_responses = dict()
	unique_values = []
	for i, row in df_response.iterrows():
		if [row['text'], row['item_value']] not in unique_values:
			unique_values.append([row['text'], row['item_value']])

	for value in unique_values:
		text = value[0]
		item_value = value[1]
		if isinstance(item_value, str):
			if str(item_value)[-2:] == '.0':
				item_value = item_value[:-2]

			write_response_table(text, item_value)
			response_id = get_response_id(text, item_value)
			dictionary_responses[text+item_value] = response_id
		else:
			write_response_table(text, None)
			response_id = get_response_id(text, None)
			dictionary_responses[text+'None'] = response_id




	return dictionary_responses

def populate_module_table(df):
	dictionary_modules = dict()

	unique_modules = df.module.unique()
	write_module_table(unique_modules)

	for module in unique_modules:
		module_id = get_module_id(module)
		dictionary_modules[module] =  module_id


	return dictionary_modules

def populate_survey_table(df):
	unique_studies = df.Study.unique()
	first_survey_item_id = []

	for study in unique_studies:
		for i, row in df.iterrows():
			if re.compile(study+'.*_0').match(row['survey_item_ID']):
				first_survey_item_id.append(row['survey_item_ID'])

	surveys = []
	for survey_item_id in first_survey_item_id:
		surveyid, study, wave_round, year, country_language = get_metadata_from_survey_item_id(survey_item_id)
		surveys.append([surveyid, study, wave_round, year, country_language])

	write_survey_table(surveys)

	dictionary_surveys = dict()
	for survey in surveys:
		survey_id = get_survey_id(survey[0])
		dictionary_surveys[survey[0]] = survey_id

	return dictionary_surveys

	

def concatenate_files(files, metainfo, folder_path):
	file_list = list()
	for index, file in enumerate(files):
		df = pd.read_csv(file)
		column_names = df.columns
		text = column_names[-1]
		file_list.append(df)

	all_files = pd.concat(file_list, axis=0, ignore_index=True)
	all_files.to_csv(folder_path+'/'+metainfo+".csv", index=False)


def get_directory_list(folder_path):
	directory_list = list()
	for root, dirs, files in os.walk(folder_path, topdown=False):
		for name in dirs:
			directory_list.append(os.path.join(root, name))

	return directory_list


def prepare_dataset(folder_path):
	directory_list = get_directory_list(folder_path)
	for directory in directory_list:
		metainfo = directory.split('/')[-1]
		files = os.listdir(directory)
		os.chdir(directory)
		concatenate_files(files, metainfo, folder_path)
		os.chdir(folder_path)

def main(folder_path, concatenate):
	if concatenate == 1:
		prepare_dataset(folder_path)
		
	os.chdir(folder_path)
	files = os.listdir(folder_path)
	for index, file in enumerate(files):
		if file.endswith(".csv"):
			print(file)
			language = file.replace('.csv', '')
			df = pd.read_csv(file, dtype=str)

			d_modules = populate_module_table(df)
			d_surveys = populate_survey_table(df)
			d_introductions = populate_introduction_table(df)
			d_instructions = populate_instruction_table(df)
			d_requests = populate_request_table(df)
			d_responses = populate_response_table(df)
			populate_survey_item(df, d_surveys, d_modules, d_introductions, d_instructions, d_requests, d_responses)


				

if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	concatenate = int(sys.argv[2])
	main(folder_path,concatenate)