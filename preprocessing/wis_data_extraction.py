import sys
import os
import re
import pandas as pd
from preprocessing_ess_utils import *
import utils as ut

def harmonize_item_type(wis_item_type):
	"""
	Translates the item type indicated in the WIS exports to the item types that are present in the MCSQ.
	Args:
		param1 wis_item_type (string): the item type value in a give row from the WIS export.

	Returns:
		an item type (string) that corresponds to the MCSQ item types. Could be INTRODUCTION, RESPONSE, REQUEST or INSTRUCTION.
	"""
	if 'intro' in wis_item_type or 'heading' in wis_item_type:
		return 'INTRODUCTION' 
	elif 'option'in wis_item_type:
		return 'RESPONSE' 
	elif 'question' in wis_item_type or 'matrix group' in wis_item_type:
		return 'REQUEST' 
	elif 'hint' in wis_item_type or 'alert' in wis_item_type: 
		return 'INSTRUCTION' 

def simplify_item_name(wis_item_name):
	"""
	Simplifies the unique item names in the WIS exports to atribute unique item names for each survey item.
	This makes easier to find the survey items inside the MCSQ, as you will not need to search for each unique variable name 
	(as it is in the WIS export).
	Args:
		param1 wis_item_name (string): the item name value in a give row from the WIS export.

	Returns:
		an item name (string) that will be used for all segments concerning a given WIS survey item.
	"""
	if  re.findall(r'.*_\d+$',wis_item_name) or  re.findall(r'.*_yn$',wis_item_name) or re.findall(r'.*_\-8$',wis_item_name) or re.findall(r'.*_\-7$',wis_item_name):
		wis_item_name = wis_item_name.rpartition('_')[0]
	if re.findall(r'.*_hint$',wis_item_name) or re.findall(r'.*_hint1$',wis_item_name) or re.findall(r'.*_hint2$',wis_item_name):
		wis_item_name = wis_item_name.rpartition('_')[0]
	if re.findall(r'.*_alert$',wis_item_name) or re.findall(r'.*_alert1$',wis_item_name) or re.findall(r'.*_alert2$',wis_item_name):
		wis_item_name = wis_item_name.rpartition('_')[0]
	if re.findall(r'.*_yn$',wis_item_name):
		wis_item_name = wis_item_name.rpartition('_')[0]
	if re.findall(r'^HINT_',wis_item_name):
		wis_item_name = wis_item_name.replace('HINT_', '')
	if 'NOT_USED_' in wis_item_name:
		wis_item_name = wis_item_name.replace('NOT_USED_', '')
	if  re.findall(r'^INFO_end\d+$',wis_item_name) or wis_item_name=='textbox_end4' or wis_item_name=='INFO_endclick':
		wis_item_name = 'INFO_end'
	if  'introD' in wis_item_name:
		wis_item_name = wis_item_name.replace('_introD', '')
	if  wis_item_name == 'MNSUBS_API' or wis_item_name == 'mnsubnosay' or wis_item_name == 'mnsubother':
		wis_item_name = 'mnsub'
	if wis_item_name == 'supv3_alert':
		wis_item_name = 'supv2'
	if wis_item_name == 'jobhist5':
		wis_item_name = 'jobhist4'
	if wis_item_name == 'yyeduca_1001':
		wis_item_name = 'yyeduca'
	if wis_item_name == 'washif61':
		wis_item_name = 'washifts'
	if wis_item_name == 'wadirt61':
		wis_item_name = 'wadirty'
	if wis_item_name == 'watips61':
		wis_item_name = 'watips'
	if wis_item_name == 'waseni61':
		wis_item_name = 'wasenior'
	if wis_item_name == 'waperf61':
		wis_item_name = 'waperfom'
	if wis_item_name == 'wapers62':
		wis_item_name = 'waperson'
	if wis_item_name == 'waannu61':
		wis_item_name = 'waannual'
	if wis_item_name == 'waothe61':
		wis_item_name = 'waother'
	
	return wis_item_name

