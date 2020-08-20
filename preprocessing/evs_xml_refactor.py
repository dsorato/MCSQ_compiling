import pandas as pd
import xml.etree.ElementTree as ET
import utils as ut
from preprocessing_evs_utils import *
from evsmodules import * 

"""
Retrieves the module of the survey_item, based on information from the EVSModulesYYYY objects.
This information comes from the EVS_modules_reference.xlsx file, sent by Evelyn.
:param study:
:param country_language:
:param name: attribute 'name' of the analyzed node, which is an EVS variable. 
The interest variables are listed in the EVSModulesYYYY objects.

:returns: module of survey_item in string format.
"""
def retrieve_item_module(study, country_language, name):
	"""
	Names such as PT26, PT11-PT12 will be attributed to a National Module.
	Such variables are not referenced in the EVS_modules_reference.xlsx file.
	"""
	country = country_language.split('_')[-1]
	if name.find(country) != -1:
		return 'Country-localized questions'

	else:
		"""
		Instantiate either EVSModules2008 or EVSModules1999 class, depending on the study year.
		The EVSModulesYYYY class holds information about EVS modules for the year YYYY. 
		"""

		"""
		The modules 'Life Experiences', "Respondent's parents" and "Respondent's partner" 
		are not present in EVS 1999.
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
		elif name.lower() in evsmodules.administrative:
				return 'Administrative/Protocol Variables'
		else:
			return None

"""
Extracts information from preQTxt node (requests and introductions). The text is split into 
sentences and appropriate metadata is attributed to it. 

:param filename: name of the input file. It will be used to instantiate the sentence splitter.
:param preQTxt: valid node that is being analyzed.
:param survey_item_prefix: prefix of the survey_item_ID metadata
:param study: study metadata, retrieved from the filename.
:param item_name: item_name metadata, retrieved from the process_valid_node() method.
:param module: module of survey_item, extracted in previous steps of the loop.
:param df_questionnaire: pandas dataframe where the questionnaire is being stored.

:returns: df_questionnaire, with new information extracted from the preQTxt node.
"""
def process_preqtxt_node(filename, preQTxt, survey_item_prefix, study, item_name, module, df_questionnaire):
	splitter = ut.get_sentence_splitter(filename)

	if '?' not in preQTxt.text:
		item_type = 'INTRODUCTION'
		text = clean_text(preQTxt.text, filename)
	else:
		text = clean_text(preQTxt.text, filename)
		item_type = 'REQUEST'

	sentences = splitter.tokenize(text)

	for sentence in sentences:
		if df_questionnaire.empty:
			survey_item_id = ut.get_survey_item_id(survey_item_prefix)
		else:
			survey_item_id = ut.update_survey_item_id(survey_item_prefix)

		data = {"survey_item_ID": survey_item_id,'Study': study, 'module': module,'item_type': item_type, 
		'item_name': item_name, 'item_value': None,  'text': sentence}
		df_questionnaire = df_questionnaire.append(data, ignore_index = True)

	return df_questionnaire

"""
Extracts information from ivuInstr node (instructions). The text is split into sentences and appropriate 
metadata is attributed to it. 

:param filename: name of the input file. It will be used to instantiate the sentence splitter.
:param ivuInstr: valid node that is being analyzed.
:param survey_item_prefix: prefix of the survey_item_ID metadata
:param study: study metadata, retrieved from the filename.
:param item_name: item_name metadata, retrieved from the process_valid_node() method.
:param module: module of survey_item, extracted in previous steps of the loop.
:param df_questionnaire: pandas dataframe where the questionnaire is being stored.

