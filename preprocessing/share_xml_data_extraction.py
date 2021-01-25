"""
Python3 script (work in progress) to extract data from XML SHARE input files
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 
import xml.etree.ElementTree as ET
import pandas as pd
import sys
import re
import utils as ut
from preprocessing_ess_utils import *
from sharemodules import *
from share_w7_instructions import *


def get_module_metadata(item_name, share_modules):
	module = None
	for k, v in list(share_modules.items()):
		if item_name[:2] == k:
			return v

	return module

def fill_substitution_in_answer(text, fills, df_procedures):
	texts = []
	df_procedure_filtered = df_procedures[df_procedures['fill_name'].str.lower()==fills[0].lower()]
	if df_procedure_filtered.empty == False:
		last_text = None
		for i, row in df_procedure_filtered.iterrows():
			text_var = text.replace(fills[0], row['text'])
			text_var = text_var.replace('^', ' ')
			if last_text is None or text_var != last_text:
				texts.append(text_var)
				last_text = text_var

	return texts

def eliminate_showcardID_and_adjust_item_type(text, item_name, w7_flag):
	if 'intro' in item_name.lower():
		item_type = 'INTRODUCTION'
		if '^SHOWCARD_ID, si us plau.' in text:
			text = re.sub('\^SHOWCARD_ID', str(ut.update_showcard_id()), text)
			item_type = 'INSTRUCTION'
		elif 'SHOWCARD_ID, si us plau.' in text:
			text = re.sub('SHOWCARD_ID', str(ut.update_showcard_id()), text)
			item_type = 'INSTRUCTION'
		elif '^SHOWCARD_ID, por favor.' in text:
			text = re.sub('\^SHOWCARD_ID', str(ut.update_showcard_id()), text)
			item_type = 'INSTRUCTION'
		elif 'SHOWCARD_ID, por favor.' in text:
			text = re.sub('SHOWCARD_ID', str(ut.update_showcard_id()), text)
			item_type = 'INSTRUCTION'
		elif '^SHOWCARD_ID.' in text:
			text = re.sub('\^SHOWCARD_ID', str(ut.update_showcard_id()), text)
			item_type = 'INSTRUCTION'
		elif '^SHOWCARD_ID' in text:
			text = re.sub('\^SHOWCARD_ID', str(ut.update_showcard_id()), text)
		elif 'SHOWCARD_ID.' in text:
			text = re.sub('SHOWCARD_ID', str(ut.update_showcard_id()), text)
			item_type = 'INSTRUCTION'
		elif 'SHOWCARD_ID' in text:
			text = re.sub('SHOWCARD_ID', str(ut.update_showcard_id()), text)
	elif '^SHOWCARD_ID, si us plau.' in text:
		text = re.sub('\^SHOWCARD_ID', str(ut.update_showcard_id()), text)
		item_type = 'INSTRUCTION'
	elif 'SHOWCARD_ID, si us plau.' in text:
		text = re.sub('SHOWCARD_ID', str(ut.update_showcard_id()), text)
		item_type = 'INSTRUCTION'
	elif '^SHOWCARD_ID, por favor.' in text:
		text = re.sub('\^SHOWCARD_ID', str(ut.update_showcard_id()), text)
		item_type = 'INSTRUCTION'
	elif 'SHOWCARD_ID, por favor.' in text:
		text = re.sub('SHOWCARD_ID', str(ut.update_showcard_id()), text)
		item_type = 'INSTRUCTION'
	elif '^SHOWCARD_ID.' in text:
		text = re.sub('\^SHOWCARD_ID', str(ut.update_showcard_id()), text)
		item_type = 'INSTRUCTION'
	elif '^SHOWCARD_ID' in text:
		text = re.sub('\^SHOWCARD_ID', str(ut.update_showcard_id()), text)
		item_type = 'REQUEST'
	elif 'SHOWCARD_ID.' in text:
		text = re.sub('SHOWCARD_ID', str(ut.update_showcard_id()), text)
		item_type = 'INSTRUCTION'
	elif 'SHOWCARD_ID' in text:
		text = re.sub('SHOWCARD_ID', str(ut.update_showcard_id()), text)
		item_type = 'REQUEST'
	else:
		if w7_flag == True:
			item_type = None
		else:
			item_type = 'REQUEST'	

	return text, item_type		


def fill_unrolling(text, fills, df_procedures, df_questionnaire, survey_item_id, item_name, share_modules, w7_flag, item_type_w7):
	if w7_flag:
		study = 'SHA_R07_2017'
	else:
		study = 'SHA_R08_2019'

	if len(fills) == 1:
		df_procedure_filtered = df_procedures[df_procedures['fill_name'].str.lower()==fills[0].lower()]
		last_text = None
		if df_procedure_filtered.empty == False:
			for i, row in df_procedure_filtered.iterrows():
				text_var = text.replace(fills[0], row['text'])
				text_var = text_var.replace('^', ' ')

				if last_text is None or text_var != last_text:
					text_var, item_type = eliminate_showcardID_and_adjust_item_type(text_var, item_name, w7_flag)
					if w7_flag and item_type is None:
						item_type = item_type_w7

					if '{empty}' not in text_var and 'empty' not in text_var:
						data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': get_module_metadata(item_name, share_modules), 
						'item_type':item_type, 'item_name':item_name, 
						'item_value':None, 'text': re.sub(' +', ' ', text_var)}
						df_questionnaire = df_questionnaire.append(data, ignore_index = True)

						last_text = text_var
	else:
		texts = []
		for i, fill in enumerate(fills):
			df_procedure_filtered = df_procedures[df_procedures['fill_name'].str.lower()==fill.lower()]
			last_text = None
			if df_procedure_filtered.empty == False:
				for i, row in df_procedure_filtered.iterrows():
					if i == 0:
						text_var = text.replace(fill, row['text'])
						text_var = text_var.replace('^', ' ')
						if last_text is None or text_var != last_text:
							texts.append(text_var)
							last_text = text_var
					else:
						texts_aux = []
						for text in texts:
							text_var = text.replace(fill, row['text'])
							text_var = text_var.replace('^', ' ')
							if last_text is None or text_var != last_text:
								texts_aux.append(text_var)
								last_text = text_var
						texts = texts_aux

		for i, text in enumerate(texts):
			text, item_type = eliminate_showcardID_and_adjust_item_type(text, item_name, w7_flag)
			if w7_flag and item_type is None:
				item_type = item_type_w7

			if '{empty}' not in text and 'empty' not in text:
				data = {'survey_item_ID':survey_item_id, 'Study': study, 'module': get_module_metadata(item_name, share_modules), 
				'item_type':item_type, 'item_name':item_name, 'item_value':None, 'text':re.sub(' +', ' ', text)}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)


	return df_questionnaire




def fill_extraction(text):
	match = re.compile('\^FL.*_\d').findall(text)
	fill_list = []
	if match:
		for item in match:
			split = item.split('^')
			for substring in split:
				if substring != '':
					if ' ' in substring:
						split_substring = substring.split(' ')
						for s in split_substring:
							match = re.compile('FL').match(s)
							if match:
								if ',' in substring:
									substring = substring.replace(',', '')
								fill_list.append(s)
					else:
						if ',' in substring:
							substring = substring.replace(',', '')

						fill_list.append(substring)
	
	if not fill_list:
		return None
	else:
		return fill_list

def replace_fill_in_answer(text):
	text = re.sub('\^FLCurr', 'euros', text)
	text = re.sub('\^img_infinity_correct_copy', '', text)
	text = re.sub('\^img_infinity_incorrect_copy', '', text)
	text = re.sub('\^CH004_FirstNameOfChild', 'Tom/Maria', text)
	text = re.sub('\^FLLastYear', '2018', text)
	text = re.sub('\^XT008_MonthDied', '', text)
	text = re.sub('\^FLRosterName', 'Tom/Maria', text)
	text = re.sub('\+piNameChild\+', 'Tom/Maria', text)
	text = re.sub('\^piName', 'Tom/Maria', text)


	return text


def clean_answer_text(text, country_language):
	text = text.replace('etc.', '')
	text = text.replace('e.g.', 'eg')
	text = text.replace('(Ex.', '(Ex:')
	text = text.replace('@B', '')
	text = text.replace(' ?', '?')
	text = text.replace('<b>', '')
	text = text.replace('.?', '?')
	text = text.replace('</b>', '')
	text = text.replace('<B>', '')
	text = text.replace('</B>', '')
	text = text.replace('<br>', '')
	text = text.replace('<br />', '')
	text = text.replace('<strong>', '')
	text = text.replace('</strong>', '')
	text = text.replace('&nbsp;', ' ')
	text = text.replace('<em>', ' ')
	text = text.replace('</em>', ' ')
	text = text.replace('@b', ' ')
	text = text.replace('@/', ' ')
	text = text.replace('}', '')
	text = text.replace('{', '')
	text = text.replace('</p>', '')
	text = text.replace('<p>', '')
	text = text.replace('[br]', '')

	text = text.rstrip()

	if text == '':
		text = None

	return text

def clean_text(text, country_language):
	text = text.replace('^MN015_ELIGIBLES', '')
	text = text.replace('etc.', '')
	text = text.replace('e.g.', 'eg')
	text = text.replace('(Ex.', '(Ex:')
	text = text.replace('@B', '')
	text = text.replace(' ?', '?')
	text = text.replace('<b>', '')
	text = text.replace('.?', '?')
	text = text.replace('</b>', '')
	text = text.replace('<B>', '')
	text = text.replace('</B>', '')
	text = text.replace('<br>', '')
	text = text.replace('<br />', '')
	text = text.replace('<strong>', '')
	text = text.replace('</strong>', '')
	text = text.replace('&nbsp;', ' ')
	text = text.replace('<em>', ' ')
	text = text.replace('</em>', ' ')
	text = text.replace('@b', ' ')
	text = text.replace('@/', ' ')
	text = text.replace('\n', ' ').replace('\r', '')
	text = text.replace('}', '')
	text = text.replace('{', '')
	text = text.replace('</p>', '')
	text = text.replace('<p>', '')
	text = text.replace('[br]', '')
	text = text.replace('(^FLDay)', '')
	text = text.replace('(^FLMonth)', '')
	text = text.replace('(^FLYear)', '')
	text = text.replace('(^FLToday)', '')
	text = re.sub('\^FLChildName', 'Tom/Maria', text)
	text = text.replace('^FLMonthFill ^FLYearFill', '...')
	text = text.replace('^FLMonthFill', '...')
	text = text.replace('^FLYearFill', '...')
	text = text.replace('^FL_MONTH', '...')
	text = text.replace('^FL_YEAR', '...')
	text = text.replace('^FL_NAME / ^FL_LASTNAME', 'Tom/Maria')
	text = re.sub('^\s?\d+\.\s', '', text)
	text = re.sub('\^FL_ADDRESS', '...', text)
	text = re.sub('\^FL_TEL', '', text)
	text = re.sub('\^FL_XT622_5L', 'Tom/Maria', text)
	text = re.sub('\^RP004_prtname', 'Tom/Maria', text)
	text = re.sub('\^RespRelation', 'Tom/Maria', text)
	text = re.sub('\^RA003_acyrest', '1980', text)
	text = text.replace('[--CodeAll--]', '')
	text = re.sub('\^FL_XT625_1', 'Tom/Maria', text)
	text = re.sub('\+FL_year\+', '2017', text)
	text = re.sub('\^CHILDNAME', 'Tom/Maria', text)
	text = re.sub('\^DN002_MoBirth', '', text)
	text = re.sub('\^FLCurr', 'euros', text)
	text = re.sub('\^img_infinity_correct_copy', '', text)
	text = re.sub('\^img_infinity_incorrect_copy', '', text)
	text = re.sub('\^CH004_FirstNameOfChild', 'Tommy/Mary', text)
	text = re.sub('\^FL_CHILD_NAME', 'Tommy/Mary', text)
	text = re.sub('\^FLLastInterviewMonthYear', '2017', text)
	text = re.sub('\^FLTwoYearsBackMonth', '2016', text)
	text = re.sub('\^FLLastYearMonth', '2017', text)
	text = re.sub('\^FLLastYear', '2017', text)
	text = re.sub('\^XT008_MonthDied', '', text)
	text = re.sub('\^FLMedia', '', text)
	text = re.sub('\^FLMedia2', '', text)
	text = re.sub('\^FLMedia2', '', text)
	text = re.sub('\^SN002_Roster', 'Tom/Maria', text)
	text = re.sub('\^FLRosterName', 'Tom/Maria', text)
	text = re.sub('\^FLChildName', 'Tom/Maria', text)
	text = re.sub('\^FLChildname', 'Tom/Maria', text)
	text = re.sub('\^\s?FL_XT622_5', 'Tom/Maria', text)
	text = re.sub('\^\s?FL_XT625_1', 'Tom/Maria', text)
	text = re.sub('\+piNameChild\+', 'Tom/Maria', text)
	text = re.sub('\^FL_NAME', 'Tom/Maria', text)
	text = re.sub('\^piName', 'Tom/Maria', text)
	text = re.sub('\^FLRespondentName', 'Tom/Maria', text)
	text = re.sub('\^localRelationText', '', text)
	text = re.sub('\^FLAgeTen', '80', text)
	text = re.sub('\^img_cube_score_2', '', text)
	text = re.sub('\^img_cube_score_1', '', text)
	text = re.sub('\^EP127_PeriodFromMonth', '', text)
	text = re.sub('\^EP129_PeriodToMonth', '', text)
	text = re.sub('\^piRelation', '', text)
	text = re.sub('\^TempRelationshipString', '', text)
	text = re.sub('\^AffordExpenseAmount', 'X', text)
	text = re.sub('\^XT102_DecMonthBirth', '', text)

	if 'ENG' not in country_language:
		text = text.replace('else', ' ')

	if 'SPA' in country_language:
		text = text.replace('Ud.', 'usted')
		text = text.replace('Ud', 'usted')

	
	text = text.rstrip()

	if text == '':
		text = None

	return text

"""
Extract answers text from XML node

