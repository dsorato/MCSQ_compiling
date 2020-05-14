import xml.etree.ElementTree as ET
from sentence_splitter import SentenceSplitter, split_text_into_sentences
import pandas as pd 
import nltk.data
import sys
import re
import string
import utils as ut



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
		text = re.sub('</br>', "",text)
		text = re.sub('<br />', "",text)
		text = re.sub('<br>', "",text)
		text = re.sub('</u>', "",text)
		text = re.sub('<u>', "",text)
		text = re.sub('&lt;', "",text)
		text = re.sub('&gt;', "",text)
		text = re.sub('&gt;', "",text)
		text = re.sub('&lt', "",text)
		text = re.sub('&gt', "",text)
		text = re.sub('&nbsp', "",text)
		text = re.sub(';', "",text)
		text = text.replace('\n',' ')
		text = text.rstrip()
		text = text.lstrip()
	else:
		text = ''


	return text
def clean(text):
	if isinstance(text, str):
		text = re.sub("…", "...", text)
		text = re.sub("’", "'", text)
		text = re.sub(" :", ":", text)
		text = re.sub("Enq.", "Enquêteur", text)
		text = re.sub("\s+\?", "?", text)
		text = re.sub("[.]{4,}", "", text)
		text = re.sub("[!]{2,}", "!", text)
		text = re.sub('</strong>', "",text)
		text = re.sub('<strong>', "",text)
		text = re.sub('</br>', "",text)
		text = re.sub('<br />', "",text)
		text = re.sub('<br>', "",text)
		text = re.sub('</u>', "",text)
		text = re.sub('<u>', "",text)
		text = re.sub('&lt;', "",text)
		text = re.sub('&gt;', "",text)
		text = re.sub('&gt;', "",text)
		text = re.sub('&lt', "",text)
		text = re.sub('&gt', "",text)
		text = re.sub('&nbsp', "",text)
		text = re.sub(';', "",text)
		text = text.replace('\n',' ')
		text = text.rstrip()
		text = text.lstrip()
	else:
		text = ''


	return text

def identify_showcard_instruction(text, language_country):
	item_type = 'REQUEST'
	if 'FRE' in language_country:
		if 'CH' in language_country:
			showcard = 'CARTE'

	if re.compile(showcard).match(text):
		item_type = 'INSTRUCTION'

	return item_type

def append_data_to_df(df_questions, parent_map, node, item_name, item_type, splitter, tokenizer, language_country):
	if node.text != '' and  isinstance(node.text, str):
		if splitter:
			split_into_sentences = splitter.split(text=clean(node.text))
		else:
			split_into_sentences = tokenizer.tokenize(clean(node.text))

		for text in split_into_sentences:
			if item_type == 'REQUEST':
				data = {'question_id': parent_map[node].attrib['tmt_id'], 'item_name':item_name, 
				'item_type':identify_showcard_instruction(text, language_country), 'text':text}
			else:
				data = {'question_id': parent_map[node].attrib['tmt_id'], 'item_name':item_name, 'item_type':item_type, 'text':text}
			df_questions = df_questions.append(data, ignore_index=True)
	else:
		return df_questions

	return df_questions


def main(filename):
	dict_answers = dict()
	dict_category_values = dict()
	df_survey_item = pd.DataFrame(columns=['survey_itemid', 'module','item_type', 'item_name', 'item_value', 'text',  'item_is_source'])

	#Reset the initial survey_id sufix, because main is called iterativelly for every XML file in folder 
	ut.reset_initial_sufix()

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

	country = ut.determine_country(filename)
	#The prefix is study+'_'+language+'_'+country+'_'
	prefix = re.sub('\.xml', '', filename)+'_'

	# parse an xml file by name
	file = str(filename)
	tree = ET.parse(file)
	root = tree.getroot()

	parent_map = dict((c, p) for p in tree.getiterator() for c in p)
	ess_questions = root.findall('.//questionnaire/questions')
	ess_answers = root.findall('.//questionnaire/answers')
	ess_showcards = root.findall('.//questionnaire/showcards')

	survey_id = filename.replace('.xml', '')
	split_survey_id = survey_id.split('_')
	language_country = split_survey_id[3]+'_'+split_survey_id[4]

	df_questions =  pd.DataFrame(columns=['question_id', 'item_name', 'item_type', 'text']) 
	df_answers =  pd.DataFrame(columns=['question_id', 'item_name', 'item_type', 'text', 'item_value']) 
	item_name = ''
	text = ''
	item_type = ''
	item_value = None
	for question in ess_questions:
		for node in question.getiterator():
			if node.tag == 'question' and 'name' in node.attrib and 'tmt_id' in node.attrib:
				item_name = node.attrib['name']
			if node.tag == 'text' and 'translation_id' in node.attrib and node.attrib['translation_id'] != '1':
				if 'type_name' in parent_map[node].attrib and parent_map[node].attrib['type_name'] == 'QText':
					text = node.text
					item_type = 'REQUEST'
					df_questions = append_data_to_df(df_questions, parent_map, node, item_name, item_type, splitter,
					tokenizer, language_country)

				if 'type_name' in parent_map[node].attrib and parent_map[node].attrib['type_name'] == 'QInstruction':
					text = node.text
					item_type = 'INSTRUCTION'
					df_questions = append_data_to_df(df_questions, parent_map, node, item_name, item_type, splitter, 
					tokenizer, language_country)

	for answer in ess_answers:
		for node in answer.getiterator():
			if node.tag == 'answer' and 'name' in node.attrib and 'tmt_id' in node.attrib:
				item_name = node.attrib['name']
				item_name = item_name.split('_')
				item_name = item_name[1]
			if node.tag == 'text' and 'translation_id' in node.attrib and node.attrib['translation_id'] != '1':
				text = node.text
				if node.text != '' and  isinstance(node.text, str) and 'does not exist in' not in text:
					item_type = 'RESPONSE'
					question_id = parent_map[node].attrib['tmt_id']
					item_value = parent_map[node].attrib['labelvalue']
					data = {'question_id': question_id, 'item_name': item_name, 'item_type':'RESPONSE', 
					'text': clean_answer_category(text), 'item_value': item_value}
					df_answers = df_answers.append(data, ignore_index=True)

		


			
	df_questions.to_csv('questions.csv', encoding='utf-8-sig', index=False)
	df_answers.to_csv('answers.csv', encoding='utf-8-sig', index=False)


if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_data_extraction.py EVS_FRE_FR_R05_2017.xlsx
	filename = str(sys.argv[1])
	print("Executing data cleaning/extraction script for ESS 2018 (xml files)")
	main(filename)
