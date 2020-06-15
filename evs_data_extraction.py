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


def dk_nr_standard(item_value):
	# Standard
	# Refusal 777
	# Don't know 888
	# Does not apply 999
	if isinstance(item_value, str) or isinstance(item_value, int):
		item_value = str(item_value)
		item_value = re.sub("[8]{1,}", "888", item_value)
		item_value = re.sub("[9]{1,}", "999", item_value)
		item_value = re.sub("[7]{1,}", "777", item_value)


	return item_value


def clean_text(text):
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
					

def replace_intro_in_item_name(next_item_name, item_name):
	if 'INTRO' in item_name:
		item_name = next_item_name

	return item_name

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
	
	list_unique_modules = questionnaire.Module.unique()
	list_unique_modules = ['No module' if isinstance(x, float) else x for x in list_unique_modules]

	filename_without_path = filename.split('/')[-1]
	filename_without_extension = filename_without_path.replace('.xlsx', '')
	metadata = filename_without_extension.split('_')
	study = metadata[0]+'_'+metadata[1]+'_'+metadata[2]
	country_language = metadata[3]+'_'+metadata[4]
	#The prefix is study+'_'+language+'_'+country+'_'
	prefix = filename_without_extension+'_'

	if 'ENG_SOURCE' in country_language:
		item_is_source = True
	else:
		item_is_source = False

	df = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', country_language, 'item_is_source'])
	row_iterator = questionnaire.iterrows()
	_, last = row_iterator.__next__()

	old_item_name = 'Q1'
	for index, row in row_iterator: 
		#case 1: Translated row is not null = We have the tranlated text
		if pd.isna(row['Translated']) == False and pd.isna(row['QuestionName']) == False:
			if row['QuestionName'] != 'IWER_INTRO' and row['QuestionName'] != 'INTRO0' and 'SECTION' not in row['QuestionName']:
				#item is a constant. A constant can be type: INSTRUCTION, INTRODUCTION or REQUEST
				if pd.notna(row['Translated']) and row['QuestionElement'] == 'Constant' and row['Translated'] not in response_constants:
					constant = row['Translated']
					text = extract_constant(constants, constant)
					next_item_name = row_iterator.__next__()
					next_item_name = next_item_name[1]['QuestionName']
					item_name = replace_intro_in_item_name(next_item_name, row['QuestionName']) 
					# item_name = check_item_name(row)
					if text != '':
						data = {'survey_item_ID':decide_on_survey_item_id(prefix, old_item_name, item_name), 'Study':study,
						'module': row['Module'], 'item_type':decide_item_type_constant(constant, row), 'item_name': item_name, 
						'item_value':None, country_language:clean_text(text), 'item_is_source': item_is_source}
						df = df.append(data, ignore_index = True)
						old_item_name = item_name
			
				#item is a response. A response can be only type RESPONSE				
				elif pd.notna(row['Translated']) and (row['QuestionElement'] == 'AnswerType' or row['QuestionElement'] == 'Answer' or 
					row['Translated'] in response_constants):
					response = row['Translated']
					if response in response_constants:
						text = extract_constant(constants, response)
						if text != '':
							item_name = row['QuestionName']
							# item_name = check_item_name(row)
							data = {'survey_item_ID':decide_on_survey_item_id(prefix, old_item_name, item_name), 'Study':study,
							'module': row['Module'], 'item_type':'RESPONSE', 'item_name':item_name, 
							'item_value':dk_nr_standard(row['QuestionElementNr']), country_language:clean_text(text), 'item_is_source': item_is_source}
							df = df.append(data, ignore_index = True)
							old_item_name = item_name
					elif row['QuestionElement'] == 'Answer':
						item_name = row['QuestionName']
						# item_name = check_item_name(row)
						data = {'survey_item_ID':decide_on_survey_item_id(prefix, old_item_name, item_name), 'Study':study,
						'module': row['Module'], 'item_type':'RESPONSE', 'item_name':item_name, 
						'item_value':dk_nr_standard(row['QuestionElementNr']), country_language:clean_text(response), 'item_is_source': item_is_source}
						df = df.append(data, ignore_index = True)
						old_item_name = item_name
					else:
						text = extract_response_types(response_types, text)
						item_name = row['QuestionName']
						# item_name = check_item_name(row)
						if text != '':
							for item in text:
								data = {'survey_item_ID':decide_on_survey_item_id(prefix, old_item_name, item_name), 'Study':study,
								'module': row['Module'], 'item_type':'RESPONSE', 'item_name':item_name, 
								'item_value':dk_nr_standard(row['QuestionElementNr']), country_language:clean_text(item), 'item_is_source': item_is_source}
								df = df.append(data, ignore_index = True)
								old_item_name = item_name

			
				# item type can be INTRODUCTION, INSTRUCTION or REQUEST
				else:
					if pd.notna(row['Translated']):
						text = clean_text(row['Translated'])
						next_item_name = row_iterator.__next__()
						next_item_name = next_item_name[1]['QuestionName']
						item_name = replace_intro_in_item_name(next_item_name, row['QuestionName']) 
						split_into_sentences = tokenizer.tokenize(text)
						for item in split_into_sentences:
							data = {'survey_item_ID':decide_on_survey_item_id(prefix, old_item_name, item_name), 'Study':study,
							'module': row['Module'], 'item_type':decide_item_type_other(row), 'item_name':item_name, 
							'item_value':None, country_language:clean_text(item), 'item_is_source': item_is_source}
							df = df.append(data, ignore_index = True)
							old_item_name = item_name
			
	df.to_csv(filename_without_extension+'.csv', encoding='utf-8-sig', index=False)



if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_data_extraction.py EVS_FRE_FR_R05_2017.xlsx
	filename = str(sys.argv[1])
	print("Executing data cleaning/extraction script for EVS 2017")
	main(filename)
