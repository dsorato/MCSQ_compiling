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
	"""
	Standardizes special category values (don't know, refusal and not applicable).
	Standard:
	Refusal 777
	Don't know 888
	Does not apply 999
	
	Args:
		param1 item_value (string): item value metadata extarcted from QuestionElementNr in the input file.
	Returns: 
		Standardized item_value (string) metadata, if it is a special answer category
	"""	
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
	"""
	Cleans text segments by removing undesired characters and character sequences.
	A string input is expected, if the input is not a string instance, 
	the method returns '', so the entry is ignored in the data extraction loop.

	Args:
		param1 text (string): text segment to be cleaned.

	Returns: 
		cleaned text (string).
	"""
	if isinstance(text, str):
		text = re.sub("\n", " ", text)
		text = re.sub("…", "...", text)
		text = re.sub("’", "'", text)
		text = text.replace('e.g.', 'eg')
		text = text.replace('e.g', 'eg')
		text = text.replace('i.e.', 'ie')
		text = text.replace('?:', '?')
		text = text.replace(' ?', '?')
		text = text.replace('‑', '-')
		text = text.replace('[', '')
		text = text.replace(']', '')
		text = re.sub('’',"'", text)
		text = re.sub('´',"'", text)
		text = re.sub("…", "...", text)
		text = text.replace("... ...", "...")
		text = re.sub(" :", ":", text)
		text = re.sub("’", "'", text)
		text = text.replace('. . .', '')
		text = re.sub("[.]{4,}", "", text)
		text = re.sub("[?]{2,}", "?", text)
		text = re.sub("^\d\.\s+", "", text)
		tags = re.compile(r'<.*?>')
		text = tags.sub('', text)
		text = text.rstrip()

	return text

def get_module(row, module_dict):
	"""
	Gets the module metadata. Initial information comes from the column Module of the input file,
	in the form A, B, C, etc. If the letter is present in the module_dict (hard coded), then return 
	the full module name, otherwise return original value from the column Module of the input file.
	A string is expected in row['Module'].

	Args:
		param1 row: pandas dataframe row being currently analyzed.
		param2 module_dict (dictionary): hard coded dictionary contaning the full name of modules.

	Returns: 
		module name metadata (string).
	"""
	if isinstance(row['Module'], str):
		module = module_dict[row['Module']]
	else:
		module = row['Module']

	return module

def adjust_item_name(QuestionElementNr, item_name):
	"""
	Tries to solve the problem of QItems not having different item names by combining the initial
	item name information from the column QuestionName of the input file with a transformation of the
	value in the QuestionElementNr column.

	Args:
		param1 QuestionElementNr (string): item value (in row) extracted from QuestionElementNr column of input file.
		param2 item_name (string): item name (in row) extracted from QuestionName column of input file.

	Returns: 
		adjusted item name metadata (string).
	"""
	if isinstance(QuestionElementNr, str) and isinstance(item_name, str):
		if re.compile('^Q\d+[a-z]$').match(item_name) is None and QuestionElementNr != ' ':
			item_name = item_name.rstrip()
			item_name = item_name+chr(int(QuestionElementNr)+64).lower()
		else:
			item_name = item_name.rstrip()
			item_name = item_name
	else:
		item_name = item_name

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

