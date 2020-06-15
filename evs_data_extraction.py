import pandas as pd
from populate_tables import *
import nltk.data
import numpy as np
import sys
import os
import re
from utils import *

initial_sufix = 0
constants_dict = dict()
response_types_dict = dict()
instruction_constants = ['ASKALL','C_CERT','INT_INS','R_LINE','R_ONLY','SHOWC','CHECK_APP','GO_TO','SKIP_MSG']
response_constants = ['DK', 'DKext', 'NA','NAext','NAP','OTHER','DK_cawi_mail','DKext_cawi_mail','NA_cawi_mail','NAext_cawi_mail','WOULD_NOT_MIND']

def clean_text(text):
	text = re.sub("…", "...", text)
	text = re.sub("’", "'", text)
	text = re.sub("[.]{4,}", "", text)
	tags = re.compile(r'<.*?>')
	text = tags.sub('', text)
	text = text.rstrip()


	return text

def update_item_id(survey_id):
	global initial_sufix
	prefix = survey_id+'_'
	survey_item_id = prefix+str(initial_sufix)
	initial_sufix = initial_sufix + 1

	return survey_item_id

def remove_trailing(clean):
	without_trailing = []
	for item in clean:
		item = item.rstrip()
		without_trailing.append(item)

	return without_trailing

def get_survey_info_and_populate_table(survey_id):
	split_items = survey_id.split('_')

	study = split_items[0]
	wave_round = split_items[3]
	year = split_items[-1]
	country_language = split_items[1]+'_'+split_items[2]

	write_survey_table(survey_id, study, wave_round, int(year), country_language)

def extract_response_types(response_types, a_response_type):
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
			else:
				ret = iter(filtered_response_types_df.TranslatableElement)
				ret = list(ret)

			clean_text_ret = []
			for item in ret:
				item = clean_text(item)
				clean_text_ret.append(item)

			
			response_types_dict[a_response_type] = clean_text_ret

	return ret

def extract_constant(constants, a_constant):
	filtered_constants_df = constants[constants['Code'] == a_constant]

	if a_constant in constants_dict:
		ret = constants_dict[a_constant]

	else:
		if filtered_constants_df.empty:
			ret = ''
		else:
			translated_cell = iter(filtered_constants_df.Translated)
			translated_cell = list(translated_cell)[0]
			
			if pd.notna(translated_cell) and translated_cell != 'Translation':
				ret = translated_cell
			else:
				ret = iter(filtered_constants_df.TranslatableElement)
				ret = list(ret)[0]

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
					
def decide_module(module_dict, row_module):
	if isinstance(row_module, float):
		module = module_dict['No module']
	else:
		module = module_dict[row_module]

	return module

def populate_introduction_table(df_survey_item):
	filtered_introduction_df = df_survey_item[df_survey_item['item_type'] == 'INTRODUCTION']
	for index, row in filtered_introduction_df.iterrows():
		print(row)
		survey_itemid = row['survey_itemid']
		final_text = row['text']
		item_name = row['item_name']
		item_type = row['item_type']
		write_introduction_table(survey_itemid, final_text, '', '', '', '', item_name, item_type)

def populate_instruction_table(df_survey_item):
	filtered_instruction_df = df_survey_item[df_survey_item['item_type'] == 'INSTRUCTION']
	for index, row in filtered_instruction_df.iterrows():
		print(row)
		survey_itemid = row['survey_itemid']
		final_text = row['text']
		item_name = row['item_name']
		item_type = row['item_type']
		write_instruction_table(survey_itemid, final_text, '', '', '', '', item_name, item_type)

def populate_response_table(df_survey_item):
	filtered_response_df = df_survey_item[df_survey_item['item_type'] == 'RESPONSE']
	for index, row in filtered_response_df.iterrows():
		print(row)
		survey_itemid = row['survey_itemid']
		final_text = row['text']
		item_name = row['item_name']
		item_type = row['item_type']
		if isinstance(row['item_value'], float):
			item_value = 0
		else:
			item_value = int(row['item_value'])
		write_response_table(survey_itemid, final_text, '', '', '', '', item_name, item_type, item_value)

def populate_request_table(df_survey_item):
	filtered_request_df = df_survey_item[df_survey_item['item_type'] == 'REQUEST']
	for index, row in filtered_request_df.iterrows():
		print(row)
		survey_itemid = row['survey_itemid']
		final_text = row['text']
		item_name = row['item_name']
		item_type = row['item_type']
		write_request_table(survey_itemid, final_text, '', '', '', '', item_name, item_type)



