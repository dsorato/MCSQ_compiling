"""
Python3 script to convert ESS item names to two-digit format
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 


import os
import sys
import pandas as pd
import nltk.data
import re


import sys
import os
import re
import pandas as pd 

def convert_item_name(file):
	data = pd.read_csv(file)
	item_name_pattern = re.compile('[A-Z][0-9][a-z]?$')
	for i, row in data.iterrows():
		if item_name_pattern.match(row['item_name']):
			print(row['item_name'])
			new_item_name = row['item_name'][0] + '0' + row['item_name'][1:]
			data.at[i,'item_name'] = new_item_name

	data.to_csv(file, encoding='utf-8', index=False)


def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)
	csv_file = ''
	for index, file in enumerate(files):
		if file.endswith(".csv"):
			print(file)
			
			convert_item_name(file)


if __name__ == "__main__":
	#Call script using folder_path
	#For instance: reset && python3 main.py /home/upf/workspace/txt_to_spreadsheet/data
	folder_path = str(sys.argv[1])
	main(folder_path)