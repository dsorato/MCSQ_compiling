"""
This is an ad hoc solution to tag the Russian dictionaries, as Auri does not have enough memory to load
the Russian pos tagging model
""" 


from flair.models import SequenceTagger
import sys
from flair.data import Sentence
import flair.datasets
import pickle


def save_russian_dictionaries(path, dicts):
	with open(path, 'wb') as handle:
		pickle.dump(dicts, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_russian_untagged_dictionaries():
	with open('/home/danielly/workspace/trained_pos_models/rus_dicts.pickle', 'rb') as handle:
		rus_dicts = pickle.load(handle)

	return rus_dicts

def russian_ad_hoc_tagging():
	rus_dicts = load_russian_untagged_dictionaries()
	tagger = SequenceTagger.load('/home/danielly/workspace/trained_pos_models/rus_150ep.pt') 
	for k, v in list(rus_dicts.items()):
		rus_dicts[k] = tag_dictionary(tagger, v)

	save_russian_dictionaries('/home/danielly/workspace/trained_pos_models/rus_dicts_tagged.pickle', rus_dicts)



def main():	
	russian_ad_hoc_tagging()