import pandas as pd
from populate_tables import *
from extract_information import *
import numpy as np
import os
import re

def main():
	data = pd.read_excel('data/shocc_export_EVS2017_270819.xlsx')
	#delete unwanted elements in dataset
	print('Deleting columns there are at least 90 per cent empty')
	cols_to_delete = data.columns[data.isnull().sum()/len(data) > .90]
	data.drop(cols_to_delete, axis = 1, inplace = True)
	print('Deleted columns: ', cols_to_delete)

	print('Deleting unwanted columns')
	data = data.drop(['questionnaire', 'parent_type', 'parent', 'item_name.1', 'item_order', 'call'], axis=1)

	print('Remaining columns:')
	for col in data.columns:
		print(col)

	df_metadata = data[['doc_id', 'module', 'item_type', 'item_name', 'mode', 'generic description id', 'generic description']]
	df_text = data.drop(['doc_id', 'module', 'item_type', 'item_name', 'mode', 'generic description id', 'generic description'], axis=1)

	translations = []
	for col in df_text.columns:
		translations.append(col)

	groups = group_by_prefix(translations)


	dfs = dict()

	dfNames = []
	for item in groups:
		dfName = get_code(item[0])
		if dfName not in dfNames:
			dfNames.append(dfName)
			dfNew = data[item]
			dfs[dfName] = dfNew

	module_unique = df_metadata.module.unique()
	item_type_unique = df_metadata.item_type.unique()
	print(module_unique)
	print(item_type_unique)

if __name__ == "__main__":
	print("Executing data cleaning script for EVS")
	main()
