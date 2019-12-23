import xml.etree.ElementTree as ET
import pandas as pd 
import nltk.data
import sys
import re
import string
from utils import *


initial_sufix = 0
initial_request= ["Reporter sur votre: VOTRE CODE ENQUETEUR, VOTRE NOM , la date d'interview et le numéro d'interview:",
"Numéro d'interview"]


def update_item_id(survey_id):
	global initial_sufix
	prefix = survey_id+'_'
	survey_item_id = prefix+str(initial_sufix)
	initial_sufix = initial_sufix + 1

	return survey_item_id

def check_if_sentence_is_uppercase(text):
	is_uppercase = False
	if isinstance(text, str):
		for word in text:
			if word.isupper() and word not in string.punctuation:
				is_uppercase = True

	return is_uppercase

def clean_instruction(text):
	if isinstance(text, str):
		text = re.sub("…", "...", text)
		text = re.sub("’", "'", text)
		text = re.sub("[.]{4,}", "", text)
		text = re.sub('>', "",text)
		text = re.sub('<', "",text)
		text = re.sub('Q[0-9]*\.', "",text)
		text = re.sub('\[', "",text)
		text = re.sub('\]', "",text)
		text = text.replace('\n',' ')
		text = text.rstrip()
	else:
		text = ''


	return text



def clean_text(text):
	if isinstance(text, str):
		text = re.sub(" \?", "?", text)
		text = re.sub("…", "...", text)
		text = re.sub("’", "'", text)
		text = re.sub("[.]{4,}", "", text)
		text = re.sub("[_]{2,}", "", text)
		text = re.sub('>', "",text)
		text = re.sub('<', "",text)
		text = re.sub('Q[0-9]*\.', "",text)
		text = re.sub('\[', "",text)
		text = re.sub('\]', "",text)
		text = re.sub('^[A-Z]\.\s', "",text)
		text = re.sub('^[A-Z]\s', "",text)
		text = re.sub('S\.R\.', "SR",text)
		text = re.sub('S\.R', "SR",text)
		text = re.sub('SR\.', "SR",text)
		text = re.sub('s\.r', "SR",text)
		text = re.sub('s\.r\.', "SR",text)
		text = text.replace('\n',' ')
		text = text.rstrip()
	else:
		text = ''


	return text

def standartize_item_name(item_name):
	item_name = re.sub("\.", "", item_name)
	item_name = item_name.lower()
	item_name = re.sub("q", "Q", item_name)

	if '_'  in item_name:
		item_name = item_name.split('_')
		item_name = item_name[0]

	return item_name

def determine_survey_item_module(item_name, filename):
	module = 'No module'
	if 'Q' in item_name:

		digits_in_item_name = re.sub("[^\d]", "", item_name)
		# digits_in_item_name = re.sub("a", "", digits_in_item_name)
		# digits_in_item_name = re.sub("b", "", digits_in_item_name)
		# digits_in_item_name = re.sub("c", "", digits_in_item_name)
		# digits_in_item_name = re.sub("d", "", digits_in_item_name)
		# digits_in_item_name = re.sub("e", "", digits_in_item_name)
		# digits_in_item_name = re.sub("f", "", digits_in_item_name)
		# digits_in_item_name = re.sub("g", "", digits_in_item_name)
		# digits_in_item_name = re.sub("h", "", digits_in_item_name)

		if '/' in digits_in_item_name:
			digits_in_item_name = digits_in_item_name.split('/')
			digits_in_item_name = digits_in_item_name[0]
		# if '_'  in digits_in_item_name:
		# 	digits_in_item_name = digits_in_item_name.split('_')
		# 	digits_in_item_name = digits_in_item_name[0]


		digits_in_item_name = int(digits_in_item_name)
		


		if '2008' in filename:
			#QUESTIONS SUR LA VIE EN GÉNÉRAL, LES LOISIRS ET DE TRAVAIL
			if digits_in_item_name < 22:
				module = 'A'
			#QUESTIONS SUR LE SENS DE LA VIE
			if digits_in_item_name >= 22 and digits_in_item_name < 42:
				module = 'B'
			#LA FAMILLE ET DU MARIAGE
			if digits_in_item_name >= 42 and digits_in_item_name < 54:
				module = 'C'
			#QUESTIONS SUR DES SUJETS DE SOCIETE
			if digits_in_item_name >= 54 and digits_in_item_name < 86:
				module = 'D'
			#CARACTERISTIQUES DEMOGRAPHIQUES
			if digits_in_item_name >= 86:
				module = 'E'

		if '1999' in filename:
			#QUESTIONS SUR LA VIE EN GÉNÉRAL, LES LOISIRS
			if digits_in_item_name < 13:
				module = 'A'
			#TRAVAIL
			if digits_in_item_name >= 13 and digits_in_item_name < 21:
				module = 'B'
			#RELIGION
			if digits_in_item_name >= 21 and  digits_in_item_name < 40:
				module = 'C'
			#LA FAMILLE ET DU MARIAGE
			if digits_in_item_name >= 40 and digits_in_item_name < 51:
				module = 'D'
			#POLITIQUE
			if digits_in_item_name >= 51 and digits_in_item_name < 64:
				module = 'E'
			#SOCIETE (not so sure about where it starts...)
			if digits_in_item_name >= 64 and digits_in_item_name < 84:
				module = 'F'
			#CARACTERISTIQUES DEMOGRAPHIQUES
			if digits_in_item_name >= 84:
				module = 'G'

	return module




