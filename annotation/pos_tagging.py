from flair.models import SequenceTagger
import sys
import pandas as pd
from flair.data import Sentence
# from retrieve_from_tables import *
import flair.datasets
from flair.trainers import ModelTrainer
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, FlairEmbeddings



def get_pos_model(language):
	if 'ENG' in language:
		return SequenceTagger.load('upos') 
	elif 'CAT' in language:
		
		train_tagger(corpus)
	elif 'RUS' in language:
		corpus = flair.datasets.UD_RUSSIAN()
		train_tagger(corpus)
	else:
		return SequenceTagger.load('pos-multi') 

def train_cat_tagger():
	corpus = flair.datasets.UD_CATALAN()
	tag_type = 'pos'
	tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

	
	embedding_types = [WordEmbeddings('ca')]
	embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

	tagger: SequenceTagger = SequenceTagger(hidden_size=256,embeddings=embeddings,tag_dictionary=tag_dictionary,tag_type=tag_type,use_crf=True)

	trainer: ModelTrainer = ModelTrainer(tagger, corpus)

	trainer.train('/home/danielly/workspace',learning_rate=0.1,mini_batch_size=32, max_epochs=150)

def train_rus_tagger():
	corpus = flair.datasets.UD_RUSSIAN()
	tag_type = 'pos'
	tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

	embedding_types = [WordEmbeddings('ru')]
	embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

	tagger: SequenceTagger = SequenceTagger(hidden_size=256,embeddings=embeddings,tag_dictionary=tag_dictionary,tag_type=tag_type,use_crf=True)

	trainer: ModelTrainer = ModelTrainer(tagger, corpus)

	trainer.train('/home/danielly/workspace',learning_rate=0.1,mini_batch_size=32, max_epochs=150)

def main():

	train_cat_tagger()

	# train_rus_tagger()
	
	# languages  = ['POR', 'NOR', 'SPA', 'CAT', 'GER', 'CZE', 'FRE']

	
	# for l in languages:
	# 	get_pos_model(l)
		# result_dictionary = get_response_text_and_id_per_language(l)
		# print(result_dictionary)

	# tagger =  get_model(filename)

	# for i, row in df.iterrows():
	# 	sentence = row['text']
	# 	if isinstance(sentence, str):
	# 		sentence = Sentence(sentence)

	# 		tagger.predict(sentence)

	# 		print(sentence.to_tagged_string())

if __name__ == "__main__":
	main()