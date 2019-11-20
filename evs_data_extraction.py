import pandas as pd
from populate_tables import *
# from extract_information import *
# from module_enum import *
# from itemtype_enum import *
import numpy as np
import sys
import os
import re


def get_survey_info_and_populate_table(filename):
	surveyid = filename.replace('.xlsx', '')
	split_items = surveyid.split('_')

	study = split_items[0]
	wave_round = split_items[3]
	year = split_items[-1]
	country_language = split_items[1]+'_'+split_items[2]

	write_survey_table(surveyid, study, wave_round, int(year), country_language)



def main(filename):
	constants = pd.read_excel(open('data/'+str(filename), 'rb'), sheet_name='Constants')
	questionnaire = pd.read_excel(open('data/'+str(filename), 'rb'), sheet_name='Questionnaire')
	answer_types = pd.read_excel(open('data/'+str(filename), 'rb'), sheet_name='Questionnaire')

	#populate survey table
	get_survey_info_and_populate_table(filename)
	
	#populate module table
	list_unique_modules = questionnaire.Module.unique()
	list_unique_modules = ['No module' if isinstance(x, float) else x for x in list_unique_modules]
	write_module_table(list_unique_modules)


	


	# write_itemtype_table(new_types)
	# write_item_name_table(new_names)

	# item_type_unique = data.item_type.unique()
	# new_item_types = find_additional_item_types(item_type_unique)
	# new_types = get_item_type(new_item_types)

	# item_name_unique = data.item_name2.unique()
	# new_item_names= find_additional_item_names(item_name_unique)
	# new_names = get_item_name(new_item_names)

	# module_enum = ModuleEnum()
	# itemtype_enum = ItemTypeEnum()
	# dict_item_names = get_item_name_as_dict()


	# #write to Document table source language documents
	# old = 'old'
	# for index, row in data.iterrows():
	# 	if type(row['module']) is str:
	# 		if old != row['doc_id']:
	# 			old = row['doc_id']
	# 			#@params=documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
	# 			parameters_document = [row['doc_id'], 2, get_module_enum(row['module'], module_enum), row['doc_id'], 'ENG_GB', 'ENG_GB', False]
	# 			write_document_table(parameters_document)
	# 	else:
	# 		if old != row['doc_id']:
	# 			old = row['doc_id']
	# 			#@params=documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
	# 			parameters_document = [row['doc_id'], 2, 10, row['doc_id'], 'ENG_GB', 'ENG_GB', False]
	# 			write_document_table(parameters_document)

	# #write to Document table translated documents
	# old = 'old'
	# for name in dfNames:
	# 	for index, row in dfs[name].iterrows():
	# 		columns = dfs[name].columns
	# 		column_id = get_id_column_name(columns)
	# 		if ('ENG' in name or 'RUS' in name or 'GER' in name or 'FR' in name or 'FRE' in name) and (name != 'ENG_GB'):
	# 			if type(row['module']) is str:
	# 				if column_id != '':
	# 					if old != row[column_id]:
	# 						old = row[column_id]
	# 						#documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
	# 						parameters_document = [row[column_id], 2, get_module_enum(row['module'], module_enum), row['doc_id'], 'ENG_GB', name, True]
	# 						write_document_table(parameters_document)
	# 			else:
	# 				if column_id != '':
	# 					if old != row[column_id]:
	# 						old = row[column_id]
	# 						#documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
	# 						parameters_document = [row[column_id], 2, 10, row['doc_id'], 'ENG_GB', name, True]
	# 						write_document_table(parameters_document)


	# #write to DocumentItem table source language documents items
	# for index, row in data.iterrows():
	# 	if type(row['generic description']) is str:
	# 		if len(row['generic description']) > 1:
	# 			parameters_document_item = [row['doc_id'], get_item_type_enum(row['item_type'], itemtype_enum), remove_html_tags(row['generic description']), False, '', '', '', '', '', False, row['item_name2']] 
	# 			edit_params(parameters_document_item, dict_item_names)
	# 			write_document_item_table(parameters_document_item)
	# 		else:
	# 			parameters_document_item = [row['doc_id'], get_item_type_enum(row['item_type'], itemtype_enum), '', False, '', '', '', '', '', False, row['item_name2']] 
	# 			edit_params(parameters_document_item, dict_item_names)
	# 			write_document_item_table(parameters_document_item)

	#write to DocumentItem table translated documents items
	# for name in dfNames:
	# 	if ('ENG' in name or 'RUS' in name or 'GER' in name or 'FR' in name or 'FRE' in name) and (name != 'ENG_GB'):
	# 		review = ''
	# 		review2 = ''
	# 		for c in dfs[name].columns:
	# 			if 'review' in c.lower():
	# 				review = c
	# 			if 'review2' in c.lower():
	# 				review2 = c
	# 		for index, row in dfs[name].iterrows():
	# 			columns = dfs[name].columns
	# 			column_id = get_id_column_name(columns)
	# 			if column_id != '':
	# 				if review != '' and type(review) is str:
	# 					if review2 != '' and type(review2) is str:
	# 						parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 						row[review], False, row[review2], '', '', '', '', False, row['item_name2']]
	# 					else:
	# 						parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 						row[review], False, '', '', '', '', '', False, row['item_name2']]

	# 					#if check_if_param_is_nan(parameters_document_item) == False:
	# 					edit_params(parameters_document_item, dict_item_names)
	# 					print(parameters_document_item)
	# 					write_document_item_table(parameters_document_item)


	

if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_data_extraction.py EVS_FRE_FR_R05_2017.xlsx
	filename = str(sys.argv[1])
	print("Executing data cleaning/extraction script for EVS 2017")
	main(filename)