def instantiate_survey_item_prefix(study, column_name):
	"""
	Maps the WIS data export text column names to the ISO standards used in MCSQ.
	Then, defines the prefix of the survey item in accordance to the MCSQ standard nomenclature.
	The prefix of an MCSQ survey item is study+'_'+language+'_'+country+'_'

	Args:
		param1 study (string): the name of the study, embedded in the WIS export filename.
		param2 column_name (string): the name of the text column, from the WIS export.

	Returns:
		a language specific survey item ID prefix (string).

	"""
	language_country_pairs = {'source': 'ENG_SOURCE', 'en_GB': 'ENG_GB', 'fr_FR': 'FRE_FR', 'pt_PT': 'POR_PT', 'ru_RU': 'RUS_RU',
	'de_DE': 'GER_DE', 'es_ES': 'SPA_ES', 'no_NO': 'NOR_NO', 'cs_CZ': 'CZE_CZ'}

	return study+'_'+language_country_pairs[column_name]+'_'

def extract_wis_data(df, df_questionnaire, study):
	"""
	Extracts and preprocesses WIS data from df, attibuting MCSQ metadata (and also harmonizing metadata e.g. item names, item types, when necessary). 

	Args:
		param1 df (pandas dataframe): the input data in a dataframe representation.
		param2 df_questionnaire (pandas dataframe): a dataframe to hold the processed questionnaire data.
		param3 study (string): the name of the study, embedded in the WIS export filename.

	Returns:
		the df_questionnaire (pandas dataframe) with the preprocessed data.

	"""
	survey_item_prefix_source = instantiate_survey_item_prefix(study, 'source')
	survey_item_prefix_eng = instantiate_survey_item_prefix(study, 'en_GB')
	survey_item_prefix_fre = instantiate_survey_item_prefix(study, 'fr_FR')
	survey_item_prefix_por = instantiate_survey_item_prefix(study, 'pt_PT')
	survey_item_prefix_rus = instantiate_survey_item_prefix(study, 'ru_RU')
	survey_item_prefix_ger = instantiate_survey_item_prefix(study, 'de_DE')
	survey_item_prefix_spa = instantiate_survey_item_prefix(study, 'es_ES')
	survey_item_prefix_nor = instantiate_survey_item_prefix(study, 'no_NO')
	survey_item_prefix_cze = instantiate_survey_item_prefix(study, 'cs_CZ')
	
	df['NEXT_ITEM_TYPE'] = df['ITEM_TYPE'].shift(-1)

	flag = 0
	for i, row in df.iterrows():
		if isinstance(row['PAGE'], str) and row['PAGE'] != 'ALERT_1' and row['PAGE'] != 'ALERT_2':
			item_name = simplify_item_name(row['UNIQUE IDENTIFIER (PER SURVEY)'])
			item_value = row['VALUES of VAR']
			wis_item_type = row['ITEM_TYPE']
			item_type = harmonize_item_type(wis_item_type)

			if str(row['source']) != 'TRANSLATION IN TASK_API' and 'NO TRANSLATION' not in str(row['en_GB']):
				if isinstance(row['source'], str) or isinstance(row['source'], int):
					if wis_item_type == 'matrix question' and row['NEXT_ITEM_TYPE'] != 'matrix option':
						if flag == 0:
							count = 0
							flag = 1
						else:
							count = count+1

						df_questionnaire.iloc[-1, df_questionnaire.columns.get_loc('item_name')] =item_name+'_'+str(count)


						df['item_name'] = df['UNIQUE IDENTIFIER (PER SURVEY)'].replace(to_replace=row['LAST_ITEM_NAME'], value=item_name+'_introD')

						df_by_item_name = df[df['UNIQUE IDENTIFIER (PER SURVEY)'] == row['UNIQUE IDENTIFIER (PER SURVEY)']]
						df_by_item_name_responses = df_by_item_name[df_by_item_name['ITEM_TYPE']=='matrix option']

						if df_questionnaire.empty:
							survey_item_id_source = ut.get_survey_item_id(survey_item_prefix_source)
						else:
							survey_item_id_source = ut.update_survey_item_id(survey_item_prefix_source)

						data = {'Study': study, 'module': row['PAGE'], 'item_type': item_type, 
						'wis_item_type': wis_item_type,'item_name':item_name+'_'+str(count),'item_value':item_value, 
						'ENG_SOURCE_survey_item_ID':survey_item_id_source,  'ENG_SOURCE_text':row['source'],
						'ENG_GB_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_eng),  'ENG_GB_text':row['en_GB'], 
						'FRE_FR_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_fre),  'FRE_FR_text':row['fr_FR'],
						'POR_PT_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_por),  'POR_PT_text':row['pt_PT'],
						'RUS_RU_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_rus),  'RUS_RU_text':row['ru_RU'], 
						'GER_DE_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_ger),  'GER_DE_text':row['de_DE'],
						'SPA_ES_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_spa),  'SPA_ES_text':row['es_ES'],
						'NOR_NO_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_nor),  'NOR_NO_text':row['no_NO'],
						'CZE_CZ_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_cze),  'CZE_CZ_text':row['cs_CZ']}
						df_questionnaire = df_questionnaire.append(data, ignore_index = True)

						for i, row in df_by_item_name_responses.iterrows():
							survey_item_id_source = ut.update_survey_item_id(survey_item_prefix_source)
							item_name = simplify_item_name(row['UNIQUE IDENTIFIER (PER SURVEY)'])
							item_value = row['VALUES of VAR']
							wis_item_type = row['ITEM_TYPE']
							item_type = harmonize_item_type(wis_item_type)

							data = {'Study': study, 'module': row['PAGE'], 'item_type': item_type, 
							'wis_item_type': wis_item_type,'item_name':item_name+'_'+str(count),'item_value':item_value, 
							'ENG_SOURCE_survey_item_ID':survey_item_id_source,  'ENG_SOURCE_text':row['source'],
							'ENG_GB_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_eng),  'ENG_GB_text':row['en_GB'], 
							'FRE_FR_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_fre),  'FRE_FR_text':row['fr_FR'],
							'POR_PT_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_por),  'POR_PT_text':row['pt_PT'],
							'RUS_RU_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_rus),  'RUS_RU_text':row['ru_RU'], 
							'GER_DE_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_ger),  'GER_DE_text':row['de_DE'],
							'SPA_ES_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_spa),  'SPA_ES_text':row['es_ES'],
							'NOR_NO_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_nor),  'NOR_NO_text':row['no_NO'],
							'CZE_CZ_survey_item_ID': ut.get_survey_item_id(survey_item_prefix_cze),  'CZE_CZ_text':row['cs_CZ']}
							df_questionnaire = df_questionnaire.append(data, ignore_index = True)

					else:
						flag = 0
						if df_questionnaire.empty:
							survey_item_id_source = ut.get_survey_item_id(survey_item_prefix_source)
						else:
							survey_item_id_source = ut.update_survey_item_id(survey_item_prefix_source)


						data = {'Study': study, 'module': row['PAGE'], 'item_type': item_type, 
						'wis_item_type': wis_item_type,'item_name':item_name,'item_value':item_value, 
						'ENG_SOURCE_survey_item_ID':survey_item_id_source,  'ENG_SOURCE_text':row['source'],
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

def prepare_df_for_data_extraction(df, df_questionnaire, study):
	"""
	Does preliminary editions in the input data to make the data extraction easier, such as harmonizing the item names
	of matrix survey item segments.
	Then, calls the data extraction method.

	Args:
		param1 df (pandas dataframe): the input data in a dataframe representation.
		param2 df_questionnaire (pandas dataframe): a dataframe to hold the processed questionnaire data.
		param3 study (string): the name of the study, embedded in the WIS export filename.

	Returns:
		the df_questionnaire (pandas dataframe) with the preprocessed data.

	"""

	df['LAST_ITEM_TYPE'] = df['ITEM_TYPE'].shift(1)
	df['LAST_ITEM_NAME'] = df['UNIQUE IDENTIFIER (PER SURVEY)'].shift(1)

	for i, row in df.iterrows():
		item_name = row['UNIQUE IDENTIFIER (PER SURVEY)']
		wis_item_type = row['ITEM_TYPE']
		if row['LAST_ITEM_TYPE'] == 'heading':
			df['UNIQUE IDENTIFIER (PER SURVEY)'] = df['UNIQUE IDENTIFIER (PER SURVEY)'].replace(to_replace=row['LAST_ITEM_NAME'], value=item_name+'_introD')
		if wis_item_type == 'matrix group':
			m_group_name  = item_name
		if  wis_item_type == 'matrix question' or wis_item_type == 'matrix option':
			df=df.replace(to_replace=r'^'+row['UNIQUE IDENTIFIER (PER SURVEY)']+'$', value=m_group_name, regex=True)
		
	
	df_questionnaire = extract_wis_data(df, df_questionnaire, study)

	return df_questionnaire
	
		
def post_process_questionnaire(df_questionnaire):
	"""
	Loops through the language/country pairs to export questionnaire and alignment data separatedely 
	(one questionnaire file and one aligment per language/country pair).

	Args:
		param1 df_questionnaire (pandas dataframe): the preprocessed questionnaire data, containing the text for all language/country pairs.

	"""

	language_country_pairs = ['ENG_GB', 'FRE_FR', 'POR_PT', 'RUS_RU','GER_DE', 'SPA_ES','NOR_NO', 'CZE_CZ']
	for l in language_country_pairs:
		df = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 'text'])
		df_alignment = pd.DataFrame(columns=['source_survey_item_ID', 'target_survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 
		'source_text', 'target_text'])
		for i, row in df_questionnaire.iterrows():
			data = {'survey_item_ID': row[l+'_survey_item_ID'], 'Study': row['Study'], 'module': row['module'], 'item_type': row['item_type'], 
			'item_name': row['item_name'], 'item_value': row['item_value'], 'text':row[l+'_text']}
			df = df.append(data, ignore_index = True)	

			data = {'source_survey_item_ID': row['ENG_SOURCE_survey_item_ID'], 'target_survey_item_ID': row[l+'_survey_item_ID'], 
			'Study': row['Study'], 'module': row['module'], 'item_type': row['item_type'], 
			'item_name': row['item_name'], 'item_value': row['item_value'], 'source_text':row['ENG_SOURCE_text'], 'target_text':row[l+'_text']}
			df_alignment = df_alignment.append(data, ignore_index = True)	
			
			study = row['Study']

		df.to_csv(study+'_'+l+'.csv', sep='\t', encoding='utf-8-sig', index=False)
		df_alignment.to_csv('ENG_SOURCE'+'_'+l+'_'+study+'.csv', sep='\t', encoding='utf-8-sig', index=False)




