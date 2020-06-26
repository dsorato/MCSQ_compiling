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

def get_alignment_per_row(df):
	for i, row in df.iterrows():
		if pd.isnull(row['source']):
			item_id = get_id_from_text(row['target'], row['item_type']) 
		elif pd.isnull(row['target']):
			item_id = get_id_from_text(row['source'], row['item_type']) 
		else:
			item_id_source = get_id_from_text(row['source'], row['item_type']) 
			item_id_target = get_id_from_text(row['target'], row['item_type']) 

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