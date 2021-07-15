import sys
import os 
import pandas as pd

def add_annotation(df_source, df_target, df_alignment):
	"""
	Adds NER/POS annotations in the alignment files by copying the annotations from the spreadsheets.
	Differently from the EVS, ESS and SHARE files, all the WIS files have 1-1 correspondences and come prealigned,
	therefore these files do not have to go through the Alignment algorithm.  
	
	Args:
		param1 df_source (pandas dataframe): the dataframe that holds the preprocessed annotated source questionnaire.
		param2 df_target (pandas dataframe): the dataframe that holds the preprocessed annotated target questionnaire.
		param3 df_alignment (pandas dataframe): the dataframe that holds the alignment questionnaire, without annotations.

	Returns:
		df_alignment (pandas dataframe) with added NER and POS annotations that were copied from the df_source and df_target. 
	"""
	df_alignment['source_ner_tagged_text'] = df_source['ner_tagged_text'].values 
	df_alignment['source_pos_tagged_text'] = df_source['pos_tagged_text'].values 

	df_alignment['target_ner_tagged_text'] = df_target['ner_tagged_text'].values 
	df_alignment['target_pos_tagged_text'] = df_target['pos_tagged_text'].values 


	return df_alignment

def main(folder_path, filename_source, filename_target, filename_alignment):
	path = os.chdir(folder_path)
	df_source = pd.read_csv(filename_source,  dtype=str, sep='\t')
	df_target = pd.read_csv(filename_target,  dtype=str, sep='\t')
	df_alignment = pd.read_csv(filename_alignment,  dtype=str, sep='\t')



	df = add_annotation(df_source, df_target, df_alignment)
	df.to_csv(filename_alignment, encoding='utf-8', sep='\t', index=False)


if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	filename_source = str(sys.argv[2])
	filename_target = str(sys.argv[3])
	filename_alignment = str(sys.argv[4])
	main(folder_path, filename_source, filename_target, filename_alignment)