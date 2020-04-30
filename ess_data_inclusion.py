#python3.6 script for ESS dataset inclusion in the MCSQ database
#Author: Danielly Sorato
#Before running the script, install pandas, numpy, SQLAlchemy, psycopg2
import pandas as pd
import numpy as np
import sys
import os
from populate_tables import *

#Function responsible for getting the module full names in a given study/round.
def get_module_full_names(study, wave_round):
	if study == 'ESS':
		if wave_round == 'R01':
			module_names = {'A': 'A - Media; social trust', 'B': 'B - Politics, including: political interest, efficacy, trust, electoral and other forms of participation, party allegiance, socio-political evaluations/orientations, multi-level governance',
			'C': 'C - Subjective well-being and social exclusion; religion; perceived discrimination; national and ethnic identity', 'D': 'D - Immigration and asylum issues, including: attitudes, perceptions, policy preferences and knowledge',
			'E': 'E - Citizen involvement: including organisational membership, family and friendship bonds, citizenship values, working environment', 
			'F': 'F - Socio-demographic profile, including: Household composition, sex, age, type of area, Education & occupation details of respondent, partner, parents, union membership, household income, marital status',
			'SUPP_G': 'Human values scale', 'SUPP_GF': 'Human values scale', 'SUPP_GS': 'Human values scale', 'SUPP_H': 'Test questions', 'SUPP_I': 'Interviewer questions', 'INTRO_MODULE': 'Specific from MCSQ database: text that introduces a given module'}


	return module_names 


def populate_survey_table(surveyid, study, wave_round, year, country_language):
	write_survey_table(surveyid, study, wave_round, year, country_language)


def populate_module_table(file):
	#import data from preprocessed csv into a dataframe
	data = pd.read_csv(file)
	module = data['module']
	#get only unique values in module column
	module_unique = data.module.unique()
	
	print(module_unique)

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
			# populate_survey_table(surveyid, study, wave_round, year, country_language)
			populate_module_table(file)

			

		



if __name__ == "__main__":
	#Call script using folder_path
	#For instance: reset && python3 main.py /home/upf/workspace/txt_to_spreadsheet/data
	folder_path = str(sys.argv[1])
	main(folder_path)