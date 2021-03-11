from flair.models import SequenceTagger
import sys
import pandas as pd
from flair.data import Sentence




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


def main():

	tagger = SequenceTagger.load('/home/danielly/workspace/trained_pos_models/cat_40ep.pt') 

	df = pd.read_csv('/home/danielly/workspace/pcsq_data/ESS/R01_2002/spreadsheets/ESS_R01_2002_CAT_ES.csv', sep='\t')

	for i, row in df.iterrows():
		sentence = row['text']
		if isinstance(sentence, str):
			sentence = Sentence(sentence)

			tagger.predict(sentence)

			print(sentence.to_tagged_string())

if __name__ == "__main__":
	main()