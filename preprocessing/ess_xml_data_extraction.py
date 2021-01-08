"""
Python3 script to transform XML ESS data into spreadsheet format used as input for MCSQ
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
"""
import xml.etree.ElementTree as ET
import pandas as pd 
import nltk.data
import sys
import re
import string
import utils as ut
from preprocessing_ess_utils import *



def clean_answer_category(text):
	"""
	Cleans the answer segment, by standardizing the text and removing undesired elements.

	Args:
		param1 text (string): answer segment currently being analyzed.

	Returns: 
		standardized answer text (string).
	"""
	if isinstance(text, str):
		text = re.sub(r"<br>\s?\s?\d+$", "", text)
		text = re.sub(r"<br />\s?\s?\d+$", "", text)
		text = re.sub(r"<br>\s?\s?\+\d+$", "", text)
		text = re.sub(r"<br />\s?\s?\-\d+$", "", text)
		text = re.sub(r"<br>\s?\s?\-\d+$", "", text)
		text = re.sub("…", "...", text)
		text = re.sub("’", "'", text)
		text = re.sub(" :", ":", text)
		text = re.sub("(\s0\s?$)", "", text)
		text = re.sub("(\s10\s?$)", "", text)
		text = re.sub("(\s\+\d\s?$)", "", text)
		text = re.sub("(\s\-\d\s?$)", "", text)
		text = re.sub("\s+\?", "?", text)
		text = re.sub("[.]{4,}", "", text)
		text = re.sub("[!]{2,}", "!", text)
		text = re.sub('</strong>', "",text)
		text = re.sub('<strong>', "",text)
		text = re.sub('</p>', "",text)
		text = re.sub('<p>', "",text)
		text = re.sub('</em>', "",text)
		text = re.sub('<em>', "",text)
		text = re.sub('</br>', " ",text)
		text = re.sub('<br />', " ",text)
		text = re.sub('<br>', " ",text)
		text = re.sub('<b><b>', " ",text)
		text = re.sub('</b></b>', " ",text)
		text = re.sub('<b>', " ",text)
		text = re.sub('</b>', " ",text)
		text = re.sub('</u>', " ",text)
		text = re.sub('<u>', " ",text)
		text = re.sub('&lt;', " ",text)
		text = re.sub('&gt;', " ",text)
		text = re.sub('&gt;', " ",text)
		text = re.sub('&lt', " ",text)
		text = re.sub('&gt', " ",text)
		text = re.sub('&nbsp', " ",text)
		text = re.sub(';', "",text)
		text = text.replace('------->','')
		text = text.replace('__________','')
		text = text.replace('________________________','')
		text = text.replace('\n','')
		text = text.replace('(','')
		text = text.replace(')','')
		text = text.replace('[','')
		text = text.replace(']','')
		text = text.replace('<i>','')
		text = text.replace('</i>','')
		text = text.replace('^footnote','')
		
		text = text.rstrip()
		text = text.lstrip()

		
	else:
		text = ''

	return text

def clean(text):
	"""
	Cleans the question or instruction segment, by standardizing the text and removing undesired elements.

	Args:
		param1 text (string): question or instruction segment currently being analyzed.

	Returns: 
		standardized question or instruction text (string).
	"""
	if isinstance(text, str):
		text = text.replace('\n','')
		text = text.replace('\r','')
		text = text.replace(' ?','?')
		text = re.sub("»", "", text)
		text = re.sub("^\s?\.\s?", "", text)
		text = re.sub("«", "", text)
		text = re.sub("…", "...", text)
		text = re.sub("’", "'", text)
		text = re.sub(" :", ":", text)
		text = re.sub("Enq.:", "Enquêteur:", text, flags=re.I)
		text = re.sub("INT.:", "INTERVIEWER:", text, flags=re.I)
		text = re.sub("[.]{4,}", "", text)
		text = re.sub("[!]{2,}", "!", text)
		text = re.sub('</strong>', "",text)
		text = re.sub('<strong>', "",text)
		text = re.sub('</p>', "",text)
		text = re.sub('<p>', "",text)
		text = re.sub('~', " ",text)
		text = re.sub('<b><b>', " ",text)
		text = re.sub('</b></b>', " ",text)
		text = re.sub('<b>', " ",text)
		text = re.sub('</b>', " ",text)
		text = re.sub('</em>', "",text)
		text = re.sub('<em>', "",text)
		text = re.sub('</br>', " ",text)
		text = re.sub('<br />', " ",text)
		text = re.sub('<br>', " ",text)
		text = re.sub('</u>', " ",text)
		text = re.sub('<u>', " ",text)
		text = re.sub('&lt;', " ",text)
		text = re.sub('&gt;', " ",text)
		text = re.sub('&gt;', " ",text)
		text = re.sub('&lt', " ",text)
		text = re.sub('&gt', " ",text)
		text = re.sub('&nbsp', " ",text)
		text = re.sub(';', "",text)
		text = text.replace('einfg.','einfügen')
		text = text.replace('[^footnote]','')
		text = text.replace('e.g','')
		text = text.replace('<P STYLE="text-align: left">','')
		text = text.replace('<P STYLE="text-align: right">','')
		text = text.replace('>','')
		text = text.replace('<','')

		
		text = text.rstrip()
		text = text.lstrip()
	else:
		text = ''


	return text