def set_initial_structures(filename):
	"""
	Set initial structures that are necessary for the extraction of each questionnaire.

	Args:
		param1 filename (string): name of the input file.

	Returns: 
		df_questionnaire to store questionnaire data (pandas dataframe) and the study (string), which is embedded in the file name.
	"""
	df_questionnaire = pd.DataFrame(columns=['Study', 'module', 'item_type', 'wis_item_type',
		'item_name', 'item_value', 'ENG_SOURCE_survey_item_ID',  'ENG_SOURCE_text',
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
	Main method of the Wage Indicator data extraction and processing script.
	The data is extracted, preprocessed and receives appropriate metadata attribution.  

	The algorithm outputs the tsv representation of the df_questionnaire, used to store 
	questionnaire data (pandas dataframe).

	Args:
		param1 folder_path: path to the folder where the WIS master file is.
	"""
	path = os.chdir(folder_path)
	files = os.listdir(path)


	for index, file in enumerate(files):
		if file.endswith(".xlsx"):	
			df = pd.read_excel(file, sheet_name='WIS')
			df = df[['source', 'en_GB', 'fr_FR', 'pt_PT', 'ru_RU', 'de_DE', 'es_ES', 'no_NO', 'cs_CZ',
			'UNIQUE IDENTIFIER (PER SURVEY)', 'VALUES of VAR', 'ITEM_TYPE','PAGE']]

			df_questionnaire, study = set_initial_structures(file)
			df_questionnaire = prepare_df_for_data_extraction(df, df_questionnaire, study)
			# df_questionnaire.to_csv('pre.csv', sep='\t', encoding='utf-8-sig', index=False)
			post_process_questionnaire(df_questionnaire)
			




if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)