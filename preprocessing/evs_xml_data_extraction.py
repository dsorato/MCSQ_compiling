"""
Python3 script to transform XML EVS data into spreadsheet format used as input for MCSQ
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
"""
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from sentence_splitter import SentenceSplitter, split_text_into_sentences
import pandas as pd 
import nltk.data
import sys
import re
import string
import utils as ut


dict_module_letters_1999 = {'Perceptions of Life': 'A - Perceptions of Life', 'Environment': 'B - Environment', 'Work': 'C - Work', 
'Family': 'D - Family', 'Politics and Society': 'E - Politics and Society', 'Religion and Morale': 'F - Religion and Morale', 
'National Identity': 'G - National Identity', 'Socio Demographics and Interview char.': 'H - Socio Demographics and Interview Characteristics', 
'Additional country-specific variables': 'I - Additional country-specific variables'}

dict_module_letters_2008 = {'Perceptions of Life': 'A - Perceptions of Life', 'Politics and Society': 'B - Politics and Society', 'Work': 'C - Work', 
'Religion and Morale': 'D - Religion and Morale', 'Family': 'E - Family', 'National Identity': 'F - National Identity',  'Environment': 'G - Environment',
'Life experiences': 'H - Life experiences', "Respondent's parents": "I - Respondent's parents", "Respondent's partner": "J - Respondent's partner",
  'Socio Demographics and Interview Characteristics': 'K - Socio Demographics and Interview Characteristics'}



def check_if_sentence_is_uppercase(text):
	is_uppercase = False
	if isinstance(text, str):
		for word in text:
			if word.isupper() and word not in string.punctuation:
				is_uppercase = True

	return is_uppercase

def clean_instruction(text):
	if isinstance(text, str):
		# text = re.sub("…", "...", text)
		text = re.sub("’", "'", text)
		text = re.sub(";", ",", text)
		text = re.sub("[.]{4,}", "", text)
		text = re.sub('>', "",text)
		text = re.sub('<', "",text)
		text = re.sub('Q[0-9]*\.', "",text)
		text = re.sub('\[', "",text)
		text = re.sub('\]', "",text)
		text = text.replace('\n',' ')
		text = text.rstrip()
		text = text.lstrip()
	else:
		text = ''


	return text



def clean_text(text, filename):
	if isinstance(text, str):
		text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)
		text = re.sub("…", "...", text)
		text = re.sub(" :", ":", text)
		text = re.sub(";", ",", text)
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
		text = re.sub('e\.g\.', "e.g.,",text)


		if 'ITA' in filename:
			text = re.sub('^NS', "Non so",text)
			text = re.sub('^NR', "Non risponde",text)
			text = re.sub('^NP', "Non pertinente",text)
		if 'FRE' in filename:
			text = re.sub('^NSP', "Ne sait pas",text, flags=re.IGNORECASE)
			text = re.sub('^S\.R\.', "Pas de réponse",text)
			text = re.sub('^S\.R', "Pas de réponse",text)
			text = re.sub('^SR\.', "Pas de réponse",text)
			text = re.sub('^s\.r', "Pas de réponse",text)
			text = re.sub('^s\.r\.', "Pas de réponse",text)
			text = re.sub('^S\.r', "Pas de réponse",text)
			text = re.sub('^SR', "Pas de réponse",text)
		if 'GER' in filename:
			text = re.sub('^TNZ', "Trifft nicht zu",text)
			text = re.sub('^WN', "weiß nicht",text)
			text = re.sub('^KA', "keine antwort",text)
			text = re.sub('^NZT', "nicht zutreffend",text)

		if 'HRV' in filename:
			text = re.sub('^n\.o\.', "nema odgovora",text)
			text = re.sub('^n\.z\.', "ne znam",text)
			

		if 'ENG' in filename:
			text = re.sub('^NAP', "Not applicable",text)
			text = re.sub('^DK', "Don't know",text)
			text = re.sub('^na', "No answer",text)
			text = re.sub('^NA', "No answer",text)
			text = re.sub('^nap', "Not applicable",text)
			text = re.sub('^dk', "Don't know",text)
			text = re.sub('^N/A', "Not applicable",text)
			
		if 'POR' in filename:
			text = re.sub('^Na\b', "Não se aplica",text, flags=re.IGNORECASE)
			text = re.sub('^NAP', "Não se aplica",text)
			text = re.sub('^Ns', "Não sabe",text, flags=re.IGNORECASE)
			text = re.sub('^NS', "Não sabe",text, flags=re.IGNORECASE)
			text = re.sub('^Nr', "Não responde",text, flags=re.IGNORECASE)
			text = re.sub('^NR', "Não responde",text, flags=re.IGNORECASE)

		if 'SPA' in filename:
			text = re.sub('^NS', "No sabe",text)
			text = re.sub('^NC', "No contesta",text)
		
		if 'DUT' in filename:
			text = re.sub('^nap', "niet van toepassing",text, flags=re.IGNORECASE)

		if 'FIN' in filename:
			text = re.sub('^EOS', "Ei osaa sanoa",text, flags=re.IGNORECASE)

		if 'LTZ' in filename:
			text = re.sub('^NSP', "Ne sait pas",text)
			text = re.sub('^SR', "Pas de réponse",text)
			text = re.sub('^S\.R\.', "Pas de réponse",text)
		if 'TUR' in filename:
			text = re.sub('^FY', "BİLMİYOR-FİKRİ YOK",text, flags=re.IGNORECASE)
			text = re.sub('^CY', "CEVAP VERMİYOR",text, flags=re.IGNORECASE)
			text = re.sub('^SS', "Soru Sorulmadı",text, flags=re.IGNORECASE)

		if 'RUS_EE' in filename or 'RUS_AZ' in filename or 'RUS_GE' in filename or 'RUS_MD' in filename:
			text = re.sub('^Н.О.', "Нет ответа",text)
			text = re.sub('^З.О.', "Затрудняюсь ответить",text)
			text = re.sub('^Н.П.', "Не подходит",text)
			text = re.sub('^Н.О', "Нет ответа",text)
			text = re.sub('^З.О', "Затрудняюсь ответить",text)
			text = re.sub('^Н.П', "Не подходит",text)
			text = re.sub('^ЗО', "Затрудняюсь ответить",text)

		if 'RUS_BY' in filename:
			text = re.sub('^НО', "Нет ответа",text)
			text = re.sub('^НЗ', "НЕ ЗНАЮ",text)

		if 'RUS_UA' in filename:
			text = re.sub('^ЗО', "затрудняюсь ответить",text)
			text = re.sub('^ООО', "отказ от ответа",text)



		text = text.replace('\n',' ')
		text = text.rstrip()
	else:
		text = ''



	return text