def main(filename):
	#Punkt Sentence Tokenizer from NLTK	
	sentence_splitter_prefix = 'tokenizers/punkt/'
	sentence_splitter_suffix = determine_sentence_tokenizer(filename)
	sentence_splitter = sentence_splitter_prefix+sentence_splitter_suffix
	tokenizer = nltk.data.load(sentence_splitter)

	country = determine_country(filename)

	# parse an xml file by name
	file = str(filename)
	tree = ET.parse(file)
	root = tree.getroot()

	# labls = root.findall('.//dataDscr/var/labl')
	# qstnLit = root.findall('.//dataDscr/var/qstn/qstnLit')
	evs_vars = root.findall('.//dataDscr/var')

	survey_id = filename.replace('.xml', '')
	df_survey_item = pd.DataFrame(columns=['survey_itemid', 'module','item_type', 'item_name', 'item_value', 'text',  'item_is_source'])

	

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
				elem_item_name = var.find('labl').text
				item_name = elem_item_name[elem_item_name.find("(")+1:elem_item_name.find(")")]

			item_name = standartize_item_name(item_name)
			# module = 'No module'
			
			if node.tag=='preQTxt':
				if is_uppercase == True:
					item_type = 'INSTRUCTION'
					text = clean_instruction(node.text)
				else:
					text = clean_text(node.text)
					item_type = 'INTRODUCTION'
				
				module = determine_survey_item_module(item_name, filename)

				split_into_sentences = tokenizer.tokenize(text)
				for item in split_into_sentences:
					data = {"survey_itemid": update_item_id(survey_id), 'module': module,'item_type': item_type, 
					'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
				last_tag = node.tag

			if node.tag=='ivuInstr':
				text = clean_instruction(node.text)	
				item_type = 'INSTRUCTION'
				module = determine_survey_item_module(item_name, filename)

				split_into_sentences = tokenizer.tokenize(text)
				for item in split_into_sentences:
					data = {"survey_itemid": update_item_id(survey_id), 'module': module,'item_type': item_type, 
					'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
				last_tag = node.tag

			if node.tag=='qstnLit':
				text = clean_text(node.text)
				item_type = 'REQUEST'
				print(text)
				if len(text) != 1 and text.isnumeric() == False:
					module = determine_survey_item_module(item_name, filename)
					if text in initial_request:
						split_into_sentences = tokenizer.tokenize(text)
						for item in split_into_sentences:
							data = {"survey_itemid": update_item_id(survey_id), 'module': module,'item_type': item_type, 
								'item_name': 'INTRODUCTION', 'item_value': item_value,  'text': item, 'item_is_source': False}
							df_survey_item = df_survey_item.append(data, ignore_index = True)
						last_tag = node.tag
					else:
						# item_type = 'REQUEST'
						split_into_sentences = tokenizer.tokenize(text)
						for item in split_into_sentences:
							data = {"survey_itemid": update_item_id(survey_id), 'module': module,'item_type': item_type, 
							'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
							df_survey_item = df_survey_item.append(data, ignore_index = True)
						last_tag = node.tag

			if node.tag=='txt' and last_tag != 'catgry' and 'country' not in item_name and 'split' not in item_name:
				is_uppercase = check_if_sentence_is_uppercase(node.text)
				text = clean_text(node.text)
				item_type = 'REQUEST'

				# if is_uppercase == True:
				# 	text = clean_instruction(node.text)
				# 	item_type = 'INSTRUCTION'
				# else:
					
				module = determine_survey_item_module(item_name, filename)
				# if 'level' in node.attrib:
				# 	item_name = node.attrib['level']
				# 	item_name = standartize_item_name(item_name)
				if 'sample' not in text and text != country: 
					split_into_sentences = tokenizer.tokenize(text)
					for item in split_into_sentences:
						data = {"survey_itemid": update_item_id(survey_id), 'module': module, 'item_type': item_type, 
						'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
						df_survey_item = df_survey_item.append(data, ignore_index = True)
					last_tag = node.tag

			if node.tag=='catgry' and 'country' not in item_name and 'split' not in item_name:
				txt = node.find('txt')
				if txt is not None:
					text = clean_text(txt.text)
					if 'sample' not in text and text != country: 
						item_type = 'RESPONSE'
						module = determine_survey_item_module(item_name, filename)
						catValu = node.find('catValu')
						item_value = catValu.text
						split_into_sentences = tokenizer.tokenize(text)
						for item in split_into_sentences:
							data = {"survey_itemid": update_item_id(survey_id), 'module': module, 'item_type': item_type, 
							'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
							df_survey_item = df_survey_item.append(data, ignore_index = True)
						last_tag = node.tag


	

	file_to_csv_name = filename.replace('.xml', '')
	df_survey_item.to_csv(str(file_to_csv_name)+'.csv')

		




if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_xml_data_extraction.py EVS_R03_1999_FRE_FR.xml
	filename = str(sys.argv[1])
	print("Executing data extraction script for EVS 1999/2008 (xml files)")
	main(filename)
