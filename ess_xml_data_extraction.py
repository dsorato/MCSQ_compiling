import xml.etree.ElementTree as ET
from sentence_splitter import SentenceSplitter, split_text_into_sentences
import pandas as pd 
import nltk.data
import sys
import re
import string
import utils as ut


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

	for question in ess_questions:
		for node in question.getiterator():
			print(node.tag, node.attrib)


if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_data_extraction.py EVS_FRE_FR_R05_2017.xlsx
	filename = str(sys.argv[1])
	print("Executing data cleaning/extraction script for ESS 2018 (xml files)")
	main(filename)
