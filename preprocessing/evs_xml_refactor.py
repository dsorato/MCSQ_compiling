import pandas as pd
import xml.etree.ElementTree as ET
import utils as ut
from preprocessing_evs_utils import *
from evsmodules import * 


def retrieve_item_module(study, country_language, name):
	"""
	Names such as PT26 will be attributed to a National Module.
	"""
	country = country_language.split('_')[-1]
	if name.find(country) != -1:
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
		elif name.lower() in evsmodules.administrative:
				return 'Administrative/Protocol Variables'
		else:
			return None


def retrieve_item_name(node):
	item_name = ''
	qstn = node.find('qstn')
	txt = node.find('txt')

	if txt is not None and qstn is None and 'level' in txt.attrib:
		item_name = txt.attrib['level']
	
	else:
		if qstn is not None and 'seqNo' in qstn.attrib:
			item_name = qstn.attrib['seqNo'] 
	
	if item_name:
		return standartize_item_name(item_name)
	else:
		return None


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


def process_valid_node(filename, node, survey_item_prefix, study, module, df_questionnaire):
	qstn = node.find('qstn')
	if qstn is not None and 'seqNo' in qstn.attrib:
		item_name = qstn.attrib['seqNo']

		preQTxt = qstn.find('preQTxt')
		if preQTxt is not None:
			df_questionnaire= process_preqtxt_node(filename,preQTxt, survey_item_prefix, study, item_name, module, df_questionnaire)
		ivuInstr = qstn.find('ivuInstr')
		if ivuInstr is not None:
			df_questionnaire = process_ivuinstr_node(filename,ivuInstr, survey_item_prefix, study, item_name, module, df_questionnaire)
		qstnLit = qstn.find('qstnLit')
		if qstnLit is not None:
			df_questionnaire = process_qstnLit_node(filename,qstnLit, survey_item_prefix, study, item_name, module, df_questionnaire)

	txt = node.find('txt')
	if txt is not None and 'level' in txt.attrib:
		item_name = txt.attrib['level']
		text = txt.text
		df_questionnaire = process_txt_node(filename,txt, survey_item_prefix, study, item_name, module, df_questionnaire)

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
			if 'name' in node.attrib:
				module = retrieve_item_module(study, country_language, node.attrib['name'])
				if module != None:
					df_questionnaire = process_valid_node(filename, node, survey_item_prefix, study, module, df_questionnaire)

	csv_name = filename.replace('.xml', '')
	df_questionnaire.to_csv(str(csv_name)+'.csv', encoding='utf-8-sig', index=False)



if __name__ == "__main__":
	#Call script using filename. 
	#For instance: reset && python3 evs_xml_data_extraction.py EVS_R03_1999_FRE_FR.xml
	filename = str(sys.argv[1])
	print("Executing data extraction script for EVS 1999/2008 (xml files)")
	main(filename)
