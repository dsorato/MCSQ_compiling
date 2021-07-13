"""
Python3 script to extract data from XML SHARE input files
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
from share_instructions import *
from string import printable


def get_module_metadata(item_name, share_modules):
	"""
	Gets the module to which a given survey item pertains. based on the survey item name.

	Args:
		param1 item_name (string): item_name metadata, extracted direcly from the input xml file.
		param2 share_modules (dictionary): a dictionary of module names (taken from SHARE website), encapsulated in the SHAREModules object.

	Returns:
		module (string) the module name.
	"""
	module = None
	for k, v in list(share_modules.items()):
		if item_name[:2] == k:
			return v

	return module

def fill_substitution_in_answer(text, fills, df_procedures):
	"""
	Substitutes the fills in the answer text segments. The fill is substituted only if it was found in the procedure nodes (this can
	be checked by filtering the df_procedures dataframe by the fill present in the answer segment).

	Args:
		param1 text (string): the answer text segment.
		param2 fills (list): the list of fills that are present in the text segment. Effectivelly, for answers the fill list has just one element.
		param3 df_procedures (pandas dataframe): a dataframe that stores the contents of the procedures nodes, where the fill definitions are.

	Returns:
		module (string) the module name.
	"""
	texts = []
	df_procedure_filtered = df_procedures[df_procedures['fill_name'].str.lower()==fills[0].lower()]
	if df_procedure_filtered.empty == False:
		last_text = None
		for i, row in df_procedure_filtered.iterrows():
			text_var = text.replace(fills[0], row['text'])
			text_var = re.sub('^\\\s?', '', text_var)
			text_var = text_var.replace('^', ' ')
			if last_text is None or text_var != last_text:
				texts.append(text_var)
				last_text = text_var

	return texts

def remove_pishowcardid(text):
	if "'+piSHOWCARD_ID+'" in text:
		text = text.replace("'+piSHOWCARD_ID+'", 'X') 
	elif '+piSHOWCARD_ID+' in text:
		text = text.replace('+piSHOWCARD_ID+', 'X')  
	elif 'piSHOWCARD_ID' in text:
		text = text.replace('piSHOWCARD_ID', 'X') 

	return text

def eliminate_showcardID_and_adjust_item_type(text, item_name):
	"""
	Substitutes the SHOWCARD_ID strings with a card number (the card IDs are not available in the input XML files).

	Args:
		param1 text (string): the text segment being analyzed (either request or instruction).
		param2 item_name (string): item_name metadata, extracted direcly from the input xml file. If 'intro' is in the item_name, the segment receives the introduction item_type.

	Returns:
		text (string) and item_type (string). The SHOWCARD_ID strings are removed from the text segment.
	"""
	if 'intro' in item_name.lower():
		if '^SHOWCARD_ID, ' in text:
			text = re.sub('\^SHOWCARD_ID', str(ut.update_showcard_id()), text)
			item_type = 'INSTRUCTION'
		elif 'SHOWCARD_ID, ' in text:
			text = re.sub('SHOWCARD_ID', str(ut.update_showcard_id()), text)
			item_type = 'INSTRUCTION'
		elif '^SHOWCARD_ID.' in text:
			text = re.sub('\^SHOWCARD_ID\.', str(ut.update_showcard_id())+'. ', text)
			item_type = 'INSTRUCTION'
		elif 'SHOWCARD_ID.' in text:
			text = re.sub('SHOWCARD_ID\.', str(ut.update_showcard_id())+'. ', text)
			item_type = 'INSTRUCTION'
		elif '^SHOWCARD_ID' in text:
			text = re.sub('\^SHOWCARD_ID', str(ut.update_showcard_id()), text)
		elif 'SHOWCARD_ID' in text:
			text = re.sub('SHOWCARD_ID', str(ut.update_showcard_id()), text)
		else:
			item_type = None

	if '^SHOWCARD_ID, ' in text:
		text = re.sub('\^SHOWCARD_ID', str(ut.update_showcard_id()), text)
		item_type = 'INSTRUCTION'
	elif 'SHOWCARD_ID, ' in text:
		text = re.sub('SHOWCARD_ID', str(ut.update_showcard_id()), text)
		item_type = 'INSTRUCTION'
	elif '^SHOWCARD_ID.' in text:
		text = re.sub('\^SHOWCARD_ID\.', str(ut.update_showcard_id())+'. ', text)
		item_type = 'INSTRUCTION'
	elif 'SHOWCARD_ID.' in text:
		text = re.sub('SHOWCARD_ID\.', str(ut.update_showcard_id())+'. ', text)
		item_type = 'INSTRUCTION'
	elif '^SHOWCARD_ID' in text:
		text = re.sub('\^SHOWCARD_ID', str(ut.update_showcard_id()), text)
		item_type = None
	elif 'SHOWCARD_ID' in text:
		text = re.sub('SHOWCARD_ID', str(ut.update_showcard_id()), text)
		item_type = None
	else:
		item_type = None
	

	return text, item_type		


def fill_unrolling(text, fills, df_procedures, df_questionnaire, survey_item_id, item_name, share_modules, study, item_type):
	"""
	Replaces all dynamic fills found in a given text segment by their string definitions in the df_procedures dataframe.

	Args:
		param1 text (string): the text segment that contains at least one dynamic fill.
		param2 fills (list): the list of dynamic fills found in the text segment passed as parameter.
		param3 df_procedures (pandas dataframe): the dataframe that holds the procedures for fills substitution, extracted from the XML nodes in previous steps.
		param4 df_questionnaire (pandas dataframe): a dataframe to hold the final questionnaire.
		param5 item_name (string): the item name metadata, extracted in previous steps.
		param6 share_modules (dictionary): a dictionary (round dependent) with the full name of all SHARE modules.
		param7 study (string): the study metadata, embedded in the input filename or hard-coded in the case of ENG_SOUCE data extraction.
		param8 item_type (string): the item type metadata, extracted in previous steps.

	Returns: 
		The updated df_questionnaire (pandas dataframe). The dynamic fill(s) in the text segment was properly replaced.
	"""
	if len(fills) == 1:
		df_procedure_filtered = df_procedures[df_procedures['fill_name'].str.lower()==fills[0].lower()]
		last_text = None
		if df_procedure_filtered.empty == False:
			for i, row in df_procedure_filtered.iterrows():
				text_var = text.replace(fills[0], row['text'])
				text_var = text_var.replace('^', ' ')
				text_var = text_var.rstrip()
				text_var = text_var.lstrip()

				if last_text is None or text_var != last_text:
					if '{empty}' not in text_var and 'empty' not in text_var:
						text_var = remove_pishowcardid(text_var)
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
			if '{empty}' not in text and 'empty' not in text:
				text = remove_pishowcardid(text)
				data = {'survey_item_ID':survey_item_id, 'Study': study, 'module': get_module_metadata(item_name, share_modules), 
				'item_type':item_type, 'item_name':item_name, 'item_value':None, 'text':re.sub(' +', ' ', text)}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)


	return df_questionnaire




def fill_extraction(text):
	"""
	Retrieves all dynamic fills (if there is any) from a given SHARE text segment, 
	so later on these fills can be replaces by their natural language text definition.

	Args:
		param1 text (string): the text segment.

	Returns:
		either a list of fills (list of strings), or null if there are no matching fills in the text segment.
	"""
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
	"""
	Substitutes certain fills in the answer text segments with fixed values.

	Args:
		param1 text (string): the answer text segment.

	Returns:
		the answer text (string) where the fills were replaced (if present in original string).
	"""
	text = re.sub('\^FLCurr', 'euros', text)
	text = re.sub('\^FLCURR', 'euros', text)
	text = re.sub('\^FLCUrr', 'euros', text)
	text = re.sub('\^img_infinity_correct_copy', '', text)
	text = re.sub('\^img_infinity_incorrect_copy', '', text)
	text = re.sub('\^CH004_FirstNameOfChild', 'Tom/Maria', text)
	text = re.sub('\^FLLastYear', '2018', text)
	text = re.sub('\^XT008_MonthDied', '', text)
	text = re.sub('\^FLRosterName', 'Tom/Maria', text)
	text = re.sub('\+piNameChild\+', 'Tom/Maria', text)
	text = re.sub('\^piName', 'Tom/Maria', text)
	text = re.sub('\^FL_MEMBER', 'Tom/Maria', text)
	text = text.replace('\^FL_PARTNER', 'Tom/Maria')
	text = text.replace('^FL_PARTNER', 'Tom/Maria')
	text = re.sub('^\\\s?', '', text)


	return text


def clean_answer_text(text, country_language):
	"""
	Substitutes HTML markups in the answer text segments with fixed values

	Args:
		param1 text (string): the answer text segment.
		param2 country_language (string): country_language metadata, embedded in file name.

	Returns:
		the answer text (string) where the markups were replaced (if present in original string).
	"""
	text = text.replace('etc.', '')
	text = text.replace('e.g.', 'eg')
	text = text.replace('Ex.', 'Ex:')
	text = text.replace('ex.', 'ex:')
	text = text.replace('@B', '')
	text = text.replace(' ?', '?')
	text = text.replace('<b>', '')
	text = text.replace('.?', '?')
	text = text.replace('<u>', '')
	text = text.replace('</u>', '')
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
	text = re.sub('\sR\s', ' respondent ', text)
	text = re.sub('\sR\s?\.', ' respondent.', text)
	text = re.sub('^\\\s?', '', text)

	text = text.rstrip()
	text = text.lstrip()

	if text == '':
		text = None


	return text

def clean_text_share(text, country_language, w7flag):
	"""
	Substitutes HTML markups and certain fills in the text segments with fixed values.

	Args:
		param1 text (string): the answer text segment.
		param2 country_language (string): country_language metadata, embedded in file name.
		param3 w7_flag (boolean): a boolean flag that indicates if the segment comes from a input xml file in SHARE w7.

	Returns:
		the text (string) where the markups and fills were replaced (if present in original string).
	"""
	text = text.replace('^MN015_ELIGIBLES', '')
	text = text.replace('^MN015_Eligibles', '')
	text = text.replace('etc.', '')
	text = text.replace('i.e.', 'i.e')
	text = re.sub('^:', '', text)
	text = text.replace('<<', '"')
	text = text.replace('>>', '"')
	text = text.replace(').', '). ')
	text = text.replace('E.G.', 'E.G')
	text = text.replace('e.g.', 'e.g')
	text = text.replace('Ex.', 'Ex:')
	text = text.replace('ex.', 'ex:')
	text = text.replace('@B', '')
	text = text.replace(' ?', '?')
	text = text.replace('<b>', '')
	text = text.replace('.?', '?')
	text = text.replace('</b>', '')
	text = text.replace('<u>', '')
	text = text.replace('</u>', '')
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
	text = text.replace('(^FLYEAR)', '')
	text = text.replace('(^FLToday)', '')
	text = text.replace('(^FLDAY)', '')
	text = text.replace('(^FLMONTH)', '')
	text = text.replace('(^FLTODAY)', '')
	text = text.replace('[--CodeAll--]', '')
	text = text.replace('^FLMonthFill ^FLYearFill', '...')
	text = text.replace('^FLMonthFill', '...')
	text = text.replace('^FLYearFill', '...')
	text = text.replace('^FL_MONTH', '...')
	text = text.replace('^FL_YEAR', '...')
	text = text.replace('(^FL_MEMBERS)', '')
	text = text.replace('^FL_NAME / ^FL_LASTNAME', 'Tom/Maria')
	text = text.replace("'+FLNumber+", '')
	text = text.replace("^FL_MOVED_IN_Y", '')
	text = text.replace('^FL_LASTNAME', '')
	text = text.replace('z.B. 13. und 14.', 'z.B. 13 und 14')
	text = text.replace('z.B. 13., 14.', 'z.B. 13, 14')
	text = text.replace('z. B.', 'z.B.')
	text = text.replace('Bonus, 13.', 'Bonus, 13')
	text = text.replace('z.B. 13.', 'z.B. 13')

	
	if w7flag:
		text = text.replace('[FLLastInterviewMonthYear]', '2014')
		text = re.sub('\^FLLastInterviewMonthYear', '2014', text)
		text = re.sub('\^FLTwoYearsBackMonth', '2013', text)
		text = re.sub('\^FLLastYearMonth', '2015', text)
		text = re.sub('\^FLLastYear', '2015', text)
		text = re.sub('\+FL_year\+', '2016', text)
	else:
		text = text.replace('[FLLastInterviewMonthYear]', '2017')
		text = re.sub('\^FLLastInterviewMonthYear', '2017', text)
		text = re.sub('\^FLTwoYearsBackMonth', '2016', text)
		text = re.sub('\^FLLastYearMonth', '2017', text)
		text = re.sub('\^FLLastYear', '2017', text)
		text = re.sub('\+FL_year\+', '2017', text)
	
	text = re.sub('\^FL_MEMBER', 'Tom/Maria', text)
	text = re.sub("\s?RA026_acwhere,?\s?", '', text)
	text = re.sub("'\s?\+\s?FL_livingin\s?\+\s?'", '', text)
	text = re.sub('\^FLChildName', 'Tom/Maria', text)
	text = re.sub('^\s?\d+\.\s', '', text)
	text = re.sub('\^FL_ADDRESS', '...', text)
	text = re.sub('\^FL_TEL', '', text)
	text = re.sub('\^FL_XT622_5L', 'Tom/Maria', text)
	text = re.sub('\^RP004_prtname', 'Tom/Maria', text)
	text = re.sub('\^RespRelation', 'Tom/Maria', text)
	text = re.sub('\^RA003_acyrest', '1980', text)
	text = re.sub('\^FL_XT625_1', 'Tom/Maria', text)
	text = re.sub('\^CHILDNAME', 'Tom/Maria', text)
	text = re.sub('\^DN002_MoBirth', '', text)
	text = re.sub('\^FLCurr', 'euros', text)
	text = re.sub('\^FLCURR', 'euros', text)
	text = re.sub('\^FLCUrr', 'euros', text)
	text = re.sub('\^img_infinity_correct_copy', '', text)
	text = re.sub('\^img_infinity_incorrect_copy', '', text)
	text = re.sub('\^CH004_FirstNameOfChild', 'Tommy/Mary', text)
	text = re.sub('\^FL_CHILD_NAME', 'Tommy/Mary', text)
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
	text = re.sub('\^img_clockface_allright', '', text)
	text = re.sub('\^img_clockface_12incl', '', text)
	text = re.sub('\^img_clockface_handscorrect', '', text)
	text = re.sub('\^img_clockface_1handcorrect_1_3', '', text)
	text = re.sub('\^TempRelationshipString', '', text)
	text = re.sub('\^AffordExpenseAmount', 'X', text)
	text = re.sub('\^XT102_DecMonthBirth', '', text)
	text = re.sub('\^RespondentID', 'X', text)

	if 'ENG' not in country_language:
		text = text.replace('else', ' ')

	if 'ENG' in country_language:
		text = re.sub('\sR\s', ' respondent ', text)
		text = re.sub('\sR\s?\.', ' respondent.', text)

	if 'SPA' in country_language:
		text = text.replace('Ud.', 'usted')
		text = text.replace('Ud', 'usted')

	
	text = text.rstrip()
	text = text.lstrip()
	

	if text == '':
		text = None

	return text


def extract_answers(subnode, df_answers, name, country_language, output_source_questionnaire_flag):
	"""
	Extract answers text from XML nodes of SHARE w8 files.

	Args:
		param1 subnode: child node being analyzed in outer loop.
		param2 df_answers: pandas dataframe containing answers extracted from XML file
		param3 name (string): name of the answer structure inside XML file
		param4 country_language (string): country_language metadata, embedded in file name.
		param5 output_source_questionnaire_flag (string): indicates if the data to be extracted in the source (1) or the target language (any other value)
		
	Returns: 
		df_answers (pandas dataframe) filled with retrieved answer segments extracted from answer_element nodes. 
	"""
	for child in subnode.getiterator():
		if child.tag == 'answer_element':
			item_value = child.attrib['labelvalue']
			text_nodes = child.findall('text')
			for text_node in text_nodes:
				text = None
				if output_source_questionnaire_flag == '1':
					if text_node.attrib['translation_id'] == '1' and text_node.text is not None:
						text = clean_text_share(text_node.text, country_language, False)
				else:
					if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
						text = clean_text_share(text_node.text, country_language, False)

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

def extract_categories(subnode, df_answers, name, country_language, output_source_questionnaire_flag):
	"""
	Extracts the categories (i.e., answers) from SHARE W07 XML files.

	Args:
		param1 subnode: subnode of categories node.
		param2 df_answers (pandas dataframe): a dataframe to store answer text and its attributes
		param3 country_language (string): country and language metadata, contained in the filename
		param4 output_source_questionnaire_flag (string): indicates if the data to be extracted in the source (1) or the target language (any other value)

	Returns: 
		df_answers (pandas dataframe) filled with retrieved answer segments extracted from category_element nodes. 
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
				if output_source_questionnaire_flag == '1':
					if text_node.attrib['translation_id'] == '1' and text_node.text is not None:
						if fl_child.match(text_node.text) is None and fl_job.match(text_node.text) is None and fl_movies.match(text_node.text) is None and fl_default.match(text_node.text) is None:
							item_value, text = split_answer_text_item_value_from_categories(text_node.text)
							text = clean_answer_text(text, country_language)
				else:
					if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
						if fl_child.match(text_node.text) is None and fl_job.match(text_node.text) is None and fl_movies.match(text_node.text) is None and fl_default.match(text_node.text) is None:
							item_value, text = split_answer_text_item_value_from_categories(text_node.text)
							text = clean_answer_text(text, country_language)

				if text is not None and '{empty}' not in text and 'empty' not in text:
					data = {'item_name': name, 'item_value':item_value, 'text': text}
					df_answers = df_answers.append(data, ignore_index = True)

	return df_answers

