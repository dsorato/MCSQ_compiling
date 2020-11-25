"""
Python3 script (work in progress) to extract data from XML SHARE input files
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 
import xml.etree.ElementTree as ET
import pandas as pd
import sys
import re
import utils as ut
from preprocessing_ess_utils import *



def replace_fill_in_answer(text):
	text = re.sub('\^FLCurr', 'euros', text)
	text = re.sub('\^img_infinity_correct_copy', '', text)
	text = re.sub('\^img_infinity_incorrect_copy', '', text)
	

	return text

def clean_text(text, country_language):
	text = text.replace('<b>', '')
	text = text.replace('.?', '?')
	text = text.replace('</b>', '')
	text = text.replace('<br>', '')
	text = text.replace('<br />', '')
	text = text.replace('<strong>', '')
	text = text.replace('</strong>', '')
	text = text.replace('&nbsp;', ' ')
	text = text.replace('<em>', ' ')
	text = text.replace('</em>', ' ')
	text = text.replace('@B', '')
	text = text.replace('@b', ' ')
	text = text.replace('\n', ' ').replace('\r', '')
	text = text.replace('}', '')
	text = text.replace('{', '')
	text = re.sub('^\s?\d+\.\s', '', text)

	if 'ENG' not in country_language:
		text = text.replace('else', ' ')

	
	text = text.rstrip()

	if text == '':
		text = None

	return text

"""
Extract answers text from XML node

:param name: name of the answer structure inside XML file
:param subnode: child node being analyzed in outer loop
:param df_answers: pandas dataframe containing answers extracted from XML file
:returns: answers dataframe, with new answer category retrieved (when appliable)
"""
def extract_answers(subnode, df_answers, name, country_language):
	for child in subnode.getiterator():
		if child.tag == 'answer_element':
			item_value = child.attrib['labelvalue']
			text_nodes = child.findall('text')
			for text_node in text_nodes:
				if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
					text = clean_text(text_node.text, country_language)
					if re.compile('\^PreloadChild').match(text) is None and re.compile('\^FLChild').match(text) is None and re.compile('\^FLSNmember').match(text) is None:
						data = {'item_name': name, 'item_value':item_value, 'text': text}
						df_answers = df_answers.append(data, ignore_index = True)

	return df_answers


"""
Extract questions text from XML node

:param name: name of the answer structure inside XML file
:param subnode: child node being analyzed in outer loop
:param df_questions: pandas dataframe containing questions extracted from XML file
:returns: questions dataframe, with new question retrieved (when appliable)
"""
def extract_questions_and_procedures(subnode, df_questions, df_procedures, parent_map, name, splitter, country_language):
	for child in subnode.getiterator():
		if child.tag == 'question_element' and 'type_name' in child.attrib:
			if child.attrib['type_name'] == 'QText':
				text_nodes = child.findall('text')
				for text_node in text_nodes:
					if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
						text = clean_text(text_node.text, country_language)
						sentences = splitter.tokenize(text)
						for sentence in sentences:
							data = {'item_name': name, 'text': sentence}
							df_questions = df_questions.append(data, ignore_index = True)
		elif child.tag == 'procedure':
			proc_name = child.attrib['name']
			fills = child.find('fills')
			fill_nodes = fills.findall('fill')
			for fill_node in fill_nodes:
				fill_name = fill_node.attrib['name']
				fill_option_nodes = fill_node.findall('fill_option')

				for fill_option_node in fill_option_nodes:
					text_nodes = fill_option_node.findall('text')
					for text_node in text_nodes:
						if text_node.attrib['translation_id'] != '1' and text_node.text is not None and text_node.text != '{}':
							text = clean_text(text_node.text, country_language)
							order = parent_map[text_node].attrib['order']
							data = {'item_name': proc_name, 'fill_name':fill_name, 'order':order, 'text': text}
							df_procedures = df_procedures.append(data, ignore_index = True)


	return df_questions, df_procedures




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

def main(filename):
	"""
	Parse tree of input XML file.
	"""
	file = str(filename)
	tree = ET.parse(file)
	root = tree.getroot()

	"""
	Create a dictionary to map the information of node relations.
	"""
	parent_map = dict((c, p) for p in tree.getiterator() for c in p)

	df_questionnaire, survey_item_prefix, study, country_language,splitter = set_initial_structures(filename)

	questions = root.findall('.//questionnaire/questions')
	answers = root.findall('.//questionnaire/answers')

	df_answers = pd.DataFrame(columns=['item_name', 'item_value', 'text'])
	df_questions = pd.DataFrame(columns=['item_name', 'text'])
	df_procedures = pd.DataFrame(columns=['item_name', 'fill_name', 'order', 'text'])

	special_answer_categories = instantiate_special_answer_category_object(country_language)

	for node in questions:
		for subnode in node.getiterator():
			if subnode.tag == 'question':
				name = subnode.attrib['name']
				df_questions, df_procedures = extract_questions_and_procedures(subnode, df_questions, df_procedures, parent_map, name, splitter, country_language)

					
	for node in answers:
		for subnode in node.getiterator():
			if subnode.tag == 'answer':
				name = subnode.attrib['name']
				df_answers = extract_answers(subnode, df_answers, name, country_language)


	unique_question_item_names = df_questions.item_name.unique()
	for unique_item_name in unique_question_item_names:
		df_questions_by_item_name = df_questions[df_questions['item_name'].str.lower()==unique_item_name.lower()]
		df_answers_by_item_name = df_answers[df_answers['item_name'].str.lower()==unique_item_name.lower()]

		for i, row in df_questions_by_item_name.iterrows():
			if df_questionnaire.empty:
				survey_item_id = ut.get_survey_item_id(survey_item_prefix)
			else:
				survey_item_id = ut.update_survey_item_id(survey_item_prefix)	

			data = {'survey_item_ID':survey_item_id, 'Study':'SHA_2019', 'module': None, 'item_type':'REQUEST', 'item_name':row['item_name'], 
			'item_value':None, 'text':row['text']}
			df_questionnaire = df_questionnaire.append(data, ignore_index = True)

		if df_answers_by_item_name.empty == False:
			for i, row in df_answers_by_item_name.iterrows():
				survey_item_id = ut.update_survey_item_id(survey_item_prefix)	
				text = replace_fill_in_answer(row['text'])
				

				data = {'survey_item_ID':survey_item_id, 'Study':'SHA_2019', 'module': None, 'item_type':'RESPONSE', 'item_name':row['item_name'], 
				'item_value':row['item_value'], 'text':text}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)
		else:
			survey_item_id = ut.update_survey_item_id(survey_item_prefix)
			answer_text, item_value = special_answer_categories.write_down[0], special_answer_categories.write_down[1]
			last_row = df_questionnaire.iloc[-1]

			data = {"survey_item_ID": survey_item_id,'Study':'SHA_2019', 'module': None, 
			'item_type': 'RESPONSE', 'item_name': last_row['item_name'], 'item_value': item_value,  'text': answer_text}
			df_questionnaire = df_questionnaire.append(data, ignore_index = True)



				
							
	


	df_answers.to_csv('share_answers.csv', encoding='utf-8', index=False)
	df_questions.to_csv('share_questions.csv', encoding='utf-8', index=False)
	df_procedures.to_csv('share_procedures.csv', encoding='utf-8', index=False)
	df_questionnaire.to_csv('df_questionnaire.csv', encoding='utf-8', index=False)


"""
main method is executed for each file inside the given directory.
"""
if __name__ == "__main__":
	filename = str(sys.argv[1])
	print("Executing data extraction script for SHARE wave 8 (xml files)")
	main(filename)