def process_constant_segment(constants, row, study, splitter, module_dict, df_questionnaire):
	"""
	Processes the text segments of a constant, extracted in the process_constant() method and
	adds it to the questionnaire dataframe (df_questionnaire). If the segment is an instruction of the 
	type SHOWC, combine the text with the card number, available in QuestionElementNr column of the
	input file.

	Args:
		param1 constants (pandas dataframe): pandas dataframe with contents of constants sheet.
		param2 row (series): current row of input file being analyzed in outter loop.
		param3 study (string): metadata parameter about study embedded in the file name.
		param4 splitter (NLTK object): sentence segmentation from NLTK library.
		param5 module_dict (dictionary): hard coded dictionary contaning the full name of modules.
		param6 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.

	Returns: 
		updated df_questionnaire (pandas dataframe) with constant text and its metadata, 
		if the contant text exists.
	"""
	constant_text, item_type = process_constant(constants, row['Translated'])

	if constant_text != None:
		if item_type == 'RESPONSE':
			item_value = dk_nr_standard(row['QuestionElementNr']) 

			data = {'Study':study, 'module': get_module(row, module_dict), 
			'item_type':item_type, 'item_name': row['QuestionName'], 'item_value':item_value, 
			'text':clean_text(constant_text), 'QuestionElement': row['QuestionElement'], 'QuestionElementNr': row['QuestionElementNr']}
			df_questionnaire = df_questionnaire.append(data, ignore_index = True)
		else:
			if item_type == 'INSTRUCTION' and row['TranslatableElement'] == 'SHOWC':
				constant_text = constant_text+' '+row['QuestionElementNr']
				data = {'Study':study, 'module': get_module(row, module_dict), 
					'item_type':item_type, 'item_name': row['QuestionName'], 'item_value':None, 'text': constant_text,
					'QuestionElement': row['QuestionElement'], 'QuestionElementNr': row['QuestionElementNr']}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)
			else:
				constant_text = clean_text(constant_text)
				sentences = splitter.tokenize(constant_text)
				for sentence in sentences:
					data = {'Study':study, 'module': get_module(row, module_dict), 
					'item_type':item_type, 'item_name': row['QuestionName'], 'item_value':None, 'text': sentence,
					'QuestionElement': row['QuestionElement'], 'QuestionElementNr': row['QuestionElementNr']}
					df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire

def add_valid_request_segments(text, study, row,last_row, module_dict, splitter, df_questionnaire):
	"""
	Splits text into sentences, assigns item_type metadata based on information contained in
	QuestionElement column and adds segments to the questionnaire dataframe (df_questionnaire).

	Args:
		param1 text (string): text segments from input file.
		param2 study (string): metadata parameter about study embedded in the file name.
		param3 row (series): current row of input file being analyzed in outter loop.
		param4 last_row (series): previous row of input file being analyzed in outter loop.
		param5 module_dict (dictionary): hard coded dictionary contaning the full name of modules.
		param6 splitter (NLTK object): sentence segmentation from NLTK library.
		param7 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.

	Returns: 
		updated df_questionnaire (pandas dataframe) with request/introduction text and its metadata.
	"""
	text = clean_text(text)
	sentences = splitter.tokenize(text)

	if row['QuestionElement'] == 'QIntro':
		item_type = 'INTRODUCTION'
	else:
		item_type = 'REQUEST'
			
	for sentence in sentences:
		if sentence != last_row['text']:
			data = {'Study':study, 'module': get_module(row, module_dict), 
			'item_type':item_type, 'item_name': row['QuestionName'], 'item_value':None, 'text':sentence,
			'QuestionElement': row['QuestionElement'], 'QuestionElementNr': row['QuestionElementNr']}
			df_questionnaire = df_questionnaire.append(data, ignore_index = True)

	return 	df_questionnaire


def process_request_segment(row, study, country_language, splitter, module_dict, df_questionnaire):
	"""
	Processes request segments and calls the add_valid_request_segments() method when the segment
	is valid. A text segment is valid if: 1) its QuestionElementNr attribute is different from the previous row
	2)  its QuestionElement attribute is different from the previous row.

	Args:
		param1 row (series): current row of input file being analyzed in outter loop.
		param2 study (string): metadata parameter about study embedded in the file name.
		param3 country_language (string): metadata parameter about country_language embedded in the file name.
		param4 splitter (NLTK object): sentence segmentation from NLTK library.
		param5 module_dict (dictionary): hard coded dictionary contaning the full name of modules.
		param6 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.

	Returns: 
		updated df_questionnaire (pandas dataframe) with request text and its metadata.
	"""
	if isinstance(row['Translated'], float) or row['Translated'] == 'Translation':
		if 'ENG' in country_language:
			if isinstance(row['TranslatableElement'], float):
				return df_questionnaire
			else:
				text = row['TranslatableElement']
		else:
			return df_questionnaire
	else:
		text = row['Translated']

	if df_questionnaire.empty ==False:
		last_row = df_questionnaire.iloc[-1]
		if last_row['QuestionElementNr'] != row['QuestionElementNr']:
			df_questionnaire = add_valid_request_segments(text, study, row,last_row, module_dict, splitter, df_questionnaire)
		elif last_row['QuestionElement'] != row['QuestionElement']:
			df_questionnaire = add_valid_request_segments(text, study, row,last_row, module_dict, splitter, df_questionnaire)	
	else:
		text = clean_text(text)
		sentences = splitter.tokenize(text)

		if row['QuestionElement'] == 'QIntro':
			item_type = 'INTRODUCTION'
		else:
			item_type = 'REQUEST'
			
		for i, sentence in enumerate(sentences):
			if i > 0:
				last_row = df_questionnaire.iloc[-1]
				if sentence != last_row['text']:
					data = {'Study':study, 'module': get_module(row, module_dict), 
					'item_type':item_type, 'item_name': row['QuestionName'], 'item_value':None, 'text':sentence,
					'QuestionElement': row['QuestionElement'], 'QuestionElementNr': row['QuestionElementNr']}
					df_questionnaire = df_questionnaire.append(data, ignore_index = True)
			else:
				data = {'Study':study, 'module': get_module(row, module_dict), 
				'item_type':item_type, 'item_name': row['QuestionName'], 'item_value':None, 'text':sentence,
				'QuestionElement': row['QuestionElement'], 'QuestionElementNr': row['QuestionElementNr']}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)

	return df_questionnaire

