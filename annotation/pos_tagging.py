from flair.models import SequenceTagger
import sys
from flair.data import Sentence
import flair.datasets
from populate_tables import *
from retrieve_from_tables import *


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

def tag_text_in_table(tagger, dictionary):
	for k, v in list(dictionary.items()):
		sentence = Sentence(v)
		tagger.predict(sentence)
		tagged_sentence = sentence.to_tagged_string()
		print(tagged_sentence)


def main():
	
	languages  = ['POR', 'NOR', 'SPA', 'CAT', 'GER', 'CZE', 'FRE', 'ENG', 'RUS']

	
	for l in languages:
		tagger = get_pos_model(l)
		survey_item, request, response, instruction, introduction = build_id_dicts_per_language(l)
		dict_list = [survey_item, request, response, instruction, introduction]
		for d in dict_list:
			tag_text_in_table(tagger, d)


if __name__ == "__main__":
	main()