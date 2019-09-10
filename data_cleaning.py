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

	dfNames = []
	for item in groups:
		dfName = get_code(item[0])
		dfNames.append(dfName)
		dfNew = pd.concat([df_metadata, data[item]], axis=1)
		dfs[dfName] = dfNew


	module_enum = ModuleEnum()


	old = 'old'
	for index, row in data.iterrows():
		if type(row['module']) is str:
			if old != row['doc_id']:
				old = row['doc_id']
				#documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
				parameters = [row['doc_id'], 1, get_module_enum(row['module'], module_enum), row['doc_id'], 'ENG_GB', 'ENG_GB', False]
				write_document_table(parameters)
			
	old = 'old'
	for name in dfNames:
		for index, row in dfs[name].iterrows():
			if type(row['module']) is str:
					columns = dfs[name].columns
					column_id = get_id_column_name(columns)
					if column_id != '':
						if old != row[column_id]:
							old = row[column_id]
							#documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
							parameters = [row[column_id], 1, get_module_enum(row['module'], module_enum), row['doc_id'], 'ENG_GB', name, True]
							print(parameters)
							write_document_table(parameters)

	# for k,v in enumerate(dfs.items()):
	# 	for index, row in v.iterrows():
	# 		if old != row['doc_id']:
	# 			print('******')
	# 			print(v)
	# 			print('******')
		# 		old = row['doc_id']
		# 		parameters = [row['doc_id'], 1, get_module_enum(row['module'], module_enum), row['doc_id'], 'ENG_GB', 'ENG_GB', True]
		# 	else:
		# 		pass


if __name__ == "__main__":
	print("Executing data cleaning script for ESS")
	main()


