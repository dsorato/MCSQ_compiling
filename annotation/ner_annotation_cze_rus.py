from deeppavlov import build_model
import os
import sys
import pandas as pd

def ner_annotation(df, ner):
	df_tagged = pd.DataFrame(columns=['survey_itemID', 'Study', 'module', 'item_type', 'item_name', 'item_value',  'text', 'ner_tagged_text', 'pos_tagged_text'])
	for i, row in df.iterrows():
		print(ner([row['text']]))

def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)
	ner_model = build_model("/home/danielly/workspace/Slavic-BERT-NER/ner_bert_slav.json", download=True)


	for index, file in enumerate(files):
		if file.endswith(".csv"):
			df = pd.read_csv(file,  dtype=str, sep='\t')
			ner_annotation(df, ner_model)

if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)