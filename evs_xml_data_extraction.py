import xml.etree.ElementTree as ET
import pandas as pd 
import nltk.data
import sys
import re
import string
import utils as ut


initial_request= ["Reporter sur votre: VOTRE CODE ENQUETEUR, VOTRE NOM , la date d'interview et le numéro d'interview:",
"Numéro d'interview"]



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
		text = text.lstrip()
	else:
		text = ''


	return text



def clean_text(text, filename):
	if isinstance(text, str):
		text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)
		text = re.sub("…", "...", text)
		text = re.sub(" :", ":", text)
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
			text = re.sub('^TNZ', "Trifft nicht zu",text, flags=re.IGNORECASE)
		if 'ENG' in filename:
			text = re.sub('^NAP\b', "Not applicable",text, flags=re.IGNORECASE)
			text = re.sub('^DK\b', "Don't know",text, flags=re.IGNORECASE)
			text = re.sub('^na\b', "No answer",text, flags=re.IGNORECASE)
		if 'POR' in filename:
			text = re.sub('^Na\b', "Não se aplica",text, flags=re.IGNORECASE)
			text = re.sub('^Ns', "Não sabe",text, flags=re.IGNORECASE)
			text = re.sub('^NS', "Não sabe",text, flags=re.IGNORECASE)
			text = re.sub('^Nr', "Não responde",text, flags=re.IGNORECASE)
			text = re.sub('^NR', "Não responde",text, flags=re.IGNORECASE)
		
		if 'DUT' in filename:
			text = re.sub('^nap', "niet van toepassing",text, flags=re.IGNORECASE)

		if 'FIN' in filename:
			text = re.sub('^EOS', "Ei osaa sanoa",text, flags=re.IGNORECASE)

		if 'TUR' in filename:
			text = re.sub('^FY', "BİLMİYOR-FİKRİ YOK",text, flags=re.IGNORECASE)
			text = re.sub('^CY', "CEVAP VERMİYOR",text, flags=re.IGNORECASE)
			text = re.sub('^SS', "Soru Sorulmadı",text, flags=re.IGNORECASE)


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

	if '_'  in item_name:
		item_name = item_name.split('_')
		item_name = item_name[0]+item_name[1].lower()

	if item_name[0].isdigit():
		item_name = 'Q'+item_name

	return item_name

def determine_survey_item_module(item_name, filename):
	module = 'No module'
	if ('Q' in item_name or 'f' in item_name) and (len(item_name) <= 10):
		digits_in_item_name = re.sub("[^\d]", "", item_name)


		if '/' in digits_in_item_name:
			digits_in_item_name = digits_in_item_name.split('/')
			digits_in_item_name = digits_in_item_name[0]
	
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