def standartize_item_name(item_name):
	item_name = re.sub("\.", "", item_name)
	item_name = item_name.lower()
	item_name = re.sub("^q", "Q", item_name)
	item_name = re.sub("^f", "Q", item_name)
	# item_name = re.sub(")", "", item_name)

	if '_'  in item_name:
		item_name = item_name.split('_')
		item_name = item_name[0]+item_name[1].lower()

	if item_name[0].isdigit() or len(item_name)==1:
		item_name = 'Q'+item_name

	return item_name


def determine_survey_item_module(filename, parent_id, dictionary_vars_in_module, df_survey_item):
	module = 'No module'

	if '1999' in filename:
		dictionary = dict_module_letters_1999
	elif '2008' in filename:
		dictionary = dict_module_letters_2008


	for k, v in list(dictionary_vars_in_module.items()):
		sp = v.split(' ')
		for value in sp:
			if value == parent_id:
				return dictionary[k]
			


	if module == 'No module' and df_survey_item.empty == False:
		module = df_survey_item['module'].iloc[-1]


	return module

def dk_nr_standard(filename, catValu, text):
	# Standard
	# Refusal 777
	# Don't know 888
	# Does not apply 999
	print('text', text)

	if ut.recognize_standard_response_scales(filename, text)=='refusal':
		item_value = '777'
	elif ut.recognize_standard_response_scales(filename, text)=='dk':
		item_value = '888'
	elif ut.recognize_standard_response_scales(filename, text)=='dontapply':
		item_value = '999'
	else:
		item_value = catValu

	return item_value

"""
This function retrieves the country/language and study metadata based on the input filename.

Args:
    param1: filename

Returns:
    country/language and study metadata.
"""
def get_country_language_and_study_info(filename):
	filename_without_extension = re.sub('\.xml', '', filename)
	filename_split = filename_without_extension.split('_')

	study = filename_split[0]+'_'+filename_split[1]+'_'+filename_split[2]
	country_language = filename_split[3]+'_'+filename_split[4]

	return study, country_language


