from flair.models import SequenceTagger
import sys
from flair.data import Sentence
import flair.datasets
import pickle
import spacy
from spacy.lang.nb.examples import sentences 
import os
import pandas as pd


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

def select_ner_model(language):
	"""
	Selects the appropriate named entity recognition (NER) model based on the language.
	ENG, GER, FRE, SPA language use pretrained models provided by Flair.
	CZE and RUS languages use multilingual pretrained model provided by Deeppavlov.
	NOR and POR languages use pretrained models provided by SpaCy
	CAT languages uses pretrained model from https://github.com/ccoreilly/spacy-catala

	Args:
		param1 language (string): 3-digit language ISO code.
	Returns:
		NER tagging model.  
	"""
	if 'ENG' in language:
		return SequenceTagger.load('flair/ner-english')
	elif 'CAT' in language:
		return spacy.load('ca')
	elif 'GER' in language:
		return SequenceTagger.load('flair/ner-german') 
	elif 'FRE' in language:
		return SequenceTagger.load('flair/ner-french') 
	elif 'SPA' in language:
		return SequenceTagger.load('flair/ner-spanish-large') 
	elif 'NOR' in language:
		return spacy.load("nb_core_news_sm")
	elif 'POR' in language:
		return spacy.load("pt_core_news_sm")
	elif 'RUS' in language or 'CZE' in language:
		return build_model("./ner_bert_slav.json", download=True)
	


def ner_annotation(df, ner, filename):
	df_tagged = pd.DataFrame(columns=['survey_itemID', 'Study', 'module', 'item_type', 'item_name', 'item_value',  'text', 'ner_tagged_text', 'pos_tagged_text'])
	for i, row in df.iterrows():
		if 'ENG' in filename or 'GER' in filename or 'FRE' in filename or 'SPA' in filename:
			sentence = Sentence(row['text'])
			ner.predict(sentence)
			tagged_sentence = sentence.to_tagged_string()
			print(tagged_sentence)

		elif 'CAT' in filename or 'POR' in filename or 'NOR' in filename:
			doc = ner(row['text'])
			for ent in doc.ents:
				print(ent.text, ent.start_char, ent.end_char, ent.label_)
		elif 'RUS' in filename or 'CZE' in filename:
			print(ner([row['text']]))

def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)


	for index, file in enumerate(files):
		if file.endswith(".csv"):
			df = pd.read_csv(file,  dtype=str, sep='\t')
			ner = select_ner_model(file)
			ner_annotation(df, ner, file)

if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)