def add_valid_instruction_segments(text, study, row,last_row, module_dict, splitter, df_questionnaire):
	"""
	Splits text into sentences and adds segments to the questionnaire dataframe (df_questionnaire).

	Args:
		param1 text (string): text segments from input file.
		param2 study (string): metadata parameter about study embedded in the file name.
		param3 row (series): current row of input file being analyzed in outter loop.
		param4 last_row (series): previous row of input file being analyzed in outter loop.
		param5 module_dict (dictionary): hard coded dictionary contaning the full name of modules.
		param6 splitter (NLTK object): sentence segmentation from NLTK library.
		param7 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.

	Returns: 
		updated df_questionnaire (pandas dataframe) with instruction text and its metadata.
	"""
	text = clean_text(text)
	sentences = splitter.tokenize(text)
	for sentence in sentences:
		data = {'Study':study, 'module': get_module(row, module_dict), 
		'item_type':'INSTRUCTION', 'item_name': row['QuestionName'], 'item_value':None, 'text': sentence,
		'QuestionElement': row['QuestionElement'], 'QuestionElementNr': row['QuestionElementNr']}
		df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire

def process_instruction_segment(row, study, country_language, splitter, module_dict, df_questionnaire):
	"""
	Processes instruction segments and calls the add_valid_instruction_segments() method when the segment
	is valid. A text segment is valid if: 1) its QuestionElementNr attribute is different from the previous row
	2)  its QuestionElement attribute is different from the previous row.

	Args:
		param1 row (series): current row of input file being analyzed in outter loop.
		param2 study (string): metadata parameter about study embedded in the file name.
		param3 country_language (string): metadata parameter about country_language embedded in the file name.
		param4 splitter (NLTK object): sentence segmentation from NLTK library.
		param5 module_dict (dictionary): hard coded dictionary contaning the full name of modules.
		param6 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.

	Returns: 
		updated df_questionnaire (pandas dataframe) with instruction text and its metadata.
	"""
	if isinstance(row['Translated'], float) or row['Translated'] == 'Translation':
		if 'ENG' in country_language:
			if isinstance(row['TranslatableElement'], float):
				return df_questionnaire
			else:
				text = row['TranslatableElement']
		else:
			return df_questionnaire
	else:
		text = row['Translated']

	if df_questionnaire.empty ==False:
		last_row = df_questionnaire.iloc[-1]
		if last_row['QuestionElementNr'] != row['QuestionElementNr']:
			df_questionnaire = add_valid_instruction_segments(text, study, row,last_row, module_dict, splitter, df_questionnaire)	
		elif last_row['QuestionElement'] != row['QuestionElement']:
			df_questionnaire = add_valid_instruction_segments(text, study, row,last_row, module_dict, splitter, df_questionnaire)	
	else:
		df_questionnaire = add_valid_instruction_segments(text, study, row,last_row, module_dict, splitter, df_questionnaire)

	return df_questionnaire

