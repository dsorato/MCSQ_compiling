from flair.models import SequenceTagger
import sys
from flair.data import Sentence
import flair.datasets
from flair.trainers import ModelTrainer
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, FlairEmbeddings, FastTextEmbeddings



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


def train_por_tagger():
	corpus = flair.datasets.UD_PORTUGUESE()
	tag_type = 'upos'
	tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

	print(tag_dictionary)

	embedding_types = [WordEmbeddings('pt')]
	# embedding_types = [FastTextEmbeddings('/home/danielly/workspace/trained_pos_models/pt/pt.bin')]

	embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

	tagger: SequenceTagger = SequenceTagger(hidden_size=256,embeddings=embeddings,tag_dictionary=tag_dictionary,tag_type=tag_type,use_crf=True)

	trainer: ModelTrainer = ModelTrainer(tagger, corpus)

	trainer.train('/home/danielly/workspace',learning_rate=0.1,mini_batch_size=32, max_epochs=150)

def train_rus_tagger():
	corpus = flair.datasets.UD_RUSSIAN()
	tag_type = 'upos'
	tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)


	embedding_types = [FastTextEmbeddings('/home/danielly/workspace/trained_pos_models/ru/ru.bin')]
	embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

	tagger: SequenceTagger = SequenceTagger(hidden_size=256,embeddings=embeddings,tag_dictionary=tag_dictionary,tag_type=tag_type,use_crf=True)

	trainer: ModelTrainer = ModelTrainer(tagger, corpus)

	trainer.train('/home/danielly/workspace',learning_rate=0.1,mini_batch_size=32, max_epochs=150)

def main():

	train_cat_tagger()
	train_por_tagger()
	train_rus_tagger()
	

if __name__ == "__main__":
	main()