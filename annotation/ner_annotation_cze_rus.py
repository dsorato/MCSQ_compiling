from deeppavlov import build_model
import os
import sys
import pandas as pd

def ner_annotation(df, ner):
	"""
	Iterates through the preprocessed and POS tag annotated RUS and CZE spreadsheets, adding the NER annotation. 
	POS tag is done in the mcsq_annotation script.
	CZE and RUS languages use multilingual pretrained model provided by Deeppavlov.

	The Slavic-BERT-NER from Deeppavlov uses lib versions that are imcompatible with the ones from the mcsq_annotation script,
	therefore this script should be run using a separate virtual environment.

	Args:
		param1 df (pandas dataframe): the dataframe that holds the preprocessed and POS tag annotated questionnaire.
		param2 ner (BERT model): pretrained NER model provided by Deeppavlov.
		
	Returns:
		df_tagged (pandas dataframe), the questionnaire with added NER annotations. 
	"""
	df_tagged = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value',  'text', 'ner_tagged_text', 'pos_tagged_text'])
	for i, row in df.iterrows():
		tagged = ner([row['text']])
		flat_list = [item for sublist in tagged for item in sublist]
		entities = []
		for token, tag in zip(flat_list[0], flat_list[1]):
			if tag != 'O':
				entities.append(token+'<'+tag+'>')

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



def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)
	ner_model = build_model("/home/danielly/workspace/Slavic-BERT-NER/ner_bert_slav.json", download=True)


	for index, file in enumerate(files):
		if file.endswith(".csv"):
			if 'CZE' in file or 'RUS' in file:
				print(file)
				df = pd.read_csv(file,  dtype=str, sep='\t')
				df_tagged = ner_annotation(df, ner_model)
				df_tagged.to_csv(file, encoding='utf-8', sep='\t', index=False)

if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)