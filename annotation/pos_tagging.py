from flair.models import SequenceTagger
import sys
from flair.data import Sentence
import flair.datasets
from populate_tables import *
from retrieve_from_tables import *
from populate_tables import *


def get_pos_model(language):
	if 'ENG' in language:
		return SequenceTagger.load('upos') 
	elif 'CAT' in language:
		return SequenceTagger.load('/home/danielly/workspace/trained_models/cat_150ep.pt') 
	elif 'RUS' in language:
		return SequenceTagger.load('/home/danielly/workspace/trained_models/rus_150ep.pt') 
	elif 'POR' in language:
		return SequenceTagger.load('/home/danielly/workspace/trained_models/por_150ep.pt') 
	else:
		return SequenceTagger.load('pos-multi') 

def tag_text_in_table(tagger, dictionary_name, dictionary):
	if dictionary_name == 'survey_item':
		table_name = 'survey_item'
		table_id_name = 'survey_itemid'
		survey_item_flag = 1
	elif dictionary_name == 'request':
		table_name = 'request'
		table_id_name = 'requestid'
		survey_item_flag = 0
	elif dictionary_name == 'response':
		table_name = 'response'
		table_id_name = 'responseid'
		survey_item_flag = 0
	elif dictionary_name == 'instruction':
		table_name = 'instruction'
		table_id_name = 'instructionid'
		survey_item_flag = 0
	elif dictionary_name == 'introduction':
		table_name = 'introduction'
		table_id_name = 'introductionid'
		survey_item_flag = 0

	for k, v in list(dictionary.items()):
		sentence = Sentence(v)
		tagger.predict(sentence)
		tagged_sentence = sentence.to_tagged_string()
		tag_table_text(tagged_sentence, table_name, table_id_name, k, survey_item_flag)


def main():
	
	languages  = ['POR', 'NOR', 'SPA', 'CAT', 'GER', 'CZE', 'FRE', 'ENG', 'RUS']

	
	for l in languages:
		tagger = get_pos_model(l)
		survey_item, request, response, instruction, introduction = build_id_dicts_per_language(l)
		dicts = {'survey_item': survey_item, 'request': request, 'response': response, 'instruction': instruction, 'introduction': introduction}
		for k, v in list(dicts.items()):
			tag_text_in_table(tagger, k, v)


if __name__ == "__main__":
	main()