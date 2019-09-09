#python3.6 script for dataset cleaning
#Author: Danielly Sorato
#Before running the script, install pandas
import pandas as pd
from populate_tables import *
from extract_information import *
from module_enum import *
import os
import re	


def remove_html_tags(text):
	text = re.sub("<.*?>", "", text)

	return text

def lowercase(text):
	return text.lower()


def main():
	#change directory to round 8 folder and read csv
	os.chdir('/home/upf/workspace/ESS/round8')
	data = pd.read_csv('ess_r8.csv')

	#delete unwanted elements in dataset
	print('Deleting columns there are at least 90 per cent empty')
	cols_to_delete = data.columns[data.isnull().sum()/len(data) > .90]
	data.drop(cols_to_delete, axis = 1, inplace = True)
	print('Deleted columns: ', cols_to_delete)

	print('Deleting unwanted columns')
	data = data.drop(['parent_type', 'parent', 'item_name'], axis=1)

	print('Remaining columns:')
	for col in data.columns:
		print(col)

	df_metadata = data[['doc_id', 'module', 'item_type']]
	module_unique = data.module.unique()
	module_names = get_module_name(module_unique)
	module_names.append('No module')

	item_type_unique = data.item_type.unique()
	item_types = get_item_type(item_type_unique)


	# write_survey_table()
	# write_module_table(module_names)
	# write_itemtype_table(item_types)
	# update_itemtype_table()


	df_text = data.drop(['doc_id', 'module', 'item_type'], axis=1)
	translations = []
	for col in df_text.columns:
		translations.append(col)

	groups = group_by_prefix(translations)

	dfs = dict()

	for item in groups:
		dfName = get_code(item[0])
		dfNew = df_metadata.append(data[item], sort=False)
		dfs[dfName] = dfNew

	# for k, v in enumerate(dfs.items()):
	# 	print(k,v)


	module_enum = ModuleEnum()


	old = 'old'
	for index, row in data.iterrows():
		if old != row['doc_id']:
			print('oi')
			old = row['doc_id']
			parameters = [row['doc_id'], 1, get_module_enum(row['module'], module_enum), row['doc_id'], 'ENG_GB', 'ENG_GB', False]
			write_source_documents(parameters)
		else:
			pass
			
	
	


if __name__ == "__main__":
	print("Executing data cleaning script for ESS")
	main()


