"""
Main file that calls text to spreadsheet transformation algorithm
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
"""
import os
import sys
sys.path.insert(0, 'txt2spreadsheet')
sys.path.insert(0, 'utils')
import utils
import txt2spreadsheet 


"""
This main file calls the transformation algorithm inside txt2spreadsheet script.

The algorithm transforms a plain text file (within specifications) to a structured spreadsheet format
with valuable metadata. The algorithm also concatenates the aforementioned file and
pre-processed spreadsheets from the SQP database (suplementary modules of ESS).

Call main script using folder_path, for instance: 
reset && python3 main.py /home/upf/workspace/txt_to_spreadsheet/data

:param folder_path: the path of the directory containing the files to tranform

"""
def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)
	csv_file = ''
	for index, file in enumerate(files):
		if file.endswith(".txt"):
			print(file)
			txt_file = file
			remove_file_extension = file.replace('.txt', '')
			split_filename = remove_file_extension.split('_')
			"""
			The filenames respect a nomenclature rule, as follows:
			SSS_RRR_YYYY_CC_LLL
			S = study name 
			R = round or wave
			Y = study year
			C = Country (ISO code with two digits, except for SOURCE)
			L = Language
			"""
			study = split_filename[0]+'_'+split_filename[1]+'_'+split_filename[2]
			language_country = split_filename[3]+'_'+split_filename[4]

		if file.endswith(".csv"):
			print(file)
			csv_file = file
		
	# python3 txt2spr.py ESS_R01_2002_SOURCE_ENG.txt SOURCE_ENG ESS_R01_2002
	txt2spr.main(csv_file, txt_file, language_country, study)
		



if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)