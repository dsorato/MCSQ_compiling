from flair.models import SequenceTagger
import sys
from flair.data import Sentence
import flair.datasets
import pickle
import spacy
import os
import pandas as pd
import re

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
		return SequenceTagger.load('/home/danielly/workspace/trained_pos_models/cat_150ep.pt') 
	elif 'RUS' in language:
		return SequenceTagger.load('/home/danielly/workspace/trained_pos_models/rus_150ep.pt') 
	elif 'POR' in language:
		return SequenceTagger.load('/home/danielly/workspace/trained_pos_models/por_150ep.pt') 
	else:
		return SequenceTagger.load('pos-multi') 

def select_ner_model(language):
	"""
	Selects the appropriate named entity recognition (NER) model based on the language.
	ENG, GER, FRE, SPA language use pretrained models provided by Flair.
	CZE and RUS languages use multilingual pretrained model provided by Deeppavlov.
	CAT, NOR and POR languages use pretrained models provided by SpaCy

	Args:
		param1 language (string): 3-digit language ISO code.
	Returns:
		NER tagging model.  
	"""
	if 'ENG' in language:
		return SequenceTagger.load('flair/ner-english')
	elif 'CAT' in language:
		return spacy.load('ca_core_news_lg')
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
	
	


def ner_annotation(df, ner, filename):
	df_tagged = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value',  'text', 'ner_tagged_text', 'pos_tagged_text'])
	for i, row in df.iterrows():
		if 'ENG' in filename or 'GER' in filename or 'FRE' in filename or 'SPA' in filename:
			sentence = Sentence(row['text'])
			ner.predict(sentence)
			tagged_sentence = sentence.to_tagged_string()
			if re.findall(r'<.*>', tagged_sentence):
				data = {'survey_item_ID': row['survey_item_ID'], 'Study': row['Study'], 'module': row['module'], 'item_type': row['item_type'], 
				'item_name': row['item_name'], 'item_value': row['item_value'],  'text': row['text'], 
				'ner_tagged_text': tagged_sentence, 'pos_tagged_text': row['pos_tagged_text']}
			else:
				data = {'survey_item_ID': row['survey_item_ID'], 'Study': row['Study'], 'module': row['module'], 'item_type': row['item_type'], 
				'item_name': row['item_name'], 'item_value': row['item_value'],  'text': row['text'], 'ner_tagged_text': None, 'pos_tagged_text': row['pos_tagged_text']}

			df_tagged = df_tagged.append(data, ignore_index = True)

		elif 'POR' in filename or 'NOR' in filename or 'CAT' in filename:
			doc = ner(row['text'])
			entities = []
			for ent in doc.ents:
				entities.append(ent.text+'<'+ent.label_+'>')
			if ''.join(entities) != '':
				data = {'survey_item_ID': row['survey_item_ID'], 'Study': row['Study'], 'module': row['module'], 'item_type': row['item_type'], 
				'item_name': row['item_name'], 'item_value': row['item_value'],  'text': row['text'], 
				'ner_tagged_text': ' '.join(entities), 'pos_tagged_text': row['pos_tagged_text']}
			else:
				data = {'survey_item_ID': row['survey_item_ID'], 'Study': row['Study'], 'module': row['module'], 'item_type': row['item_type'], 
				'item_name': row['item_name'], 'item_value': row['item_value'],  'text': row['text'], 
				'ner_tagged_text': None, 'pos_tagged_text': row['pos_tagged_text']}

			df_tagged = df_tagged.append(data, ignore_index = True)

	return df_tagged

def pos_tag_annotation(df, pos, filename):
	df_tagged = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value',  'text', 'ner_tagged_text', 'pos_tagged_text'])
	for i, row in df.iterrows():
		sentence = Sentence(row['text'])
		pos.predict(sentence)
		tagged_sentence = sentence.to_tagged_string()
		
		data = {'survey_item_ID': row['survey_item_ID'], 'Study': row['Study'], 'module': row['module'], 'item_type': row['item_type'], 
		'item_name': row['item_name'], 'item_value': row['item_value'],  'text': row['text'], 'ner_tagged_text': None, 'pos_tagged_text': tagged_sentence}
		df_tagged = df_tagged.append(data, ignore_index = True)

	return df_tagged
		
def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)


	for index, file in enumerate(files):
		if file.endswith(".csv"):
			print(file)
			df = pd.read_csv(file,  dtype=str, sep='\t')
			pos = select_pos_model(file)
			df_tagged = pos_tag_annotation(df, pos, file)

			if 'CZE' not in file and 'RUS' not in file:
				ner = select_ner_model(file)
				df_tagged = ner_annotation(df_tagged, ner, file)
		
			df_tagged.to_csv(file, encoding='utf-8', sep='\t', index=False)

if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)