:param name: name of the answer structure inside XML file
:param subnode: child node being analyzed in outer loop
:param df_answers: pandas dataframe containing answers extracted from XML file
:returns: answers dataframe, with new answer category retrieved (when appliable)
"""
def extract_answers(subnode, df_answers, name, country_language, output_source_questionnaire_flag):
	for child in subnode.getiterator():
		if child.tag == 'answer_element':
			item_value = child.attrib['labelvalue']
			text_nodes = child.findall('text')
			for text_node in text_nodes:
				text = None
				if output_source_questionnaire_flag == '0':
					if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
						text = clean_text(text_node.text, country_language)
				else:
					if text_node.attrib['translation_id'] == '1' and text_node.text is not None:
						text = clean_text(text_node.text, country_language)

				if text is not None and '{empty}' not in text and 'empty' not in text:
					if re.compile('\^PreloadChild').match(text) is None and re.compile('\^FLChild').match(text) is None and re.compile('\^FLSNmember').match(text) is None:
						data = {'item_name': name, 'item_value':item_value, 'text': text}
						df_answers = df_answers.append(data, ignore_index = True)

	return df_answers

def split_answer_text_item_value_from_categories(text):
	"""
	Splits the answer text and its item value in the category node
	Args:
		param1 text (string): text from category node, containing item value and answer text segment

	Returns: 
		item_value (string) and answer text segment (string)
	"""
	if '. ' in text:
		text = text.split('. ')
		item_value = text[0] 
		answer_text = text[1]
	elif '.' in text:
		text = text.split('.')
		item_value = text[0] 
		answer_text = text[1]
	else:
		item_value = '0'
		answer_text = text


	return item_value, answer_text

def extract_categories(subnode, df_answers, name, country_language):
	"""
	Extracts the categories (i.e., answers) from SHARE W07 XML files.
	Args:
		param1 subnode: subnode of categories node.
		param2 df_answers (pandas dataframe): a dataframe to store answer text and its attributes
		param3 country_language (string): country and language metadata, contained in the filename

	Returns: 
		retrieved answer segments. 
	"""
	fl_child = re.compile('(\^FLChild\[.+\]|{llista amb el nom dels fills})')
	fl_job =  re.compile('\^(Sec_RE\.)?FJobTitle\[.+\]')
	fl_movies= re.compile('.*\^FLMovies\[.+\]')
	fl_default= re.compile('.*\^FLDefault\[.+\]')

	
	for child in subnode.getiterator():
		if child.tag == 'category_element':
			text_nodes = child.findall('text')
			for text_node in text_nodes:
				text = None
				if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
					if fl_child.match(text_node.text) is None and fl_job.match(text_node.text) is None and fl_movies.match(text_node.text) is None and fl_default.match(text_node.text) is None:
						item_value, text = split_answer_text_item_value_from_categories(text_node.text)
						text = clean_answer_text(text, country_language)

				if text is not None and '{empty}' not in text and 'empty' not in text:
					data = {'item_name': name, 'item_value':item_value, 'text': text}
					df_answers = df_answers.append(data, ignore_index = True)

	return df_answers

def extract_qenums(subnode, df_answers, name, country_language):
	"""
	Extracts the qenums (i.e., answers) from SHARE W07 XML files.
	Args:
		param1 subnode: subnode of categories node.
		param2 df_answers (pandas dataframe): a dataframe to store answer text and its attributes
		param3 country_language (string): country and language metadata, contained in the filename

	Returns: 
		retrieved answer segments. 
	"""
	fl_child = re.compile(r'(\^FLChild\[.+\]|{llista amb el nom dels fills})')
	fl_job =  re.compile(r'\^(Sec_RE\.)?FJobTitle\[.+\]')
	fl_movies= re.compile(r'\^FLMovies\[.+\]')
	fl_default= re.compile(r'\^FLDefault\[.+\]')

	item_value = 0

	for child in subnode.getiterator():
		if child.tag == 'qenum_element':
			text_nodes = child.findall('text')		
			for text_node in text_nodes:
				text = None
				if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
					if fl_child.match(text_node.text) is None and fl_job.match(text_node.text) is None and fl_movies.match(text_node.text) is None and fl_default.match(text_node.text) is None:
						text = clean_text(text_node.text, country_language)

				if text is not None and '{empty}' not in text and 'empty' not in text:
					data = {'item_name': name, 'item_value':item_value, 'text': text}
					df_answers = df_answers.append(data, ignore_index = True)
					item_value = item_value+1

	return df_answers



def extract_questions_and_procedures(subnode, df_questions, df_procedures, parent_map, name, splitter, country_language, output_source_questionnaire_flag):
	for child in subnode.getiterator():
		if child.tag == 'question_element' and 'type_name' in child.attrib:
			if child.attrib['type_name'] == 'QText':
				text_nodes = child.findall('text')
				for text_node in text_nodes:
					text = None
					if output_source_questionnaire_flag == '0':
						if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
							text = clean_text(text_node.text, country_language)
					else:
						if text_node.attrib['translation_id'] == '1' and text_node.text is not None:
							text = clean_text(text_node.text, country_language)

					if text is not None and '^LblOnlyTesting' not in text and '^LblSucInstalled' not in text:
						if name == 'THIS_INTERVIEW':
							last_row = df_questions.iloc[-1]
							name = last_row['item_name']
						
						sentences = splitter.tokenize(text)
						for sentence in sentences:
							data = {'item_name': name, 'text': sentence}
							df_questions = df_questions.append(data, ignore_index = True)							
		elif child.tag == 'procedure':
			proc_name = child.attrib['name']
			fills = child.find('fills')
			fill_nodes = fills.findall('fill')
			for fill_node in fill_nodes:
				fill_name = fill_node.attrib['name']
				fill_option_nodes = fill_node.findall('fill_option')

				for fill_option_node in fill_option_nodes:
					text_nodes = fill_option_node.findall('text')
					for text_node in text_nodes:
						text = None
						if output_source_questionnaire_flag == '0':
							if text_node.attrib['translation_id'] != '1' and text_node.text is not None and text_node.text != '{}':
								text = clean_text(text_node.text, country_language)
						else:
							if text_node.attrib['translation_id'] == '1' and text_node.text is not None and text_node.text != '{}':
								text = clean_text(text_node.text, country_language)

						if text is not None and '+piHO004_OthPer+' not in text and '{empty}' not in text and 'empty' not in text:
							order = parent_map[text_node].attrib['order']
							data = {'item_name': proc_name, 'fill_name':fill_name, 'order':order, 'text': text}
							df_procedures = df_procedures.append(data, ignore_index = True)


	return df_questions, df_procedures

def replace_untranslated_instructions(country_language, text):
	if 'CAT_ES' in country_language:
		share_w7_instructions = SHAREW7InstructionsCAT()

	text = re.sub('\^CodeAll', share_w7_instructions.code_all, text)
	text = re.sub('\^ReadOut', share_w7_instructions.read_out, text)
	text = re.sub('\^Especifiqui', 'Especifiqui', text)
	text = re.sub('\^Especifiqueu', 'Especifiqueu', text)
	text = re.sub('\^FL_RE012a', share_w7_instructions.job_position, text)
	text = re.sub('\^FL_RE012b', share_w7_instructions.job_position, text)
	text = re.sub('\^RE012_jobtitle', share_w7_instructions.job_position, text)
	text = re.sub('\^FL_HIS_HER', share_w7_instructions.he_she, text)

	

	return text


def extract_questions_and_procedures_w7(subnode, df_questions, df_procedures, parent_map, name, tmt_id, splitter, country_language):
	for child in subnode.getiterator():
		if child.tag == 'question_element' and 'type_name' in child.attrib:
			if child.attrib['type_name'] == 'QText' or child.attrib['type_name'] == 'QInstruction':

				if child.attrib['type_name'] == 'QText':
					item_type = 'REQUEST'
				else:
					item_type = 'INSTRUCTION'
				
				text_nodes = child.findall('text')
				for text_node in text_nodes:
					text = None
					if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
						text = clean_text(text_node.text, country_language)

					if text is not None:
						if name == 'THIS_INTERVIEW':
							last_row = df_questions.iloc[-1]
							name = last_row['item_name']

						text = replace_untranslated_instructions(country_language, text)
						sentences = splitter.tokenize(text)
						for sentence in sentences:
							if '^Children_table' not in sentence and '^Press' not in sentence:
								data = {'item_name': name, 'item_type':item_type, 'tmt_id': tmt_id, 'text': sentence}
								df_questions = df_questions.append(data, ignore_index = True)	
		elif child.tag == 'procedure':
			proc_name = child.attrib['name']
			fills = child.find('fills')
			fill_nodes = fills.findall('fill')
			for fill_node in fill_nodes:
				fill_name = fill_node.attrib['name']
				fill_option_nodes = fill_node.findall('fill_option')

				for fill_option_node in fill_option_nodes:
					text_nodes = fill_option_node.findall('text')
					for text_node in text_nodes:
						text = None
						if text_node.attrib['translation_id'] != '1' and text_node.text is not None and text_node.text != '{}':
							text = clean_text(text_node.text, country_language)

						if text is not None and '{empty}' not in text and 'empty' not in text:
							order = parent_map[text_node].attrib['order']
							data = {'item_name': proc_name, 'fill_name':fill_name, 'order':order, 'text': text}
							df_procedures = df_procedures.append(data, ignore_index = True)


	return df_questions, df_procedures




def set_initial_structures(filename, output_source_questionnaire_flag):
	"""
	Set initial structures that are necessary for the extraction of each questionnaire.

	Args:
		param1 filename (string): name of the input file.

	Returns: 
		df_questionnaire to store questionnaire data (pandas dataframe),
		survey_item_prefix, which is the prefix of survey_item_ID (string), 
		study/country_language, which are metadata parameters embedded in the file name (string and string)
		and sentence splitter to segment request/introduction/instruction segments when necessary (NLTK object). 
	"""

	"""
	A pandas dataframe to store questionnaire data.
	"""
	df_questionnaire = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 'item_name', 'item_value', 'text'])

	"""
	The prefix of a EVS survey item is study+'_'+language+'_'+country+'_'
	"""
	if output_source_questionnaire_flag == '0':
		survey_item_prefix = re.sub('\.xml', '', filename)+'_'
	else:
		survey_item_prefix = 'SHA_R08_2019_ENG_SOURCE'

	"""
	Reset the initial survey_id sufix, because main is called iterativelly for every file in folder.
	"""
	ut.reset_initial_sufix()

	"""
	Reset the initial showcard_id sufix, because main is called iterativelly for every file in folder.
	"""
	ut.reset_initial_showcard()

	"""
	Retrieve study and country_language information from the name of the input file. 
	"""
	if output_source_questionnaire_flag == '0':
		study, country_language = get_country_language_and_study_info(filename)
	else:
		study, country_language = get_country_language_and_study_info('SHA_R08_2019_ENG_SOURCE')
	
	"""
	Instantiate a NLTK sentence splitter based on file input language. 
	"""
	if output_source_questionnaire_flag == '0':
		splitter = ut.get_sentence_splitter(filename)
	else:
		splitter = ut.get_sentence_splitter('SHA_R08_2019_ENG_SOURCE')
	
	return df_questionnaire, survey_item_prefix, study, country_language,splitter

def build_questionnaire_structure(df_questions, df_answers,df_procedures, df_questionnaire, survey_item_prefix, share_modules, special_answer_categories):
	unique_question_item_names = df_questions.item_name.unique()
	for unique_item_name in unique_question_item_names:
		df_questions_by_item_name = df_questions[df_questions['item_name'].str.lower()==unique_item_name.lower()]
		df_answers_by_item_name = df_answers[df_answers['item_name'].str.lower()==unique_item_name.lower()]

		for i, row in df_questions_by_item_name.iterrows():
			if df_questionnaire.empty:
				survey_item_id = ut.get_survey_item_id(survey_item_prefix)
			else:
				survey_item_id = ut.update_survey_item_id(survey_item_prefix)	

			text = row['text']
			fills = fill_extraction(text)

			if fills is None:
				text, item_type = eliminate_showcardID_and_adjust_item_type(text, row['item_name'], False)
					
				data = {'survey_item_ID':survey_item_id, 'Study':'SHA_R08_2019', 'module': get_module_metadata(row['item_name'], share_modules), 
				'item_type':item_type, 'item_name':row['item_name'], 
				'item_value':None, 'text':re.sub(' +', ' ', text)}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)
			else:
				for fill in fills:
					df_questionnaire = fill_unrolling(text, fills, df_procedures, df_questionnaire, survey_item_id, row['item_name'], share_modules, False, None)

		if df_answers_by_item_name.empty:
			last_row = df_questionnaire.iloc[-1]
			if last_row['item_type'] != 'INTRODUCTION':
				answer_text, item_value = special_answer_categories.write_down[0], special_answer_categories.write_down[1]
				
				if last_row['text'] != answer_text:
					survey_item_id = ut.update_survey_item_id(survey_item_prefix)
					data = {"survey_item_ID": survey_item_id,'Study':'SHA_R08_2019', 'module': get_module_metadata(last_row['item_name'], share_modules), 
					'item_type': 'RESPONSE', 'item_name': last_row['item_name'], 'item_value': item_value,  'text': re.sub(' +', ' ', answer_text)}
					df_questionnaire = df_questionnaire.append(data, ignore_index = True)
		else:
			last_row = df_questionnaire.iloc[-1]
			if last_row['item_type'] != 'INTRODUCTION':
				for i, row in df_answers_by_item_name.iterrows():
					
					survey_item_id = ut.update_survey_item_id(survey_item_prefix)	
					text = replace_fill_in_answer(row['text'])

					fills = fill_extraction(row['text'])
					if fills:
						texts = fill_substitution_in_answer(row['text'], fills, df_procedures)

						if texts:
							for text in texts:
								data = {'survey_item_ID':survey_item_id, 'Study':'SHA_R08_2019', 'module': get_module_metadata(row['item_name'], share_modules), 
								'item_type':'RESPONSE', 'item_name':row['item_name'], 
								'item_value':row['item_value'], 'text':re.sub(' +', ' ', text)}
								df_questionnaire = df_questionnaire.append(data, ignore_index = True)
					else:
						data = {'survey_item_ID':survey_item_id, 'Study':'SHA_R08_2019', 'module': get_module_metadata(row['item_name'], share_modules), 
						'item_type':'RESPONSE', 'item_name':row['item_name'], 
						'item_value':row['item_value'], 'text':re.sub(' +', ' ', text)}
						df_questionnaire = df_questionnaire.append(data, ignore_index = True)

	return df_questionnaire

def build_questionnaire_structure_w7(df_questions, df_answers,df_procedures, df_questionnaire, survey_item_prefix, share_modules, special_answer_categories):
	"""
	First filter the question and answer dataframes by the tmt_ids
	"""
	unique_question_tmt_ids = df_questions.tmt_id.unique()
	for unique_tmt_id in unique_question_tmt_ids:
		df_questions_tmt_id = df_questions[df_questions['tmt_id'].str.lower()==unique_tmt_id.lower()]
		df_answers_tmt_id = df_answers[df_answers['item_name'].str.lower()==unique_tmt_id.lower()]

		for i, row in df_questions_tmt_id.iterrows():
			if df_questionnaire.empty:
				survey_item_id = ut.get_survey_item_id(survey_item_prefix)
			else:
				survey_item_id = ut.update_survey_item_id(survey_item_prefix)	

			text = row['text']
			fills = fill_extraction(text)

			if fills is None:
				text, item_type = eliminate_showcardID_and_adjust_item_type(text, row['item_name'], True)

				if item_type is None:
					item_type = row['item_type']
					
				data = {'survey_item_ID':survey_item_id, 'Study':'SHA_R07_2017', 'module': get_module_metadata(row['item_name'], share_modules), 
				'item_type':item_type, 'item_name':row['item_name'], 
				'item_value':None, 'text':re.sub(' +', ' ', text)}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)
			else:
				for fill in fills:
					df_questionnaire = fill_unrolling(text, fills, df_procedures, df_questionnaire, survey_item_id, row['item_name'], share_modules, True, item_type)

			last_item_name = row['item_name']
			last_row = df_questionnaire.iloc[-1]
			last_module = last_row['module']

		
		if last_row['item_type'] != 'INTRODUCTION':
			for i, row in df_answers_tmt_id.iterrows():
					
				survey_item_id = ut.update_survey_item_id(survey_item_prefix)	
				text = replace_fill_in_answer(row['text'])

				fills = fill_extraction(row['text'])
				if fills:
					texts = fill_substitution_in_answer(row['text'], fills, df_procedures)

					if texts:
						for text in texts:
							data = {'survey_item_ID':survey_item_id, 'Study':'SHA_R07_2017', 'module': last_module, 
							'item_type':'RESPONSE', 'item_name':last_item_name, 
							'item_value':row['item_value'], 'text':re.sub(' +', ' ', text)}
							df_questionnaire = df_questionnaire.append(data, ignore_index = True)
				else:
					data = {'survey_item_ID':survey_item_id, 'Study':'SHA_R07_2017', 'module': last_module, 
					'item_type':'RESPONSE', 'item_name':last_item_name, 
					'item_value':row['item_value'], 'text':re.sub(' +', ' ', text)}
					df_questionnaire = df_questionnaire.append(data, ignore_index = True)

	return df_questionnaire




def main(filename):
	output_source_questionnaire_flag = '0'

	"""
	Parse tree of input XML file.
	"""
	file = str(filename)
	tree = ET.parse(file)
	root = tree.getroot()

	"""
	Create a dictionary to map the information of node relations.
	"""
	parent_map = dict((c, p) for p in tree.getiterator() for c in p)

	df_questionnaire, survey_item_prefix, study, country_language,splitter = set_initial_structures(filename, output_source_questionnaire_flag)

	questions = root.findall('.//questionnaire/questions')
	answers = root.findall('.//questionnaire/answers')
	"""
	The categories and qenums nodes in w7 correspond to the answer nodes in w8
	"""
	categories = root.findall('.//questionnaire/categories')
	qenums = root.findall('.//questionnaire/qenums')

	df_answers = pd.DataFrame(columns=['item_name', 'item_value', 'text'])
	df_procedures = pd.DataFrame(columns=['item_name', 'fill_name', 'order', 'text'])
	if 'SHA_R07' in filename:
		df_questions = pd.DataFrame(columns=['item_name', 'item_type', 'tmt_id', 'text'])
	elif 'SHA_R08' in filename:
		df_questions = pd.DataFrame(columns=['item_name', 'text'])

	special_answer_categories = instantiate_special_answer_category_object(country_language)

	"""
	Instantiate SHAREModules object, that encapsulates the dictionaries containing the module names by round.
	"""
	share_modules_object = SHAREModules()

	
	if 'SHA_R08' in filename:
		share_modules = share_modules_object.modules_w8
		for node in questions:
			for subnode in node.getiterator():
				if subnode.tag == 'question':
					name = subnode.attrib['name']
					df_questions, df_procedures = extract_questions_and_procedures(subnode, df_questions, df_procedures, parent_map, name, splitter, country_language, output_source_questionnaire_flag)

					
		for node in answers:
			for subnode in node.getiterator():
				if subnode.tag == 'answer':
					name = subnode.attrib['name']
					df_answers = extract_answers(subnode, df_answers, name, country_language, output_source_questionnaire_flag)


		
		df_questionnaire = build_questionnaire_structure(df_questions, df_answers,df_procedures, df_questionnaire, survey_item_prefix, share_modules, special_answer_categories)
				
		if output_source_questionnaire_flag == '0':
			df_questionnaire.to_csv(survey_item_prefix[:-1]+'.csv', encoding='utf-8', index=False)
		else:
			df_questionnaire.to_csv('SHA_R08_2019_ENG_SOURCE.csv', encoding='utf-8', index=False)


	elif 'SHA_R07' in filename:
		share_modules = share_modules_object.modules_w7
		for node in questions:
			for subnode in node.getiterator():
				if subnode.tag == 'question':
					name = subnode.attrib['name']
					tmt_id = subnode.attrib['tmt_id']
					df_questions, df_procedures = extract_questions_and_procedures_w7(subnode, df_questions, df_procedures, parent_map, name, tmt_id, splitter, country_language)

		for node in categories:
			for subnode in node.getiterator():
				if 'tmt_id' in subnode.attrib:
					tmt_id = subnode.attrib['tmt_id']
					df_answers = extract_categories(subnode, df_answers, tmt_id, country_language)


		for node in qenums:
			for subnode in node.getiterator():
				if 'question_id' in subnode.attrib:
					question_id = subnode.attrib['question_id']
					df_answers = extract_qenums(subnode, df_answers, question_id, country_language)


		df_questionnaire = build_questionnaire_structure_w7(df_questions, df_answers,df_procedures, df_questionnaire, survey_item_prefix, share_modules, special_answer_categories)
		df_questionnaire.to_csv(survey_item_prefix[:-1]+'.csv', encoding='utf-8', index=False)




"""
main method is executed for each file inside the given directory.
"""
if __name__ == "__main__":
	filename = str(sys.argv[1])
	print("Executing data extraction script for SHARE wave 8 (xml files)")
	main(filename)