def extract_qenums(subnode, df_answers, name, country_language, output_source_questionnaire_flag):
	"""
	Extracts the qenums (i.e., answers) from SHARE W07 XML files.

	Args:
		param1 subnode: subnode of categories node.
		param2 df_answers (pandas dataframe): a dataframe to store answer text and its attributes
		param3 country_language (string): country and language metadata, contained in the filename
		param4 output_source_questionnaire_flag (string): indicates if the data to be extracted in the source (1) or the target language (any other value)

	Returns: 
		df_answers (pandas dataframe) filled with retrieved answer segments extracted from qenum_element nodes. 
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
				if output_source_questionnaire_flag == '1':
					if text_node.attrib['translation_id'] == '1' and text_node.text is not None:
						if fl_child.match(text_node.text) is None and fl_job.match(text_node.text) is None and fl_movies.match(text_node.text) is None and fl_default.match(text_node.text) is None:
							text = clean_text_share(text_node.text, country_language, True)
				else:
					if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
						if fl_child.match(text_node.text) is None and fl_job.match(text_node.text) is None and fl_movies.match(text_node.text) is None and fl_default.match(text_node.text) is None:
							text = clean_text_share(text_node.text, country_language, True)

				if text is not None and '{empty}' not in text and 'empty' not in text:
					data = {'item_name': name, 'item_value':item_value, 'text': text}
					df_answers = df_answers.append(data, ignore_index = True)
					item_value = item_value+1

	return df_answers







def replace_untranslated_instructions(country_language, text):
	"""
	Replaces certain dynamic fills that are not defined in the input file by language-dependent fixed values.

	Args:
		param1 country_language (string): country and language metadata, contained in the filename.
		param2 text (string): the text segment.

	Returns: 
		The text segment (string) without certain dynamic fills (if there were any).
	"""
	if 'CAT_ES' in country_language:
		share_instructions = SHAREInstructionsCAT()
	elif 'CZE_CZ' in country_language:
		share_instructions =SHAREInstructionsCZE()
	elif 'ENG' in country_language:
		share_instructions =SHAREInstructionsENG()
	elif 'FRE' in country_language:
		share_instructions =SHAREInstructionsFRE()
	elif 'SPA' in country_language:
		share_instructions =SHAREInstructionsSPA()
	elif 'POR' in country_language:
		share_instructions =SHAREInstructionsPOR()
	elif 'GER' in country_language:
		share_instructions =SHAREInstructionsGER()
	elif 'RUS' in country_language:
		share_instructions =SHAREInstructionsRUS()

	if 'CAT_ES' in country_language:
		text = re.sub('\^ReadOutNeed', 'Llegeixi, si cal. ', text)
		text = re.sub('\^Especifiqui', 'Especifiqui. ', text)
		text = re.sub('\^Especifiqueu', 'Especifiqueu. ', text)
	elif 'CZE_CZ' in country_language:
		text = re.sub('\^ReadOutNeed', 'Prečtěte pokud nutno. ', text)
		text = re.sub('\^Specify', 'Upřesněte. ', text)
		text = re.sub('\^FL_HISHER', ' jeho její ', text)
		text = re.sub('\^FL_VERB', ' byl narozen ', text)
	elif 'ENG' in country_language:
		text = re.sub('\^ReadOutNeed', 'Read out if necessary. ', text)
		text = re.sub('\^Specify', 'Specify. ', text)
		text = re.sub('\^FL_HISHER', ' his/her ', text)
		text = re.sub('\^FL_VERB', ' was born ', text)
	elif 'FRE' in country_language:
		text = re.sub('\^ReadOutNeed', 'Lire à haute voix si nécessaire. ', text)
		text = re.sub('\^Specify', 'Spécifier. ', text)
		text = re.sub('\^FL_HISHER', ' son/sa ', text)
		text = re.sub('\^FL_VERB', ' est né(e) ', text)
	elif 'SPA' in country_language:
		text = re.sub('\^ReadOutNeed', 'Lea en voz alta si es necesario. ', text)
		text = re.sub('\^Specify', 'Especificar. ', text)
		text = re.sub('\^FL_HISHER', ' su/suya ', text)
		text = re.sub('\^FL_VERB', ' nació ', text)
	elif 'POR' in country_language:
		text = re.sub('\^ReadOutNeed', 'Leia em voz alta, se necessário. ', text)
		text = re.sub('\^Specify', 'Especificar. ', text)
		text = re.sub('\^FL_HISHER', ' seu/sua ', text)
		text = re.sub('\^FL_VERB', ' nasceu ', text)
	elif 'GER' in country_language:
		if 'LU' in country_language:
			text = re.sub('\^ReadOutNeed', 'Auslesen, falls erforderlich. ', text)
		elif 'DE' in country_language or 'CH' in country_language:
			text = re.sub('\^ReadOutNeed', 'Vorlesen, falls nötig. ', text)
		elif 'AT':
			text = re.sub('\^ReadOutNeed', 'Falls nötig vorlesen. ', text)	
		text = re.sub('\^Specify', 'Angeben. ', text)
		text = re.sub('\^FL_HISHER', ' sein/ihr ', text)
		text = re.sub('\^FL_VERB', ' wurde geboren ', text)
	elif 'RUS' in country_language:
		if 'LV' in country_language or 'LT' in country_language:
			text = re.sub('\^ReadOutNeed', 'Прочитайте, если это необходимо. ', text)
		elif 'EE' in country_language:
			text = re.sub('\^ReadOutNeed', 'Зачитайте, если необходимо. ', text)
		elif 'IL' in country_language:
			text = re.sub('\^ReadOutNeed', 'При необходимости зачитайте. ', text)
		text = re.sub('\^Specify', 'Уточнить. ', text)
		text = re.sub('\^FL_HISHER', ' его/ее ', text)
		text = re.sub('\^FL_VERB', ' родился ', text)

	text = re.sub('\^CodeAll', share_instructions.code_all, text)
	text = re.sub('\^ReadOut', share_instructions.read_out, text)
	text = re.sub('\^FL_RE012a', share_instructions.job_position, text)
	text = re.sub('\^FL_RE012b', share_instructions.job_position, text)
	text = re.sub('\^RE012_jobtitle', share_instructions.job_position, text)
	text = re.sub('\^EP616c_NTofJobCode', share_instructions.job_position, text)
	text = re.sub('\^EP152c_NTofJobCode', share_instructions.job_position, text)
	text = re.sub('\^EX613c_LastJobPartnerCode', share_instructions.job_position, text)
	text = re.sub('\^DN029c_JobOfParent10Code', share_instructions.job_position, text)
	text = re.sub('\^FL_HIS_HER', share_instructions.he_she, text)
	text = re.sub('\^FL_GENDER', share_instructions.gender, text)
	text = re.sub('\^FL_MOVED_IN_M', share_instructions.moved_in_month, text)



	return text


def extract_questions_and_procedures_w8(subnode, df_questions, df_procedures, parent_map, name, splitter, country_language, output_source_questionnaire_flag):
	"""
	Extracts the questions and procedures text segments from SHARE wave 8 XML files.

	Args:
		param1 df_questions (pandas dataframe): the dataframe that holds the question segments extracted from the XML nodes in previous steps.
		param2 df_procedures (pandas dataframe): the dataframe that holds the procedures for fills substitution, extracted from the XML nodes in previous steps.
		param3 parent_map (dictionary): a dictionary that maps each child to its parent in the XML tree.
		param4 name (string): name node attribute inside XML file
		param5 splitter (NLTK object): Sentence segmenter object from NLTK
		param6 country_language (string): country and language metadata, contained in the filename
		param7 output_source_questionnaire_flag (string): indicates if the data to be extracted in the source (1) or the target language (any other value)

	Returns: 
		df_questions (pandas dataframe) and df_procedures (pandas dataframe) datafarmes filled with the extracted text segments from questions and procedures nodes.
	"""
	for child in subnode.getiterator():
		if child.tag == 'question_element' and 'type_name' in child.attrib:
			if child.attrib['type_name'] == 'QText' or child.attrib['type_name'] == 'QInstruction':

				if child.attrib['type_name'] == 'QText':
					item_type_aux = 'REQUEST'
				else:
					item_type_aux = 'INSTRUCTION'
				
				text_nodes = child.findall('text')
				for text_node in text_nodes:
					
					text = None
					if output_source_questionnaire_flag == '1':
						if text_node.attrib['translation_id'] == '1' and text_node.text is not None:
							text = clean_text_share(text_node.text, country_language, False)
					else:
						if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
							text = clean_text_share(text_node.text, country_language, False)

					if text is not None and '^LblOnlyTesting' not in text and '^LblSucInstalled' not in text:
						if name == 'THIS_INTERVIEW':
							last_row = df_questions.iloc[-1]
							name = last_row['item_name']

						text = replace_untranslated_instructions(country_language, text)
						text, item_type = eliminate_showcardID_and_adjust_item_type(text, name)
						sentences = splitter.tokenize(text)
						for sentence in sentences:
							if '?' in sentence:
								item_type = 'REQUEST'
							if item_type is None:
								item_type = item_type_aux
							if sentence != '.':
								data = {'item_name': name, 'item_type':item_type, 'text': sentence}
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
						if output_source_questionnaire_flag == '1':
							if text_node.attrib['translation_id'] == '1' and text_node.text is not None and text_node.text != '{}':
								text = clean_text_share(text_node.text, country_language, False)
						else:
							if text_node.attrib['translation_id'] != '1' and text_node.text is not None and text_node.text != '{}':
								text = clean_text_share(text_node.text, country_language, False)

						if text is not None and '+piHO004_OthPer+' not in text and '{empty}' not in text and 'empty' not in text:
							order = parent_map[text_node].attrib['order']
							data = {'item_name': proc_name, 'fill_name':fill_name, 'order':order, 'text': text}
							df_procedures = df_procedures.append(data, ignore_index = True)


	return df_questions, df_procedures

def extract_questions_and_procedures_w7(subnode, df_questions, df_procedures, parent_map, name, tmt_id, splitter, country_language, output_source_questionnaire_flag):
	"""
	Extracts the questions and procedures text segments from SHARE wave 7 XML files.

	Args:
		param1 df_questions (pandas dataframe): the dataframe that holds the question segments extracted from the XML nodes in previous steps.
		param2 df_procedures (pandas dataframe): the dataframe that holds the procedures for fills substitution, extracted from the XML nodes in previous steps.
		param3 parent_map (dictionary): a dictionary that maps each child to its parent in the XML tree.
		param4 name (string): name node attribute inside XML file
		param5 tmt_id (string): tmt_id node attribute inside XML file
		param6 splitter (NLTK object): Sentence segmenter object from NLTK
		param7 country_language (string): country and language metadata, contained in the filename
		param8 output_source_questionnaire_flag (string): indicates if the data to be extracted in the source (1) or the target language (any other value)

	Returns: 
		df_questions (pandas dataframe) and df_procedures (pandas dataframe) datafarmes filled with the extracted text segments from questions and procedures nodes.
	"""

	for child in subnode.getiterator():
		if child.tag == 'question_element' and 'type_name' in child.attrib:
			if child.attrib['type_name'] == 'QText' or child.attrib['type_name'] == 'QInstruction':

				if child.attrib['type_name'] == 'QText':
					item_type_aux = 'REQUEST'
				else:
					item_type_aux = 'INSTRUCTION'
				
				text_nodes = child.findall('text')
				for text_node in text_nodes:
					text = None
					if output_source_questionnaire_flag == '1':
						if text_node.attrib['translation_id'] == '1' and text_node.text is not None:
							text = clean_text_share(text_node.text, country_language, True)
							if text is not None and 'No.' in text:
								text = text.replace('No.', 'nº')
					else:
						if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
							text = clean_text_share(text_node.text, country_language, True)

					if text is not None:
						if name == 'THIS_INTERVIEW':
							last_row = df_questions.iloc[-1]
							name = last_row['item_name']

						text = replace_untranslated_instructions(country_language, text)
						text, item_type = eliminate_showcardID_and_adjust_item_type(text, name)
						sentences = splitter.tokenize(text)
						for sentence in sentences:
							if '?' in sentence:
								item_type = 'REQUEST'
							if item_type is None:
								item_type = item_type_aux
							if '^Children_table' not in sentence and '^Press' not in sentence and '^FLDefault[84] ^Amount' not in sentence and name != 'JobCode' and name != 'CountryCode' and sentence != '.':
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
						if output_source_questionnaire_flag == '1':
							if text_node.attrib['translation_id'] == '1' and text_node.text is not None and text_node.text != '{}':
								text = clean_text_share(text_node.text, country_language, True)
						else:
							if text_node.attrib['translation_id'] != '1' and text_node.text is not None and text_node.text != '{}':
								text = clean_text_share(text_node.text, country_language, True)

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
	Retrieve study and country_language information from the name of the input file. 
	Instantiate a NLTK sentence splitter based on file input language. 
	"""
	if output_source_questionnaire_flag == '1' and 'SHA_R08' in filename:
		survey_item_prefix = 'SHA_R08_2019_ENG_SOURCE_'
		study, country_language = get_country_language_and_study_info('SHA_R08_2019_ENG_SOURCE')
		splitter = ut.get_sentence_splitter('SHA_R08_2019_ENG_SOURCE')
	elif output_source_questionnaire_flag == '1' and 'SHA_R07' in filename:
		survey_item_prefix = 'SHA_R07_2017_ENG_SOURCE_'
		study, country_language = get_country_language_and_study_info('SHA_R07_2017_ENG_SOURCE')
		splitter = ut.get_sentence_splitter('SHA_R07_2017_ENG_SOURCE')
	else:
		survey_item_prefix = re.sub('\.xml', '', filename)+'_'
		study, country_language = get_country_language_and_study_info(filename)
		splitter = ut.get_sentence_splitter(filename)

	"""
	Reset the initial survey_id sufix, because main is called iterativelly for every file in folder.
	"""
	ut.reset_initial_sufix()

	"""
	Reset the initial showcard_id sufix, because main is called iterativelly for every file in folder.
	"""
	ut.reset_initial_showcard()
		
	
	return df_questionnaire, survey_item_prefix, study, country_language,splitter

