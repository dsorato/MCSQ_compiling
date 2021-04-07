from flair.models import SequenceTagger
import sys
import pandas as pd
from flair.data import Sentence



def main():

	tagger = SequenceTagger.load('upos') 

	df = pd.read_csv('/home/danielly/workspace/pcsq_data/ESS/R03_2006/spreadsheets/ESS_R03_2006_ENG_SOURCE.csv', sep='\t')

	for i, row in df.iterrows():
		sentence = row['text']
		if isinstance(sentence, str):
			sentence = Sentence(sentence)

			tagger.predict(sentence)

			print(sentence.to_tagged_string())

if __name__ == "__main__":
	main()