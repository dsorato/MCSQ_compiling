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

constants_dict = dict()
response_types_dict = dict()
instruction_constants = ['ASKALL','C_CERT','INT_INS','R_LINE','R_ONLY','SHOWC','CHECK_APP','GO_TO','SKIP_MSG']
response_constants = ['DK', 'DKext', 'NA','NAext','NAP','OTHER','DK_cawi_mail','DKext_cawi_mail','NA_cawi_mail','NAext_cawi_mail','WOULD_NOT_MIND']


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



def extract_response_types(response_types, a_response_type):
	ret = ''
	filtered_response_types_df = response_types[response_types['Code'] == a_response_type]

	if a_response_type in response_types_dict:
		ret = response_types_dict[a_response_type]

	else:
		if filtered_response_types_df.empty:
			ret = ''
		else:
			translated_cells = iter(filtered_response_types_df.Translated)
			translated_cells = list(translated_cells)
			
			if pd.notna(translated_cells).all() and 'Translation' not in translated_cells:
				ret = translated_cells
			# else:
			# 	ret = iter(filtered_response_types_df.TranslatableElement)
			# 	ret = list(ret)

				clean_text_ret = []
				for item in ret:
					item = clean_text(item)
					clean_text_ret.append(item)

			
				response_types_dict[a_response_type] = clean_text_ret

	return ret

def extract_constant(constants, a_constant):
	ret = ''
	filtered_constants_df = constants[constants['Code'] == a_constant]

	if a_constant in constants_dict:
		ret = constants_dict[a_constant]

	else:
		if filtered_constants_df.empty:
			ret = ''
		else:
			translated_cell = iter(filtered_constants_df.Translation)
			translated_cell = list(translated_cell)[0]
			
			if pd.notna(translated_cell) and translated_cell != 'Translation':
				ret = translated_cell
			# else:
			# 	ret = iter(filtered_constants_df.TranslatableElement)
			# 	ret = list(ret)[0]

				ret = clean_text(ret)
				constants_dict[a_constant] = ret

	return ret

def check_question_name(question_name):
	ret = ''
	if isinstance(question_name, str):
		if 'INTRODUCTION' in question_name:
			ret =  'INTRODUCTION'
		else:
			ret =  'REQUEST'

	return ret

def check_item_name(row):
	if isinstance(row['VariableName'], str):
		ret = row['VariableName']
	else:
		ret =  row['QuestionName'] 

	return ret

def decide_item_type_other(row):
	if 'CodInstruction' in str(row['QuestionElement']):
		item_type = 'INSTRUCTION'
	elif ('INTRO' or 'SECTION') in str(row['QuestionName']):
		item_type = 'INTRODUCTION'
	else:
		item_type = 'REQUEST'

	return item_type

def decide_item_type_constant(constant, row):
	if constant in instruction_constants:
		item_type = 'INSTRUCTION'
	else:
		item_type = check_question_name(row['QuestionName'])

	return item_type
					

def replace_intro_in_item_name(column_item_name, item_name):
	item_name_index = column_item_name.index(item_name)
	if 'INTRO' in item_name:
		for i, value in enumerate(column_item_name[item_name_index:]):
			if 'INTRO' not in value and 'SECTION' not in value:
				item_name = value
				break

	return item_name