def build_questionnaire_structure(df_questions, df_answers,df_procedures, df_questionnaire, survey_item_prefix, share_modules, special_answer_categories, study):
	"""
	Build the final questionnaire from df_questions, df_answers and df_procedures.
	Calls the fill_extraction() and fill_unrolling() methods to replace the dynamic fills in the texts for the appropriate string definitions found in df_procedures.

	Args:
		param1 df_questions (pandas dataframe): the dataframe that holds the question segments extracted from the XML nodes in previous steps.
		param2 df_answers (pandas dataframe): the dataframe that holds the answer segments extracted from the XML nodes in previous steps.
		param3 df_procedures (pandas dataframe): the dataframe that holds the procedures for fills substitution, extracted from the XML nodes in previous steps.
		param4 df_questionnaire (pandas dataframe): a dataframe to hold the final questionnaire.
		param5 survey_item_prefix (string): the prefix of survey item IDS, either embedded in the filename or hard-coded in the case of ENG_SOUCE data extraction.
		param6 share_modules (dictionary): a dictionary (round dependent) with the full name of all SHARE modules.
		param7 special_answer_categories (Python object): a language-specific instantiated object that contains string definitions of special answer categories (Don't know, Refuse, etc)
		param8 study (string): the study metadata, embedded in the input filename or hard-coded in the case of ENG_SOUCE data extraction.

	Returns: 
		The final SHARE questionnaire, stored in df_questionnaire (pandas dataframe).
	"""
	for i, row in df_questions.iterrows():
		if df_questionnaire.empty:
			survey_item_id = ut.get_survey_item_id(survey_item_prefix)
		else:
			survey_item_id = ut.update_survey_item_id(survey_item_prefix)	

		text = row['text']
		fills = fill_extraction(text)
			
		if fills is None:				
			data = {'survey_item_ID':survey_item_id, 'Study': study, 'module': get_module_metadata(row['item_name'], share_modules), 
			'item_type':row['item_type'], 'item_name':row['item_name'], 
			'item_value':None, 'text':re.sub(' +', ' ', text)}
			df_questionnaire = df_questionnaire.append(data, ignore_index = True)
		else:
			for fill in fills:
				df_questionnaire = fill_unrolling(text, fills, df_procedures, df_questionnaire, survey_item_id, row['item_name'], share_modules, study, row['item_type'])

		last_item_name = row['item_name']
		last_row = df_questionnaire.iloc[-1]
		last_module = last_row['module']

		
	if last_row['item_type'] != 'INTRODUCTION':
		j=0
		for i, row in df_answers.iterrows():		
			survey_item_id = ut.update_survey_item_id(survey_item_prefix)	
			text = replace_fill_in_answer(row['text'])

			fills = fill_extraction(row['text'])
			if fills:
				texts = fill_substitution_in_answer(row['text'], fills, df_procedures)

				if texts:
					for text in texts:
						data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': last_module, 
						'item_type':'RESPONSE', 'item_name':last_item_name, 
						'item_value':j, 'text':re.sub(' +', ' ', text)}
						df_questionnaire = df_questionnaire.append(data, ignore_index = True)
						j=j+1
						
			else:
				data = {'survey_item_ID':survey_item_id, 'Study':study, 'module': last_module, 
				'item_type':'RESPONSE', 'item_name':last_item_name, 
				'item_value':j, 'text':re.sub(' +', ' ', text)}
				df_questionnaire = df_questionnaire.append(data, ignore_index = True)
				j=j+1
				

	return df_questionnaire

