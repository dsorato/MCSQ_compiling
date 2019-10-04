#python3.6 script for dataset cleaning
#Author: Danielly Sorato
#Before running the script, install pandas
import pandas as pd
import numpy as np
from populate_tables import *
from retrieve_from_table import *
from extract_information import *
from module_enum import *
from itemtype_enum import *
import numpy as np
import os
import re


def check_if_itemname(value, dict_item_names):
	itemname = None
	if type(value) is str and value in dict_item_names:
		itemname = dict_item_names[value]


	return itemname

def check_if_scale_in_list(alist, asublist):
	scale_in_list = False
	for item in alist:
		if set(item) == set(asublist):
			scale_in_list = True
			break

	return scale_in_list


def check_if_param_is_nan(params):
	isnan = False
	for param in params:
		if pd.isnull(param):
			isnan = True
			break

	return isnan 	

#@params: 0=documentid, 1=itemtypeid, 2=text, 3=morethanonetranslation, 4=translation2, 5=translation3, 6=translationadjudication, 
#7=translationverification, 8=translationdescription, 9=translationupdated, 10=itemnameid
def edit_params(params, dict_item_names):
	params[10] = check_if_itemname(params[10], dict_item_names)
	params[2] = remove_html_tags(params[2])
	if params[4] != '':
		params[3] = True
		params[4] = remove_html_tags(params[4])
		if params[6] != '' and params[7] != '':
			params[6] = remove_html_tags(params[6])
			params[7] = remove_html_tags(params[7])
		elif params[7] == '' and params[6] != '':
			params[6] = remove_html_tags(params[6])
		elif params[7] != '' and params[6] == '':
			params[7] = remove_html_tags(params[7])

	else:
		if params[6] != '' and params[7] != '':
			params[6] = remove_html_tags(params[6])
			params[7] = remove_html_tags(params[7])
		elif params[7] == '' and params[6] != '':
			params[6] = remove_html_tags(params[6])
		elif params[7] != '' and params[6] == '':
			params[7] = remove_html_tags(params[7])

	return params


def remove_html_tags(text):
	if type(text) is str:
		text = re.sub("<.*?>", "", text)
		text = re.sub("’", "'", text)
		text = re.sub("[^a-zA-Z'а-яА-Я.?!(),öäüÖÄÜß`àâçéèêëîïôûùüÿñæœ:;¿¡/\"’\[\]0-9\-]+", "		",text)
		text = " ".join(text.split())
		text = text.strip()

	return text

def lowercase(text):
	return text.lower()


