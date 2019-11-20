import pandas as pd
from populate_tables import *
import nltk.data
import numpy as np
import sys
import os
import re

initial_sufix = 0

def update_item_id(survey_id):
	global initial_sufix
	prefix = survey_id+'_'
	item_id = prefix+str(initial_sufix)
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

def extract_constant(constants, a_constant):
	filtered_constants_df = constants[constants['Code'] == a_constant]
	print(filtered_constants_df.Translated)
	# if pd.notna(filtered_constants_df.Translation):
	# 	ret = filtered_constants_df.Translation
	# else:
	# 	ret = filtered_constants_df.TranslatableElement

	# print(ret)

	return ret



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
	answer_types = pd.read_excel(open('data/'+str(filename), 'rb'), sheet_name='Questionnaire')

	# #populate survey table
	# survey_id = filename.replace('.xlsx', '')
	# get_survey_info_and_populate_table(survey_id)
	
	# #populate module table
	# list_unique_modules = questionnaire.Module.unique()
	# list_unique_modules = ['No module' if isinstance(x, float) else x for x in list_unique_modules]
	# write_module_table(list_unique_modules)

	df_survey_item = pd.DataFrame(columns=['survey_itemid', 'surveyid', 'moduleid', 'country_language', 'item_is_source'])

	#put everything in df_survey_item to attribute survey_item IDs and then extract using item_type
	for index, row in questionnaire.iterrows(): 
		if pd.isna(row['Translated']):
			if pd.notna(row['TranslatableElement']) and row['QuestionElement'] == 'Constant':
				survey_item = row['TranslatableElement']
				extract_constant(constants, survey_item)
				
			if pd.notna(row['TranslatableElement']) and row['QuestionElement'] == 'AnswerType':
				survey_item = row['TranslatableElement']
				# print(survey_item)

		else:
			if pd.notna(row['TranslatableElement']) and row['QuestionElement'] == 'Constant':
				survey_item = row['Translated']
				# print(survey_item)
			if pd.notna(row['TranslatableElement']) and row['QuestionElement'] == 'AnswerType':
				survey_item = row['Translated']
				# print(survey_item)
			





	

if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_data_extraction.py EVS_FRE_FR_R05_2017.xlsx
	filename = str(sys.argv[1])
	print("Executing data cleaning/extraction script for EVS 2017")
	main(filename)