def filter_items_to_build_questionnaire_structure_w8(df_questions, df_answers,df_procedures, df_questionnaire, survey_item_prefix, share_modules, special_answer_categories, study):
	"""
	Filters the question and answer dataframes by the item name.
	Only segments with the same item name are considered as alignment candidates.
	Calls the build_questionnaire_structure() function to build the final questionnaire from df_questions, df_answers and df_procedures.

	Args:
		param1 df_questions (pandas dataframe): the dataframe that holds the question segments extracted from the XML nodes in previous steps.
		param2 df_answers (pandas dataframe): the dataframe that holds the answer segments extracted from the XML nodes in previous steps.
		param3 df_procedures (pandas dataframe): the dataframe that holds the procedures for fills substitution, extracted from the XML nodes in previous steps.
		param4 df_questionnaire (pandas dataframe): a dataframe to hold the final questionnaire.
		param5 survey_item_prefix (string): the prefix of survey item IDS, either embedded in the filename or hard-coded in the case of ENG_SOUCE data extraction.
		param6 share_modules (dictionary): a dictionary (round dependent) with the full name of all SHARE modules.
		param7 special_answer_categories (Python object): a language-specific instantiated object that contains string definitions of special answer categories (Don't know, Refuse, etc)
		param8 study (string): the study metadata, embedded in the input filename or hard-coded in the case of ENG_SOUCE data extraction.

	Returns: 
		The final SHARE wave 8 questionnaire, stored in df_questionnaire (pandas dataframe), after passing through the build_questionnaire_structure() function. 
	"""
	unique_question_item_names = df_questions.item_name.unique()
	for unique_item_name in unique_question_item_names:
		df_questions_by_item_name = df_questions[df_questions['item_name'].str.lower()==unique_item_name.lower()]
		df_answers_by_item_name = df_answers[df_answers['item_name'].str.lower()==unique_item_name.lower()]

		df_questionnaire = build_questionnaire_structure(df_questions_by_item_name, df_answers_by_item_name, df_procedures, df_questionnaire, survey_item_prefix, share_modules, special_answer_categories, study)

	return df_questionnaire

