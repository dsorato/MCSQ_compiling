from flair.models import SequenceTagger
import sys
from flair.data import Sentence
import flair.datasets
from populate_tables import *
from retrieve_from_tables import *
import pickle


def select_pos_model(language):
	"""
	Selects the appropriate pos tagging model based on the language.
	ENG language uses a pretrained model provided by Flair.
	NOR, SPA, GER, CZE, and FRE languages use multilingual pretrained model provided by Flair.
	CAT, RUS and POR languages use models trained by me.

	Args:
		param1 language (string): 3-digit language ISO code.
	Returns:
		part-of-speech tagging model (Pytorch object).  
	"""
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


def output_language_specific_dictionaries(languages):
	"""
	Gets each text segment and its ID from the database, building 4 dictionaries (request, response, instruction, introduction).
	After, saves the dictionaries as a pickle dump.
	
	Args:
		param1 languages (list of strings): list of 3-digit language ISO codes.
	
	"""
	for l in languages:
		request, response, instruction, introduction = build_id_dicts_per_language(l)
		dicts = {'request': request, 'response': response, 'instruction': instruction, 'introduction': introduction}
		save_dictionaries('/home/danielly/workspace/trained_models/'+l+'_dicts.pickle', dicts)


def from_tagged_dict_to_table(dicts):
	"""
	Uses the tagged dictionaries containing the tagged data from each table to 
	update the respective pos_tagged_text columns in the database.
	The survey_item table is also updated using the same IDs
	
	Args:
		param1 dicts (a dictionary of dictionaries): the dictionary name corresponds to the table name (key), 
		and the dictionary (value) has the IDs and the tagged text. 
	
	"""
	for k, v in list(dicts.items()):
		if k == 'request':
			table_name = 'request'
			table_id_name = 'requestid'
	
		elif k == 'response':
			table_name = 'response'
			table_id_name = 'responseid'

		elif k == 'instruction':
			table_name = 'instruction'
			table_id_name = 'instructionid'
		
		elif k == 'introduction':
			table_name = 'introduction'
			table_id_name = 'introductionid'

		tag_item_type_table(v, table_name, table_id_name)
		tag_survey_item(v, table_id_name)

	
def load_dict(path):
	"""
	Loads a dictionary stored as a picke object.
	Args:
		param1 path (string): the path to the dictionary
	Returns:
		the loaded dictionary.
	"""
	with open(path, 'rb') as handle:
		dicts = pickle.load(handle)

	return dicts

def save_dictionaries(path, dicts):
	"""
	Saves a dictionary as a picke object.
	Args:
		param1 path (string): the path to the dictionary
		param2 dicts (a dictionary of dictionaries): the dictionary name corresponds to the table name (key), 
		and the dictionary (value) has the IDs and the tagged text. 
	
	"""
	with open(path, 'wb') as handle:
		pickle.dump(dicts, handle, protocol=pickle.HIGHEST_PROTOCOL)

def tag_dictionary(tagger, dictionary):
	"""
	Tags each sentence of the untagged dictionary and updates its value to the tagged sentence.
	Args:
		param1 part-of-speech tagging model (Pytorch object): language specific (or multilingual) pos tagging model
		param2 dictionary (dictionary): has the IDs and the untagged text. 
	Returns:
		A dictionary with the text segment IDs and the tagged text.
	"""
	for k, v in list(dictionary.items()):
		sentence = Sentence(v)
		tagger.predict(sentence)
		tagged_sentence = sentence.to_tagged_string()
		dictionary[k] = tagged_sentence

	return dictionary
		

def save_tagged_dictionary(tagger, language):
	"""
	Loads a given untagged dictionary, calls the tagging method and saves the tagged dictionary.
	Args:
		param1 part-of-speech tagging model (Pytorch object): language specific (or multilingual) pos tagging model
		param2 language (string): 3-digit language ISO code.
	
	"""
	dicts = load_dict('/home/danielly/workspace/trained_models/'+language+'_dicts.pickle')

	for k, v in list(dicts.items()):
		dicts[k] = tag_dictionary(tagger, v)

	save_dictionaries('/home/danielly/workspace/trained_models/'+language+'_dicts_tagged.pickle', dicts)

def main():	
	languages  = ['POR', 'NOR', 'SPA', 'CAT', 'GER', 'CZE', 'FRE', 'ENG', 'RUS']

	output_language_specific_dictionaries(languages)

	for l in languages:
		tagger = select_pos_model(l)
		save_tagged_dictionary(tagger, l)
		dicts = load_dict('/home/danielly/workspace/trained_models/'+l+'_dicts_tagged.pickle')
		from_tagged_dict_to_table(dicts)




	



if __name__ == "__main__":
	main()