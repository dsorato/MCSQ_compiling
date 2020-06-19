"""
Python3 script for ESS dataset inclusion in the MCSQ database
Before running the script, install requirements: pandas, numpy, SQLAlchemy, psycopg2
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 


import pandas as pd
import numpy as np
import sys
import os
from populate_tables import *
from retrieve_from_tables import *

global instruction_id 
instruction_id = 0

global request_id 
request_id = 0

global response_id 
response_id = 0

def get_response_id():
	global response_id
	return response_id

def update_response_id():
	global response_id
	response_id = response_id +1
	return response_id

def get_instuction_id():
	global instruction_id
	return instruction_id

def update_instruction_id():
	global instruction_id
	instruction_id = instruction_id +1
	return instruction_id

def get_request_id():
	global request_id
	return request_id

def update_request_id():
	global request_id
	request_id = request_id +1
	return request_id

"""
Gets the module description based on a hard-coded dictionary for a given study and round.
Some ESS modules don't change with the round, such as modules A, B, C and F.
Args:
    param1: Study
    param2: Wave/round

Returns:
    Module description
"""
def get_module_description(study, wave_round):
	#Module descriptions for ESS.
	if study == 'ESS':
		module_description = {'A': 'ESS module about Media; social trust', 'B': 'ESS module about Politics, including: political interest, efficacy, trust, electoral and other forms of participation, party allegiance, socio-political evaluations/orientations, multi-level governance',
		'C': 'ESS module about Subjective well-being and social exclusion; religion; perceived discrimination; national and ethnic identity', 'D': 'Immigration and asylum issues, including: attitudes, perceptions, policy preferences and knowledge',
		'E': 'ESS module about Citizen involvement: including organisational membership, family and friendship bonds, citizenship values, working environment', 
		'F': 'ESS module about Socio-demographic profile, including: Household composition, sex, age, type of area, Education & occupation details of respondent, partner, parents, union membership, household income, marital status',
		'SUPP_G': 'ESS Human values scale',  'SUPP_H': 'ESS Test questions', 'SUPP_I': 'ESS Interviewer questions', 'SUPP_N':'ESS National Module',
		'SUPP_A': 'ESS Supplementary questions with module A equivalents (from SQP database)', 'SUPP_B': 'ESS Supplementary questions with module B equivalents (from SQP database)',
		'SUPP_C': 'ESS Supplementary questions with module C equivalents (from SQP database)', 'SUPP_D': 'ESS Supplementary questions with module D equivalents (from SQP database)',
		'SUPP_E': 'ESS Supplementary questions with module E equivalents (from SQP database)', 'SUPP_F': 'ESS Supplementary questions with module F equivalents (from SQP database)',
		'SUPP_HF': 'ESS Human values scale','SUPP_HS': 'ESS Human values scale','SUPP_IF': 'ESS Test questions', 'SUPP_K': 'ESS Administration'}

		if wave_round == 'R02':
			module_description['D'] = 'ESS R02 module about Health and care seekin health, medicine, and doctor/patient relations'
			module_description['E'] = 'ESS R02 module about Economic morality Trust and interactions between producers and consumers'
			module_description['SUPP_G'] = 'ESS R02 module about Family Work and Wellbeing work-life balance'
			module_description['SUPP_H'] = 'ESS R02 Human values scale'
			module_description['SUPP_I'] = 'ESS R02 Test questions'
			module_description['SUPP_J'] = 'ESS R02 Interviewer self-completion questions'

		elif wave_round == 'R03':
			module_description['D'] = 'ESS R03 module about Timing of life; the life course; timing of key life events, attitudes to ideal age, youngest age and oldest age of life events, planning for retirement'
			module_description['E'] = 'ESS R03 module about Personal and social well-being, helping others, feelings in the last week, life satisfaction, satisfaction with work.'
			module_description['SUPP_I'] = 'ESS R03 module about Interviewer self-completion questions'

		
		elif wave_round == 'R04':
			module_description['D'] = 'ESS R04 module about Welfare includes attitudes towards welfare provision, size of claimant groups, views on taxation, attitudes towards service delivery and likely future dependence on welfare.'
			module_description['E'] = 'ESS R04 module about Ageism covers attitudes towards and experiences of ageism, age related status, stereotypes, experience of discrimination and contact with people in other age groups.'
			module_description['SUPP_I'] = 'ESS R04 Interviewer self-completion questions'

		elif wave_round == 'R05':
			module_description['D'] = 'ESS R05 module about Trust in the Police and Courts, including: confidence in the police and courts, cooperation with the police and courts, contact with the police and attitudes towards punishment.'
			module_description['SUPP_I'] = 'ESS R05 Interviewer self-completion questions'
			module_description['SUPP_G'] = 'ESS R05 module about Work, Family and Wellbeing, including: impact of the recession on households and work, job security, housework, wellbeing, experiences of unemployment and work-life balance.'
			module_description['SUPP_H'] = 'ESS R05 Human values scale'
			module_description['SUPP_I'] = 'ESS R05 Test questions'
			module_description['SUPP_J'] = 'ESS R05 Interviewer self-completion questions'

	#Module descriptions for EVS.
	if study == 'EVS':
		if wave_round == 'R03':
			module_description = {'No module': 'No module EVS', 'A - Perceptions of Life': 'EVS R03 module about Perceptions of Life', 'B - Environment':  'EVS R03 module about Environment',
			'C - Work': 'EVS R03 module about Work', 'D - Family': 'EVS R03 module about Family', 'E - Politics and Society': 'EVS R03 module about Politics and Society',
			'F - Religion and Morale': 'EVS R03 module about Religion and Morale','G - National Identity': 'EVS R03 module about National Identity',
			'H - Socio Demographics and Interview Characteristics': 'EVS R03 module about Socio Demographics and Interview Characteristics',
			'I - Additional country-specific variables':'EVS R03 Additional country-specific variables'}

		elif wave_round == 'R04':
			module_description = {'No module': 'No module EVS','A - Perceptions of Life': 'EVS R04 module about Perceptions of Life', 'B - Politics and Society':  'EVS R04 module about Politics and Society',
			'C - Work': 'EVS R04 module about Work', 'D - Religion and Morale': 'EVS R04 module about Religion and Morale', 'E - Family': 'EVS R04 module about Family',
			'F - National Identity': 'EVS R04 module about National Identity','G - Environment': 'EVS R04 module about Environment',
			'H - Life experiences': 'EVS R04 module about Life experiences',
			"I - Respondent's parents":"EVS R04 module about Respondent's parents", "J - Respondent's partner":"EVS R04 module about Respondent's partner",
			'K - Socio Demographics and Interview Characteristics': 'EVS R04 module about Socio Demographics and Interview Characteristics'}

	
	return module_description 

"""
Gets the Country/language metadata.

