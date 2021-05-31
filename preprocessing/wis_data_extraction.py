import sys
import os
import re
import pandas as pd
from preprocessing_ess_utils import *
import utils as ut

def harmonize_item_type(wis_item_type):
	if 'intro' in wis_item_type or 'heading' in wis_item_type:
		return 'INTRODUCTION' 
	elif 'option'in wis_item_type:
		return 'RESPONSE' 
	elif 'question' in wis_item_type or 'matrix group' in wis_item_type:
		return 'REQUEST' 
	elif 'hint' in wis_item_type or 'alert' in wis_item_type: 
		return 'INSTRUCTION' 

def simplify_item_name(wis_item_name):
	if  re.findall(r'.*_\d+$',wis_item_name) or re.findall(r'.*_hint$',wis_item_name) or re.findall(r'.*_yn$',wis_item_name) or re.findall(r'.*_\-8$',wis_item_name) or re.findall(r'.*_\-7$',wis_item_name) or re.findall(r'.*_hint1$',wis_item_name) or re.findall(r'.*_hint2$',wis_item_name):
		return wis_item_name.rpartition('_')[0]
	else:
		return wis_item_name

def instantiate_survey_item_prefix(study, column_name):

	"""
	The prefix of a EVS survey item is study+'_'+language+'_'+country+'_'
	"""
	language_country_pairs = {'source': 'ENG_SOURCE', 'en_GB': 'ENG_GB', 'fr_FR': 'FRE_FR', 'pt_PT': 'POR_PT', 'ru_RU': 'RUS_RU',
	'de_DE': 'GER_DE', 'es_ES': 'SPA_ES', 'no_NO': 'NOR_NO', 'cs_CZ': 'CZE_CZ'}

	return study+'_'+language_country_pairs[column_name]+'_'

def extract_wis_data(df, df_questionnaire, study):
	survey_item_prefix_source = instantiate_survey_item_prefix(study, 'source')
	survey_item_prefix_eng = instantiate_survey_item_prefix(study, 'en_GB')
	survey_item_prefix_fre = instantiate_survey_item_prefix(study, 'fr_FR')
	survey_item_prefix_por = instantiate_survey_item_prefix(study, 'pt_PT')
	survey_item_prefix_rus = instantiate_survey_item_prefix(study, 'ru_RU')
	survey_item_prefix_ger = instantiate_survey_item_prefix(study, 'de_DE')
	survey_item_prefix_spa = instantiate_survey_item_prefix(study, 'es_ES')
	survey_item_prefix_nor = instantiate_survey_item_prefix(study, 'no_NO')
	survey_item_prefix_cze = instantiate_survey_item_prefix(study, 'cs_CZ')
	

	for i, row in df.iterrows():
		item_name = simplify_item_name(row['UNIQUE IDENTIFIER (PER SURVEY)'])
		item_value = row['VALUES of VAR']
		wis_item_type = row['ITEM_TYPE']
		item_type = harmonize_item_type(wis_item_type)

		if str(row['source']) != 'TRANSLATION IN TASK_API' and 'NO TRANSLATION' not in str(row['source']) and isinstance(row['source'], str):
			if df_questionnaire.empty:
				survey_item_id_source = ut.get_survey_item_id(survey_item_prefix_source)
			else:
				survey_item_id_source = ut.update_survey_item_id(survey_item_prefix_source)

			data = {'Study': study, 'module': row['PAGE'], 'item_type': item_type, 'item_name':item_name, 
			'item_value':item_value, 'ENG_SOURCE_survey_item_ID':survey_item_id_source,  'ENG_SOURCE_text':row['source'],
			'ENG_GB_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_eng),  'ENG_GB_text':row['en_GB'], 
			'FRE_FR_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_fre),  'FRE_FR_text':row['fr_FR'],
			'POR_PT_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_por),  'POR_PT_text':row['pt_PT'],
			'RUS_RU_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_rus),  'RUS_RU_text':row['ru_RU'], 
			'GER_DE_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_ger),  'GER_DE_text':row['de_DE'],
			'SPA_ES_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_spa),  'SPA_ES_text':row['es_ES'],
			'NOR_NO_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_nor),  'NOR_NO_text':row['no_NO'],
			'CZE_CZ_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_cze),  'CZE_CZ_text':row['cs_CZ']}
			df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	return df_questionnaire

def group_wis_data(df, df_questionnaire, study):
	list_of_question_names = []
	for i, row in df.iterrows():
		item_name = row['UNIQUE IDENTIFIER (PER SURVEY)']
		wis_item_type = row['ITEM_TYPE']
		if wis_item_type == 'question':
			list_of_question_names.append(item_name)
		if row['ITEM_TYPE'] == 'heading':
			last_row = df.iloc[-1]
			df=df.replace(to_replace=last_row['UNIQUE IDENTIFIER (PER SURVEY)'], value=item_name+'_intro')
		if wis_item_type == 'matrix group':
			list_of_question_names.append(item_name)
			m_group_name  = item_name
		if  wis_item_type == 'matrix question' or wis_item_type == 'matrix option':
			df=df.replace(to_replace=r'^'+row['UNIQUE IDENTIFIER (PER SURVEY)']+'$', value=m_group_name, regex=True)
		

	unique_item_names = df.ITEM_TYPE.unique()
	for u in unique_item_names:
		df_filtered = df.filter(regex='^'+u,axis=1)
		df_questionnaire = extract_wis_data(df, df_questionnaire, study)

	return df_questionnaire
	
		
def post_process_questionnaire(df_questionnaire):
	language_country_pairs = ['ENG_GB', 'FRE_FR', 'POR_PT', 'RUS_RU','GER_DE', 'SPA_ES','NOR_NO', 'CZE_CZ']
	for l in language_country_pairs:
		df = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 'text'])
		df_alignment = pd.DataFrame(columns=['source_survey_itemID', 'target_survey_itemID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 
		'source_text', 'target_text'])
		for i, row in df_questionnaire.iterrows():
			data = {'survey_item_ID': row[l+'_survey_item_ID'], 'Study': row['Study'], 'module': row['module'], 'item_type': row['item_type'], 
			'item_name': row['item_name'], 'item_value': row['item_value'], 'text':row[l+'_text']}
			df = df.append(data, ignore_index = True)	

			data = {'source_survey_itemID': row['ENG_SOURCE_survey_item_ID'], 'target_survey_itemID': row[l+'_survey_item_ID'], 
			'Study': row['Study'], 'module': row['module'], 'item_type': row['item_type'], 
			'item_name': row['item_name'], 'item_value': row['item_value'], 'source_text':row['ENG_SOURCE_text'], 'target_text':row[l+'_text']}
			df_alignment = df_alignment.append(data, ignore_index = True)	
			study = row['Study']

		df.to_csv(l+'_'+study.rpartition('_')[0]+'.csv', sep='\t', encoding='utf-8-sig', index=False)
		df_alignment.to_csv('ENG_SOURCE'+'_'+l+'_'+study.rpartition('_')[0]+'.csv', sep='\t', encoding='utf-8-sig', index=False)