def main(filename):
	dict_answers = dict()
	dict_category_values = dict()
	study, country_language = get_country_language_and_study_info(filename)

	df_survey_item = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module','item_type', 'item_name', 'item_value', country_language,  'item_is_source'])

	#Reset the initial survey_id sufix, because main is called iterativelly for every XML file in folder 
	ut.reset_initial_sufix()
	
	#Decide on a (sentence) spliter based on the language.
	#ICE, HUN, LAV, LIT and SLO languages are not present in the NLTK library, 
	#so another splitter library is necessary 
	splitter = None
	if 'ICE_IS' in filename:
		splitter = SentenceSplitter(language='is')
	elif 'HUN_HU' in filename:
		splitter = SentenceSplitter(language='hu')
	elif 'LAV_LV' in filename:
		splitter = SentenceSplitter(language='lv')
	elif 'LIT_LT' in filename:
		splitter = SentenceSplitter(language='lt')
	elif 'SLO_SK' in filename:
		splitter = SentenceSplitter(language='sk')
	else:
		#Punkt Sentence Tokenizer from NLTK	
		sentence_splitter_prefix = 'tokenizers/punkt/'
		sentence_splitter_suffix = ut.determine_sentence_tokenizer(filename)
		sentence_splitter = sentence_splitter_prefix+sentence_splitter_suffix
		tokenizer = nltk.data.load(sentence_splitter)

	#Determine the country using the information contained in the filename.
	#Information needed to exclude some unecessary segments of the EVS XML file.
	country = ut.determine_country(filename)
	#The prefix is study+'_'+language+'_'+country+'_'
	prefix = re.sub('\.xml', '', filename)+'_'

	#Parse the input XML file by filename
	file = str(filename)
	tree = ET.parse(file)
	root = tree.getroot()

	#Create a dictionary containing parent-child relations of the parsed tree
	parent_map = dict((c, p) for p in tree.getiterator() for c in p)
	evs_vars = root.findall('.//dataDscr/var')
	evs_var_grps = root.findall('.//dataDscr/varGrp')

	survey_id = filename.replace('.xml', '')
	
	list_module_names = []
	list_vars_in_module = []
	for var in evs_var_grps:
		for node in var.getiterator():
			if node.tag == 'labl' and 'VAR' not in node.text and 'Weight' not in node.text and 'Archive' not in node.text:
				list_module_names.append(node.text)
				
			if 'var' in node.attrib:
				list_vars_in_module.append(node.attrib['var'])
	
	dictionary_vars_in_module = dict(zip(list_module_names, list_vars_in_module))
	print(dictionary_vars_in_module)


	last_tag = 'tag'
	old_item_name = 'last'
	item_name = ''
	for var in evs_vars:

		for node in var.getiterator():
			text = ''
			item_type = ''
			item_value = ''
			qstn = var.find('qstn')
			if node.tag=='txt' and 'level' in node.attrib:
				item_name = node.attrib['level']

			elif qstn is not None and 'seqNo' in qstn.attrib and 'level' not in node.attrib:
				item_name = qstn.attrib['seqNo'] 

			if item_name:
				item_name = standartize_item_name(item_name)
				
	
			if node.tag=='preQTxt':
				survey_item_id = ut.decide_on_survey_item_id(prefix, old_item_name, item_name)
				old_item_name = item_name

				if check_if_sentence_is_uppercase(node.text) == True and '?' not in node.text:
					item_type = 'INSTRUCTION'
					text = clean_instruction(node.text)
				elif '?' in node.text:
					text = clean_text(node.text, filename)
					item_type = 'REQUEST'
				else:
					text = clean_text(node.text, filename)
					item_type = 'INTRODUCTION'
				
				if item_name == 'Q1':
					module = 'A - Perceptions of Life'
				else:
					parent_id = parent_map[node].attrib['ID']
					module = determine_survey_item_module(filename, parent_id, dictionary_vars_in_module, df_survey_item)


				if splitter:
					split_into_sentences = splitter.split(text=text)
				else:
					split_into_sentences = tokenizer.tokenize(text)

				for item in split_into_sentences:
					data = {"survey_item_ID": survey_item_id,'Study': study, 'module': module,'item_type': item_type, 
					'item_name': item_name, 'item_value': item_value,  country_language: item, 'item_is_source': False}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
				last_tag = node.tag

			if node.tag=='ivuInstr':
				

				text = clean_instruction(node.text)
				if 	'?' in text:
					item_type = 'REQUEST'
				else:
					item_type = 'INSTRUCTION'

				if item_name == 'Q1':
					module = 'A - Perceptions of Life'
				else:
					parent_id = parent_map[node].attrib['ID']
					module = determine_survey_item_module(filename, parent_id, dictionary_vars_in_module, df_survey_item)

				survey_item_id = ut.decide_on_survey_item_id(prefix, old_item_name, item_name)
				old_item_name = item_name

				if splitter:
					split_into_sentences = splitter.split(text=text)
				else:
					split_into_sentences = tokenizer.tokenize(text)

				for item in split_into_sentences:
					data = {"survey_item_ID": survey_item_id, 'Study': study,'module': module,'item_type': item_type, 
					'item_name': item_name, 'item_value': item_value,  country_language: item, 'item_is_source': False}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
				last_tag = node.tag

			if node.tag=='qstnLit':
				text = clean_text(node.text, filename)
				
				if len(text) != 1 and text.isnumeric() == False:
					if item_name == 'Q1':
						module = 'A - Perceptions of Life'
					else:
						parent_id = parent_map[node].attrib['ID']
						module = determine_survey_item_module(filename, parent_id, dictionary_vars_in_module, df_survey_item)
						
					survey_item_id = ut.decide_on_survey_item_id(prefix, old_item_name, item_name)
					item_type = 'REQUEST'
					old_item_name = item_name

					if splitter:
						split_into_sentences = splitter.split(text=text)
					else:
						split_into_sentences = tokenizer.tokenize(text)

					for item in split_into_sentences:
						data = {"survey_item_ID": survey_item_id, 'Study': study,'module': module,'item_type': item_type, 
						'item_name': item_name, 'item_value': item_value,  country_language: item, 'item_is_source': False}
						df_survey_item = df_survey_item.append(data, ignore_index = True)
					last_tag = node.tag

			if node.tag=='txt' and 'split' not in item_name and 'name' in parent_map[node].attrib:
				is_uppercase = check_if_sentence_is_uppercase(node.text)
				text = clean_text(node.text, filename)
				item_type = 'REQUEST'

				parent_id = parent_map[node].attrib['ID']
				module = determine_survey_item_module(filename, parent_id, dictionary_vars_in_module, df_survey_item)

				if 'sample' not in text and text != country: 
					
					survey_item_id = ut.decide_on_survey_item_id(prefix, old_item_name, item_name)
					old_item_name = item_name

					if splitter:
						split_into_sentences = splitter.split(text=text)
					else:
						split_into_sentences = tokenizer.tokenize(text)

					for item in split_into_sentences:
						data = {"survey_item_ID": survey_item_id, 'Study': study,'module': module, 'item_type': item_type, 
						'item_name': item_name, 'item_value': item_value,  country_language: item, 'item_is_source': False}
						df_survey_item = df_survey_item.append(data, ignore_index = True)
					last_tag = node.tag
					last_text = node.text

			if node.tag=='catgry' and 'country' not in item_name and 'split' not in item_name:
				txt = node.find('txt')

				if df_survey_item.empty==False:
					item_name = df_survey_item['item_name'].iloc[-1]

				if txt is not None:
					text = clean_text(txt.text, filename)
					catValu = node.find('catValu')

					dict_answers[node.attrib['ID']] = text
					dict_category_values[node.attrib['ID']] = catValu
			
				elif txt is None and 'sdatrefs' in node.attrib:
					if node.attrib['sdatrefs'] in dict_answers:
						text = dict_answers[node.attrib['sdatrefs']]
						catValu = dict_category_values[node.attrib['sdatrefs']]

				if text:
					if 'sample' not in text and text != country and text != '':

						if 'SOURCE' in filename and ("cntry" in parent_map[node].attrib['name'] or "country" in parent_map[node].attrib['name']):
							pass
						else:
							survey_item_id = ut.decide_on_survey_item_id(prefix, old_item_name, item_name)
							old_item_name = item_name

						
							parent_id = parent_map[node].attrib['ID']
							module = determine_survey_item_module(filename, parent_id, dictionary_vars_in_module, df_survey_item)
							
							item_type = 'RESPONSE'
							item_value = dk_nr_standard(filename, catValu.text, text)

							if splitter:
								split_into_sentences = splitter.split(text=text)
							else:
								split_into_sentences = tokenizer.tokenize(text)
							for item in split_into_sentences:
								data = {"survey_item_ID": survey_item_id, 'Study': study,'module': module, 'item_type': item_type, 
								'item_name': item_name, 'item_value': item_value,  country_language: item, 'item_is_source': False}
								df_survey_item = df_survey_item.append(data, ignore_index = True)
							last_tag = node.tag


	file_to_csv_name = filename.replace('.xml', '')
	df_survey_item.to_csv(str(file_to_csv_name)+'.csv', encoding='utf-8-sig', index=False)

		




if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_xml_data_extraction.py EVS_R03_1999_FRE_FR.xml
	filename = str(sys.argv[1])
	print("Executing data extraction script for EVS 1999/2008 (xml files)")
	main(filename)