Args:
    param1: df with data
    param2: language

Returns:
    Country/language metadata
"""
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

"""
Data preparation and calls to functions that populate Survey and Module tables.
Args:
    param1: dataframe with data
    param2: country/language
"""
def populate_survey_and_module_table(df, country_language):
	unique_studies = df.Study.unique()
	for study in unique_studies:
		surveyid = study+'_'+country_language
		split_surveyid = surveyid.split('_')
		study_name = split_surveyid[0]
		wave_round = split_surveyid[1]
		year = split_surveyid[2]
		write_survey_table(surveyid, study_name, wave_round, year, country_language)
		populate_module_table(study_name, wave_round, df)

def preparation_to_populate_survey_and_module_table(file, meta_country_language, is_country_and_language):
	df = pd.read_csv(file)
	if is_country_and_language:
		populate_survey_and_module_table(df, meta_country_language)

	else:
		unique_country_language = get_country_and_language(df, meta_country_language)
		for country_language in unique_country_language:
			filtered_df = df[df['survey_item_ID'].str.contains(country_language)]
			populate_survey_and_module_table(filtered_df, country_language)

	return df

def populate_module_table(study, wave_round, df):
	modules_dict =  dict()

	module_description = get_module_description(study, wave_round)
	# #import data from preprocessed csv into a dataframe
	# data = pd.read_csv(file)
	module = df['module']
	#get only unique values in module column
	module_unique_names = df.module.unique()

	modules_in_questionnaire = dict()
	for module_name in module_unique_names:
		if module_name in module_description:
			modules_dict[module_name] = module_description[module_name]
		
	write_module_table(modules_dict)


def populate_survey_item_table_simple_version(file, country_language):
	data = pd.read_csv(file)
	item_is_source = False
	mod = retrieve_module_table_as_dict()
	surveyid = retrieve_survey_last_record()

	if country_language == 'ENG_SOURCE':
		item_is_source = True 

	for i, row in data.iterrows():
		write_survey_item_table(row['survey_item_ID'], surveyid, mod[row['module']], country_language, item_is_source, row['item_name'], row['item_type'])
		last_survey_item_unique = retrieve_survey_item_last_record()
		if row['item_type'] == 'REQUEST':
			write_request_table(last_survey_item_unique, row['survey_item_ID'], row[country_language], '', '', '', '', row['item_name'], row['item_type'])
		elif row['item_type'] == 'INSTRUCTION':
			write_instruction_table(last_survey_item_unique, row['survey_item_ID'], row[country_language], '', '', '', '', row['item_name'], row['item_type'])
		elif row['item_type'] == 'RESPONSE':
			if pd.isnull(row['item_value']):
				write_response_table(last_survey_item_unique, row['survey_item_ID'], row[country_language], '', '', '', '', row['item_name'], row['item_type'], None)
			else:
				write_response_table(last_survey_item_unique, row['survey_item_ID'], row[country_language], '', '', '', '', row['item_name'], row['item_type'], row['item_value'])
		elif row['item_type'] == 'INTRO' or row['item_type'] == 'INTRODUCTION':
			write_introduction_table(last_survey_item_unique, row['survey_item_ID'], row[country_language], '', '', '', '', row['item_name'], row['item_type'])


def filter_instructions(instructions, unique_instructions, country_language):
	reduced_instructions = pd.DataFrame(columns=['instruction_id', 'survey_item_ID', 'text', 'module', 'country_language', 'item_name', 'item_type', 'request_reference'])
	for instruction in unique_instructions:
		analyzed_instruction_df = instructions.loc[instructions[country_language] == instruction]
		size_df = len(analyzed_instruction_df.index)
		if size_df == 1:
			data = {'instruction_id': get_instuction_id(), 'survey_item_ID': analyzed_instruction_df['survey_item_ID'].iloc[0], 
			'text': analyzed_instruction_df[country_language].iloc[0], 'module':  analyzed_instruction_df['module'].iloc[0], 
			'country_language':country_language, 'item_name': analyzed_instruction_df['item_name'].iloc[0], 
			'item_type': analyzed_instruction_df['item_type'].iloc[0], 'request_reference': None}
			reduced_instructions = reduced_instructions.append(data, ignore_index = True)
			update_instruction_id()
		elif size_df > 1:
			for i, row in analyzed_instruction_df.iterrows():
				if row['survey_item_ID'] == analyzed_instruction_df['survey_item_ID'].iloc[0]:
					data = {'instruction_id': get_instuction_id(), 'survey_item_ID': row['survey_item_ID'], 
					'text': row[country_language], 'module':  row['module'], 
					'country_language':country_language, 'item_name': row['item_name'], 
					'item_type': row['item_type'], 'instruction_reference': None}
					reduced_instructions = reduced_instructions.append(data, ignore_index = True)
					reference = get_instuction_id()
					update_instruction_id()

				else:
					data = {'instruction_id': None, 'survey_item_ID': row['survey_item_ID'], 
					'text': row[country_language], 'module':  row['module'], 
					'country_language':country_language, 'item_name': row['item_name'], 
					'item_type': row['item_type'], 'instruction_reference': reference}
					reduced_instructions = reduced_instructions.append(data, ignore_index = True)

	reduced_instructions.to_csv('unique_instructions.csv', encoding='utf-8', index=False)

	return reduced_instructions

def filter_requests(requests, unique_requests, country_language):
	reduced_requests = pd.DataFrame(columns=['requests_id', 'survey_item_ID', 'text', 'module', 'country_language', 'item_name', 'item_type', 'request_reference'])
	for request in unique_requests:
		analyzed_request_df = requests.loc[requests[country_language] == request]
		size_df = len(analyzed_request_df.index)
		if size_df == 1:
			data = {'requests_id': get_request_id(), 'survey_item_ID': analyzed_request_df['survey_item_ID'].iloc[0], 
			'text': analyzed_request_df[country_language].iloc[0], 'module':  analyzed_request_df['module'].iloc[0], 
			'country_language':country_language, 'item_name': analyzed_request_df['item_name'].iloc[0], 
			'item_type': analyzed_request_df['item_type'].iloc[0], 'request_reference': None}
			reduced_requests = reduced_requests.append(data, ignore_index = True)
			update_request_id()
		elif size_df > 1:
			for i, row in analyzed_request_df.iterrows():
				if row['survey_item_ID'] == analyzed_request_df['survey_item_ID'].iloc[0]:
					data = {'requests_id': get_request_id(), 'survey_item_ID': row['survey_item_ID'], 
					'text': row[country_language], 'module':  row['module'], 
					'country_language':country_language, 'item_name': row['item_name'], 
					'item_type': row['item_type'], 'instruction_reference': None}
					reduced_requests = reduced_requests.append(data, ignore_index = True)
					reference = get_request_id()
					update_request_id()

				else:
					data = {'requests_id': None, 'survey_item_ID': row['survey_item_ID'], 
					'text': row[country_language], 'module':  row['module'], 
					'country_language':country_language, 'item_name': row['item_name'], 
					'item_type': row['item_type'], 'instruction_reference': reference}
					reduced_requests = reduced_requests.append(data, ignore_index = True)

	reduced_requests.to_csv('unique_requests.csv', encoding='utf-8', index=False)

	return reduced_requests

def populate_requests_table(unique_requests):
	write_request_table(unique_requests)

def populate_instruction_table(unique_instructions):
	write_instruction_table(unique_instructions)

def populate_introductions_table(unique_introductions):
	write_introduction_table(unique_introductions)

def check_if_df_is_in_list(list_of_df_responses, analyzed_df):
	for i, df in enumerate(list_of_df_responses):
		comparison_matrix = df.values == analyzed_df.values
		df_in_list = np.all(comparison_matrix == True)
		if df_in_list:
			#If the dataframe is already in the list, return the index position of df in the list
			return True, i

	return False, None


def find_unique_responses(responses, country_language):
	responses_with_multiple_values_aux = []
	responses_with_unique_values = []
	responses_with_multiple_values = []

	#Index dictionary for responses with single values
	#Dictionary is cleaned every time the language/country pair changes
	d_r_with_unique_values = dict()
	#Index dictionary for responses with multiple values
	#Dictionary is cleaned every time the language/country pair changes
	d_r_with_multiple_values = dict()

	unique_survey_id_values = responses['survey_item_ID'].unique()
	for unique_id in unique_survey_id_values:
		a_response = responses[responses.survey_item_ID == unique_id]
		response_text = a_response[[country_language]]
		#Treating cases of responses with only one value (e.g WRITE DOWN)
		survey_item_id = a_response.iloc[0]['survey_item_ID']
		if len(response_text) == 1:
			#Case where the list is empty
			if not responses_with_unique_values:
				d_r_with_unique_values[survey_item_id] = 0
				responses_with_unique_values.append(response_text.iloc[0][country_language])
			#Case where the list is not empty
			else:
				#If response is not on the list
				if response_text.iloc[0][country_language] not in responses_with_unique_values:
					responses_with_unique_values.append(response_text.iloc[0][country_language])
				#wheter the response was in the list or not, add the index to the dictionary
				d_r_with_unique_values[survey_item_id] = responses_with_unique_values.index(response_text.iloc[0][country_language])

		else:
			#Case where the list is empty
			if not responses_with_multiple_values_aux:
				d_r_with_multiple_values[survey_item_id] = 0
				responses_with_multiple_values_aux.append(response_text)
				responses_with_multiple_values.append(a_response[[country_language, 'item_value']])
			#Case where the list is not empty
			else:
				df_in_list = check_if_df_is_in_list(responses_with_multiple_values_aux, response_text)
				if df_in_list[0] == False:
					responses_with_multiple_values_aux.append(response_text)
					responses_with_multiple_values.append(a_response[[country_language, 'item_value']])
					#If the response was appended, the index is the last one
					d_r_with_multiple_values[survey_item_id] = len(responses_with_multiple_values) -1 
				elif df_in_list[0] == True:
					d_r_with_multiple_values[survey_item_id] = df_in_list[1]

	return responses_with_unique_values, responses_with_multiple_values, d_r_with_unique_values, d_r_with_multiple_values

def update_response_dictionary(dictionary, response_index, response_id):
	for k,v in list(dictionary.items()):
		if v == response_index:
			dictionary[k] = response_id

	return dictionary

def populate_responses_table(responses_with_unique_values, responses_with_multiple_values, d_r_with_unique_values, d_r_with_multiple_values, country_language):
	for i, item in enumerate(responses_with_unique_values):
		write_response_table(update_response_id(), item, None)
		response_id = get_response_id()
		response_item_id = retrieve_response_item_last_record()
		update_response_dictionary(d_r_with_unique_values, i, [response_id, response_item_id])
		
	for j, df in enumerate(responses_with_multiple_values):
		response_id = update_response_id()
		for i, row in df.iterrows():
			write_response_table(response_id, row[country_language], row['item_value'])
			response_item_id = retrieve_response_item_last_record()
			update_response_dictionary(d_r_with_multiple_values, j, [response_id, response_item_id])

	return d_r_with_unique_values, d_r_with_multiple_values


def get_surveyid_moduleid(survey_item_id, module_name):
	survey_id = survey_item_id.rsplit('_', 1)[0]
	split_info = survey_item_id.split('_')
	study = split_info[0]
	wave_round = split_info[1]

	module_description_dict = get_module_description(study, wave_round)
	module_description = module_description_dict[module_name]
	module_id = retrieve_module_id(module_name, module_description)

	return survey_id, module_id

def populate_survey_item_table(df,country_language, d_r_with_unique_values, d_r_with_multiple_values):
	########## Survey_item table params ##########
	#survey_itemid, surveyid, moduleid, requestid, responseid, response_item_id, instructionid,introductionid, 
	#country_language, item_is_source, item_name, item_type
	##############################################
	#Both for EVS and ESS, the source questionnaire is in English
	if 'ENG_SOURCE' in country_language:
		item_is_source = True
	else:
		item_is_source = False

	response_item_id_dict = dict()

	for i, row in df.iterrows():
		survey_id, module_id = get_surveyid_moduleid(row['survey_item_ID'], row['module'])
		if row['item_type'] == 'REQUEST':
			requestid = retrieve_request_id(row[country_language])
			write_survey_item_table(row['survey_item_ID'], survey_id, module_id, requestid, None, None, None,None, country_language, item_is_source, row['item_name'], 'REQUEST')

		if row['item_type'] == 'INSTRUCTION':
			instructiontid = retrieve_instruction_id(row[country_language])
			write_survey_item_table(row['survey_item_ID'], survey_id, module_id, None, None, None, instructiontid,None, country_language, item_is_source, row['item_name'], 'INSTRUCTION')


		if row['item_type'] == 'INTRODUCTION' or row['item_type'] == 'INTRO':
			introductionid = retrieve_introduction_id(row[country_language])
			write_survey_item_table(row['survey_item_ID'], survey_id, module_id, None, None, None, None,introductionid, country_language, item_is_source, row['item_name'], 'INTRODUCTION')

		if row['item_type'] == 'RESPONSE':
			if row['survey_item_ID'] in d_r_with_unique_values:
				#The response table has a conjoint PK consisting of responseid and response_item_id
				#This is necessary because of scale responses.
				response_combined_id = d_r_with_unique_values[row['survey_item_ID']]
				responseid = response_combined_id[0]
				response_item_id  = response_combined_id[1]
				write_survey_item_table(row['survey_item_ID'], survey_id, module_id, None, responseid, response_item_id, None,None, country_language, item_is_source, row['item_name'], 'RESPONSE')
			elif row['survey_item_ID'] in d_r_with_multiple_values:
				response_combined_id = d_r_with_multiple_values[row['survey_item_ID']]
				# print(row['survey_item_ID'], response_combined_id)
				responseid = response_combined_id[0]
				response_item_id  = response_combined_id[1]
				if row['survey_item_ID'] not in response_item_id_dict:
					response_item_id_dict[row['survey_item_ID']] = response_item_id
				else:
					response_item_id_dict[row['survey_item_ID']] += 1
					response_item_id = response_item_id_dict[row['survey_item_ID']]

				write_survey_item_table(row['survey_item_ID'], survey_id, module_id, None, responseid, response_item_id,None,None, country_language, item_is_source, row['item_name'], 'RESPONSE')


def populate_survey_item_table_multiple_countries(df,meta_country_language, country_language, d_r_with_unique_values, d_r_with_multiple_values):
	########## Survey_item table params ##########
	#survey_itemid, surveyid, moduleid, requestid, responseid, response_item_id, instructionid,introductionid, 
	#country_language, item_is_source, item_name, item_type
	##############################################
	#Both for EVS and ESS, the source questionnaire is in English
	if 'ENG_SOURCE' in country_language:
		item_is_source = True
	else:
		item_is_source = False

	response_item_id_dict = dict()

	for i, row in df.iterrows():
		survey_id, module_id = get_surveyid_moduleid(row['survey_item_ID'], row['module'])
		if row['item_type'] == 'REQUEST':
			requestid = retrieve_request_id(row[meta_country_language])
			write_survey_item_table(row['survey_item_ID'], survey_id, module_id, requestid, None, None, None,None, country_language, item_is_source, row['item_name'], 'REQUEST')

		if row['item_type'] == 'INSTRUCTION':
			instructiontid = retrieve_instruction_id(row[meta_country_language])
			write_survey_item_table(row['survey_item_ID'], survey_id, module_id, None, None, None, instructiontid,None, country_language, item_is_source, row['item_name'], 'INSTRUCTION')


		if row['item_type'] == 'INTRODUCTION' or row['item_type'] == 'INTRO':
			introductionid = retrieve_introduction_id(row[meta_country_language])
			write_survey_item_table(row['survey_item_ID'], survey_id, module_id, None, None, None, None,introductionid, country_language, item_is_source, row['item_name'], 'INTRODUCTION')

		if row['item_type'] == 'RESPONSE':
			if row['survey_item_ID'] in d_r_with_unique_values:
				#The response table has a conjoint PK consisting of responseid and response_item_id
				#This is necessary because of scale responses.
				response_combined_id = d_r_with_unique_values[row['survey_item_ID']]
				responseid = response_combined_id[0]
				response_item_id  = response_combined_id[1]
				write_survey_item_table(row['survey_item_ID'], survey_id, module_id, None, responseid, response_item_id, None,None, country_language, item_is_source, row['item_name'], 'RESPONSE')
			elif row['survey_item_ID'] in d_r_with_multiple_values:
				response_combined_id = d_r_with_multiple_values[row['survey_item_ID']]
				# print(row['survey_item_ID'], response_combined_id)
				responseid = response_combined_id[0]
				response_item_id  = response_combined_id[1]
				if row['survey_item_ID'] not in response_item_id_dict:
					response_item_id_dict[row['survey_item_ID']] = response_item_id
				else:
					response_item_id_dict[row['survey_item_ID']] += 1
					response_item_id = response_item_id_dict[row['survey_item_ID']]

				write_survey_item_table(row['survey_item_ID'], survey_id, module_id, None, responseid, response_item_id,None,None, country_language, item_is_source, row['item_name'], 'RESPONSE')

def preparation_to_populate_remaining_table(df, meta_country_language, is_country_and_language):
	#Dataframe filtered by item_type 'REQUEST'
	requests = df[df.item_type == 'REQUEST']
	#Dataframe filtered by item_type 'INSTRUCTION'
	instructions = df[df.item_type == 'INSTRUCTION']
	#Dataframe filtered by item_type 'RESPONSE'
	responses = df[df.item_type == 'RESPONSE']
	#Dataframe filtered by item_type 'INTRODUCTION'
	df_check = ['INTRODUCTION', 'INTRO']
	intro = df[df.item_type == 'INTRO']
	introduction = df[df.item_type == 'INTRODUCTION']
	frames = [intro, introduction]
	introductions = pd.concat(frames)

	unique_instructions = instructions[meta_country_language].unique()
	populate_instruction_table(unique_instructions)
	# reduced_instructions = filter_instructions(instructions, unique_instructions, meta_country_language)

	unique_introductions = introductions[meta_country_language].unique()
	populate_introductions_table(unique_introductions)

	unique_requests = requests[meta_country_language].unique()
	populate_requests_table(unique_requests)
	# reduced_requests = filter_requests(requests, unique_requests, meta_country_language)

	responses_with_unique_values, responses_with_multiple_values, d_r_with_unique_values, d_r_with_multiple_values = find_unique_responses(responses, meta_country_language)
	d_r_with_unique_values, d_r_with_multiple_values = populate_responses_table(responses_with_unique_values, responses_with_multiple_values, d_r_with_unique_values, d_r_with_multiple_values, meta_country_language)

	if is_country_and_language:
		populate_survey_item_table(df,meta_country_language, d_r_with_unique_values, d_r_with_multiple_values)
	else:
		unique_country_language = get_country_and_language(df, meta_country_language)
		for country_language in unique_country_language:
			print(country_language)
			filtered_df = df[df['survey_item_ID'].str.contains(country_language)]
			print(filtered_df)
			populate_survey_item_table_multiple_countries(filtered_df,meta_country_language,country_language, d_r_with_unique_values, d_r_with_multiple_values)



	

def concatenate_files(files, metainfo, folder_path):
	file_list = list()
	for index, file in enumerate(files):
		df = pd.read_csv(file)
		column_names = df.columns
		text = column_names[-1]
		df = df.rename(columns={text: metainfo})
		file_list.append(df)

	all_files = pd.concat(file_list, axis=0, ignore_index=True)
	all_files.to_csv(folder_path+'/'+metainfo+".csv", index=False)

	
def get_directory_list(folder_path):
	directory_list = list()
	for root, dirs, files in os.walk(folder_path, topdown=False):
		for name in dirs:
			directory_list.append(os.path.join(root, name))

	return directory_list


def preparation_to_include_data(folder_path):
	directory_list = get_directory_list(folder_path)
	for directory in directory_list:
		if 'ESS' in folder_path:
			metainfo = directory.split('ESS_')[1]
		elif 'EVS' in folder_path:
			metainfo = directory.split('EVS_')[1]
		files = os.listdir(directory)
		os.chdir(directory)
		concatenate_files(files, metainfo, folder_path)
		os.chdir(folder_path)

def main(folder_path, concatenate):
	if concatenate_files:
		preparation_to_include_data(folder_path)
		
	os.chdir(folder_path)
	files = os.listdir(folder_path)
	for index, file in enumerate(files):
		if file.endswith(".csv"):
			print(file)
			is_country_and_language = False
			meta_about_country_language = file.replace('.csv', '')
			more_contries_with_same_language = meta_about_country_language.split('_')
			if len(more_contries_with_same_language) == 2:
				is_country_and_language = True

			df = preparation_to_populate_survey_and_module_table(file, meta_about_country_language, is_country_and_language)
			preparation_to_populate_remaining_table(df, meta_about_country_language, is_country_and_language)

				

if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	concatenate = str(sys.argv[2])
	main(folder_path,concatenate)