def set_initial_structures(filename):
	"""
	Set initial structures that are necessary for the extraction of each questionnaire.

	Args:
		param1 filename (string): name of the input file.

	Returns: 
		df_questionnaire to store questionnaire data (pandas dataframe),
		survey_item_prefix, which is the prefix of survey_item_ID (string), 
		study/language_country, which are metadata parameters embedded in the file name (string and string)
		and sentence splitter to segment request/introduction/instruction segments when necessary (NLTK object). 
	"""

	"""
	A pandas dataframe to store questionnaire data.
	"""
	df_questionnaire = pd.DataFrame(columns=['Study', 'module', 'item_type', 'item_name', 'item_value', 'ENG_SOURCE_survey_item_ID',  'ENG_SOURCE_text',
		'ENG_GB_survey_item_ID',  'ENG_GB_text', 'FRE_FR_survey_item_ID',  'FRE_FR_text', 'POR_PT_survey_item_ID',  'POR_PT_text',
		'RUS_RU_survey_item_ID',  'RUS_RU_text', 'GER_DE_survey_item_ID',  'GER_DE_text', 'SPA_ES_survey_item_ID',  'SPA_ES_text',
		'NOR_NO_survey_item_ID',  'NOR_NO_text', 'CZE_CZ_survey_item_ID',  'CZE_CZ_text'])

	"""
	Study information from the name of the input file. 
	"""
	study = re.sub('\.xlsx', '', filename)


	"""
	Reset the initial survey_id sufix, because main is called iterativelly for every file in folder.
	"""
	ut.reset_initial_sufix()


	return df_questionnaire, study


def main(folder_path):
	"""
	Main method of the Wage Indicator data extraction script.
	The data is extracted, preprocessed and receives appropriate metadata attribution.  

	The algorithm outputs the tsv representation of the df_questionnaire, used to store 
	questionnaire data (pandas dataframe)

	Args:
		param1 folder_path: path to the folder where the WIS master file is.
	"""
	path = os.chdir(folder_path)
	files = os.listdir(path)


	for index, file in enumerate(files):
		if file.endswith(".xlsx"):	
			df = pd.read_excel(file, sheet_name='WIS')
			df_questionnaire, study = set_initial_structures(file)
			df_questionnaire = group_wis_data(df, df_questionnaire, study)
			post_process_questionnaire(df_questionnaire)
			




if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)