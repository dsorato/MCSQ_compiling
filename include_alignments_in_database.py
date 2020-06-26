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
from retrieve_from_tables import *


def retrieve_based_on_item_type(text, item_type):
	if item_type == 'INSTRUCTION':
		item_id =  get_instruction_id(text)
		items_to_include = get_survey_item_info_from_id(item_id, 'instructionid')
	elif item_type == 'REQUEST':
		item_id =  get_request_id(text)
		items_to_include = get_survey_item_info_from_id(item_id, 'requestid')
	elif item_type == 'INTRODUCTION':
		item_id =  get_introduction_id(text)
		items_to_include = get_survey_item_info_from_id(item_id, 'introductionid')

	return items_to_include
	

def get_alignment_per_row(df):
	for i, row in df.iterrows():
		if row['item_type'] != 'RESPONSE':
			if pd.isnull(row['source']):
				items_to_include = retrieve_based_on_item_type(row['target'], row['item_type']) 
				for i in items_to_include:
					write_alignment_table(None, row['target'], None, i[0])
			elif pd.isnull(row['target']):
				items_to_include = retrieve_based_on_item_type(row['source'], row['item_type']) 
				for i in items_to_include:
					write_alignment_table(row['source'], None, i[0], None)
			else:
				items_to_include_source = retrieve_based_on_item_type(row['source'], row['item_type']) 
				items_to_include_target = retrieve_based_on_item_type(row['target'], row['item_type'])

				for source, target in zip(items_to_include_source, items_to_include_target):
					write_alignment_table(row['source'], row['target'], source[0], target[0])

		# print(row['item_type'], row['source'], row['target'])

def main(folder_path):
	os.chdir(folder_path)
	files = os.listdir(folder_path)
	for index, file in enumerate(files):
		if file.endswith(".csv"):
			print(file)
			df = pd.read_csv(file)
			get_alignment_per_row(df)
				

if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)