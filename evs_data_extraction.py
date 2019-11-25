import pandas as pd
from populate_tables import *
import nltk.data
import numpy as np
import sys
import os
import re

initial_sufix = 0
constants_dict = dict()
answer_types_dict = dict()
instruction_constants = ['ASKALL','C_CERT','INT_INS','R_LINE','R_ONLY','SHOWC','CHECK_APP','GO_TO','SKIP_MSG']
answer_constants = ['DK', 'DKext', 'NA','NAext','NAP','OTHER','DK_cawi_mail','DKext_cawi_mail','NA_cawi_mail','NAext_cawi_mail','WOULD_NOT_MIND']

def clean_text(text):
	text = re.sub("…", "...", text)
	text = re.sub("’", "'", text)
	text = re.sub("\.\.\.\.\.\.\.\.\.\.\.\.\.", "", text)


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

	write_survey_table(surveyid, study, wave_round, int(year), country_language)

def extract_answer_types(answer_types, a_answer_type):
	filtered_answer_types_df = answer_types[answer_types['Code'] == a_answer_type]

	if a_answer_type in answer_types_dict:
		ret = answer_types_dict[a_answer_type]

	else:
		if filtered_answer_types_df.empty:
			ret = ''
		else:
			translated_cells = iter(filtered_answer_types_df.Translated)
			translated_cells = list(translated_cells)
			
			if pd.notna(translated_cells).all() and 'Translation' not in translated_cells:
				ret = translated_cells
			else:
				ret = iter(filtered_answer_types_df.TranslatableElement)
				ret = list(ret)

			clean_text_ret = []
			for item in ret:
				item = clean_text(item)
				clean_text_ret.append(item)

			
			answer_types_dict[a_answer_type] = clean_text_ret

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
		if 'INTRO' in question_name:
			ret =  'INTRO'
		else:
			ret =  'REQUEST'

	return ret

def check_item_name(row):
	if isinstance(row['VariableName'], str):
		ret = row['VariableName']
	else:
		ret =  row['QuestionName'] 

	return ret

def decide_item_type(constant, row):
	if constant in instruction_constants:
		item_type = 'INSTRUCTION'
	else:
		item_type = check_question_name(row['QuestionName'])

	return item_type

						