def main(filename):
	sentence_splitter_prefix = 'tokenizers/punkt/'

	sentence_splitter_suffix = determine_sentence_tokenizer(filename)

	sentence_splitter = sentence_splitter_prefix+sentence_splitter_suffix
	tokenizer = nltk.data.load(sentence_splitter)

	constants = pd.read_excel(open(filename, 'rb'), sheet_name='Constants')
	#dropping unecessary information
	constants = constants.drop(['QuestionElement', 'PAPI', 'CAPI', 'CAWI', 'MAIL'], axis=1)

	questionnaire = pd.read_excel(open(filename, 'rb'), sheet_name='Questionnaire')

	response_types = pd.read_excel(open(filename, 'rb'), sheet_name='AnswerTypes')

	#populate survey table
	survey_id = filename.replace('.xlsx', '')
	# get_survey_info_and_populate_table(survey_id)
	
	#populate module table
	list_unique_modules = questionnaire.Module.unique()
	list_unique_modules = ['No module' if isinstance(x, float) else x for x in list_unique_modules]
	# write_module_table(list_unique_modules)

	survey_last_id = get_survey_last_record()
	module_dict = get_module_table_as_dict()

	df_survey_item = pd.DataFrame(columns=['survey_itemid', 'text', 'surveyid', 'moduleid', 'item_type', 'item_name', 'item_value', 'item_is_source'])

	#put everything in df_survey_item to attribute survey_item IDs and then extract using item_type
	for index, row in questionnaire.iterrows(): 

		#case 1: Translated row is null = we only have the source text
		if pd.isna(row['Translated']):
			#item is a constant. A constant can be type: INSTRUCTION, INTRODUCTION or REQUEST
			if pd.notna(row['TranslatableElement']) and row['QuestionElement'] == 'Constant' and row['TranslatableElement'] not in response_constants:
				constant = row['TranslatableElement']
				survey_item = extract_constant(constants, constant)
				if survey_item == '':
					pass
				else:
					data = {"survey_itemid": update_item_id(survey_last_id), 'text': survey_item, 'surveyid': survey_last_id, 
						'moduleid': decide_module(module_dict, row['Module']), 'item_type': decide_item_type_constant(constant, row), 'item_name': check_item_name(row),
						'item_value': row['QuestionElementNr'], 'item_is_source': True}
					df_survey_item = df_survey_item.append(data, ignore_index = True)

			#item is a response. A response can be only type RESPONSE
			elif pd.notna(row['TranslatableElement']) and (row['QuestionElement'] == 'AnswerType' or row['QuestionElement'] == 'Answer' or 
				row['TranslatableElement'] in response_constants):
				response = row['TranslatableElement']
				if response in response_constants:
					survey_item = extract_constant(constants, response)
					if survey_item == '':
						pass
					else:
						data = {"survey_itemid": update_item_id(survey_last_id), 'text': clean_text(survey_item), 'surveyid': survey_last_id, 
						'moduleid': decide_module(module_dict, row['Module']), 'item_type':  'RESPONSE', 'item_name': check_item_name(row),
						'item_value': row['QuestionElementNr'],'item_is_source': True}
						df_survey_item = df_survey_item.append(data, ignore_index = True)
				elif row['QuestionElement'] == 'Answer':
					data = {"survey_itemid": update_item_id(survey_last_id), 'text': clean_text(response), 'surveyid': survey_last_id, 
					'moduleid': decide_module(module_dict, row['Module']), 'item_type':  'RESPONSE', 'item_name': check_item_name(row),
					'item_value': row['QuestionElementNr'],'item_is_source': True}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
				else:
					survey_item = extract_response_types(response_types, survey_item)
					if survey_item == '':
						pass
					else:
						for item in survey_item:
							data = {"survey_itemid": update_item_id(survey_last_id), 'text': item, 'surveyid': survey_last_id, 
							'moduleid': decide_module(module_dict, row['Module']), 'item_type':  'RESPONSE', 'item_name': check_item_name(row),
							'item_value': row['QuestionElementNr'],'item_is_source': True}
							df_survey_item = df_survey_item.append(data, ignore_index = True)

			#item type can be INTRODUCTION, INSTRUCTION or REQUEST
			else:
				if pd.notna(row['TranslatableElement']):
					survey_item = clean_text(row['TranslatableElement'])
					split_into_sentences = tokenizer.tokenize(survey_item)
					for item in split_into_sentences:
						data = {"survey_itemid": update_item_id(survey_last_id), 'text': item, 'surveyid': survey_last_id, 
						'moduleid': decide_module(module_dict, row['Module']), 'item_type': decide_item_type_other(row), 'item_name': check_item_name(row),
						'item_value': row['QuestionElementNr'],'item_is_source': True}
						df_survey_item = df_survey_item.append(data, ignore_index = True)
		


		#case 2: Translated row is not null = We have the tranlated text
		else:
			#item is a constant. A constant can be type: INSTRUCTION, INTRODUCTION or REQUEST
			if pd.notna(row['Translated']) and row['QuestionElement'] == 'Constant' and row['Translated'] not in response_constants:
				constant = row['Translated']
				survey_item = extract_constant(constants, constant)
				if survey_item == '':
					pass
				else:
					data = {"survey_itemid": update_item_id(survey_last_id), 'text': clean_text(survey_item), 'surveyid': survey_last_id, 
					'moduleid': decide_module(module_dict, row['Module']), 'item_type':  decide_item_type_constant(constant, row), 'item_name': check_item_name(row),
					'item_value': row['QuestionElementNr'],'item_is_source': False}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
			
			#item is a response. A response can be only type RESPONSE				
			elif pd.notna(row['Translated']) and (row['QuestionElement'] == 'AnswerType' or row['QuestionElement'] == 'Answer' or 
				row['Translated'] in response_constants):
				response = row['Translated']
				if response in response_constants:
					survey_item = extract_constant(constants, response)
					if survey_item == '':
						pass
					else:
						data = {"survey_itemid": update_item_id(survey_last_id), 'text': clean_text(survey_item), 'surveyid': survey_last_id, 
						'moduleid': decide_module(module_dict, row['Module']), 'item_type':  'RESPONSE', 'item_name': check_item_name(row),
						'item_value': row['QuestionElementNr'],'item_is_source': False}
						df_survey_item = df_survey_item.append(data, ignore_index = True)
				elif row['QuestionElement'] == 'Answer':
					data = {"survey_itemid": update_item_id(survey_last_id), 'text': clean_text(response), 'surveyid': survey_last_id, 
					'moduleid': decide_module(module_dict, row['Module']), 'item_type':  'RESPONSE', 'item_name': check_item_name(row),
					'item_value': row['QuestionElementNr'],'item_is_source': False}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
				else:
					survey_item = extract_response_types(response_types, survey_item)
					if survey_item == '':
						pass
					else:
						for item in survey_item:
							data = {"survey_itemid": update_item_id(survey_last_id), 'text': item, 'surveyid': survey_last_id, 
							'moduleid': decide_module(module_dict, row['Module']), 'item_type':  'RESPONSE', 'item_name': check_item_name(row),
							'item_value': row['QuestionElementNr'],'item_is_source': False}
							df_survey_item = df_survey_item.append(data, ignore_index = True)
			
			# item type can be INTRODUCTION, INSTRUCTION or REQUEST
			else:
				if pd.notna(row['Translated']):
					survey_item = clean_text(row['Translated'])
					split_into_sentences = tokenizer.tokenize(survey_item)
					for item in split_into_sentences:
						data = {"survey_itemid": update_item_id(survey_last_id), 'text': item, 'surveyid': survey_last_id, 
						'moduleid': decide_module(module_dict, row['Module']), 'item_type': decide_item_type_other(row), 
						'item_name': check_item_name(row),'item_value': row['QuestionElementNr'], 'item_is_source': False}
						df_survey_item = df_survey_item.append(data, ignore_index = True)
			

	filename_without_extension = filename.replace('.xlsx', '')
	split_items = filename_without_extension.split('_')
	country_language = split_items[1]+'_'+split_items[2]

	#populate survey item table
	for index, row in df_survey_item.iterrows():
		print(row)
	# 	survey_itemid = row['survey_itemid']
	# 	surveyid = row['surveyid']
	# 	moduleid = row['moduleid']
	# 	item_name = row['item_name']
	# 	item_type = row['item_type']
	# 	item_is_source = row['item_is_source']
	# 	write_survey_item_table(survey_itemid, surveyid, moduleid, country_language, item_is_source, item_name, item_type)

	# #populate introduction table
	# populate_introduction_table(df_survey_item)

	# #populate instruction table
	# populate_instruction_table(df_survey_item)

	# #populate response table
	# populate_response_table(df_survey_item)

	# #populate request table
	# populate_request_table(df_survey_item)
		

	

if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_data_extraction.py EVS_FRE_FR_R05_2017.xlsx
	filename = str(sys.argv[1])
	print("Executing data cleaning/extraction script for EVS 2017")
	main(filename)
