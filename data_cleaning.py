#python3.6 script for dataset cleaning
#Author: Danielly Sorato
#Before running the script, install pandas
import pandas as pd
from populate_tables import *
from extract_information import *
from module_enum import *
from itemtype_enum import *
import os
import re	

#@params: 0=documentid, 1=itemtypeid, 3=text, 4=morethanonetranslation, 5=translation2, 6=translation3, 7=translationadjudication, 
#8=translationverification, 9=translationdescription, 10=translationupdated
def edit_params(params):
	params[3] = remove_html_tags(params[3])
	if translation2 != '':
		params[4] = True
		params[5] = remove_html_tags(params[5])
		if adjudication != '' and verification != '':
			params[7] = remove_html_tags(params[7])
			params[8] = remove_html_tags(params[8])
		elif verification == '' and adjudication != '':
			params[7] = remove_html_tags(params[7])
		elif verification != '' and adjudication == '':
			params[8] = remove_html_tags(params[8])

	else:
		if adjudication != '' and verification != '':
			params[7] = remove_html_tags(params[7])
			params[8] = remove_html_tags(params[8])
		elif verification == '' and adjudication != '':
			params[7] = remove_html_tags(params[7])
		elif verification != '' and adjudication == '':
			params[8] = remove_html_tags(params[8])

	return params


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
	item_types.append('No type')

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
		if dfName not in dfNames:
			dfNames.append(dfName)
			dfNew = pd.concat([df_metadata, data[item]], axis=1)
			dfs[dfName] = dfNew


	module_enum = ModuleEnum()
	itemtype_enum = ItemTypeEnum()


	# old = 'old'
	# for index, row in data.iterrows():
	# 	if type(row['module']) is str:
	# 		if old != row['doc_id']:
	# 			old = row['doc_id']
	# 			#@params=documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
	# 			parameters_document = [row['doc_id'], 1, get_module_enum(row['module'], module_enum), row['doc_id'], 'ENG_GB', 'ENG_GB', False]
	# 			write_document_table(parameters_document)
			
	# old = 'old'
	# for name in dfNames:
	# 	for index, row in dfs[name].iterrows():
	# 		if type(row['module']) is str:
	# 				columns = dfs[name].columns
	# 				column_id = get_id_column_name(columns)
	# 				if column_id != '':
	# 					if old != row[column_id]:
	# 						old = row[column_id]
	# 						#documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
	# 						parameters_document = [row[column_id], 1, get_module_enum(row['module'], module_enum), row['doc_id'], 'ENG_GB', name, True]
	# 						write_document_table(parameters_document)

	# for index, row in data.iterrows():
	# 	if type(row['ENG_GB']) is str:
	# 		if len(row['ENG_GB']) > 1:
	# 			parameters_document_item = [row['doc_id'], get_item_type_enum(row['item_type'], itemtype_enum), remove_html_tags(row['ENG_GB']), False, '', '', '', '', '', False] 
	# 			write_document_item_table(parameters_document_item)

	for name in dfNames:
		if name != 'ENG_GB':
			print(dfs[name].columns)
			verification = ''
			adjudication = ''
			translation1 = ''
			translation2 = ''
			translation3 = ''
			for c in dfs[name].columns:
				if 'verification' in c.lower():
					verification = c
				if 'adjudication' in c.lower():
					adjudication = c
				if 'translation1' in c.lower():
					translation1 = c
				if 'translation2' in c.lower():
					translation2 = c
				if 'translation3' in c.lower():
					translation3 = c
			for index, row in dfs[name].iterrows():
				columns = dfs[name].columns
				column_id = get_id_column_name(columns)
				if column_id != '':
					if translation1 != '':
						parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
						translation1, False, translation2, translation3, adjudication, verification, '', False]
						print(parameters_document_item)
						edit_params(parameters_document_item)
						write_document_table(parameters_document_item)
					else:
						parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
						row[name], False, translation2, translation3, adjudication, verification, '', False]
						print(parameters_document_item)
						edit_params(parameters_document_item)
						write_document_table(parameters_document_item)

if __name__ == "__main__":
	print("Executing data cleaning script for ESS")
	main()