def add_valid_response_segments(item_value, text, study, row,last_row, module_dict, df_questionnaire):
	"""
	Adds reponse segments to the questionnaire dataframe (df_questionnaire).

	Args:
		param1 item_value (string): item_value metadata, extracted from QuestionElementNr and modified in process_response_segment()
		param2 text (string): text segments from input file.
		param3 study (string): metadata parameter about study embedded in the file name.
		param4 row (series): current row of input file being analyzed in outter loop.
		param5 last_row (series): previous row of input file being analyzed in outter loop.
		param6 module_dict (dictionary): hard coded dictionary contaning the full name of modules.
		param7 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.

	Returns: 
		updated df_questionnaire (pandas dataframe) with instruction text and its metadata.
	"""
	data = {'Study':study, 'module': get_module(row, module_dict), 
		'item_type':'RESPONSE', 'item_name': row['QuestionName'], 'item_value':str(item_value), 
		'text':clean_text(text), 'QuestionElement': row['QuestionElement'], 'QuestionElementNr': item_value}

	df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire


def process_response_segment(row, study, country_language, module_dict, df_questionnaire):
	"""
	Processes response segments and calls the add_valid_response_segments() method when the segment
	is valid. A text segment is valid if: 1) its QuestionElementNr attribute is different from the previous row
	2)  its QuestionElement attribute is different from the previous row.

	Args:
		param1 row (series): current row of input file being analyzed in outter loop.
		param2 study (string): metadata parameter about study embedded in the file name.
		param3 country_language (string): metadata parameter about country_language embedded in the file name.
		param4 splitter (NLTK object): sentence segmentation from NLTK library.
		param5 module_dict (dictionary): hard coded dictionary contaning the full name of modules.
		param6 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.

	Returns: 
		updated df_questionnaire (pandas dataframe) with response text and its metadata.
	"""
	if isinstance(row['Translated'], float) or row['Translated'] == 'Translation':
		if 'ENG' in country_language:
			if isinstance(row['TranslatableElement'], float):
				return df_questionnaire
			else:
				text = row['TranslatableElement']
		else:
			return df_questionnaire
	else:
		text = row['Translated'] 

	if re.compile('^Religion\s\d+$').match(text) is None and re.compile('^Education\s\d+$').match(text) is None and re.compile('^PARTY\s\d+').match(text) is None:
		item_value = row['QuestionElementNr']
		if pd.isna(item_value):
			item_value = '0'
		if isinstance(row['TranslatableElement'], str):
			if 'Code:' in row['TranslatableElement']:
				item_value = '1'
			if 'Write in' in row['TranslatableElement']:
				item_value = '0'

		if df_questionnaire.empty ==False:
			last_row = df_questionnaire.iloc[-1]
			if last_row['QuestionElementNr'] != row['QuestionElementNr']:
				df_questionnaire = add_valid_response_segments(item_value, text, study, row,last_row, module_dict, df_questionnaire)	
			elif last_row['QuestionElement'] != row['QuestionElement']:
				df_questionnaire = add_valid_response_segments(item_value, text, study, row,last_row, module_dict, df_questionnaire)
		else:
			df_questionnaire = add_valid_response_segments(item_value, text, study, row,last_row, module_dict, df_questionnaire) 

	return df_questionnaire

def process_response_type_segment(response_types, code, row, study, country_language, module_dict, df_questionnaire):
	"""
	Processes response type segments if the code is in the response_type sheet. Builds a mask based on response code
	and iterates through text segments in mask dataframe to extract the response segments. If the segment is of type
	Religion n, Education n, PARTY n, the segment is ignored because these are placeholders.

	Args:
		param1 response_types (pandas dataframe): pandas dataframe with contents of response type sheet.
		param2 code (string): code of response type.
		param3 row (series): current row of input file being analyzed in outter loop.
		param4 study (string): metadata parameter about study embedded in the file name.
		param5 country_language (string): metadata parameter about country_language embedded in the file name.
		param6 module_dict (dictionary): hard coded dictionary contaning the full name of modules.
		param7 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.

	Returns: 
		updated df_questionnaire (pandas dataframe) with response text and its metadata.
	"""
	mask = response_types.loc[response_types['Code'] == code]
	
	if not mask.empty:
		for i, mask_row in mask.iterrows():
			if isinstance(mask_row['Translation'], float) or mask_row['Translation'] == 'Translation': 
				if 'ENG' in country_language:
					if isinstance(mask_row['Translatable Element'], float):
						return df_questionnaire
					else:
						text = mask_row['Translatable Element']
				else:
					return df_questionnaire
			else:
				text = mask_row['Translation'] 

			if text != '':
				if re.compile('^Religion\s\d+$').match(text) is None and re.compile('^Education\s\d+$').match(text) is None and re.compile('^PARTY\s\d+').match(text) is None:
					item_name = row['QuestionName']

					data = {'Study':study, 'module': get_module(row, module_dict), 
					'item_type':'RESPONSE', 'item_name': item_name, 'item_value':mask_row['QuestionElementNr'], 
					'text':clean_text(text), 'QuestionElement': mask_row['QuestionElement'], 'QuestionElementNr': mask_row['QuestionElementNr']}
					df_questionnaire = df_questionnaire.append(data, ignore_index = True)	


	return df_questionnaire

