"""
Python3 script  to transform EVS spreadsheet data (from TMT) into spreadsheet format used as input for MCSQ
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
"""
import pandas as pd
import nltk.data
import numpy as np
import sys
import os
import re
import utils as ut
from preprocessing_ess_utils import *
import math


def dk_nr_standard(item_value):
	# Standard
	# Refusal 777
	# Don't know 888
	# Does not apply 999
	if isinstance(item_value, str) or isinstance(item_value, int):
		item_value = str(item_value)
		if item_value == '8':
			return "888"
		elif item_value == '9':
			return "999"
		elif item_value == '7':
			return "777"
		else:
			item_value = re.sub("[8]{2,}", "888", item_value)
			item_value = re.sub("[9]{2,}", "999", item_value)
			item_value = re.sub("[7]{2,}", "777", item_value)


	return item_value


def clean_text(text):
	if isinstance(text, str):
		text = re.sub("\n", " ", text)
		text = re.sub("…", "...", text)
		text = re.sub("’", "'", text)
		text = text.replace('e.g.', 'eg')
		text = text.replace('e.g', 'eg')
		text = text.replace('[', '')
		text = text.replace(']', '')
		text = re.sub("[.]{4,}", "", text)
		tags = re.compile(r'<.*?>')
		text = tags.sub('', text)
		text = text.rstrip()

	return text


def remove_trailing(clean):
	without_trailing = []
	for item in clean:
		item = item.rstrip()
		without_trailing.append(item)

	return without_trailing

def get_module(row, module_dict):
	if isinstance(row['Module'], str):
		module = module_dict[row['Module']]
	else:
		module = row['Module']

	return module

def adjust_item_name(row):
	print(row)
	if isinstance(row['QuestionElementNr'], str) and isinstance(row['QuestionName'], str):
		if 'a' not in row['QuestionName'] and row['QuestionElementNr'] != ' ':
			item_name = row['QuestionName']+chr(int(row['QuestionElementNr'])+64).lower()
		else:
			item_name = row['QuestionName']
	else:
		item_name = row['QuestionName']

	return item_name

def standardize_item_type_in_constants_sheet(item_type):
	"""
	Standardizes the names of item_types in the TMT export to the item_types used in MCSQ. 

	Args:
		param1 item_type (string): item_type retrieved from column QuestionElement of constants sheet.

	Returns: 
		Standardized item_type (string).
	"""
	if item_type == 'IWER':
		return 'INSTRUCTION'
	elif item_type == 'Answer':
		return 'RESPONSE'
	elif item_type == 'QItemInstruction':
		return 'REQUEST'

def process_constant(constants, constant_code):
	"""
	Gets the text of a constant code in the constants sheet.
	There are many missing values in the Translation column, as a workaround the TranslatableElement
	is also considered as valid text.

	Args:
		param1 constants (pandas dataframe): pandas dataframe with contents of constants sheet.
		param2 constant_code (string): Code of constant, extracted from input file in outer loop.

	Returns: 
		constant_text, which is the text of the desired constant code (string) and its item_type (string).
	"""
	mask = constants.loc[constants['Code'] == constant_code]

	if not mask.empty:

		if isinstance(mask['Translation'].values[0], float) or mask['Translation'].values[0] == 'Translation':

			constant_text = mask['TranslatableElement'].values[0]
		else:
			constant_text = mask['Translation'].values[0]

		item_type = standardize_item_type_in_constants_sheet(mask['QuestionElement'].values[0])

		return constant_text, item_type
	else:
		return None, None

def process_constant_segment(constants, row, study, survey_item_prefix, splitter, module_dict, df_questionnaire):
	constant_text, item_type = process_constant(constants, row['Translated'])

	if constant_text != None:
		if df_questionnaire.empty:
			survey_item_id = ut.get_survey_item_id(survey_item_prefix)
		else:
			survey_item_id = ut.update_survey_item_id(survey_item_prefix)

		if item_type == 'RESPONSE':
			item_value = dk_nr_standard(row['QuestionElementNr']) 

			data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': get_module(row, module_dict), 
			'item_type':item_type, 'item_name': row['QuestionName'], 'item_value':item_value, 
			'text':clean_text(constant_text), 'QuestionElement': row['QuestionElement']}
			df_questionnaire = df_questionnaire.append(data, ignore_index = True)
		else:
			constant_text = clean_text(constant_text)
			sentences = splitter.tokenize(constant_text)
			for sentence in sentences:
				data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': get_module(row, module_dict), 
				'item_type':item_type, 'item_name': row['QuestionName'], 'item_value':None, 'text': sentence,
				'QuestionElement': row['QuestionElement']}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire


def process_request_segment(row, study, survey_item_prefix, splitter, module_dict, df_questionnaire):
	if isinstance(row['Translated'], float) or row['Translated'] == 'Translation':
		if isinstance(row['TranslatableElement'], float):
			return df_questionnaire
		else:
			text = row['TranslatableElement'] 
	else:
		text = row['Translated'] 

	text = clean_text(text)
	sentences = splitter.tokenize(text)

	if df_questionnaire.empty ==False:
		last_row = df_questionnaire.iloc[-1]
		for sentence in sentences:
			if sentence != last_row['text']:
				if df_questionnaire.empty:
					survey_item_id = ut.get_survey_item_id(survey_item_prefix)
				else:
					survey_item_id = ut.update_survey_item_id(survey_item_prefix)

				data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': get_module(row, module_dict), 
				'item_type':'REQUEST', 'item_name': row['QuestionName'], 'item_value':None, 'text':sentence,
				'QuestionElement': row['QuestionElement']}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)	
	else:
		for sentence in sentences:
			if df_questionnaire.empty:
				survey_item_id = ut.get_survey_item_id(survey_item_prefix)
			else:
				survey_item_id = ut.update_survey_item_id(survey_item_prefix)

			data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': get_module(row, module_dict), 
			'item_type':'REQUEST', 'item_name': row['QuestionName'], 'item_value':None, 'text':sentence,
			'QuestionElement': row['QuestionElement']}
			df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire

def process_instruction_segment(row, study, survey_item_prefix, splitter, module_dict, df_questionnaire):
	if isinstance(row['Translated'], float) or row['Translated'] == 'Translation':
		if isinstance(row['TranslatableElement'], float):
			return df_questionnaire
		else:
			text = row['TranslatableElement'] 
	else:
		text = row['Translated'] 

	if df_questionnaire.empty:
		survey_item_id = ut.get_survey_item_id(survey_item_prefix)
	else:
		survey_item_id = ut.update_survey_item_id(survey_item_prefix)

	text = clean_text(text)
	sentences = splitter.tokenize(text)
	for sentence in sentences:
		data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': get_module(row, module_dict), 
		'item_type':'INSTRUCTION', 'item_name': row['QuestionName'], 'item_value':None, 'text': sentence,
		'QuestionElement': row['QuestionElement']}
		df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire


def process_response_segment(row, study, survey_item_prefix, module_dict, df_questionnaire):
	if isinstance(row['Translated'], float) or row['Translated'] == 'Translation':
		if isinstance(row['TranslatableElement'], float):
			return df_questionnaire
		else:
			text = row['TranslatableElement'] 
	else:
		text = row['Translated'] 

	if df_questionnaire.empty:
		survey_item_id = ut.get_survey_item_id(survey_item_prefix)
	else:
		survey_item_id = ut.update_survey_item_id(survey_item_prefix)


	data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': get_module(row, module_dict), 
	'item_type':'RESPONSE', 'item_name': row['QuestionName'], 'item_value':row['QuestionElementNr'], 
	'text':clean_text(text), 'QuestionElement': row['QuestionElement']}
	df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire

def process_response_type_segment(response_types, code, row, study, survey_item_prefix, module_dict, df_questionnaire):
	mask = response_types.loc[response_types['Code'] == code]

	if not mask.empty:
		for i, mask_row in mask.iterrows():
			if isinstance(mask_row['Translation'], float) or mask_row['Translation'] == 'Translation': 
				if isinstance(mask_row['Translatable Element'], float):
					text = ''
				else:
					text = mask_row['Translatable Element']
			else:
				text = mask_row['Translation'] 

			if text != '':
				survey_item_id = ut.update_survey_item_id(survey_item_prefix)
				data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': get_module(row, module_dict), 
				'item_type':'RESPONSE', 'item_name': row['QuestionName'], 'item_value':row['QuestionElementNr'], 
				'text':clean_text(text), 'QuestionElement': row['QuestionElement']}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire

def questionnaire_post_processing(df_questionnaire):
	df_post= pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 'text'])
	unique_item_names = df_questionnaire.item_name.unique()

	for unique_item_name in unique_item_names:
		df_by_item_name = df_questionnaire[df_questionnaire['item_name']==unique_item_name]

		df_instruction = df_by_item_name[df_by_item_name['item_type']=='INSTRUCTION']
		df_request = df_by_item_name[df_by_item_name['item_type']=='REQUEST']
		df_response = df_by_item_name[df_by_item_name['item_type']=='RESPONSE']

		del df_response['QuestionElement']

		if df_instruction.empty == False:
			del df_instruction['QuestionElement']
			df_post = df_post.append(df_instruction, ignore_index=True)

		for i, row in df_request.iterrows():
			data = {'survey_item_ID': row['survey_item_ID'], 'Study':row['Study'], 'module':row['module'], 
			'item_type':row['item_type'], 'item_name':row['item_name'], 'item_value':row['item_value'], 'text': row['text']}
			df_post = df_post.append(data, ignore_index = True)	

			if df_response.empty == False:
				if row['QuestionElement'] == 'QItem':
					df_post = df_post.append(df_response, ignore_index=True)

		if df_response.empty == False:
			last_row = df_post.iloc[-1]
			if last_row['item_type'] != 'RESPONSE':
				df_post = df_post.append(df_response, ignore_index=True)

	return df_post