def filter_items_to_build_questionnaire_structure_w7(df_questions, df_answers,df_procedures, df_questionnaire, survey_item_prefix, share_modules, special_answer_categories, study):
	"""
	Filters the question and answer dataframes by the tmt_ids.
	Only segments with the same tmt_id are considered as alignment candidates.
	Calls the build_questionnaire_structure() function to build the final questionnaire from df_questions, df_answers and df_procedures.
	
	Args:
		param1 df_questions (pandas dataframe): the dataframe that holds the question segments extracted from the XML nodes in previous steps.
		param2 df_answers (pandas dataframe): the dataframe that holds the answer segments extracted from the XML nodes in previous steps.
		param3 df_procedures (pandas dataframe): the dataframe that holds the procedures for fills substitution, extracted from the XML nodes in previous steps.
		param4 df_questionnaire (pandas dataframe): a dataframe to hold the final questionnaire.
		param5 survey_item_prefix (string): the prefix of survey item IDS, either embedded in the filename or hard-coded in the case of ENG_SOUCE data extraction.
		param6 share_modules (dictionary): a dictionary (round dependent) with the full name of all SHARE modules.
		param7 special_answer_categories (Python object): a language-specific instantiated object that contains string definitions of special answer categories (Don't know, Refuse, etc)
		param8 study (string): the study metadata, embedded in the input filename or hard-coded in the case of ENG_SOUCE data extraction.

	Returns: 
		The final SHARE wave 7 questionnaire, stored in df_questionnaire (pandas dataframe), after passing through the build_questionnaire_structure() function. 
	"""
	unique_question_tmt_ids = df_questions.tmt_id.unique()
	for unique_tmt_id in unique_question_tmt_ids:
		df_questions_tmt_id = df_questions[df_questions['tmt_id'].str.lower()==unique_tmt_id.lower()]
		df_answers_tmt_id = df_answers[df_answers['item_name'].str.lower()==unique_tmt_id.lower()]

		df_questionnaire = build_questionnaire_structure(df_questions_tmt_id, df_answers_tmt_id, df_procedures, df_questionnaire, survey_item_prefix, share_modules, special_answer_categories, study)

	return df_questionnaire


