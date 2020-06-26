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
		item_id = get_instructionid_from_text(text)
	elif item_type == 'REQUEST':
		item_id = get_requestid_from_text(text)
	elif item_type == 'INTRODUCTION':
		item_id = get_introductionid_from_text(text)

	print(item_id)

def get_alignment_per_row(df):
	for i, row in df.iterrows():
		if row['item_type'] != 'RESPONSE':
			if pd.isnull(row['source']):
				retrieve_based_on_item_type(row['target'], row['item_type']) 
			elif pd.isnull(row['target']):
				retrieve_based_on_item_type(row['source'], row['item_type']) 
			else:
				retrieve_based_on_item_type(row['source'], row['item_type']) 
				retrieve_based_on_item_type(row['target'], row['item_type']) 

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