import sys
import os
import re
import pandas as pd
from preprocessing_ess_utils import *
import utils as ut

scale_items_to_ignore = ['01', '02', '03', '04', '05', '06', '07', '08', '09']

"""
Extracts the raw items from ESS plain text file, based on an item name regex pattern.
Also excludes blank lines and non relevant scale items.
:param file: input ESS plain text file.
:returns: retrieved raw items, in a list. 
"""
def retrieve_raw_items_from_file(file):
	item_name_question_pattern = re.compile("(?:[A-K][A-Z]?\s?[1-9]{1,3}[a-z]?)+")
	
	lines = file.readlines()
	last_line = len(lines) - 1

	index_tags = []
	for i, line in enumerate(lines):
		if item_name_question_pattern.match(line):
			index_tags.append(i)

		raw_items = []
		for i, index in enumerate(index_tags):
			if index == index_tags[-1]:
				item = lines[index:]
			else:
				next_index_element = index_tags[i+1]
				item = lines[index:next_index_element]

			clean = []
			for subitem in item:
				subitem = subitem.rstrip()
				if subitem != '' and subitem not in scale_items_to_ignore:
					clean.append(subitem)

			raw_items.append(clean)

	return raw_items


"""
Extracts and processes the question segments from a raw item.
The question segments are always between the {QUESTION} and {ANSWERS} tags, 
for instance:

G2
{QUESTION}
Per a ell és important ser ric. 
Vol tenir molts diners i coses cares.

{ANSWERS}
Se sembla molt a mi
Se sembla a mi
Se sembla una mica a mi
Se sembla poc a mi
No se sembla a mi
No se sembla gens a mi

:param raw_item: raw item, retrieved in previous steps.
"""
def process_question_segment(raw_item, survey_item_prefix, study, item_name, df_questionnaire, splitter):
	index_question_tag = raw_item.index('{QUESTION}')
	index_answer_tag = raw_item.index('{ANSWERS}')

	question_segment = raw_item[index_question_tag+1:index_answer_tag]

	for item in question_segment:
		item = clean_text(item)
		if item != '':
			sentences = splitter.tokenize(item)
			for sentence in sentences:
				if df_questionnaire.empty:
					survey_item_id = ut.get_survey_item_id(survey_item_prefix)
				else:
					survey_item_id = ut.update_survey_item_id(survey_item_prefix)

				data = {"survey_item_ID": survey_item_id,'Study': study, 'module': None,'item_type': 'REQUEST', 
				'item_name': item_name, 'item_value': None,  'text': sentence}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire



def process_intro_segment(raw_item, survey_item_prefix, study, item_name, df_questionnaire, splitter):
	index_intro_tag = raw_item.index('{INTRO}')
	index_question_tag = raw_item.index('{QUESTION}')

	intro_segment = raw_item[index_intro_tag+1:index_question_tag]

	for item in intro_segment:
		item = clean_text(item)
		if item != '':
			sentences = splitter.tokenize(item)
			for sentence in sentences:
				if df_questionnaire.empty:
					survey_item_id = ut.get_survey_item_id(survey_item_prefix)
				else:
					survey_item_id = ut.update_survey_item_id(survey_item_prefix)

				data = {"survey_item_ID": survey_item_id,'Study': study, 'module': None,'item_type': 'INTRODUCTION', 
				'item_name': item_name, 'item_value': None,  'text': sentence}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire

def process_answer_segment(raw_item, survey_item_prefix, study, item_name, df_questionnaire):
	index_answer_tag = raw_item.index('{ANSWERS}')
	answer_segment = raw_item[index_answer_tag+1:]

	for i, item in enumerate(answer_segment):
		if df_questionnaire.empty:
			survey_item_id = ut.get_survey_item_id(survey_item_prefix)
		else:
			survey_item_id = ut.update_survey_item_id(survey_item_prefix)

		data = {"survey_item_ID": survey_item_id,'Study': study, 'module': None,'item_type': 'RESPONSE', 
		'item_name': item_name, 'item_value': i,  'text': item}
		df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire


"""
Set initial structures that are necessary for the extraction of each questionnaire.
:param filename: name of the input file.
:returns: df_questionnaire, response_dict, survey_item_prefix, study, country_language
"""
def set_initial_structures(filename):
	"""
	A pandas dataframe to store questionnaire data.
	"""
	df_questionnaire = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 'text'])

	"""
	A dictionary to store responses and its category values.
	"""
	response_dict = dict()
	"""
	The prefix of a EVS survey item is study+'_'+language+'_'+country+'_'
	"""
	survey_item_prefix = re.sub('\.txt', '', filename)+'_'

	"""
	Reset the initial survey_id sufix, because main is called iterativelly for every XML file in folder.
	"""
	ut.reset_initial_sufix()

	"""
	Retrieve study and country_language information from the name of the input file. 
	"""
	study, country_language = get_country_language_and_study_info(filename)

	print(filename)

	splitter = ut.get_sentence_splitter(filename)


	return df_questionnaire, response_dict, survey_item_prefix, study, country_language,splitter

def main(folder_path, concatenate_supplementary_questionnaire):
	path = os.chdir(folder_path)
	files = os.listdir(path)

	for index, file in enumerate(files):
		if file.endswith(".txt"):	
			with open(file, 'r') as f:
				df_questionnaire, response_dict, survey_item_prefix, study, country_language, splitter = set_initial_structures(file)
				raw_items = retrieve_raw_items_from_file(f)
				for raw_item in raw_items:
					item_name = raw_item[0]
					if '{INTRO}' in raw_item:
						df_questionnaire = process_intro_segment(raw_item, survey_item_prefix, study, item_name, df_questionnaire, splitter)
					df_questionnaire = process_question_segment(raw_item, survey_item_prefix, study, item_name, df_questionnaire, splitter)
					df_questionnaire = process_answer_segment(raw_item, survey_item_prefix, study, item_name, df_questionnaire)


			f.close()
			csv_name = file.replace('.txt', '')
			df_questionnaire.to_csv(str(csv_name)+'.csv', encoding='utf-8-sig', index=False)

	






if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	concatenate_supplementary_questionnaire = bool(sys.argv[2])
	main(folder_path, concatenate_supplementary_questionnaire)