def identify_showcard_instruction(text, country_language):
	item_type = 'REQUEST'
	if 'FRE' in country_language:
		if 'CH' in country_language or 'BE' in country_language:
			showcard = 'CARTE'
		else:
			showcard = 'LISTE'
	if 'GER' in country_language:
		if 'CH' in country_language or 'AT' in country_language:
			showcard = 'KARTE'
		else:
			showcard = 'LISTE'

	if 'NOR' in country_language:
		showcard = 'KORT'

	if 'RUS' in country_language:
		showcard = 'КАРТОЧКУ'

	if 'ENG' in country_language:
		showcard = 'CARD'

	if re.compile(showcard).findall(text):
		item_type = 'INSTRUCTION'

	return item_type

def get_answer_id(node, parent_map):
	"""
	Gets the answer id from node attributes, if it exists
	Args:
		param1 node: current xml tree node being analyzed in outer loop.
		param2 parent_map (dictionary): a dictionary containing information about parent-child relationships in XML tree.

	Returns: 
		answer_id (string) if it exists, otherwise None.
	"""

	parent = parent_map[node]
	parent_of_parent = parent_map[parent]
	if 'answer_id' in parent_map[parent_of_parent].attrib:
		answer_id = parent_map[parent_of_parent].attrib['answer_id']
	else:
		answer_id = None

	return str(answer_id)

def segment_question_instruction(df_question_instruction, parent_map, node, item_name, item_type, splitter, country_language):
	if node.text != '' and  isinstance(node.text, str):
		sentences = splitter.tokenize(clean(node.text))
		item_name, modified_item_type = adjust_item_name(item_name)

		if item_name != 'REJECT QUESTION':
			if modified_item_type != None:
				item_type = modified_item_type

			for sentence in sentences:
				if item_type == 'REQUEST':
					data = {'answer_id': get_answer_id(node, parent_map), 'item_name':item_name,
					'item_type':identify_showcard_instruction(sentence, country_language), 'text':sentence}
					df_question_instruction = df_question_instruction.append(data, ignore_index=True)
				else:
					data = {'answer_id': None, 'item_name':item_name, 'item_type':item_type, 'text':sentence}
					df_question_instruction = df_question_instruction.append(data, ignore_index=True)
		else:
			return df_question_instruction

	return df_question_instruction

	

def adjust_item_name(item_name):
	"""
	Adjust item_name inconsistencies (and item_type in some cases) present in source XML file.
	Args:
		param1 item_name (string): item_name metadata, extracted from input file.

	Returns: 
		adjusted item_name and item_type metadata.
	"""
	
	if re.compile(r'F([2-4]|N)_0[2-9]').match(item_name) or item_name == 'Labels_in_F1_F4':
		item_name = 'REJECT QUESTION'
		item_type = None
	else:
		item_type = None
		if 'in' in item_name and 'minutes' not in item_name:
			item_name = item_name.split('in')
			item_name = item_name[1]
		if 'above' in item_name and '_' not in item_name:
			item_type = 'INTRODUCTION'
			item_name = item_name.split(' ')
			item_name = item_name[-1]
			return item_name, item_type
		if 'after' in item_name and '_' not in item_name:
			item_type = 'INTRODUCTION'
			item_name = item_name.split(' ')
			item_name = item_name[-1]
			return item_name, item_type
		if 'above' in item_name and '_' in item_name:
			item_type = 'INTRODUCTION'
			item_name = item_name.split('_')
			item_name = item_name[-1]
			return item_name, item_type
		if 'after' in item_name and '_' in item_name:
			item_type = 'INTRODUCTION'
			item_name = item_name.split('_')
			item_name = item_name[-1]
			return item_name, item_type
		if ' below ' in item_name:
			item_type = 'INTRODUCTION'
			item_name = item_name.split(' below ')
			item_name = item_name[-1]
			return item_name, item_type
		if '_' in item_name:
			item_name = item_name.split('_')
			item_name = item_name[0]
		if '.' in item_name:
			item_name = item_name.split('.')
			item_name = item_name[0]+item_name[1].lower()

		print(item_name)

	return item_name, item_type