def post_process_instruction(df_instruction, df_request, df_post, survey_item_prefix):
	for i, row in df_instruction.iterrows():
		if df_post.empty == False:
			last_row = df_post.iloc[-1]
			if last_row['text'] != row['text']:
				if 'QItem' in df_request.QuestionElement.unique():
					rowqitem = df_request[df_request['QuestionElement']=='QItem']
					item_name = adjust_item_name(rowqitem['QuestionElementNr'].values[0], rowqitem['item_name'].values[0])
				else:
					item_name = row['item_name']

				if df_post.empty:
					survey_item_id = ut.get_survey_item_id(survey_item_prefix)
				else:
					survey_item_id = ut.update_survey_item_id(survey_item_prefix)
							
				data = {'survey_item_ID': survey_item_id, 'Study':row['Study'], 'module':row['module'], 
					'item_type':row['item_type'], 'item_name': item_name, 'item_value':row['item_value'], 
					'text': row['text']}
				df_post = df_post.append(data, ignore_index=True)
		else:
			if 'QItem' in df_request.QuestionElement.unique():
				rowqitem = df_request[df_request['QuestionElement']=='QItem']
				item_name = adjust_item_name(rowqitem['QuestionElementNr'].values[0], rowqitem['item_name'].values[0])
			else:
				item_name = row['item_name']
				if df_post.empty:
					survey_item_id = ut.get_survey_item_id(survey_item_prefix)
				else:
					survey_item_id = ut.update_survey_item_id(survey_item_prefix)
							
				data = {'survey_item_ID': survey_item_id, 'Study':row['Study'], 'module':row['module'], 
					'item_type':row['item_type'], 'item_name': item_name, 'item_value':row['item_value'], 
					'text': row['text']}
				df_post = df_post.append(data, ignore_index=True)

	return df_post

def post_process_request_response(df_request,  df_response, df_post, survey_item_prefix):
	for i, row in df_request.iterrows():
		if df_post.empty == False:
			last_row = df_post.iloc[-1]
			if last_row['text'] != row['text']:
				if 'QItem' in df_request.QuestionElement.unique():
					item_name = adjust_item_name(row['QuestionElementNr'], row['item_name'])
				else:
					item_name = row['item_name']

				if df_post.empty:
					survey_item_id = ut.get_survey_item_id(survey_item_prefix)
				else:
					survey_item_id = ut.update_survey_item_id(survey_item_prefix)
				
				data = {'survey_item_ID': survey_item_id, 'Study':row['Study'], 'module':row['module'], 
				'item_type':row['item_type'], 'item_name': item_name, 'item_value':row['item_value'], 
				'text': row['text']}
				df_post = df_post.append(data, ignore_index = True)

				if df_response.empty == False:
					if row['QuestionElement'] == 'QItem':
						for i, response_row in df_response.iterrows():
							data = {'survey_item_ID': ut.update_survey_item_id(survey_item_prefix), 'Study':response_row['Study'], 
							'module':response_row['module'], 'item_type':response_row['item_type'], 'item_name': item_name, 
							'item_value':response_row['item_value'], 'text': response_row['text']}
							df_post = df_post.append(data, ignore_index=True)
		else:
			if 'QItem' in df_request.QuestionElement.unique():
				item_name = adjust_item_name(row['QuestionElementNr'], row['item_name'])
			else:
				item_name = row['item_name']

			if df_post.empty:
				survey_item_id = ut.get_survey_item_id(survey_item_prefix)
			else:
				survey_item_id = ut.update_survey_item_id(survey_item_prefix)
				
			data = {'survey_item_ID': survey_item_id, 'Study':row['Study'], 'module':row['module'], 
				'item_type':row['item_type'], 'item_name': item_name, 'item_value':row['item_value'], 
				'text': row['text']}
			df_post = df_post.append(data, ignore_index = True)

			if df_response.empty == False:
				if row['QuestionElement'] == 'QItem':
					for i, response_row in df_response.iterrows():
						data = {'survey_item_ID': ut.update_survey_item_id(survey_item_prefix), 'Study':response_row['Study'], 
						'module':response_row['module'], 'item_type':response_row['item_type'], 'item_name': item_name, 
						'item_value':response_row['item_value'], 'text': response_row['text']}
						df_post = df_post.append(data, ignore_index=True)

	if df_response.empty == False:
		last_row = df_post.iloc[-1]
		if last_row['item_type'] != 'RESPONSE':
			for i, response_row in df_response.iterrows():
				data = {'survey_item_ID': ut.update_survey_item_id(survey_item_prefix), 'Study':response_row['Study'], 
					'module':response_row['module'], 'item_type':response_row['item_type'], 'item_name': last_row['item_name'], 
					'item_value':response_row['item_value'], 'text': response_row['text']}
				df_post = df_post.append(data, ignore_index=True)					

	return df_post