def process_questionnaire(questionnaire, constants, response_types, df_questionnaire, survey_item_prefix, study, splitter):
	for index, row in questionnaire.iterrows(): 
		"""
		case 1: Translated row is not null = We have the tranlated text
		"""
		if pd.isna(row['Translated']) == False and pd.isna(row['QuestionName']) == False:
			if row['QuestionName'] != 'IWER_INTRO' and row['QuestionName'] != 'INTRO0' and 'SECTION' not in row['QuestionName']:
				"""
				item is a constant. A constant can be type: INSTRUCTION, INTRODUCTION or REQUEST
				"""
				if pd.notna(row['Translated']) and row['QuestionElement'] == 'Constant' and row['Translated'] not in response_constants:
					constant = row['Translated']
					text = extract_constant(constants, constant)
					column_item_name = list(questionnaire['QuestionName'])
					item_name = replace_intro_in_item_name(column_item_name, row['QuestionName']) 
					
					if text != '':
						if df_questionnaire.empty:
							survey_item_id = ut.get_survey_item_id(survey_item_prefix)
						else:
							survey_item_id = ut.update_survey_item_id(survey_item_prefix)

						data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': row['Module'], 
						'item_type':decide_item_type_constant(constant, row), 'item_name': item_name, 
						'item_value':None, 'text':clean_text(text)}
						df_questionnaire = df_questionnaire.append(data, ignore_index = True)		
				elif pd.notna(row['Translated']) and (row['QuestionElement'] == 'AnswerType' or row['QuestionElement'] == 'Answer' or row['Translated'] in response_constants):
					"""
					item is a response. A response can be only type RESPONSE
					"""		
					response = row['Translated']
					if response in response_constants:
						text = extract_constant(constants, response)
						if text != '':
							survey_item_id = ut.update_survey_item_id(survey_item_prefix)
							data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': row['Module'], 
							'item_type':decide_item_type_constant(constant, row), 'item_name': row['QuestionName'], 
							'item_value':None, 'text':clean_text(text)}
							df_questionnaire = df_questionnaire.append(data, ignore_index = True)
					#response != 'Translation' is a workaround to deal with incorrecly translated segments
					elif row['QuestionElement'] == 'Answer' and response != 'Translation':
						if text != '':
							if df_questionnaire.empty:
								survey_item_id = ut.get_survey_item_id(survey_item_prefix)
							else:
								survey_item_id = ut.update_survey_item_id(survey_item_prefix)

							data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': row['Module'], 
							'item_type':decide_item_type_constant(constant, row), 'item_name': item_name, 
							'item_value':None, 'text':clean_text(text)}
							df_questionnaire = df_questionnaire.append(data, ignore_index = True)
					else:
						text = extract_response_types(response_types, text)
						if text != '':
							for item in text:
								if item != 'Translation':

									survey_item_id = ut.update_survey_item_id(survey_item_prefix)

									data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': row['Module'], 
									'item_type': 'RESPONSE', 'item_name': row['QuestionName'], 
									'item_value':dk_nr_standard(row['QuestionElementNr']), 'text':clean_text(item)}
									df_questionnaire = df_questionnaire.append(data, ignore_index = True)			
				# item type can be INTRODUCTION, INSTRUCTION or REQUEST
				else:
					if pd.notna(row['Translated']):
						if df_questionnaire.empty:
							survey_item_id = ut.get_survey_item_id(survey_item_prefix)
						else:
							survey_item_id = ut.update_survey_item_id(survey_item_prefix)

						text = clean_text(row['Translated'])
						column_item_name = list(questionnaire['QuestionName'])
						item_name = replace_intro_in_item_name(column_item_name, row['QuestionName']) 
						sentences = splitter.tokenize(text)

						for sentence in sentences:
							data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': row['Module'], 
							'item_type':decide_item_type_other(row), 'item_name': item_name, 
							'item_value':None, 'text':clean_text(sentence)}
							df_questionnaire = df_questionnaire.append(data, ignore_index = True)		
	return df_questionnaire

