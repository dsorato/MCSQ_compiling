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
	if isinstance(text, str):
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
		text = text.replace('\n','')
		text = text.replace('(','')
		text = text.replace(')','')
		text = text.replace('[','')
		text = text.replace(']','')
		text = text.rstrip()
		text = text.lstrip()
	else:
		text = ''

	return text

def clean(text):
	if isinstance(text, str):
		text = text.replace('\n','')
		text = text.replace('\r','')
		text = text.replace(' ?','?')
		text = re.sub("»", "", text)
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
		if 'DE' in country_language:
			showcard = 'LISTE'

	if re.compile(showcard).findall(text):
		item_type = 'INSTRUCTION'

	return item_type

def get_answer_id(node, parent_map):
	#Get the answer id from node attributes, if it exists
	parent = parent_map[node]
	parent_of_parent = parent_map[parent]
	if 'answer_id' in parent_map[parent_of_parent].attrib:
		answer_id = parent_map[parent_of_parent].attrib['answer_id']
	else:
		answer_id = None

	return answer_id

def append_data_to_df(df_question_instruction, parent_map, node, item_name, item_type, splitter, country_language):
	if node.text != '' and  isinstance(node.text, str):
		print(node.text)
		sentences = splitter.tokenize(clean(node.text))
		print(sentences)

		item_name, modified_item_type = adjust_item_name(item_name)
		if modified_item_type != None:
			item_type = modified_item_type

		for sentence in sentences:
			if item_type == 'REQUEST':
				print(item_name, sentence)
				data = {'answer_id': get_answer_id(node, parent_map), 'item_name':item_name,
				'item_type':identify_showcard_instruction(sentence, country_language), 'text':sentence}
			else:
				data = {'answer_id': None, 'item_name':item_name, 
				'item_type':item_type, 'text':sentence}
			df_question_instruction = df_question_instruction.append(data, ignore_index=True)
	else:
		return df_question_instruction

	return df_question_instruction


#Automatically adjust item_name inconsistencies present in source XML file, 
#so it is in accordance to our standards.
def adjust_item_name(item_name):
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
	if '_' in item_name:
		item_name = item_name.split('_')
		item_name = item_name[0]

	print(item_name)
	return item_name, item_type


def process_question_instruction_node(ess_questions, df_question_instruction, parent_map, item_name, item_type, splitter, country_language):
	"""
	Iterates through question nodes to extract questions and instructions (introduction is not present in metadata)
	"""
	for question in ess_questions:
		for node in question.getiterator():
			if node.tag == 'question' and 'name' in node.attrib and 'tmt_id' in node.attrib:
				item_name = node.attrib['name']
			if node.tag == 'text' and 'translation_id' in node.attrib and node.attrib['translation_id'] != '1':
				if 'type_name' in parent_map[node].attrib and parent_map[node].attrib['type_name'] == 'QText':
					text = node.text
					item_type = 'REQUEST'
					df_question_instruction = append_data_to_df(df_question_instruction, parent_map, node, item_name, item_type, splitter,
					 country_language)

				if 'type_name' in parent_map[node].attrib and parent_map[node].attrib['type_name'] == 'QInstruction':
					text = node.text
					item_type = 'INSTRUCTION'
					df_question_instruction = append_data_to_df(df_question_instruction, parent_map, node, item_name, item_type, splitter, 
					 country_language)

	return df_question_instruction


def process_answer_node(ess_answers, df_answers, parent_map, item_name, item_type):
	"""
	Iterates through answer nodes to extract answers 
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
			if node.tag == 'text' and 'translation_id' in node.attrib and node.attrib['translation_id'] != '1':
				text = node.text
				if node.text != '' and  isinstance(node.text, str) and 'does not exist in' not in text:
					item_type = 'RESPONSE'
					parent = parent_map[node]
					parent_of_parent = parent_map[parent]
					answer_id = parent_map[parent_of_parent].attrib['tmt_id']
					item_value = parent_map[node].attrib['order']
					data = {'answer_id': answer_id, 'item_name': item_name, 'item_type':'RESPONSE', 
					'text': clean_answer_category(text), 'item_value': str(item_value)}
					df_answers = df_answers.append(data, ignore_index=True)

	return df_answers

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
	survey_item_prefix = re.sub('\.xml', '', filename)+'_'

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
	Reset the initial survey_id sufix, because main is called iterativelly for every file in folder.
	"""
	ut.reset_initial_sufix()

	"""
	Instantiate a NLTK sentence splitter based on file input language. 
	"""
	splitter = ut.get_sentence_splitter(filename)

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
	ess_questions = root.findall('.//questionnaire/questions')
	ess_answers = root.findall('.//questionnaire/answers')
	ess_showcards = root.findall('.//questionnaire/showcards')

	df_questionnaire, survey_item_prefix, study, country_language,splitter = set_initial_structures(filename)

	df_question_instruction =  pd.DataFrame(columns=['answer_id', 'item_name', 'item_type', 'text']) 
	df_answers =  pd.DataFrame(columns=['answer_id', 'item_name', 'item_type', 'text', 'item_value']) 
	item_name = ''
	text = ''
	item_type = ''
	item_value = None

	df_question_instruction = process_question_instruction_node(ess_questions, df_question_instruction, parent_map, item_name, 
		item_type, splitter, country_language)
	df_answers = process_answer_node(ess_answers, df_answers, parent_map, item_name, item_type)

	
	old_item_name = 'A1'
	for i, i_row in df_question_instruction.iterrows():
		item_name = i_row['item_name']
		data = {'survey_item_ID': ut.update_survey_item_id(survey_item_prefix), 'Study': study,
		'module':retrieve_item_module(item_name, study), 'item_type': i_row['item_type'], 
		'item_name':  item_name, 'item_value':None, 'text':i_row['text']}
		df_questionnaire = df_questionnaire.append(data, ignore_index=True)
		old_item_name = item_name

		corresponding_answer = df_answers[df_answers.item_name == i_row['item_name']]
		print(corresponding_answer)
		if corresponding_answer.empty == False and i_row['item_type'] == 'REQUEST':
			for j, j_row in corresponding_answer.iterrows():
				data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 'Study': study,
				'module':retrieve_item_module(item_name, study),'item_type': j_row['item_type'], 
				'item_name':  item_name, 'item_value':j_row['item_value'], 'text':j_row['text']}
				df_questionnaire = df_questionnaire.append(data, ignore_index=True)
			
	df_question_instruction.to_csv('questions.csv', encoding='utf-8-sig', index=False)
	df_answers.to_csv('answers.csv', encoding='utf-8-sig', index=False)
	df_questionnaire.to_csv(survey_item_prefix[:-1]+'.csv', encoding='utf-8-sig', index=False)
	


if __name__ == "__main__":
	filename = str(sys.argv[1])
	print("Executing data cleaning/extraction script for ESS R08 (xml files)")
	main(filename)