def main(filename):
	dict_answers = dict()
	dict_category_values = dict()
	dict_node_item_name = dict()

	#Reset the initial survey_id sufix, because main is called iterativelly for every XML file in folder 
	ut.reset_initial_sufix()
	#Punkt Sentence Tokenizer from NLTK	
	sentence_splitter_prefix = 'tokenizers/punkt/'
	sentence_splitter_suffix = ut.determine_sentence_tokenizer(filename)
	sentence_splitter = sentence_splitter_prefix+sentence_splitter_suffix
	tokenizer = nltk.data.load(sentence_splitter)

	country = ut.determine_country(filename)
	#The prefix is study+'_'+language+'_'+country+'_'
	prefix = re.sub('\.xml', '', filename)+'_'

	# parse an xml file by name
	file = str(filename)
	tree = ET.parse(file)
	root = tree.getroot()

	parent_map = dict((c, p) for p in tree.getiterator() for c in p)

	evs_vars = root.findall('.//dataDscr/var')

	survey_id = filename.replace('.xml', '')
	df_survey_item = pd.DataFrame(columns=['survey_itemid', 'module','item_type', 'item_name', 'item_value', 'text',  'item_is_source'])

	

	last_tag = 'tag'
	old_item_name = 'last'
	item_name = ''
	for var in evs_vars:
		last_node_was_sublevel = False

		for node in var.getiterator():
			text = ''
			item_type = ''
			item_value = ''
			qstn = var.find('qstn')
			if node.tag=='txt' and 'level' in node.attrib:
				item_name = node.attrib['level']

			elif qstn is not None and 'seqNo' in qstn.attrib and 'level' not in node.attrib:
				item_name = qstn.attrib['seqNo'] 
		
			# else:
			# 	elem_item_name = var.find('labl').text
			# 	item_name = elem_item_name[elem_item_name.find("(")+1:elem_item_name.find(")")]

			if item_name:
				item_name = standartize_item_name(item_name)

			dict_node_item_name[node] = item_name

				
	
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
				
				module = determine_survey_item_module(item_name, filename)

				split_into_sentences = tokenizer.tokenize(text)
				for item in split_into_sentences:
					data = {"survey_itemid": survey_item_id, 'module': module,'item_type': item_type, 
					'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
				last_tag = node.tag

			if node.tag=='ivuInstr':
				survey_item_id = ut.decide_on_survey_item_id(prefix, old_item_name, item_name)
				old_item_name = item_name

				text = clean_instruction(node.text)
				if 	'?' in text:
					item_type = 'REQUEST'
				else:
					item_type = 'INSTRUCTION'
				module = determine_survey_item_module(item_name, filename)

				split_into_sentences = tokenizer.tokenize(text)
				for item in split_into_sentences:
					data = {"survey_itemid": survey_item_id, 'module': module,'item_type': item_type, 
					'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
					df_survey_item = df_survey_item.append(data, ignore_index = True)
				last_tag = node.tag

			if node.tag=='qstnLit':
				text = clean_text(node.text, filename)
				item_type = 'REQUEST'
				if len(text) != 1 and text.isnumeric() == False:
					#workaround
					if ut.ignore_interviewer_number_segment(filename, item_name, text):
						pass
					else:
						module = determine_survey_item_module(item_name, filename)
						survey_item_id = ut.decide_on_survey_item_id(prefix, old_item_name, item_name)
						old_item_name = item_name


						split_into_sentences = tokenizer.tokenize(text)
						for item in split_into_sentences:
							data = {"survey_itemid": survey_item_id, 'module': module,'item_type': item_type, 
							'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
							df_survey_item = df_survey_item.append(data, ignore_index = True)
						last_tag = node.tag

			if node.tag=='txt' and 'split' not in item_name and 'name' in parent_map[node].attrib:
			# if node.tag=='txt' and last_tag != 'catgry' and 'country' not in item_name and 'split' not in item_name:
				is_uppercase = check_if_sentence_is_uppercase(node.text)
				text = clean_text(node.text, filename)
				item_type = 'REQUEST'

				module = determine_survey_item_module(item_name, filename)
				if 'sample' not in text and text != country: 
					
					survey_item_id = ut.decide_on_survey_item_id(prefix, old_item_name, item_name)
					old_item_name = item_name

					split_into_sentences = tokenizer.tokenize(text)
					for item in split_into_sentences:
						data = {"survey_itemid": survey_item_id, 'module': module, 'item_type': item_type, 
						'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
						df_survey_item = df_survey_item.append(data, ignore_index = True)
					last_tag = node.tag
					last_text = node.text

			if node.tag=='catgry' and 'country' not in item_name and 'split' not in item_name:
				txt = node.find('txt')
				if df_survey_item.empty==False:
					item_name = df_survey_item['item_name'].iloc[-1]
				print(item_name)

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
						survey_item_id = ut.decide_on_survey_item_id(prefix, old_item_name, item_name)
						old_item_name = item_name

						item_type = 'RESPONSE'
						module = determine_survey_item_module(item_name, filename)
						item_value = dk_nr_standard(filename, catValu.text, text)
						split_into_sentences = tokenizer.tokenize(text)
						for item in split_into_sentences:
							data = {"survey_itemid": survey_item_id, 'module': module, 'item_type': item_type, 
							'item_name': item_name, 'item_value': item_value,  'text': item, 'item_is_source': False}
							df_survey_item = df_survey_item.append(data, ignore_index = True)
						last_tag = node.tag



	# for k,v in list(dict_answers.items()):
	# 	print(k,v)

	file_to_csv_name = filename.replace('.xml', '')
	df_survey_item.to_csv(str(file_to_csv_name)+'.csv', encoding='utf-8-sig', index=False)

		




if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_xml_data_extraction.py EVS_R03_1999_FRE_FR.xml
	filename = str(sys.argv[1])
	print("Executing data extraction script for EVS 1999/2008 (xml files)")
	main(filename)
