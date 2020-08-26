import sys
import os
import re
import pandas as pd
from preprocessing_ess_utils import *
import utils as ut


scale_items_to_ignore = ['01', '02', '03', '04', '05', '06', '07', '08', '09',
'1', '2', '3', '4', '5', '6', '7', '8', '9']


"""
Extracts the raw items from ESS plain text file, based on an item name regex pattern.
Also excludes blank lines and non relevant scale items.
Args:
	param1 file (Python module): input ESS plain text file.

Returns: 
	retrieved raw items (list of strings). 
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

Args:
	param1 raw_item (list): raw survey item, retrieved in previous steps.
	param2 survey_item_prefix (string): prefix of survey_item_ID.
	param3 study (string): metadata parameter about study embedded in the file name.
	param4 item_name (string): item_name metadata parameter, retrieved in previous steps.
	param5 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.
	param6 splitter (NLTK object): sentence segmentation from NLTK library.
	param7 country_language (string): country_language metadata, embedded in file name.

Returns:
	updated df_questionnaire when new valid question segments are included, or df_questionnaire in the same state it
	was when no new valid question segments were included.
"""
def process_question_segment(raw_item, survey_item_prefix, study, item_name, df_questionnaire, splitter,country_language):
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

				sentence = expand_interviewer_abbreviations(sentence, country_language)

				if check_if_segment_is_instruction(sentence, country_language):
					item_type = 'INSTRUCTION'
				else:
					item_type = 'REQUEST'

				data = {"survey_item_ID": survey_item_id,'Study': study, 'module': retrieve_item_module(item_name, study),
				'item_type': item_type, 'item_name': item_name, 'item_value': None,  'text': sentence}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire


"""
Extracts and processes the introduction segments from a raw item.
The introduction segments are always between the item name and {QUESTION} tag, 
for instance:

{INTRO}
Ara m'agradaria fer-li algunes preguntes sobre política i el govern.

B1 
{QUESTION}
En quina mesura diria vostè que l'interessa la política? 
Vostè diria que l'interessa...

{ANSWERS}
Molt
Bastant 
Poc 
Gens 

Args:
	param1 raw_item (list): raw survey item, retrieved in previous steps.
	param2 survey_item_prefix (string): prefix of survey_item_ID.
	param3 study (string): metadata parameter about study embedded in the file name.
	param4 item_name (string): item_name metadata parameter, retrieved in previous steps.
	param5 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.
	param6 splitter (NLTK object): sentence segmentation from NLTK library.

Returns:
	updated df_questionnaire when new valid introduction segments are included, or df_questionnaire in 
	the same state it was when no new valid introduction segments were included.
"""
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

				data = {"survey_item_ID": survey_item_id,'Study': study, 'module': retrieve_item_module(item_name, study),
				'item_type': 'INTRODUCTION', 'item_name': item_name, 'item_value': None,  'text': sentence}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire


"""
Extracts and processes the answer segments from a raw item.
The answer segments are always after the {ANSWERS} tag.


Args:
	param1 raw_item (list): raw survey item, retrieved in previous steps.
	param2 survey_item_prefix (string): prefix of survey_item_ID.
	param3 study (string): metadata parameter about study embedded in the file name.
	param4 item_name (string): item_name metadata parameter, retrieved in previous steps.
	param5 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.
	param6 country_language (string): country_language metadata, embedded in file name.

Returns:
	updated df_questionnaire when new valid answer segments are included, or df_questionnaire in 
	the same state it was when no new valid answer segments were included.
"""
def process_answer_segment(raw_item, survey_item_prefix, study, item_name, df_questionnaire,country_language):
	index_answer_tag = raw_item.index('{ANSWERS}')
	answer_segment = raw_item[index_answer_tag+1:]

	ess_special_answer_categories = instantiate_special_answer_category_object(country_language)
	responses = []

	"""
	If there are no answer segments, then the answer segment is the corresponding to 
	'write down' for the target language.
	"""
	if not answer_segment:
		survey_item_id = ut.update_survey_item_id(survey_item_prefix)

		answer_text, item_value = ess_special_answer_categories.write_down[0], ess_special_answer_categories.write_down[1]

		data = {"survey_item_ID": survey_item_id,'Study': study, 'module': retrieve_item_module(item_name, study),
		'item_type': 'RESPONSE', 'item_name': item_name, 'item_value': item_value,  'text': answer_text}
		df_questionnaire = df_questionnaire.append(data, ignore_index = True)

	for i, item in enumerate(answer_segment):
		survey_item_id = ut.update_survey_item_id(survey_item_prefix)
		answer_text, answer_value = clean_answer(item,ess_special_answer_categories)
		
		if answer_text:
			if answer_value:
				item_value = answer_value
			else:
				item_value = i

			responses.append(answer_text)

			data = {"survey_item_ID": survey_item_id,'Study': study, 'module': retrieve_item_module(item_name, study),
			'item_type': 'RESPONSE', 'item_name': item_name, 'item_value': item_value,  'text': answer_text}
			df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	if ess_special_answer_categories.dont_know[0] not in responses:
		survey_item_id = ut.update_survey_item_id(survey_item_prefix)

		data = {"survey_item_ID": survey_item_id,'Study': study, 'module': retrieve_item_module(item_name, study),
		'item_type': 'RESPONSE', 'item_name': item_name, 'item_value': ess_special_answer_categories.dont_know[1],  
		'text': ess_special_answer_categories.dont_know[0]}
		df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	if ess_special_answer_categories.refuse[0] not in responses:
		survey_item_id = ut.update_survey_item_id(survey_item_prefix)

		data = {"survey_item_ID": survey_item_id,'Study': study, 'module': retrieve_item_module(item_name, study),
		'item_type': 'RESPONSE', 'item_name': item_name, 'item_value': ess_special_answer_categories.refuse[1],  
		'text': ess_special_answer_categories.refuse[0]}
		df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire


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
def set_initial_structures(filename):
	"""
	A pandas dataframe to store questionnaire data.
	"""
	df_questionnaire = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 'text'])

	"""
	The prefix of a EVS survey item is study+'_'+language+'_'+country+'_'
	"""
	survey_item_prefix = re.sub('\.txt', '', filename)+'_'

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

"""
Main method of the ESS plain text to spreadsheet data transformation algorithm.
The data is extracted from the plain text file (that obeys an internal specification
for the MCSQ project), preprocessed and receives appropriate metadata attribution.  

The algorithm outputs the csv representation of the df_questionnaire, used to store 
questionnaire data (pandas dataframe)

Args:
	param1 folder_path: path to the folder where the plain text files are.
"""
def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)

	for index, file in enumerate(files):
		if file.endswith(".txt"):	
			with open(file, 'r') as f:
				df_questionnaire, survey_item_prefix, study, country_language, splitter = set_initial_structures(file)
				raw_items = retrieve_raw_items_from_file(f)
				for raw_item in raw_items:
					item_name = raw_item[0]
					if '{INTRO}' in raw_item:
						df_questionnaire = process_intro_segment(raw_item, survey_item_prefix, study, item_name, df_questionnaire, splitter)
					df_questionnaire = process_question_segment(raw_item, survey_item_prefix, study, item_name, df_questionnaire, splitter,country_language)
					df_questionnaire = process_answer_segment(raw_item, survey_item_prefix, study, item_name, df_questionnaire,country_language)


			f.close()
			csv_name = file.replace('.txt', '')
			df_questionnaire.to_csv(str(csv_name)+'.csv', encoding='utf-8-sig', index=False)

	






if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)