def set_initial_structures(filename):
	"""
	Set initial structures that are necessary for the extraction of each questionnaire.

	Args:
		param1 filename (string): name of the input file.

	Returns: 
		df_questionnaire to store questionnaire data (pandas dataframe),
		survey_item_prefix, which is the prefix of survey_item_ID (string), 
		study/country_language, which are metadata parameters embedded in the file name (string and string),
		sentence splitter to segment request/introduction/instruction segments when necessary (NLTK object)
		and module_dict (dictionary) holding the names of modules. 
	"""

	"""
	A pandas dataframe to store questionnaire data.
	"""
	df_questionnaire = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 
		'item_value', 'text', 'QuestionElement'])

	"""
	The prefix of a EVS survey item is study+'_'+language+'_'+country+'_'
	"""
	survey_item_prefix = re.sub('\.xlsx', '', filename)+'_'

	"""
	Reset the initial survey_id sufix, because main is called iterativelly for every file in folder.
	"""
	ut.reset_initial_sufix()

	"""
	Retrieve study and country_language information from the name of the input file. 
	"""
	study, country_language = get_country_language_and_study_info(filename)

	"""
	Instantiate a NLTK sentence splitter based on file input language. 
	"""
	splitter = ut.get_sentence_splitter(filename)

	"""
	Module dictionnaire
	"""
	module_dict = {'A': 'Perceptions of Life', 'B': 'Family', 'C': 'Politics and society',
	'D': "Respondent's parents", 'E': 'Socio demographics'}

	return df_questionnaire, survey_item_prefix, study, country_language,splitter, module_dict

def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)

	for index, file in enumerate(files):
		if file.endswith(".xlsx"):	
			print(file)
			df_questionnaire, survey_item_prefix, study, country_language,splitter, module_dict = set_initial_structures(file)
			item_names_dict = dict()

			constants = pd.read_excel(open(file, 'rb'), sheet_name='Constants')
			response_types = pd.read_excel(open(file, 'rb'), sheet_name='AnswerTypes')

			questionnaire = pd.read_excel(open(file, 'rb'), sheet_name='Questionnaire', dtype=str)
			questionnaire['TranslatableElement'] = questionnaire['TranslatableElement'].replace(['NA'],'NAext')
			questionnaire['Translated'] = questionnaire['Translated'].replace(['NA'],'NAext')
			questionnaire['TranslatableElement'] = questionnaire['TranslatableElement'].replace(['DK'],'DKext')
			questionnaire['Translated'] = questionnaire['Translated'].replace(['DK'],'DKext')

			if 'ENG' not in country_language:
				questionnaire = questionnaire[questionnaire['Translated'].notna()]
				response_types = response_types[response_types['Translation'].notna()]
				constants = constants[constants['Translation'].notna()]
				
			for i, row in questionnaire.iterrows():
				if row['QuestionElement'] == 'Constant':
					df_questionnaire = process_constant_segment(constants, row, study, survey_item_prefix, splitter, module_dict, df_questionnaire)
				elif row['QuestionElement'] in ['QInstruction', 'QItemInstruction', 'QItem'] and row['QuestionName'] not in ['INTRO0', 'INTRO1']:
					df_questionnaire = process_request_segment(row, study, survey_item_prefix, splitter, module_dict, df_questionnaire)
				elif row['QuestionElement'] == 'IWER':
					if row['QuestionName'] != 'IWER_INTRO' and isinstance(row['QuestionName'], str):
						df_questionnaire = process_instruction_segment(row, study, survey_item_prefix, splitter, module_dict, df_questionnaire)
				elif row['QuestionElement'] == 'Answer':
					df_questionnaire = process_response_segment(row, study, survey_item_prefix, module_dict, df_questionnaire)
				elif row['QuestionElement'] == 'AnswerType':
					df_questionnaire = process_response_type_segment(response_types, row['TranslatableElement'], row, study, 
						survey_item_prefix, module_dict, df_questionnaire)


			csv_name = file.replace('.xlsx', '')
			df_post = questionnaire_post_processing(df_questionnaire)
			df_post.to_csv(csv_name+'.csv', encoding='utf-8-sig', index=False)



if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	print("Executing data cleaning/extraction script for EVS 2017")
	main(folder_path)
