import sys
import os
import re
import pandas as pd
from preprocessing_ess_utils import *
import utils as ut

scale_items_to_ignore = ['01', '02', '03', '04', '05', '06', '07', '08', '09']

"""
Extracts the raw items from ESS plain text file, based on an item name regex pattern.
Also excludes blank lines and non relevant scale items.
:param file: input ESS plain text file.
:returns: retrieved raw items, in a list. 
"""
def retrieve_raw_items_from_file(file):
	item_name_question_pattern = re.compile("(?:[A-K][A-Z]?\s?[1-9]{1,3}[a-z]?)+")
	
	lines = file.readlines()
	last_line = len(lines) - 1

	index_tags = []
	for i, line in enumerate(lines):
		if item_name_question_pattern.match(line):
			index_tags.append(i)

		raw_items = []
		for i, index in enumerate(index_tags):
			if index == index_tags[-1]:
				item = lines[index:]
			else:
				next_index_element = index_tags[i+1]
				item = lines[index:next_index_element]

			clean = []
			for subitem in item:
				subitem = subitem.rstrip()
				if subitem != '' and subitem not in scale_items_to_ignore:
					clean.append(subitem)

			raw_items.append(clean)

	return raw_items


"""
Extracts and processes the question segments from a raw item.
The question segments are always between the {QUESTION} and {ANSWERS} tags, 
for instance:

G2
{QUESTION}
Per a ell és important ser ric. 
Vol tenir molts diners i coses cares.

{ANSWERS}
Se sembla molt a mi
Se sembla a mi
Se sembla una mica a mi
Se sembla poc a mi
No se sembla a mi
No se sembla gens a mi

:param raw_item: raw item, retrieved in previous steps.
"""
def process_question_segment(raw_item):
	splitter = ut.get_sentence_splitter(filename)

	index_question_tag = raw_item.index('{QUESTION}')
	index_answer_tag = raw_item.index('{ANSWERS}')

	question_segment = raw_item[index_question_tag+1:index_answer_tag]

	return question_segment

def process_answer_segment(raw_item):
	splitter = ut.get_sentence_splitter(filename)

	index_answer_tag = raw_item.index('{ANSWERS}')

	answer_segment = raw_item[index_question_tag+1:]

	return answer_segment

def process_intro_segment(raw_item):
	splitter = ut.get_sentence_splitter(filename)

	index_intro_tag = raw_item.index('{INTRO}')
	index_question_tag = raw_item.index('{QUESTION}')

	intro_segment = raw_item[index_intro_tag+1:index_question_tag]

	return intro_segment

def main(folder_path, concatenate_supplementary_questionnaire):
	path = os.chdir(folder_path)
	files = os.listdir(path)

	"""
	A pandas dataframe to store questionnaire data.
	"""
	df_questionnaire = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 'text'])

	study, country_language = get_country_language_and_study_info(filename)

	for index, file in enumerate(files):
		if file.endswith(".txt"):	
			with open(file, 'r') as f:
				raw_items = retrieve_raw_items_from_file(f)
				for item in raw_items:
					item_name = item[0]
					question = process_question_segment(item, study, item_name,df_questionnaire)

					print(item_name,question)


			f.close()

	






if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	concatenate_supplementary_questionnaire = bool(sys.argv[2])
	main(folder_path, concatenate_supplementary_questionnaire)