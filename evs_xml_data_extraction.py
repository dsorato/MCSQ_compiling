import xml.etree.ElementTree as ET
import pandas as pd 
import nltk.data
import sys
import re

initial_sufix = 0

def update_item_id(survey_id):
	global initial_sufix
	prefix = survey_id+'_'
	survey_item_id = prefix+str(initial_sufix)
	initial_sufix = initial_sufix + 1

	return survey_item_id

def clean_text(text):
	if isinstance(text, str):
		text = re.sub("…", "...", text)
		text = re.sub("’", "'", text)
		text = re.sub("[.]{4,}", "", text)
		text = re.sub('>', "",text)
		text = re.sub('<', "",text)
		text = text.rstrip()
	else:
		text = ''


	return text


def main(filename):
	sentence_splitter_prefix = 'tokenizers/punkt/'

	if 'ENG' in filename:
		sentence_splitter_suffix = 'english.pickle'
	if 'FRE' in filename:
		sentence_splitter_suffix = 'french.pickle'
	if 'GER' in filename:
		sentence_splitter_suffix = 'german.pickle'

	sentence_splitter = sentence_splitter_prefix+sentence_splitter_suffix
	tokenizer = nltk.data.load(sentence_splitter)

	# parse an xml file by name
	file = 'data/'+str(filename)
	tree = ET.parse(file)
	root = tree.getroot()

	# labls = root.findall('.//dataDscr/var/labl')
	# qstnLit = root.findall('.//dataDscr/var/qstn/qstnLit')
	evs_vars = root.findall('.//dataDscr/var')

	survey_id = filename.replace('.xml', '')
	df_survey_item = pd.DataFrame(columns=['survey_itemid', 'item_type', 'item_name', 'item_value', 'text',  'item_is_source'])

	

	last_tag = 'tag'
	for var in evs_vars:
		for node in var.getiterator():
			text = ''
			item_type = ''
			item_value = ''
			qstn = var.find('qstn')
			if qstn is not None and 'seqNo' in qstn.attrib:
				item_name = qstn.attrib['seqNo']
			else:
				item_name = var.attrib['name']

			if node.tag=='preQTxt':
				text = clean_text(node.text)
				item_type = 'INTRO'
				split_into_sentences = tokenizer.tokenize(text)
				for item in split_into_sentences:
					data = {"survey_itemid": update_item_id(survey_id), 'item_type': item_type, 
					'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
					last_tag = node.tag

			if node.tag=='ivuInstr':
				text = clean_text(node.text)
				item_type = 'INSTRUCTION'
				split_into_sentences = tokenizer.tokenize(text)
				for item in split_into_sentences:
					data = {"survey_itemid": update_item_id(survey_id), 'item_type': item_type, 
					'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
					last_tag = node.tag

			if node.tag=='qstnLit':
				text = clean_text(node.text)
				item_type = 'REQUEST'
				split_into_sentences = tokenizer.tokenize(text)
				for item in split_into_sentences:
					data = {"survey_itemid": update_item_id(survey_id), 'item_type': item_type, 
					'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
					last_tag = node.tag

			if node.tag=='txt' and last_tag != 'catgry' and 'country' not in item_name and 'split' not in item_name:
				text = clean_text(node.text)
				print(text, last_tag)
				item_type = 'REQUEST'
				if 'level' in node.attrib:
					item_name = node.attrib['level']

				split_into_sentences = tokenizer.tokenize(text)
				for item in split_into_sentences:
					data = {"survey_itemid": update_item_id(survey_id), 'item_type': item_type, 
					'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
					last_tag = node.tag

			if node.tag=='catgry' and 'country' not in item_name and 'split' not in item_name:
				txt = node.find('txt')
				if txt is not None:
					text = clean_text(txt.text) 
					item_type = 'ANSWER'
					catValu = node.find('catValu')
					item_value = catValu.text
					split_into_sentences = tokenizer.tokenize(text)
					for item in split_into_sentences:
						data = {"survey_itemid": update_item_id(survey_id), 'item_type': item_type, 
						'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
						df_survey_item = df_survey_item.append(data, ignore_index = True)
						last_tag = node.tag


	


	df_survey_item.to_csv('test.csv')

		




if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_xml_data_extraction.py EVS_FRE_FR_R04_2008.xml
	filename = str(sys.argv[1])
	print("Executing data extraction script for EVS 2008 (xml files)")
	main(filename)