def questionnaire_post_processing(df_with_intro, survey_item_prefix):
	ut.reset_initial_sufix()

	df_post= pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 'text'])
	unique_item_names = df_with_intro.item_name.unique()

	for unique_item_name in unique_item_names:
		df_by_item_name = df_with_intro[df_with_intro['item_name']==unique_item_name]

		df_instruction = df_by_item_name[df_by_item_name['item_type']=='INSTRUCTION']
		df_introduction = df_by_item_name[df_by_item_name['item_type']=='INTRODUCTION']
		df_request = df_by_item_name[df_by_item_name['item_type']=='REQUEST']
		df_response = df_by_item_name[df_by_item_name['item_type']=='RESPONSE']

		del df_response['QuestionElement']

		if df_instruction.empty == False:
			df_post = post_process_instruction(df_instruction, df_request, df_post, survey_item_prefix)
			
		if df_introduction.empty == False:
			for i, row in df_introduction.iterrows():
				if 'QItem' in df_request.QuestionElement.unique():
					rowqitem = df_request[df_request['QuestionElement']=='QItem']
					item_name = adjust_item_name(rowqitem['QuestionElementNr'].values[0], rowqitem['item_name'].values[0])
				else:
					item_name = row['item_name']

				if df_post.empty:
					survey_item_id = ut.get_survey_item_id(survey_item_prefix)
				else:
					survey_item_id = ut.update_survey_item_id(survey_item_prefix)	

				data = {'survey_item_ID': survey_item_id, 'Study':row['Study'], 'module':row['module'], 
					'item_type':row['item_type'], 'item_name': item_name, 'item_value':row['item_value'], 
					'text': row['text']}
				df_post = df_post.append(data, ignore_index=True)

		df_post = post_process_request_response(df_request,  df_response, df_post, survey_item_prefix)

		

	return df_post