def main(filename):
	sentence_splitter_prefix = 'tokenizers/punkt/'

	if 'ENG' in filename:
		sentence_splitter_suffix = 'english.pickle'
	if 'FRE' in filename:
		sentence_splitter_suffix = 'french.pickle'
	if 'GER' in filename:
		sentence_splitter_suffix = 'german.pickle'

	constants = pd.read_excel(open('data/'+str(filename), 'rb'), sheet_name='Constants')
	#dropping unecessary information
	constants = constants.drop(['QuestionElement', 'PAPI', 'CAPI', 'CAWI', 'MAIL'], axis=1)

	questionnaire = pd.read_excel(open('data/'+str(filename), 'rb'), sheet_name='Questionnaire')

	answer_types = pd.read_excel(open('data/'+str(filename), 'rb'), sheet_name='AnswerTypes')

	# #populate survey table
	# survey_id = filename.replace('.xlsx', '')
	# get_survey_info_and_populate_table(survey_id)
	
	# #populate module table
	# list_unique_modules = questionnaire.Module.unique()
	# list_unique_modules = ['No module' if isinstance(x, float) else x for x in list_unique_modules]
	# write_module_table(list_unique_modules)

	survey_last_id = get_survey_last_record()

	df_survey_item = pd.DataFrame(columns=['survey_itemid', 'text', 'surveyid', 'moduleid', 'item_type', 'item_name'])

	#put everything in df_survey_item to attribute survey_item IDs and then extract using item_type
	for index, row in questionnaire.iterrows(): 
		#case 1: Translated row is null
		if pd.isna(row['Translated']):
			#item is a constant. A constant can be type: INSTRUCTION, INTRO or REQUEST
			if pd.notna(row['TranslatableElement']) and row['QuestionElement'] == 'Constant' and row['TranslatableElement'] not in answer_constants:
				constant = row['TranslatableElement']
				survey_item = extract_constant(constants, constant)
				if survey_item == '':
					pass
				else:
					data = {"survey_itemid": update_item_id(survey_last_id), 'text': survey_item, 'surveyid': survey_last_id, 
						'moduleid': row['Module'], 'item_type': decide_item_type(constant, row), 'item_name': check_item_name(row)}
					df_survey_item = df_survey_item.append(data, ignore_index = True)

			#item is a answer. A answer can be only type ANSWER
			elif pd.notna(row['TranslatableElement']) and (row['QuestionElement'] == 'AnswerType' or row['QuestionElement'] == 'Answer' or 
				row['TranslatableElement'] in answer_constants):
				answer = row['TranslatableElement']
				print('********************', answer)
				if answer in answer_constants:
					survey_item = extract_constant(constants, answer)
					if survey_item == '':
						pass
					else:
						data = {"survey_itemid": update_item_id(survey_last_id), 'text': clean_text(survey_item), 'surveyid': survey_last_id, 
						'moduleid': row['Module'], 'item_type':  'ANSWER', 'item_name': check_item_name(row)}
						df_survey_item = df_survey_item.append(data, ignore_index = True)
				elif row['QuestionElement'] == 'Answer':
					data = {"survey_itemid": update_item_id(survey_last_id), 'text': clean_text(answer), 'surveyid': survey_last_id, 
					'moduleid': row['Module'], 'item_type':  'ANSWER', 'item_name': check_item_name(row)}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
				else:
					survey_item = extract_answer_types(answer_types, survey_item)
					if survey_item == '':
						pass
					else:
						for item in survey_item:
							data = {"survey_itemid": update_item_id(survey_last_id), 'text': item, 'surveyid': survey_last_id, 
							'moduleid': row['Module'], 'item_type':  'ANSWER', 'item_name': check_item_name(row)}
							df_survey_item = df_survey_item.append(data, ignore_index = True)

			# else:
			# 	if pd.notna(row['TranslatableElement']):
			# 		survey_item = clean_text(row['TranslatableElement'])
			# 		data = {"survey_itemid": update_item_id(survey_last_id), 'text': survey_item, 'surveyid': survey_last_id, 
			# 		'moduleid': row['Module'], 'item_type': check_question_name(row['QuestionName']), 'item_name': check_item_name(row)}
			# 		df_survey_item = df_survey_item.append(data, ignore_index = True)
		


		#case 2: Translated row is not null
		else:
			#item is a constant. A constant can be type: INSTRUCTION, INTRO or REQUEST
			if pd.notna(row['Translated']) and row['QuestionElement'] == 'Constant' and row['Translated'] not in answer_constants:
				constant = row['Translated']
				survey_item = extract_constant(constants, constant)
				if survey_item == '':
					pass
				else:
					data = {"survey_itemid": update_item_id(survey_last_id), 'text': clean_text(survey_item), 'surveyid': survey_last_id, 
					'moduleid': row['Module'], 'item_type':  decide_item_type(constant, row), 'item_name': check_item_name(row)}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
			
			#item is a answer. A answer can be only type ANSWER				
			elif pd.notna(row['Translated']) and (row['QuestionElement'] == 'AnswerType' or row['QuestionElement'] == 'Answer' or 
				row['Translated'] in answer_constants):
				answer = row['Translated']
				print('********************', answer)
				if answer in answer_constants:
					survey_item = extract_constant(constants, answer)
					if survey_item == '':
						pass
					else:
						data = {"survey_itemid": update_item_id(survey_last_id), 'text': clean_text(survey_item), 'surveyid': survey_last_id, 
						'moduleid': row['Module'], 'item_type':  'ANSWER', 'item_name': check_item_name(row)}
						df_survey_item = df_survey_item.append(data, ignore_index = True)
				elif row['QuestionElement'] == 'Answer':
					data = {"survey_itemid": update_item_id(survey_last_id), 'text': clean_text(answer), 'surveyid': survey_last_id, 
					'moduleid': row['Module'], 'item_type':  'ANSWER', 'item_name': check_item_name(row)}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
				else:
					survey_item = extract_answer_types(answer_types, survey_item)
					if survey_item == '':
						pass
					else:
						for item in survey_item:
							data = {"survey_itemid": update_item_id(survey_last_id), 'text': item, 'surveyid': survey_last_id, 
							'moduleid': row['Module'], 'item_type':  'ANSWER', 'item_name': check_item_name(row)}
							df_survey_item = df_survey_item.append(data, ignore_index = True)
			# else:
			# 	if pd.notna(row['Translated']):
			# 		survey_item = clean_text(row['Translated'])
			# 		data = {"survey_itemid": update_item_id(survey_last_id), 'text': survey_item, 'surveyid': survey_last_id, 
			# 		'moduleid': row['Module'], 'item_type': check_question_name(row['QuestionName']), 'item_name': check_item_name(row)}
			# 		df_survey_item = df_survey_item.append(data, ignore_index = True)
			



	# for k, v in list(constants_dict.items()):
	# 	print(k,v)

	# print('*********')

	# for k, v in list(answer_types_dict.items()):
	# 	print(k,v)

	# print('*********')

	for index, row in df_survey_item.iterrows():
		print(row)

	

if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_data_extraction.py EVS_FRE_FR_R05_2017.xlsx
	filename = str(sys.argv[1])
	print("Executing data cleaning/extraction script for EVS 2017")
	main(filename)
