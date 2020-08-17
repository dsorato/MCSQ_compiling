"""
Main method that calls for EVS/ESS scripts to generate MCSQ spreadsheet inputs
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 
import os
import sys
sys.path.insert(0, 'evs_xml_data_extraction')
sys.path.insert(0, 'ess_xml_data_extraction')
import evs_xml_data_extraction 
import ess_xml_data_extraction 

"""
This main file calls the transformation algorithms inside evs_xml_data_extraction 
and ess_xml_data_extraction scripts.

The algorithm transforms a XML file to a structured spreadsheet format
with valuable metadata.

Call main script using folder_path, for instance: 
reset && python3 main.py /path/to/your/data

:param folder_path: the path of the directory containing the files to tranform

"""
def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)

	for index, file in enumerate(files):
		if file.endswith(".xml"):
			print('Filename:', file)
			if 'EVS' in file:
				evs_xml_data_extraction.main(file)
			elif 'ESS' in file:
				ess_xml_data_extraction.main(file)



if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)
