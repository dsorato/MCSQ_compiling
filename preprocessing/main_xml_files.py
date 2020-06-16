#python script for ESS dataset inclusion in the MCSQ database
#Author: Danielly Sorato 
#Author contact: danielly.sorato@gmail.com

import os
import sys
sys.path.insert(0, 'evs_xml_data_extraction')
sys.path.insert(0, 'ess_xml_data_extraction')
import evs_xml_data_extraction 
import ess_xml_data_extraction 


def main(folder_path):
	# print("Current Working Directory " , os.getcwd()) 
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
	#Call script using folder_path
	#For instance: reset && python3 main.py /home/upf/workspace/PCSQ/clean_and_populate/data
	folder_path = str(sys.argv[1])
	main(folder_path)