def ensure_sequential_survey_item_id(df, survey_item_prefix):
	ut.reset_initial_sufix()

	for i, row in df.iterrows():
		if i == 0:
			df.at[i,'survey_item_ID'] = ut.get_survey_item_id(survey_item_prefix)
		else:
			df.at[i,'survey_item_ID'] = ut.update_survey_item_id(survey_item_prefix)

	return df


def main(filename):
	"""
	Flag that indicates if the data to be extracted is from the source or the target questionnaire.
	"""
	output_source_questionnaire_flag = '1'

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
		df_questions = pd.DataFrame(columns=['item_name', 'item_type', 'text'])

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
					df_questions, df_procedures = extract_questions_and_procedures_w8(subnode, df_questions, df_procedures, parent_map, name, splitter, country_language, output_source_questionnaire_flag)

					
		for node in answers:
			for subnode in node.getiterator():
				if subnode.tag == 'answer':
					name = subnode.attrib['name']
					df_answers = extract_answers(subnode, df_answers, name, country_language, output_source_questionnaire_flag)


		
		df_questionnaire = filter_items_to_build_questionnaire_structure_w8(df_questions, df_answers,df_procedures, df_questionnaire, survey_item_prefix, share_modules, special_answer_categories, study)
		df_questionnaire =  ensure_sequential_survey_item_id(df_questionnaire, survey_item_prefix)


		if output_source_questionnaire_flag == '1':
			df_questionnaire.to_csv('SHA_R08_2019_ENG_SOURCE.csv', encoding='utf-8', sep='\t', index=False)
		else:
			df_questionnaire.to_csv(survey_item_prefix[:-1]+'.csv', encoding='utf-8', sep='\t', index=False)
			


	elif 'SHA_R07' in filename:
		share_modules = share_modules_object.modules_w7
		for node in questions:
			for subnode in node.getiterator():
				if subnode.tag == 'question':
					name = subnode.attrib['name']
					tmt_id = subnode.attrib['tmt_id']
					df_questions, df_procedures = extract_questions_and_procedures_w7(subnode, df_questions, df_procedures, parent_map, name, tmt_id, splitter, country_language, output_source_questionnaire_flag)

		for node in categories:
			for subnode in node.getiterator():
				if 'tmt_id' in subnode.attrib:
					tmt_id = subnode.attrib['tmt_id']
					df_answers = extract_categories(subnode, df_answers, tmt_id, country_language, output_source_questionnaire_flag)


		for node in qenums:
			for subnode in node.getiterator():
				if 'question_id' in subnode.attrib:
					question_id = subnode.attrib['question_id']
					df_answers = extract_qenums(subnode, df_answers, question_id, country_language, output_source_questionnaire_flag)


		df_questionnaire = filter_items_to_build_questionnaire_structure_w7(df_questions, df_answers,df_procedures, df_questionnaire, survey_item_prefix, share_modules, special_answer_categories, study)
		df_questionnaire =  ensure_sequential_survey_item_id(df_questionnaire, survey_item_prefix)

		if output_source_questionnaire_flag == '1':
			df_questionnaire.to_csv('SHA_R07_2017_ENG_SOURCE.csv', encoding='utf-8', sep='\t', index=False)
		else:
			df_questionnaire.to_csv(survey_item_prefix[:-1]+'.csv', encoding='utf-8', sep='\t', index=False)




if __name__ == "__main__":
	filename = str(sys.argv[1])
	print("Executing data extraction script for SHARE wave 8 (xml files)")
	main(filename)
