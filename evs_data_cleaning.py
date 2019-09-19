import pandas as pd
from populate_tables import *
from ess_data_cleaning import *
from retrieve_from_table import *
from extract_information import *
from module_enum import *
from itemtype_enum import *
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
	data = data.drop(['questionnaire', 'parent_type', 'parent', 'item_name', 'item_order', 'call'], axis=1)

	print('Remaining columns:')
	for col in data.columns:
		print(col)

	df_metadata = data[['doc_id', 'module', 'item_type', 'item_name2', 'mode', 'generic description id', 'generic description']]
	df_text = data.drop(['doc_id', 'module', 'item_type', 'item_name2', 'mode', 'generic description id', 'generic description'], axis=1)

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
	
	item_type_unique = data.item_type.unique()
	new_item_types = find_additional_item_types(item_type_unique)
	new_types = get_item_type(new_item_types)

	item_name_unique = data.item_name2.unique()
	new_item_names= find_additional_item_names(item_name_unique)
	new_names = get_item_name(new_item_names)

	write_survey_table("EVS", 5, 2017, 'unknown')
	write_itemtype_table(new_types)
	write_item_name_table(new_names)

	module_enum = ModuleEnum()
	itemtype_enum = ItemTypeEnum()
	dict_item_names = get_item_name_as_dict()


	#write to Document table source language documents
	old = 'old'
	for index, row in data.iterrows():
		if type(row['module']) is str:
			if old != row['doc_id']:
				old = row['doc_id']
				#@params=documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
				parameters_document = [row['doc_id'], 2, get_module_enum(row['module'], module_enum), row['doc_id'], 'ENG_GB', 'ENG_GB', False]
				write_document_table(parameters_document)
		else:
			if old != row['doc_id']:
				old = row['doc_id']
				#@params=documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
				parameters_document = [row['doc_id'], 2, 10, row['doc_id'], 'ENG_GB', 'ENG_GB', False]
				write_document_table(parameters_document)

	#write to Document table translated documents
	old = 'old'
	for name in dfNames:
		for index, row in dfs[name].iterrows():
			columns = dfs[name].columns
			column_id = get_id_column_name(columns)
			if ('ENG' in name or 'RUS' in name or 'GER' in name or 'FR' in name or 'FRE' in name) and (name != 'ENG_GB'):
				if type(row['module']) is str:
					if column_id != '':
						if old != row[column_id]:
							old = row[column_id]
							#documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
							parameters_document = [row[column_id], 2, get_module_enum(row['module'], module_enum), row['doc_id'], 'ENG_GB', name, True]
							write_document_table(parameters_document)
				else:
					if column_id != '':
						if old != row[column_id]:
							old = row[column_id]
							#documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
							parameters_document = [row[column_id], 2, 10, row['doc_id'], 'ENG_GB', name, True]
							write_document_table(parameters_document)


	#write to DocumentItem table source language documents items
	for index, row in data.iterrows():
		if type(row['generic description']) is str:
			if len(row['generic description']) > 1:
				parameters_document_item = [row['doc_id'], get_item_type_enum(row['item_type'], itemtype_enum), remove_html_tags(row['generic description']), False, '', '', '', '', '', False, row['item_name2']] 
				edit_params(parameters_document_item, dict_item_names)
				write_document_item_table(parameters_document_item)
			else:
				parameters_document_item = [row['doc_id'], get_item_type_enum(row['item_type'], itemtype_enum), '', False, '', '', '', '', '', False, row['item_name2']] 
				edit_params(parameters_document_item, dict_item_names)
				write_document_item_table(parameters_document_item)

	#write to DocumentItem table translated documents items
	for name in dfNames:
		if 'RUS' in name:
		#if ('ENG' in name or 'RUS' in name or 'GER' in name or 'FR' in name or 'FRE' in name) and (name != 'ENG_GB'):
			review = ''
			review2 = ''
			for c in dfs[name].columns:
				if 'review' in c.lower():
					review = c
				if 'review2' in c.lower():
					review2 = c
			for index, row in dfs[name].iterrows():
				columns = dfs[name].columns
				column_id = get_id_column_name(columns)
				if column_id != '':
					if review != '' and type(review) is str:
						if review2 != '' and type(review2) is str:
							parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
							row[review], False, row[review2], '', '', '', '', False]
						else:
							parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
							row[review], False, '', '', '', '', '', False]

						#if check_if_param_is_nan(parameters_document_item) == False:
						edit_params(parameters_document_item)
						print(parameters_document_item)
						write_document_item_table(parameters_document_item)


	

if __name__ == "__main__":
	print("Executing data cleaning script for EVS")
	main()