def process_question_instruction_node(ess_questions_instructions, df_question_instruction, parent_map, splitter, country_language, extract_source):
	"""
	Iterates through question nodes to extract questions and instructions (introduction is not present in metadata)
	Args:
		param1 ess_questions_instructions: question and instruction nodes.
		param2 df_question_instruction (pandas dataframe): a dataframe to store processed question and instruction segments
		param3 parent_map (dictionary): a dictionary containing information about parent-child relationships in XML tree.
		param4 splitter (NLTK object): sentence segmentation from NLTK library.
		param5 country_language (string): country and language metadata, extracted from the input file name.

	Returns: 
		Updated df_question_instruction dataframe, with new question and instruction segments.
	"""
	for question in ess_questions_instructions:
		for node in question.getiterator():
			if node.tag == 'question' and 'name' in node.attrib and 'tmt_id' in node.attrib:
				item_name = node.attrib['name']

			"""
			translation_id == 1 is the english version
			"""
			if extract_source == 1:
				if node.tag == 'text' and 'translation_id' in node.attrib and node.attrib['translation_id'] == '1':
					if 'type_name' in parent_map[node].attrib and parent_map[node].attrib['type_name'] == 'QText':
						text = node.text
						item_type = 'REQUEST'
						df_question_instruction = segment_question_instruction(df_question_instruction, parent_map, node, item_name, item_type, splitter,
						 country_language)

					if 'type_name' in parent_map[node].attrib and parent_map[node].attrib['type_name'] == 'QInstruction':
						text = node.text
						item_type = 'INSTRUCTION'
						df_question_instruction = segment_question_instruction(df_question_instruction, parent_map, node, item_name, item_type, splitter, 
						 country_language)
			else:
				if node.tag == 'text' and 'translation_id' in node.attrib and node.attrib['translation_id'] != '1':
					if 'type_name' in parent_map[node].attrib and parent_map[node].attrib['type_name'] == 'QText':
						text = node.text
						item_type = 'REQUEST'
						df_question_instruction = segment_question_instruction(df_question_instruction, parent_map, node, item_name, item_type, splitter,
						 country_language)

					if 'type_name' in parent_map[node].attrib and parent_map[node].attrib['type_name'] == 'QInstruction':
						text = node.text
						item_type = 'INSTRUCTION'
						df_question_instruction = segment_question_instruction(df_question_instruction, parent_map, node, item_name, item_type, splitter, 
						 country_language)

	return df_question_instruction