def main():
	#change directory to round 8 folder and read csv
	os.chdir('/home/upf/workspace/PCSQ/clean_and_populate')
	data = pd.read_excel('data/tmt_ess_r8_2016v1.xlsx')
	#data = pd.read_csv('ess_r8.csv')

	#delete unwanted elements in dataset
	print('Deleting columns there are at least 90 per cent empty')
	cols_to_delete = data.columns[data.isnull().sum()/len(data) > .90]
	data.drop(cols_to_delete, axis = 1, inplace = True)
	print('Deleted columns: ', cols_to_delete)

	print('Deleting unwanted columns')
	data = data.drop(['parent_type', 'parent'], axis=1)

	print('Remaining columns:')
	for col in data.columns:
		print(col) 

	df_metadata = data[['doc_id', 'module', 'item_type', 'item_name']]
	module_unique = data.module.unique()
	module_names = get_module_name(module_unique)
	module_names.append('No module')
	module_names = get_generic_module_name(module_names)

	item_type_unique = data.item_type.unique()
	item_types = get_item_type(item_type_unique)
	item_types.append('No type')

	item_name_unique = data.item_name.unique()
	item_names = get_item_name(item_name_unique)

	# write_survey_table("ESS", 8, 2016)
	# write_module_table(module_names)
	# write_item_name_table(item_names)


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

	dfsScales = dict()
	dfNamesScales = []
	for name in dfNames:
		prefix = name.split('_')[0]
		if name != 'item_name' and prefix == 'GER' or prefix == 'RUS' or prefix == 'FRE' or prefix == 'ENG':
			dfNamesScales.append(name)
			working_df = dfs[name]
			is_response_option = working_df['item_type']=='Response option'
			response_options = working_df[is_response_option]
			columns = response_options.columns
			print(columns)
			if name == 'RUS_RU':
				response_options_mod = response_options.dropna(how='any', subset=['RUS_RU_ReviewAdjudication'])
			elif name == 'RUS_LT':
				response_options_mod = response_options.dropna(how='any', subset=['RUS_LT_ReviewAdjudication'])
			else:
				response_options_mod = response_options.dropna(how='any', subset=[name])
			dfsScales[name] = response_options_mod
	

	#We know when doc items are from same scale because they have the same doc_id
	old_id = 'old'
	scales_list = []
	aux_list = []
	aux_language_country_list = []
	for name in dfNamesScales:
		df = dfsScales[name]
		#position 0 of language country list is always the Language and Country information
		aux_language_country_list.append([name])
		for index, row in df.iterrows():
			new_id = row['doc_id']
			if old_id != new_id:
				same_scale = df.loc[df['doc_id'] == new_id]
				for index, row in same_scale.iterrows():
					if name == 'RUS_RU':
						aux_list.append(remove_html_tags(row['RUS_RU_ReviewAdjudication']))
					elif name == 'RUS_LT':
						aux_list.append(remove_html_tags(row['RUS_LT_ReviewAdjudication']))
					else:
						aux_list.append(remove_html_tags(row[name]))

				if check_if_scale_in_list(aux_language_country_list, aux_list) == False:
					aux_language_country_list.append(aux_list)

			old_id = row['doc_id']
			aux_list = []
		scales_list.append(aux_language_country_list)
		aux_language_country_list = []

	for item in scales_list:
		print('*****')
		print(item)



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
	# 			parameters_document = [row['doc_id'], 1, get_module_enum(row['module'], module_enum), row['doc_id'], 'ENG_GB', 'ENG_GB', False]
	# 			write_document_table(parameters_document)
	# 	else:
	# 		if old != row['doc_id']:
	# 			old = row['doc_id']
	# 			#@params=documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
	# 			parameters_document = [row['doc_id'], 1, 10, row['doc_id'], 'ENG_GB', 'ENG_GB', False]
	# 			write_document_table(parameters_document)

	# #write to Document table translated documents		
	# old = 'old'
	# for name in dfNames:
	# 	for index, row in dfs[name].iterrows():
	# 		columns = dfs[name].columns
	# 		column_id = get_id_column_name(columns)
	# 		if type(row['module']) is str:
	# 			if column_id != '':
	# 				if old != row[column_id]:
	# 					old = row[column_id]
	# 					#documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
	# 					parameters_document = [row[column_id], 1, get_module_enum(row['module'], module_enum), row['doc_id'], 'ENG_GB', name, True]
	# 					write_document_table(parameters_document)
	# 		else:
	# 			if column_id != '':
	# 				if old != row[column_id]:
	# 					old = row[column_id]
	# 					#documentid, surveyid, moduleid, sourcedocumentid, sourcecountrylanguage, countrylanguage, documentistranslation
	# 					parameters_document = [row[column_id], 1, 10, row['doc_id'], 'ENG_GB', name, True]
	# 					write_document_table(parameters_document)


	# #write to DocumentItem table source language documents items
	# for index, row in data.iterrows():
	# 	if type(row['ENG_GB']) is str and row['ENG_GB'] != '-':
	# 		parameters_document_item = [row['doc_id'], get_item_type_enum(row['item_type'], itemtype_enum), row['ENG_GB'], False, '', '', '', '', '', False, row['item_name']]
	# 		edit_params(parameters_document_item, dict_item_names)
	# 		write_document_item_table(parameters_document_item)
	# 	else:
	# 		parameters_document_item = [row['doc_id'], get_item_type_enum(row['item_type'], itemtype_enum), '', False, '', '', '', '', '', False, row['item_name']] 
	# 		edit_params(parameters_document_item, dict_item_names)
	# 		write_document_item_table(parameters_document_item)



	# #write to DocumentItem table translated documents items
	# for name in dfNames:
	# 	if name != 'ENG_GB':
	# 		verification = ''
	# 		adjudication = ''
	# 		translation1 = ''
	# 		translation2 = ''
	# 		translation3 = ''
	# 		for c in dfs[name].columns:
	# 			if 'verification' in c.lower():
	# 				verification = c
	# 			if 'adjudication' in c.lower():
	# 				adjudication = c
	# 			if 'translation1' in c.lower():
	# 				translation1 = c
	# 			if 'translation2' in c.lower():
	# 				translation2 = c
	# 			if 'translation3' in c.lower():
	# 				translation3 = c
	# 		for index, row in dfs[name].iterrows():
	# 			columns = dfs[name].columns
	# 			column_id = get_id_column_name(columns)
	# 			if column_id != '':
	# 				if translation1 != '' and type(translation1) is str:
	# 					if verification != '' and adjudication != '' and translation2 != '':
	# 						parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 						row[translation1], False, row[translation2], translation3, row[adjudication], row[verification], '', False, row['item_name']]
	# 					if verification == '' and adjudication != '' and translation2 != '':
	# 						parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 						row[translation1], False, row[translation2], translation3, row[adjudication], verification, '', False, row['item_name']]
	# 					if verification == '' and adjudication == '' and translation2 != '':
	# 						parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 						row[translation1], False, row[translation2], translation3, adjudication, verification, '', False, row['item_name']]
	# 					if verification != '' and adjudication == '' and translation2 != '':
	# 						parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 						row[translation1], False, row[translation2], translation3, adjudication, row[verification], '', False, row['item_name']]
	# 					if verification != '' and adjudication == '' and translation2 == '':
	# 						parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 						row[translation1], False, translation2, translation3, adjudication, row[verification], '', False, row['item_name']]
	# 					if verification != '' and adjudication != '' and translation2 == '':
	# 						parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 						row[translation1], False, translation2, translation3, row[adjudication], row[verification], '', False, row['item_name']]
	# 					if verification == '' and adjudication != '' and translation2 == '':
	# 						parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 						row[translation1], False, translation2, translation3, row[adjudication], verification, '', False, row['item_name']]
	# 					if verification == '' and adjudication == '' and translation2 == '':
	# 						parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 						row[translation1], False, translation2, translation3, adjudication, verification, '', False, row['item_name']]

	# 					#if check_if_param_is_nan(parameters_document_item) == False:
	# 					edit_params(parameters_document_item, dict_item_names)
	# 					print(parameters_document_item)
	# 					write_document_item_table(parameters_document_item)

	# 				else:
	# 					if type(row[name]) is str:
	# 						if verification != '' and adjudication != '' and translation2 != '':
	# 							parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 							row[name], False, row[translation2], translation3, row[adjudication], row[verification], '', False, row['item_name']]
	# 						if verification == '' and adjudication != '' and translation2 != '':
	# 							parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 							row[name], False, row[translation2], translation3, row[adjudication], verification, '', False, row['item_name']]
	# 						if verification == '' and adjudication == '' and translation2 != '':
	# 							parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 							row[name], False, row[translation2], translation3, adjudication, verification, '', False, row['item_name']]
	# 						if verification != '' and adjudication == '' and translation2 != '':
	# 							parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 							row[name], False, row[translation2], translation3, adjudication, row[verification], '', False, row['item_name']]
	# 						if verification != '' and adjudication == '' and translation2 == '':
	# 							parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 							row[name], False, translation2, translation3, adjudication, row[verification], '', False, row['item_name']]
	# 						if verification != '' and adjudication != '' and translation2 == '':
	# 							parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 							row[name], False, translation2, translation3, row[adjudication], row[verification], '', False, row['item_name']]
	# 						if verification == '' and adjudication != '' and translation2 == '':
	# 							parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 							row[name], False, translation2, translation3, row[adjudication], verification, '', False, row['item_name']]
	# 						if verification == '' and adjudication == '' and translation2 == '':
	# 							parameters_document_item = [row[column_id], get_item_type_enum(row['item_type'], itemtype_enum), 
	# 							row[name], False, translation2, translation3, adjudication, verification, '', False, row['item_name']]
							
	# 						#if check_if_param_is_nan(parameters_document_item) == False:
	# 						edit_params(parameters_document_item, dict_item_names)
	# 						print(parameters_document_item)
	# 						write_document_item_table(parameters_document_item)

if __name__ == "__main__":
	print("Executing data cleaning script for ESS")
	main()


