import pandas as pd
import xml.etree.ElementTree as ET
from preprocessing_utils import *
from evsmodules import * 


def retrieve_item_module(study, country_language, name):
	"""
	Names such as PT26 will be attributed to a National Module.
	"""
	if country_language.find(name) != -1:
		return 'National Module'

	else:
		"""
		Instantiate either EVSModules2008 or EVSModules1999 class, depending on the study year.
		The EVSModulesYYYY class holds information about EVS modules for the year YYYY. 
		"""

		if '2008' in study:
			evsmodules = EVSModules2008()
			if name.lower() in evsmodules.life_experiences:
				return 'Life Experiences'
			elif name.lower() in evsmodules.respondent_parents:
				return "Respondent's parents"
			elif name.lower() in evsmodules.respondent_partner:
				return "Respondent's partner"

		elif '1999' in study:
			evsmodules = EVSModules1999()

		if name.lower() in evsmodules.perceptions_of_life:
				return 'Perceptions of Life'
		elif name.lower() in evsmodules.politics_and_society:
				return 'Politics and Society'
		elif name.lower() in evsmodules.environment:
				return 'Environment'
		elif name.lower() in evsmodules.family:
				return 'Family'
		elif name.lower() in evsmodules.work:
				return 'Work'
		elif name.lower() in evsmodules.religion_and_morale:
				return 'Religion and Morale'
		elif name.lower() in evsmodules.national_identity:
				return 'National Identity'
		elif name.lower() in evsmodules.socio_demographics:
				return 'Socio Demographics and Interview Characteristics'
		else:
			return 'NO MODULE', name






def main(filename):
	"""
	Retrieve study and country_language information from the name of the input file. 
	"""
	study, country_language = get_country_language_and_study_info(filename)
	
	
	"""
	A pandas dataframe to store the questionnaire data being extracted. 
	"""
	df_survey_item = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module','item_type', 'item_name', 'item_value', country_language])

	"""
	Parse the input XML file by filename
	"""
	file = str(filename)
	tree = ET.parse(file)
	root = tree.getroot()

	"""
	Create a dictionary containing parent-child relations of the parsed tree
	"""
	parent_map = dict((c, p) for p in tree.getiterator() for c in p)

	"""
	Relevant information from the EVS input files can be found on var nodes.
	"""
	evs_vars = root.findall('.//dataDscr/var')

	for var in evs_vars:
		for node in var.getiterator():
			if 'name' in node.attrib:
				if node.attrib['name'].lower() in evsmodules.perceptions_of_life:
					module = retrieve_item_module(study, country_language, node.attrib['name'])
					print(module)





if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_xml_data_extraction.py EVS_R03_1999_FRE_FR.xml
	filename = str(sys.argv[1])
	print("Executing data extraction script for EVS 1999/2008 (xml files)")
	main(filename)