:returns: df_questionnaire, with new information extracted from the ivuInstr node.
"""
def process_ivuinstr_node(filename, ivuInstr, survey_item_prefix, study, item_name, module, df_questionnaire):
	splitter = ut.get_sentence_splitter(filename)

	item_type = 'INSTRUCTION'
	text = clean_instruction(ivuInstr.text)
	
	sentences = splitter.tokenize(text)

	for sentence in sentences:
		if df_questionnaire.empty:
			survey_item_id = ut.get_survey_item_id(survey_item_prefix)
		else:
			survey_item_id = ut.update_survey_item_id(survey_item_prefix)

		data = {"survey_item_ID": survey_item_id,'Study': study, 'module': module,'item_type': item_type, 
		'item_name': item_name, 'item_value': None,  'text': sentence}
		df_questionnaire = df_questionnaire.append(data, ignore_index = True)

	return df_questionnaire

"""
Extracts information from qstnLit node (requests). The text is split into sentences and appropriate 
metadata is attributed to it. 

:param filename: name of the input file. It will be used to instantiate the sentence splitter.
:param qstnLit: valid node that is being analyzed.
:param survey_item_prefix: prefix of the survey_item_ID metadata
:param study: study metadata, retrieved from the filename.
:param item_name: item_name metadata, retrieved from the process_valid_node() method.
:param module: module of survey_item, extracted in previous steps of the loop.
:param df_questionnaire: pandas dataframe where the questionnaire is being stored.

:returns: df_questionnaire, with new information extracted from the qstnLit node.
"""
def process_qstnLit_node(filename, qstnLit, survey_item_prefix, study, item_name, module, df_questionnaire):
	splitter = ut.get_sentence_splitter(filename)

	item_type = 'REQUEST'
	text = clean_text(qstnLit.text, filename)
	
	sentences = splitter.tokenize(text)

	for sentence in sentences:
		if df_questionnaire.empty:
			survey_item_id = ut.get_survey_item_id(survey_item_prefix)
		else:
			survey_item_id = ut.update_survey_item_id(survey_item_prefix)

		data = {"survey_item_ID": survey_item_id,'Study': study, 'module': module,'item_type': item_type, 
		'item_name': item_name, 'item_value': None,  'text': sentence}
		df_questionnaire = df_questionnaire.append(data, ignore_index = True)

	return df_questionnaire

"""
Extracts information from txt node (requests). The text is split into sentences and appropriate 
metadata is attributed to it. 

:param filename: name of the input file. It will be used to instantiate the sentence splitter.
:param txt: valid node that is being analyzed.
:param survey_item_prefix: prefix of the survey_item_ID metadata
:param study: study metadata, retrieved from the filename.
:param item_name: item_name metadata, retrieved from the process_valid_node() method.
:param module: module of survey_item, extracted in previous steps of the loop.
:param df_questionnaire: pandas dataframe where the questionnaire is being stored.

:returns: df_questionnaire, with new information extracted from the txt node.
"""
def process_txt_node(filename, txt, survey_item_prefix, study, item_name, module, df_questionnaire):
	splitter = ut.get_sentence_splitter(filename)

	item_type = 'REQUEST'
	text = clean_text(txt.text, filename)
	
	sentences = splitter.tokenize(text)

	for sentence in sentences:
		if df_questionnaire.empty:
			survey_item_id = ut.get_survey_item_id(survey_item_prefix)
		else:
			survey_item_id = ut.update_survey_item_id(survey_item_prefix)

		data = {"survey_item_ID": survey_item_id,'Study': study, 'module': module,'item_type': item_type, 
		'item_name': item_name, 'item_value': None,  'text': sentence}
		df_questionnaire = df_questionnaire.append(data, ignore_index = True)

	return df_questionnaire

"""
Calls the appropriate method to extract information from node and its children, when the node is valid 
(variable listed in EVSModulesYYYY classes), depending on node tag.

:param filename: name of the input file. It will be used to instantiate the sentence splitter.
:param node: valid node that is being analyzed.
:param survey_item_prefix: prefix of the survey_item_ID metadata
:param study: study metadata, retrieved from the filename.
:param module: module of survey_item, extracted in previous steps of the loop.
:param df_questionnaire: pandas dataframe where the questionnaire is being stored.

