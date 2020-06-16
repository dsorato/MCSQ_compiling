import os
import sys
sys.path.insert(0, 'txt2spr')
sys.path.insert(0, 'utils')
import utils
import txt2spr 


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
			study = split_filename[0]+'_'+split_filename[1]+'_'+split_filename[2]
			language_country = split_filename[3]+'_'+split_filename[4]

		if file.endswith(".csv"):
			print(file)
			csv_file = file
		
	# python3 txt2spr.py ESS_R01_2002_SOURCE_ENG.txt SOURCE_ENG ESS_R01_2002
	txt2spr.main(csv_file, txt_file, language_country, study)
		



if __name__ == "__main__":
	#Call script using folder_path
	#For instance: reset && python3 main.py /home/upf/workspace/txt_to_spreadsheet/data
	folder_path = str(sys.argv[1])
	main(folder_path)