def set_initial_structures(filename):
	"""
	Set initial structures that are necessary for the extraction of each questionnaire.

	Args:
		param1 filename (string): name of the input file.

	Returns: 
		df_questionnaire to store questionnaire data (pandas dataframe),
		survey_item_prefix, which is the prefix of survey_item_ID (string), 
		study/country_language, which are metadata parameters embedded in the file name (string and string)
		and sentence splitter to segment request/introduction/instruction segments when necessary (NLTK object). 
	"""

	"""
	A pandas dataframe to store questionnaire data.
	"""
	df_questionnaire = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 'text'])

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


	return df_questionnaire, survey_item_prefix, study, country_language,splitter

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

		if math.isnan(mask['Translation'].values[0]) or mask['Translation'].values[0] == 'Translation':

			constant_text = mask['TranslatableElement'].values[0]
		else:
			constant_text = mask['Translation'].values[0]

		item_type = standardize_item_type_in_constants_sheet(mask['QuestionElement'].values[0])

		return constant_text, item_type
	else:
		return None, None

def process_constant_segment(constants, row, study, survey_item_prefix, splitter, df_questionnaire):
	constant_text, item_type = process_constant(constants, row['Translated'])

	if constant_text != None:
		if df_questionnaire.empty:
			survey_item_id = ut.get_survey_item_id(survey_item_prefix)
		else:
			survey_item_id = ut.update_survey_item_id(survey_item_prefix)

		if item_type == 'RESPONSE':
			item_value = dk_nr_standard(row['QuestionElementNr']) 

			data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': row['Module'], 
			'item_type':item_type, 'item_name': row['QuestionName'], 
			'item_value':item_value, 'text':clean_text(constant_text)}
			df_questionnaire = df_questionnaire.append(data, ignore_index = True)
		else:
			sentences = splitter.tokenize(constant_text)
			for sentence in sentences:
				data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': row['Module'], 
				'item_type':item_type, 'item_name': row['QuestionName'], 
				'item_value':None, 'text':clean_text(sentence)}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire


def process_request_segment(row, study, survey_item_prefix, splitter, df_questionnaire):
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

		sentences = splitter.tokenize(text)
		for sentence in sentences:
			data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': row['Module'], 
			'item_type':'REQUEST', 'item_name': row['QuestionName'], 
			'item_value':None, 'text':clean_text(sentence)}
			df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire

def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)

	for index, file in enumerate(files):
		if file.endswith(".xlsx"):	
			print(file)
			df_questionnaire, survey_item_prefix, study, country_language,splitter = set_initial_structures(file)

			constants = pd.read_excel(open(file, 'rb'), sheet_name='Constants')
			response_types = pd.read_excel(open(file, 'rb'), sheet_name='AnswerTypes')

			questionnaire = pd.read_excel(open(file, 'rb'), sheet_name='Questionnaire', dtype=str)
			questionnaire['TranslatableElement'] = questionnaire['TranslatableElement'].replace(['NA'],'NAext')
			questionnaire['Translated'] = questionnaire['Translated'].replace(['NA'],'NAext')
			questionnaire['TranslatableElement'] = questionnaire['TranslatableElement'].replace(['DK'],'DKext')
			questionnaire['Translated'] = questionnaire['Translated'].replace(['DK'],'DKext')
			# questionnaire = questionnaire[questionnaire['Translated'].notna()]
			

			for i, row in questionnaire.iterrows():
				if row['QuestionElement'] == 'Constant':
					df_questionnaire = process_constant_segment(constants, row, study, survey_item_prefix, splitter, df_questionnaire)
				elif row['QuestionElement'] in ['QInstruction', 'QItemInstruction', 'QItem']:
					df_questionnaire = process_request_segment(row, study, survey_item_prefix, splitter, df_questionnaire)
					




			
			# list_unique_modules = questionnaire.Module.unique()
			# list_unique_modules = ['No module' if isinstance(x, float) else x for x in list_unique_modules]

			# df_questionnaire = process_questionnaire(questionnaire, constants, response_types, df_questionnaire, 
			# 	survey_item_prefix, study, splitter)

			csv_name = file.replace('.xlsx', '')
			df_questionnaire.to_csv(csv_name+'.csv', encoding='utf-8-sig', index=False)




	
			
	


if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	print("Executing data cleaning/extraction script for EVS 2017")
	main(folder_path)
