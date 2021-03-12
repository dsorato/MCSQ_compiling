from flair.models import SequenceTagger
import sys
import pandas as pd
from flair.data import Sentence



def main():

	tagger = SequenceTagger.load('/home/danielly/workspace/trained_pos_models/cat_150ep.pt') 

	df = pd.read_csv('/home/danielly/workspace/pcsq_data/ESS/R01_2002/spreadsheets/ESS_R01_2002_CAT_ES.csv', sep='\t')

	for i, row in df.iterrows():
		sentence = row['text']
		if isinstance(sentence, str):
			sentence = Sentence(sentence)

			tagger.predict(sentence)

			print(sentence.to_tagged_string())

if __name__ == "__main__":
	main()