def process_answer_node(ess_answers, df_answers, parent_map, ess_special_answer_categories, extract_source):
	"""
	Iterates through answer nodes to extract answers 

	Args:
		param1 ess_answers: answer nodes.
		param2 df_answers (pandas dataframe): a dataframe to store processed answer segments
		param3 parent_map (dictionary): a dictionary containing information about parent-child relationships in XML tree.
		param4 ess_special_answer_categories (Python object): instance of SpecialAnswerCategories object, in accordance to the country_language.


	Returns: 
		Updated df_answers dataframe, with new answer segments.
	"""
	for answer in ess_answers:
		for node in answer.getiterator():
			if node.tag == 'answer' and 'name' in node.attrib and 'tmt_id' in node.attrib:
				item_name = node.attrib['name']
				if '_' in item_name:
					item_name = item_name.split('_')
					item_name = item_name[1]
			"""
			translation_id == 1 is the english version
			"""
			if extract_source == 1:
				if node.tag == 'text' and 'translation_id' in node.attrib and node.attrib['translation_id'] == '1':
					text = node.text
					if node.text != '' and  isinstance(node.text, str) and 'does not exist in' not in text:
						parent = parent_map[node]
						parent_of_parent = parent_map[parent]
						answer_id = parent_map[parent_of_parent].attrib['tmt_id']

						if 'labelvalue' in parent_map[node].attrib:
							item_value = parent_map[node].attrib['labelvalue']
						else:
							item_value = parent_map[node].attrib['order']
						
						text = clean_answer_category(text)

						if df_answers.empty ==False:
							last_row = df_answers.iloc[-1]
							if text != last_row['text']:
								text, item_value = check_if_answer_is_special_category(text, item_value, ess_special_answer_categories)
								if 'labelvalue' in parent_map[node].attrib and str(parent_map[node].attrib['labelvalue']) == str(text):
									pass
								else:				
									data = {'answer_id': answer_id, 'item_name': item_name, 'item_type':'RESPONSE', 
									'text': text, 'item_value': str(item_value)}
									df_answers = df_answers.append(data, ignore_index=True)
						else:
							text, item_value = check_if_answer_is_special_category(text, item_value, ess_special_answer_categories)
							if 'labelvalue' in parent_map[node].attrib and str(parent_map[node].attrib['labelvalue']) == str(text):
								pass
							else:				
								data = {'answer_id': answer_id, 'item_name': item_name, 'item_type':'RESPONSE', 
								'text': text, 'item_value': str(item_value)}
								df_answers = df_answers.append(data, ignore_index=True)

			else:
				if node.tag == 'text' and 'translation_id' in node.attrib and node.attrib['translation_id'] != '1':
					text = node.text
					if node.text != '' and  isinstance(node.text, str) and 'does not exist in' not in text:
						parent = parent_map[node]
						parent_of_parent = parent_map[parent]
						answer_id = parent_map[parent_of_parent].attrib['tmt_id']

						if 'labelvalue' in parent_map[node].attrib:
							item_value = parent_map[node].attrib['labelvalue']
						else:
							item_value = parent_map[node].attrib['order']
						
						text = clean_answer_category(text)

						if df_answers.empty ==False:
							last_row = df_answers.iloc[-1]
							if text != last_row['text']:
								text, item_value = check_if_answer_is_special_category(text, item_value, ess_special_answer_categories)
								if 'labelvalue' in parent_map[node].attrib and str(parent_map[node].attrib['labelvalue']) == str(text):
									pass
								else:				
									data = {'answer_id': answer_id, 'item_name': item_name, 'item_type':'RESPONSE', 
									'text': text, 'item_value': str(item_value)}
									df_answers = df_answers.append(data, ignore_index=True)
						else:
							text, item_value = check_if_answer_is_special_category(text, item_value, ess_special_answer_categories)
							if 'labelvalue' in parent_map[node].attrib and str(parent_map[node].attrib['labelvalue']) == str(text):
								pass
							else:				
								data = {'answer_id': answer_id, 'item_name': item_name, 'item_type':'RESPONSE', 
								'text': text, 'item_value': str(item_value)}
								df_answers = df_answers.append(data, ignore_index=True)

	return df_answers

def set_initial_structures(filename, extract_source):
	"""
	Set initial structures that are necessary for the extraction of each questionnaire.

	Args:
		param1 filename (string): name of the input file.

	Returns: 
		df_questionnaire to store questionnaire data (pandas dataframe),
		survey_item_prefix, which is the prefix of survey_item_ID (string), 
		study/country_language, which are metadata parameters embedded in the file name (string and string)
		and sentence splitter to segment request/instruction segments when necessary (NLTK object). 
	"""

	"""
	A pandas dataframe to store questionnaire data.
	"""
	df_questionnaire = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 'text'])

	"""
	The prefix of a EVS survey item is study+'_'+language+'_'+country+'_'
	"""
	if extract_source == 1 and 'ESS_R09' in filename:
		survey_item_prefix = 'ESS_R09_2018_ENG_SOURCE_'
	elif extract_source == 1 and 'ESS_R08' in filename:
		survey_item_prefix = 'ESS_R08_2016_ENG_SOURCE_'
	else:
		survey_item_prefix = re.sub('\.xml', '', filename)+'_'

	"""
	Reset the initial survey_id sufix, because main is called iterativelly for every file in folder.
	"""
	ut.reset_initial_sufix()

	"""
	Retrieve study and country_language information from the name of the input file. 
	"""
	if extract_source == 1 and 'ESS_R09' in filename:
		study, country_language = get_country_language_and_study_info('ESS_R09_2018_ENG_SOURCE')
	elif extract_source == 1 and 'ESS_R08' in filename:
		study, country_language = get_country_language_and_study_info('ESS_R08_2016_ENG_SOURCE')
	else:
		study, country_language = get_country_language_and_study_info(filename)

	"""
	Instantiate a NLTK sentence splitter based on file input language. 
	"""
	if extract_source == 1:
		splitter = ut.get_sentence_splitter('ESS_R09_2018_ENG_SOURCE')
	else:	
		splitter = ut.get_sentence_splitter(filename)


	return df_questionnaire, survey_item_prefix, study, country_language,splitter


