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
		module_description = {'A': 'Media; social trust', 'B': 'Politics, including: political interest, efficacy, trust, electoral and other forms of participation, party allegiance, socio-political evaluations/orientations, multi-level governance',
		'C': 'Subjective well-being and social exclusion; religion; perceived discrimination; national and ethnic identity', 'D': 'Immigration and asylum issues, including: attitudes, perceptions, policy preferences and knowledge',
		'E': 'Citizen involvement: including organisational membership, family and friendship bonds, citizenship values, working environment', 
		'F': 'Socio-demographic profile, including: Household composition, sex, age, type of area, Education & occupation details of respondent, partner, parents, union membership, household income, marital status',
		'SUPP_G': 'Human values scale', 'SUPP_GF': 'Human values scale', 'SUPP_GS': 'Human values scale', 'SUPP_H': 'Test questions', 'SUPP_I': 'Interviewer questions', 'INTRO_MODULE': 'Specific from MCSQ database: text that introduces a given module',
		'SUPP_A': 'Supplementary questions with module A equivalents (from SQP database)', 'SUPP_B': 'Supplementary questions with module B equivalents (from SQP database)',
		'SUPP_C': 'Supplementary questions with module C equivalents (from SQP database)', 'SUPP_D': 'Supplementary questions with module D equivalents (from SQP database)',
		'SUPP_E': 'Supplementary questions with module E equivalents (from SQP database)', 'SUPP_F': 'Supplementary questions with module F equivalents (from SQP database)' }

		if wave_round == 'R02':
			module_description['D'] = 'Health and care seekin health, medicine, and doctor/patient relations'
			module_description['E'] = 'Economic morality Trust and interactions between producers and consumers'
			module_description['SUPP_G'] = 'Family Work and Wellbeing work-life balance'
			module_description['SUPP_H'] = 'Human values scale'
			module_description['SUPP_I'] = 'Test questions'
			module_description['SUPP_J'] = 'Interviewer self-completion questions'

		elif wave_round == 'R03':
			module_description['D'] = 'Timing of life; the life course; timing of key life events, attitudes to ideal age, youngest age and oldest age of life events, planning for retirement'
			module_description['E'] = 'Personal and social well-being, helping others, feelings in the last week, life satisfaction, satisfaction with work.'
			module_description['SUPP_I'] = 'Interviewer self-completion questions'
		
		elif wave_round == 'R04':
			module_description['D'] = 'Welfare includes attitudes towards welfare provision, size of claimant groups, views on taxation, attitudes towards service delivery and likely future dependence on welfare.'
			module_description['E'] = 'Ageism covers attitudes towards and experiences of ageism, age related status, stereotypes, experience of discrimination and contact with people in other age groups.'
			module_description['SUPP_I'] = 'Interviewer self-completion questions'

		elif wave_round == 'R05':
			module_description['D'] = 'Trust in the Police and Courts, including: confidence in the police and courts, cooperation with the police and courts, contact with the police and attitudes towards punishment.'
			module_description['SUPP_I'] = 'Interviewer self-completion questions'
			module_description['SUPP_G'] = 'Work, Family and Wellbeing, including: impact of the recession on households and work, job security, housework, wellbeing, experiences of unemployment and work-life balance.'
			module_description['SUPP_H'] = 'Human values scale'
			module_description['SUPP_I'] = 'Test questions'
			module_description['SUPP_J'] = 'Interviewer self-completion questions'
	
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
		last_survey_item_unique = get_survey_item_last_record()
		if row['item_type'] == 'REQUEST':
			write_request_table(last_survey_item_unique, row['survey_item_ID'], row[country_language], '', '', '', '', row['item_name'], row['item_type'])
		elif row['item_type'] == 'INSTRUCTION':
			write_instruction_table(last_survey_item_unique, row['survey_item_ID'], row[country_language], '', '', '', '', row['item_name'], row['item_type'])
		elif row['item_type'] == 'RESPONSE':
			if pd.isnull(row['item_value']):
				write_response_table(last_survey_item_unique, row['survey_item_ID'], row[country_language], '', '', '', '', row['item_name'], row['item_type'], None)
			else:
				write_response_table(last_survey_item_unique, row['survey_item_ID'], row[country_language], '', '', '', '', row['item_name'], row['item_type'], row['item_value'])
		elif row['item_type'] == 'INTRO' or row['item_type'] == 'INTRODUCTION':
			write_introduction_table(last_survey_item_unique, row['survey_item_ID'], row[country_language], '', '', '', '', row['item_name'], row['item_type'])

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
			surveyid = remove_file_extension
			country_language = split_filename[3]+'_'+split_filename[4]
			populate_survey_table(surveyid, study, wave_round, year, country_language)
			populate_module_table(study, wave_round, file)
			populate_survey_item_table(file, country_language)

			

		



if __name__ == "__main__":
	#Call script using folder_path
	#For instance: reset && python3 main.py /home/upf/workspace/txt_to_spreadsheet/data
	folder_path = str(sys.argv[1])
	main(folder_path)