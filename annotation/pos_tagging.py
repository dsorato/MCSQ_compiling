from flair.models import SequenceTagger
import sys
import pandas as pd
from flair.data import Sentence


def get_model(filename):
	if 'ENG' in filename:
		return SequenceTagger.load('upos') 
	else:
		return SequenceTagger.load('pos-multi') 
		
def main(filename):
	tagger =  get_model(filename)
	df = pd.read_csv(filename, dtype=str, delimiter='\t')

	for i, row in df.iterrows():
		sentence = row['text']
		if isinstance(sentence, str):
			sentence = Sentence(sentence)

			tagger.predict(sentence)

			print(sentence.to_tagged_string())

if __name__ == "__main__":
	filename = str(sys.argv[1])
	main(filename)