:returns: df_questionnaire, with new information extracted from the valid node.
"""
def process_valid_node(filename, node, survey_item_prefix, study, module, df_questionnaire):
	"""
	A valid node can have qstn or txt (or both inside the same node) child nodes.
	The attribute that stores the item_name depends on the type of the node (qstn or txt).
	"""
	for child in node.getiterator():
		if child.tag == 'qstn' and 'seqNo' in child.attrib:
			item_name = child.attrib['seqNo']
			item_name = standartize_item_name(item_name)

			"""
			qstn nodes can have preQTxt (requests or introductions), ivuInstr (instructions) or
			qstnLit (requests) child nodes.
			"""
			for grandchild in child.getiterator():
				if grandchild.tag == 'preQTxt':
					df_questionnaire= process_preqtxt_node(filename,grandchild, survey_item_prefix, study, item_name, module, df_questionnaire)
				
				if grandchild.tag == 'ivuInstr':
					df_questionnaire = process_ivuinstr_node(filename,grandchild, survey_item_prefix, study, item_name, module, df_questionnaire)
				
				if grandchild.tag == 'qstnLit':
					df_questionnaire = process_qstnLit_node(filename,grandchild, survey_item_prefix, study, item_name, module, df_questionnaire)

		elif child.tag == 'txt' and 'level' in child.attrib:
			item_name = child.attrib['level']
			item_name = standartize_item_name(item_name)

			"""
			txt nodes do not have children.
			"""
			text = child.text
			df_questionnaire = process_txt_node(filename,child, survey_item_prefix, study, item_name, module, df_questionnaire)


	return df_questionnaire

def main(filename):
	"""
	The prefix of a EVS survey item is study+'_'+language+'_'+country+'_'
	"""
	survey_item_prefix = re.sub('\.xml', '', filename)+'_'

	"""
	Reset the initial survey_id sufix, because main is called iterativelly for every XML file in folder.
	"""
	ut.reset_initial_sufix()

	"""
	Retrieve study and country_language information from the name of the input file. 
	"""
	study, country_language = get_country_language_and_study_info(filename)
	
	"""
	Determine the country using the information contained in the filename.
	Information needed to exclude some unecessary segments of the EVS XML file.
	"""
	country = ut.determine_country(filename)

	"""
	A pandas dataframe to store the questionnaire data being extracted. 
	"""
	df_questionnaire = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module','item_type', 'item_name', 'item_value', 'text'])

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
			# print(node.attrib)
			if 'name' in node.attrib:
				module = retrieve_item_module(study, country_language, node.attrib['name'])
				if module != None:
					df_questionnaire = process_valid_node(filename, node, survey_item_prefix, study, module, df_questionnaire)

			# if node.tag=='catgry' and 'ID' in node.attrib:
			# 	txt = node.find('txt')
			# 	catValu = node.find('catValu')
			# 	if df_questionnaire.empty:
			# 		survey_item_id = ut.get_survey_item_id(survey_item_prefix)
			# 	else:
			# 		survey_item_id = ut.update_survey_item_id(survey_item_prefix)

			# 	if txt is not None and txt.text != country and txt.text is not None:
			# 		last_row = df_questionnaire.tail(1)
			# 		module = last_row['module'].values
			# 		module = "".join(module)
			# 		item_name = last_row['item_name'].values
			# 		item_name = "".join(item_name)

			# 		data = {"survey_item_ID": survey_item_id,'Study': study, 'module':module,
			# 		'item_type': 'RESPONSE', 'item_name': item_name, 'item_value': int(catValu.text),  
			# 		'text': clean_text(txt.text, filename)}
			# 		df_questionnaire = df_questionnaire.append(data, ignore_index = True)

			

	csv_name = filename.replace('.xml', '')
	df_questionnaire.to_csv(str(csv_name)+'.csv', encoding='utf-8-sig', index=False)



if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_xml_data_extraction.py EVS_R03_1999_FRE_FR.xml
	filename = str(sys.argv[1])
	print("Executing data extraction script for EVS 1999/2008 (xml files)")
	main(filename)