def fix_item_name_inconsistencies(df_questionnaire):
	"""
	Substitutes the item names like SECTION10, INTRO1, etc for item names in standardized format.
	If the item name has the aforementioned inconsistency, the method substitutes it for the next item
	name in df_questionnaire. Also sets the item type to INTRODUCTION if item name contains INTRO.

	Args:
		param1 df_questionnaire (pandas dataframe): name of the input file.

	Returns: 
		df_with_intro (pandas dataframe) with updated rows where the aforementioned incostistency was found.
		
	"""
	df_with_intro = pd.DataFrame(columns=['Study', 'module', 'item_type', 'item_name', 
		'item_value', 'text', 'QuestionElement', 'QuestionElementNr'])

	row_iterator = df_questionnaire.iterrows()
	_, last = next(row_iterator)  # take first item from row_iterator
	for i, row in row_iterator:
		if isinstance(last['item_name'], float):
			data = {'Study':last['Study'], 'module':last['module'], 
			'item_type':'INTRODUCTION', 'item_name':row['item_name'], 'item_value':last['item_value'], 'text': last['text'],
			'QuestionElement': last['QuestionElement'], 'QuestionElementNr': last['QuestionElementNr']}
		elif 'INTRO' in last['item_name'] or 'SECTION' in last['item_name']:
			data = {'Study':last['Study'], 'module':last['module'], 
			'item_type':'INTRODUCTION', 'item_name':row['item_name'], 'item_value':last['item_value'], 'text': last['text'],
			'QuestionElement': last['QuestionElement'], 'QuestionElementNr': last['QuestionElementNr']}
		else:
			data = {'Study':last['Study'], 'module':last['module'], 
			'item_type':last['item_type'], 'item_name':last['item_name'], 'item_value':last['item_value'], 'text': last['text'],
			'QuestionElement': last['QuestionElement'], 'QuestionElementNr': last['QuestionElementNr']}
		
		df_with_intro = df_with_intro.append(data, ignore_index = True)	
		last = row

	return df_with_intro




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
	df_questionnaire = pd.DataFrame(columns=['Study', 'module', 'item_type', 'item_name', 
		'item_value', 'text', 'QuestionElement', 'QuestionElementNr'])

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
	'D': "Respondent's parents/Respondent's partner", 'E': 'Socio demographics'}


	return df_questionnaire, survey_item_prefix, study, country_language,splitter, module_dict

def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)

	for index, file in enumerate(files):
		if file.endswith(".xlsx"):	
			print(file)
			df_questionnaire, survey_item_prefix, study, country_language,splitter, module_dict = set_initial_structures(file)

			constants = pd.read_excel(open(file, 'rb'), sheet_name='Constants')
			response_types = pd.read_excel(open(file, 'rb'), sheet_name='AnswerTypes')

			questionnaire = pd.read_excel(open(file, 'rb'), sheet_name='Questionnaire', dtype=str)
			questionnaire['TranslatableElement'] = questionnaire['TranslatableElement'].replace(['NA'],'NAext')
			questionnaire['Translated'] = questionnaire['Translated'].replace(['NA'],'NAext')
			questionnaire['TranslatableElement'] = questionnaire['TranslatableElement'].replace(['DK'],'DKext')
			questionnaire['Translated'] = questionnaire['Translated'].replace(['DK'],'DKext')

			#drop consecutive duplicates
			questionnaire = questionnaire.loc[questionnaire['Translated'].shift() != questionnaire['Translated']]
			# questionnaire = questionnaire.loc[questionnaire['TranslatableElement'].shift() != questionnaire['Translated']]

			if 'ENG' not in country_language:
				response_types = response_types[response_types['Translation'].notna()]
				constants = constants[constants['Translation'].notna()]
				
			for i, row in questionnaire.iterrows():
				if row['QuestionElement'] == 'Constant':
					df_questionnaire = process_constant_segment(constants, row, study, splitter, module_dict, df_questionnaire)
				elif row['QuestionElement'] in ['QInstruction', 'QItemInstruction', 'QItem', 'QIntro'] and row['QuestionName'] not in ['INTRO0', 'INTRO1']:
					df_questionnaire = process_request_segment(row, study, country_language, splitter, module_dict, df_questionnaire)
				elif row['QuestionElement'] == 'IWER':
					if row['QuestionName'] != 'IWER_INTRO' and isinstance(row['QuestionName'], str):
						df_questionnaire = process_instruction_segment(row, study, country_language, splitter, module_dict, df_questionnaire)
				elif row['QuestionElement'] == 'Answer':
					df_questionnaire = process_response_segment(row, study, country_language, module_dict, df_questionnaire)
				elif row['QuestionElement'] == 'AnswerType':
					df_questionnaire = process_response_type_segment(response_types, row['TranslatableElement'], row, study, 
					 country_language, module_dict, df_questionnaire)


			csv_name = file.replace('.xlsx', '')
			df_questionnaire.to_csv(csv_name+'.csv', encoding='utf-8-sig', index=False)
			df_with_intro = fix_item_name_inconsistencies(df_questionnaire)
			# df_with_intro.to_csv(csv_name+'intro.csv', encoding='utf-8-sig', index=False)
			df_post = questionnaire_post_processing(df_with_intro, survey_item_prefix)
			df_post.to_csv(csv_name+'.csv', encoding='utf-8-sig', sep='\t', index=False)



if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	print("Executing data cleaning/extraction script for EVS 2017")
	main(folder_path)
