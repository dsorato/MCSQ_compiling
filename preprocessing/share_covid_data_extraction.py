import sys
import utils as ut
import nltk
import pandas as pd
import os
import re


def get_language_country_iso_codes(language_country):
	"""
	Returns the ISO codes for language and country based on the values retrieved from input file.
	Only for target languages of MCSQ.
	Args:
		param1 language_country (string): language and country information retrieved from input file.
	Returns:
		language_country (string). Variable representing the language and country metadata in ISO codes.
	"""
	if language_country in ['seSE', 'nlNL', 'dkDK', 'grGR', 'nlBE', 'heIL', 'arIL', 
	'siSI', 'hrHR', 'fiFI', 'bgBG', 'seFI', 'eeEE', 'plPL', 'roRO', 'skSK', 'mtMT', 
	'huHU', 'lvLV', 'ltLT',  'grCY']:
		return None
	elif language_country == 'en':
		return 'ENG_SOURCE'
	elif language_country == 'enMT':
		return 'ENG_MT'
	elif language_country == 'deAT':
		return 'GER_AT'
	elif language_country == 'deCH':
		return 'GER_CH'
	elif language_country == 'deDE':
		return 'GER_DE'
	elif language_country == 'deLU':
		return 'GER_LU'
	elif language_country == 'czCZ':
		return 'CZE_CZ'
	elif language_country == 'frFR':
		return 'FRE_FR'
	elif language_country == 'frCH':
		return 'FRE_CH'
	elif language_country == 'frBE':
		return 'FRE_BE'
	elif language_country == 'frLU':
		return 'FRE_LU'
	elif language_country == 'itIT':
		return 'ITA_IT'
	elif language_country == 'itCH':
		return 'ITA_CH'
	elif language_country == 'esES':
		return 'SPA_ES'
	elif language_country == 'ptPT':
		return 'POR_PT'
	elif language_country == 'ruEE':
		return 'RUS_EE'
	elif language_country == 'ruLV':
		return 'RUS_LV'
	elif language_country == 'ruIL':
		return 'RUS_IL'



def retrieve_module_from_item_name(item_name):
	"""
	Returns the module of the question based on the item_name variable.
	This information comes from http://www.share-project.org/special-data-sets/share-covid-19-questionnaire.html

	Args:
		param1 item_name (string): item_name information retrieved from input file.
	Returns:
		module (string). Module of the question.
	"""
	if 'CAA' in item_name or 'CADN' in item_name:
		return 'A - Intro and basic demographics'
	elif 'CAPH' in item_name or 'CAH' in item_name or 'CAMH' in item_name  and item_name != 'CAHH017_':
		return 'H - Health (physical and mental) and health behavior'
	elif 'CAC' in item_name and item_name != 'CACO007_':
		return 'C - Corona-related infection'
	elif 'CAQ' in item_name:
		return 'Q - Quality of healthcare'
	elif 'CAW' in item_name or 'CAEP' in item_name:
		return 'W - Work'
	elif 'CAE' in item_name or item_name == 'CACO007_' or item_name == 'CAHH017_':
		return 'E - Economic situation'
	elif 'CAS' in item_name:
		return 'S - Social Networks'
	elif 'CAF' in item_name:
		return 'F - Finale'

def set_initial_structures(language_country):
	"""
	Set initial structures that are necessary for the extraction of each questionnaire.

	Args:
		param1 language_country (string): language and country of the subdataframe being analyzed

	Returns: 
		df_questionnaire to store questionnaire data (pandas dataframe),
		survey_item_prefix, which is the prefix of survey_item_ID (string), 
		and sentence splitter to segment request/introduction/instruction segments when necessary (NLTK object). 
	"""

	"""
	A pandas dataframe to store questionnaire data.
	"""
	df_questionnaire = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 'text'])

	"""
	The prefix of a EVS survey item is study+'_'+language+'_'+country+'_'
	"""
	survey_item_prefix = 'SHA_COVID_2020_'+language_country+'_'

	"""
	Reset the initial survey_id sufix, because main is called iterativelly for every file in folder.
	"""
	ut.reset_initial_sufix()

	"""
	Instantiate a NLTK sentence splitter based on file input language. 
	"""
	splitter = ut.get_sentence_splitter(language_country)


	return df_questionnaire, survey_item_prefix, splitter


  

def replace_abbreviations_and_fills(sentence):
	"""
	Replaces abbreviations and fills text from the text of input file.
	Args:
		param1 sentence (string): text segment from input file.
	Returns:
		sentence (string). Text segment without abbreviations and fills text.
	"""
	if ' Ud.' in sentence:
		sentence = sentence.replace(' Ud.', ' usted')
	if ' R ' in sentence:
		sentence = sentence.replace(' R ', ' respondent ')
	if ' R.' in sentence:
		sentence = sentence.replace(' R.', ' respondent.')
	if " R's" in sentence:
		sentence = sentence.replace(" R's", " respondent's")
	if 'IWER' in sentence:
		sentence = sentence.replace('IWER', 'Interviewer')
	if '[FILL in name of CTL institution]' in sentence:
		sentence = sentence.replace('[FILL in name of CTL institution]', '[Institution]')
	if '[FILL in name of Survey Agency]' in sentence:
		sentence = sentence.replace('[FILL in name of Survey Agency]', '[Survey Agency]')
	if '[FILL in telephone number of survey agency]' in sentence:
		sentence = sentence.replace('[FILL in telephone number of survey agency]', '[Telephone of Survey Agency]')

		 

	sentence = re.sub(" :", ":", sentence)
	sentence = re.sub("’", "'", sentence)
	sentence = re.sub("…", "...", sentence)
	sentence = re.sub(" :", ":", sentence)
	sentence = re.sub("’", "'", sentence)
	sentence = sentence.replace("&nbsp;", " ")
	sentence = sentence.replace(" ?", "?")

	return sentence



