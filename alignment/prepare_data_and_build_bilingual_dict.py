import pandas as pd
import numpy as np
import sys
import os
import pickle
from word2word import Word2word
import nltk
import re
from alignment_utils import *
from nltk.stem.snowball import FrenchStemmer
from nltk.stem.porter import *

def remove_punctuation_and_lower_case(text):
	if isinstance(text, str):
		text = text.replace('-',' ')
		text = text.replace('\n',' ')
		text = text.replace('\t',' ')
		text = text.replace('—',' ')
		text = text.replace('…',' ')
		text = text.replace('’',"'")
		
		text = text.rstrip()
		text = text.lstrip()
		

		tokens = nltk.word_tokenize(text.lower())
		tokens_without_punct = []

		for token in tokens: 
			token =  re.sub(r"[^\w'\s]+",'',token) 
			if token != '' and token != '«' and token != '»'  and token != '’':
				tokens_without_punct.append(token)

	return ' '.join(tokens_without_punct)



def main(folder_path, lang):
	os.chdir(folder_path)
	files = os.listdir(folder_path)
	for index, file in enumerate(files):
		if file.endswith(".csv") and lang in file:
			print(file)
			df = pd.read_csv(file, dtype=str, sep='\t')
			i = 0
			with open(lang, 'a') as f:
				l =  convert_iso_code(lang)
				with open(lang+'.en', 'a') as e:
					with open(lang+'.'+l, 'a') as t:
						for i, row in df.iterrows():
							if isinstance(row['source_text'], str) and isinstance(row['target_text'], str) and row['item_type'] != 'RESPONSE':
								source = remove_punctuation_and_lower_case(row['source_text'])
								target = remove_punctuation_and_lower_case(row['target_text'])
								f.write(str(i)+'|'+source+'|'+target)
								i += 1
								f.write("\n")
								e.write(str(i)+'|'+source)
								e.write("\n")
								t.write(str(i)+'|'+target)
								t.write("\n")
			f.close()
			e.close()
			t.close()

	print(folder_path+"/"+lang+"_dict")
	mcsq_dict = Word2word.make("en", l, folder_path+"/"+lang, savedir=folder_path)


	

if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	lang = str(sys.argv[2])
	main(folder_path, lang)