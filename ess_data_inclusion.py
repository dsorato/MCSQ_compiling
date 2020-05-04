#python3.6 script for ESS dataset inclusion in the MCSQ database
#Author: Danielly Sorato
#Before running the script, install pandas, numpy, SQLAlchemy, psycopg2
import pandas as pd
import numpy as np
import sys
import os
from populate_tables import *

#Function responsible for getting the module description in a given study/round.
def get_module_description(study, wave_round):
	if study == 'ESS':
		if wave_round == 'R01':
			module_description = {'A': 'Media; social trust', 'B': 'Politics, including: political interest, efficacy, trust, electoral and other forms of participation, party allegiance, socio-political evaluations/orientations, multi-level governance',
			'C': 'Subjective well-being and social exclusion; religion; perceived discrimination; national and ethnic identity', 'D': 'Immigration and asylum issues, including: attitudes, perceptions, policy preferences and knowledge',
			'E': 'Citizen involvement: including organisational membership, family and friendship bonds, citizenship values, working environment', 
			'F': 'Socio-demographic profile, including: Household composition, sex, age, type of area, Education & occupation details of respondent, partner, parents, union membership, household income, marital status',
			'SUPP_G': 'Human values scale', 'SUPP_GF': 'Human values scale', 'SUPP_GS': 'Human values scale', 'SUPP_H': 'Test questions', 'SUPP_I': 'Interviewer questions', 'INTRO_MODULE': 'Specific from MCSQ database: text that introduces a given module',
			'SUPP_A': 'Supplementary questions with module A equivalents (from SQP database)', 'SUPP_B': 'Supplementary questions with module B equivalents (from SQP database)',
			'SUPP_C': 'Supplementary questions with module C equivalents (from SQP database)', 'SUPP_D': 'Supplementary questions with module D equivalents (from SQP database)',
			'SUPP_E': 'Supplementary questions with module E equivalents (from SQP database)', 'SUPP_F': 'Supplementary questions with module F equivalents (from SQP database)' }


	return module_description 


def populate_survey_table(surveyid, study, wave_round, year, country_language):
	write_survey_table(surveyid, study, wave_round, year, country_language)


def populate_module_table(study, wave_round, file):
	modules_dict =  dict()

	module_description = get_module_description(study, wave_round)
	#import data from preprocessed csv into a dataframe
	data = pd.read_csv(file)
	module = data['module']
	#get only unique values in module column
	module_unique_names = data.module.unique()

	modules_in_questionnaire = dict()
	for module_name in module_unique_names:
		if module_name in module_description:
			modules_dict[module_name] = module_description[module_name]
		
	write_module_table(modules_dict)


def populate_survey_item_table(file, country_language):
	data = pd.read_csv(file)
	item_is_source = False
	mod = get_module_table_as_dict()
	surveyid = get_survey_last_record()

	if country_language == 'ENG_SOURCE':
		item_is_source = True 

	for i, row in data.iterrows():
		write_survey_item_table(row['survey_item_ID'], surveyid, mod[row['module']], country_language, item_is_source, row['item_name'], row['item_type'])

	# print(mod, surveyid)

	# write_survey_item_table(survey_itemid, surveyid, moduleid, country_language, item_is_source, item_name, item_type)

def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)
	csv_file = ''
	for index, file in enumerate(files):
		if file.endswith(".csv"):
			print(file)
			remove_file_extension = file.replace('.csv', '')
			split_filename = remove_file_extension.split('_')
			study = split_filename[0]
			wave_round = split_filename[1]
			year = split_filename[2]
			surveyid = split_filename[0]+'_'+split_filename[1]+'_'+split_filename[2]
			country_language = split_filename[3]+'_'+split_filename[4]
			populate_survey_table(surveyid, study, wave_round, year, country_language)
			populate_module_table(study, wave_round, file)
			populate_survey_item_table(file, country_language)

			

		



if __name__ == "__main__":
	#Call script using folder_path
	#For instance: reset && python3 main.py /home/upf/workspace/txt_to_spreadsheet/data
	folder_path = str(sys.argv[1])
	main(folder_path)