def preprocess_answer_segment(row, df_questionnaire, survey_item_prefix, splitter):
	"""
	Extracts and processes the answer segments from the input file.

	Args:
		param1 row (pandas dataframe object): dataframe row being currently analyzed.
		param2 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.
		param3 survey_item_prefix (string): prefix of survey_item_ID.
		param4 splitter (NLTK object): NLTK object for sentence segmentation instantiated in accordance to the language.

	Returns:
		updated df_questionnaire with new valid answer segments.
	"""
	sentence = replace_abbreviations_and_fills(row['text'])

	if df_questionnaire.empty:
		survey_item_id = ut.get_survey_item_id(survey_item_prefix)
	else:
		survey_item_id = ut.update_survey_item_id(survey_item_prefix)

	data = {"survey_item_ID": survey_item_id,'Study': survey_item_prefix[:-1], 'module': retrieve_module_from_item_name(row['name']),
	'item_type': 'RESPONSE', 'item_name': row['name'], 'item_value': row['item_order'],  'text': sentence}
	df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire


def preprocess_question_segment(row, df_questionnaire, survey_item_prefix, splitter):
	"""
	Extracts and processes the question segments from the input file.

	Args:
		param1 row (pandas dataframe object): dataframe row being currently analyzed.
		param2 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.
		param3 survey_item_prefix (string): prefix of survey_item_ID.
		param4 splitter (NLTK object): NLTK object for sentence segmentation instantiated in accordance to the language.

	Returns:
		updated df_questionnaire with new valid question segments.
	"""
	raw_item = replace_abbreviations_and_fills(row['text'])
	sentences = splitter.tokenize(raw_item)
	for sentence in sentences:
		if df_questionnaire.empty:
			survey_item_id = ut.get_survey_item_id(survey_item_prefix)
		else:
			survey_item_id = ut.update_survey_item_id(survey_item_prefix)

		data = {"survey_item_ID": survey_item_id,'Study': survey_item_prefix[:-1], 'module': retrieve_module_from_item_name(row['name']),
		'item_type': 'REQUEST', 'item_name': row['name'], 'item_value': None,  'text': sentence}
		df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire

def preprocess_instruction_segment(row, df_questionnaire, survey_item_prefix, splitter):
	"""
	Extracts and processes the instruction segments from the input file.

	Args:
		param1 row (pandas dataframe object): dataframe row being currently analyzed.
		param2 df_questionnaire (pandas dataframe): pandas dataframe to store questionnaire data.
		param3 survey_item_prefix (string): prefix of survey_item_ID.
		param4 splitter (NLTK object): NLTK object for sentence segmentation instantiated in accordance to the language.

	Returns:
		updated df_questionnaire with new valid instruction segments.
	"""
	raw_item = replace_abbreviations_and_fills(row['text'])
	sentences = splitter.tokenize(raw_item)
	for sentence in sentences:
		if df_questionnaire.empty:
			survey_item_id = ut.get_survey_item_id(survey_item_prefix)
		else:
			survey_item_id = ut.update_survey_item_id(survey_item_prefix)

		data = {"survey_item_ID": survey_item_id,'Study': survey_item_prefix[:-1], 'module': retrieve_module_from_item_name(row['name']),
		'item_type': 'INSTRUCTION', 'item_name': row['name'], 'item_value': None,  'text': sentence}
		df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire


def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)

	for index, file in enumerate(files):
		if file.endswith(".csv"):
			questionnaire = pd.read_csv(file)
			unique_country_language_pairs = questionnaire['lang'].unique()

		for pair in unique_country_language_pairs:
			language_country = get_language_country_iso_codes(pair)
			if language_country: 
				df_questionnaire, survey_item_prefix, splitter = set_initial_structures(language_country)
				filter_df_by_lang = questionnaire['lang']==pair
				df = questionnaire[filter_df_by_lang]
				for i, row in df.iterrows():
					if row['item_type'] == 'QText':
						df_questionnaire = preprocess_question_segment(row, df_questionnaire, survey_item_prefix, splitter)
					elif row['item_type'] == 'Response option':
						df_questionnaire = preprocess_answer_segment(row, df_questionnaire, survey_item_prefix, splitter)
					elif row['item_type'] == 'QInstruction':
						df_questionnaire = preprocess_instruction_segment(row, df_questionnaire, survey_item_prefix, splitter)

				df_questionnaire.to_csv(survey_item_prefix[:-1]+'.csv', encoding='utf-8-sig', index=False)







if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	print("Executing data extraction script for SHARE COVID-19 questionnaires")
	main(folder_path)