def main(filename):
	extract_source = 1

	"""
	Parse the input XML file by filename
	"""
	file = str(filename)
	tree = ET.parse(file)
	root = tree.getroot()

	"""
	Create a dictionary containing parent-child relations of the parsed tree
	"""
	parent_map = dict((c, p) for p in tree.getiterator() for c in p)
	ess_questions_instructions = root.findall('.//questionnaire/questions')
	ess_answers = root.findall('.//questionnaire/answers')
	ess_showcards = root.findall('.//questionnaire/showcards')

	df_questionnaire, survey_item_prefix, study, country_language,splitter = set_initial_structures(filename, extract_source)
	ess_special_answer_categories = instantiate_special_answer_category_object(country_language)

	if 'GER_AT' in filename:
		ess_special_answer_categories.refuse[0] = 'Verweigert'
		ess_special_answer_categories.dont_know[0] = 'Weiß nicht'

	if 'GER_CH' in filename:
		ess_special_answer_categories.refuse[0] = 'Antwort verweigert'
		ess_special_answer_categories.dont_know[0] = 'Weiss nicht'

	if 'GER_DE' in filename:
		ess_special_answer_categories.refuse[0] = 'Antwort verweigert'

	if 'NOR_NO' in filename:
		ess_special_answer_categories.refuse[0] = 'Nekter'



	df_question_instruction =  pd.DataFrame(columns=['answer_id', 'item_name', 'item_type', 'text']) 
	df_answers =  pd.DataFrame(columns=['answer_id', 'item_name', 'text', 'item_value']) 
	item_value = None

	df_question_instruction = process_question_instruction_node(ess_questions_instructions, df_question_instruction, parent_map, 
		splitter, country_language, extract_source)
	df_answers = process_answer_node(ess_answers, df_answers, parent_map, ess_special_answer_categories, extract_source)

	
	unique_item_names_question_instruction = df_question_instruction.item_name.unique()	
	
	for unique_item_name in unique_item_names_question_instruction:

		df_question_instruction_by_item_name = df_question_instruction[df_question_instruction['item_name'].str.lower()==unique_item_name.lower()]
		df_answers_by_item_name = df_answers[df_answers['item_name'].str.lower()==unique_item_name.lower()]
		module = retrieve_item_module(unique_item_name, study)

		last_item_name = ''
		for i, row in df_question_instruction_by_item_name.iterrows():
			item_name = row['item_name']

			if item_name =='Instruction' or item_name == 'Intro':
				item_name = last_item_name
				
			if 'Row ' not in item_name and item_name != 'CI' and item_name != 'outro':

				if df_questionnaire.empty:
					survey_item_id = ut.get_survey_item_id(survey_item_prefix)
				else:
					survey_item_id = ut.update_survey_item_id(survey_item_prefix)

				data = {'survey_item_ID': survey_item_id, 'Study': study,
				'module': module, 'item_type': row['item_type'], 
				'item_name':  item_name, 'item_value':None, 'text': row['text']}
				df_questionnaire = df_questionnaire.append(data, ignore_index=True)

				last_item_name = item_name

		if df_answers_by_item_name.empty == False:
			for j, row in df_answers_by_item_name.iterrows():
				data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 'Study': study,
				'module': module,'item_type': row['item_type'], 
				'item_name':  item_name, 'item_value':row['item_value'], 'text':row['text']}
				df_questionnaire = df_questionnaire.append(data, ignore_index=True)
			
	# df_question_instruction.to_csv('questions.csv', encoding='utf-8-sig', index=False)
	# df_answers.to_csv('answers.csv', encoding='utf-8-sig', index=False)
	df_questionnaire.to_csv(survey_item_prefix[:-1]+'.csv', encoding='utf-8-sig', sep='\t', index=False)
	


if __name__ == "__main__":
	filename = str(sys.argv[1])
	print("Executing data cleaning/extraction script for ESS (xml files)")
	main(filename)
