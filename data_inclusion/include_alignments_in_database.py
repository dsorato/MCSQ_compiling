"""
Python3 script for including alignments in the MCSQ database
Before running the script, install requirements: pandas, numpy, SQLAlchemy, psycopg2
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 
import pandas as pd
import numpy as np
import sys
import os
from populate_tables import *


"""
Populates the alignment table using the alignment files generated by the alignment_based_on_item_structure_algorithm.

Args:
	param1 df (pandas dataframe): dataframe from input alignment csv file.

"""
def populate_alignment_table(df):
	for i, row in df.iterrows():
		if pd.isnull(row['source_text']):
			write_alignment_table(None, row['target_text'], None, row['target_survey_itemID'])

		elif pd.isnull(row['target_text']):
			write_alignment_table(row['source_text'], None, row['source_survey_itemID'], None)
		
		else:
			write_alignment_table(row['source_text'], row['target_text'], row['source_survey_itemID'], row['target_survey_itemID'])



def main(folder_path):
	os.chdir(folder_path)
	files = os.listdir(folder_path)
	for index, file in enumerate(files):
		if file.endswith(".csv"):
			print(file)
			df = pd.read_csv(file)
			populate_alignment_table(df)
				

if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)