"""
Python3 script developed using spreadsheets retrieved from the SQP database as input.
This script read the contents of the raw spreadsheets of supplementary questions, 
split the contents by round and preprocess the contents for each round.
After the preprocessing, distinct spreadsheets are created with the cleaned contents.
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 

import os
import sys
import pandas as pd
import nltk.data
import re
import unidecode
import utils as ut
from preprocessing_ess_utils import *


zero_to_ten_with_value_in_five_pattern = re.compile('(^00?\s+)(.)*(0?5\s[a-z]+)(.)*(10\s[a-z]+)', re.IGNORECASE)
zero_to_ten_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?)\s+(0?6\.?)\s+(0?7\.?)\s+(0?8\.?)\s+(0?9\.?)\s+(10\.?\s+[a-z]+)', re.IGNORECASE)
zero_to_nine_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?)\s+(0?6\.?)\s+(0?7\.?)\s+(0?8\.?)\s+(0?9\.?\s+[a-z]+)', re.IGNORECASE)
one_to_ten_pattern = re.compile('(^0?1\.?\s+)(.)*\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?)\s+(0?6\.?)\s+(0?7\.?)\s+(0?8\.?)\s+(0?9\.?)\s+(10\.?\s+[a-z]+)', re.IGNORECASE)
one_to_seven_pattern = re.compile('(^0?1\.?\s+)(.)*\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?)\s+(0?6\.?)\s+(0?7\.?\s+[a-z]+)', re.IGNORECASE)
zero_to_five_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?\s+[a-z]+)', re.IGNORECASE)
one_to_five_pattern = re.compile('(^0?1\.?\s+)(.)*\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?\s+[a-z]+)', re.IGNORECASE)
zero_to_four_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?\s+[a-z]+)', re.IGNORECASE)
one_to_four_pattern = re.compile('(^0?1\.?\s+)(.)*\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?\s+[a-z]+)', re.IGNORECASE)
zero_to_three_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?)\s+(0?3\.?\s+[a-z]+)', re.IGNORECASE)
zero_to_two_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?\s+[a-z]+)', re.IGNORECASE)
zero_to_six_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?)\s+(0?6\.?)\s+[a-z]+', re.IGNORECASE)
	

def eliminate_dots(sentence):
	return "".join(filter(lambda char: char != ".", sentence))

"""
Removes undesired symbols present in input file.
Args:
	param1 sentence (string): text segment extracted from input questionnaire.
Returns:
	cleaned sentence (string)
"""
def remove_undesired_symbols(sentence):
	sentence = "".join(filter(lambda char: char != "»", sentence))
	sentence = "".join(filter(lambda char: char != "«", sentence))
	sentence = sentence.replace(" ?", "?")
	sentence = sentence.replace(" :", ":")

	return sentence

"""
Checks if answer string has numbers, to properly process it.
Args:
	param1 sentence (string): answer extracted from input questionnaire.
Returns:
	Boolean. True, if there are numbers, False otherwise.
"""
def string_has_numbers(sentence):
	return bool(re.search(r'\d', sentence))

def recursive_split_plus_minus_scale(sentence):
	dict_answers = dict()
	
	splits = ['-5', '-4','-3','-2','-1','0','+1', '+2', '+3', '+4', '+5']
	
	for i,n in enumerate(splits):
		if n not in sentence and '-' in n:
			pass
		elif n not in sentence and '+' in n:
			return dict_answers
		else:
			scale_item = sentence.split(n, 1)
			dict_answers[n] = scale_item[0]
			sentence = scale_item[1]
			


	return dict_answers

def recursive_split(sentence, flag_zero, flag_begins_with_zero, flag_parentheses, flag_begins_with_number):
	dict_answers = dict()
	
	if flag_zero == True and flag_begins_with_zero==True and flag_parentheses==False:
		splits = ['00','01','02','03','04','05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
	elif flag_zero == True and flag_begins_with_zero==False and flag_parentheses==False:
		splits = ['01','02','03','04','05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
	elif flag_zero == False and flag_begins_with_zero==True and flag_parentheses==False:
		splits = ['0','1','2','3','4','5', '6', '7', '8', '9', '10','11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
	elif flag_zero == False and flag_begins_with_zero==False and flag_parentheses==False:
		splits = ['1','2','3','4','5', '6', '7', '8', '9', '10','11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
	elif flag_zero == False and flag_begins_with_zero==False and flag_parentheses==True:
		splits = ['1)','2)','3)','4)','5)', '6)', '7)', '8)', '9)', '10)', '11)', '12)', '13)', '14)', '15)', '16)', '17)', '18)', '19)', '20)']

	if flag_begins_with_number==True:
		for i,n in enumerate(splits):
			if splits[i+1] not in sentence:
				dict_answers[n] = sentence
				return dict_answers
			else:		
				scale_item = sentence.split(splits[i+1], 1)
				if flag_parentheses==True:
					item = re.sub('1\)', '', scale_item[0])
					n = re.sub('\)', '', n)
				else:
					item = re.sub('^(\s+)?00', '', scale_item[0])
					item = re.sub('^(\s+)?0', '', item)
					item = re.sub('^(\s+)?1', '', item)
				dict_answers[n] = item
				sentence = scale_item[1]

	else:
		for i,n in enumerate(splits):
			if n not in sentence and flag_parentheses==False:
				return dict_answers
			elif splits[i+1] not in sentence and flag_parentheses==True:
				return dict_answers
			else:
				scale_item = sentence.split(n, 1)
				dict_answers[n] = scale_item[0]
				sentence = scale_item[1]
			


	return dict_answers

def recursive_split_income_question(sentence, study, country_language):
	dict_answers = dict()
	categories = ['K','S','D','N','G','T', 'L', 'Q', 'F', 'J']


	if ('R04' in study and 'GER' in country_language) or ('R09' in study and 'CH' in country_language) or ('R06' in study and 'GB' in country_language):
		categories = ['J','R','C','M','F','S', 'K', 'P', 'D', 'H']

	splits = re.compile("\s+[A-Z]\s+").split(sentence)

	dict_answers['pre'] = splits[0]
	for i, n in enumerate(splits[1:]):
		dict_answers[categories[i]] = n


	return dict_answers



def process_answer_without_numbers(answer):
	is_scale = False
	scale_items = []
	index_uppercase = []

	for i, s in enumerate(answer):
		if s.isupper():
			index_uppercase.append(i)

	
	if len(index_uppercase) > 1:
		is_scale = True
		for i, index in enumerate(index_uppercase):
			if index == index_uppercase[-1]:
				scale_items.append(answer[index:])
			else:
				scale_items.append(answer[index:(index_uppercase[i+1]-1)])


	return is_scale, scale_items


def include_special_answer_category(survey_item_prefix, study,item_name,module, country_language, df_questionnaire):
	ess_special_answer_categories = instantiate_special_answer_category_object(country_language)
	data = {"survey_item_ID": ut.update_survey_item_id(survey_item_prefix),'Study': study, 'module': module,
	'item_type': 'RESPONSE', 'item_name': item_name, 'item_value': ess_special_answer_categories.dont_know[1],  
	'text': ess_special_answer_categories.dont_know[0]}
	df_questionnaire = df_questionnaire.append(data, ignore_index = True)	

	data = {"survey_item_ID": ut.update_survey_item_id(survey_item_prefix),'Study': study, 'module': module,
	'item_type': 'RESPONSE', 'item_name': item_name, 'item_value': ess_special_answer_categories.refuse[1],  
	'text': ess_special_answer_categories.refuse[0]}
	df_questionnaire = df_questionnaire.append(data, ignore_index = True)
	
	return df_questionnaire	

def process_zero_to_ten_with_middle_text_scale(df, answer, survey_item_prefix,study,module,item_name,country_language):
	answer = eliminate_dots(answer)
	if re.compile('(00)', re.IGNORECASE).findall(answer):
		first_part = answer.split('01')
		first_part_clean = re.sub("^00 ", "", first_part[0])
		mid_part = first_part[1].split('05')
		mid_part_part = mid_part[1].split('06')
		mid_part_clean = re.sub("^\s+", "", mid_part_part[0]) 
		mid_part_clean = re.sub("\s+$", "", mid_part_clean) 
		final_part = mid_part_part[1]
		final_part = final_part.split('10')
		final_part_clean = re.sub("^\s+", "", final_part[1])
					
		"""
		first part of the scale
		"""
		data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
		'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
		'item_value': '0', 'text': first_part_clean}
		df = df.append(data, ignore_index = True)

		"""
		middle
		"""
		data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
		'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
		'item_value': '5', 'text': mid_part_clean}
		df = df.append(data, ignore_index = True)

		"""
		final part of the scale
		"""
		data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
		'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
		'item_value': '10', 'text': mid_part_clean}
		df = df.append(data, ignore_index = True)

		df = include_special_answer_category(survey_item_prefix, study, item_name,module, country_language, df)

	return df

def process_one_to_x_scale(df,higher_side, answer, survey_item_prefix,study,module,item_name,country_language):
	answer = eliminate_dots(answer)
	if re.compile('(01)', re.IGNORECASE).findall(answer):
		first_part = answer.split('02')
		first_part_clean = re.sub("^01 ", "", first_part[0])
		if higher_side == '10':
			final_part = first_part[1].split('10')
		else:
			final_part = first_part[1].split('0'+higher_side)

		final_part_clean = re.sub("^\s", "", final_part[1]) 

					
	else:
		final_part = answer.split(higher_side)
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('2')
		first_part_clean = re.sub("^1 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)
		
	"""
	first part of the scale
	"""
	data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
	'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
	'item_value': '0', 'text': first_part_clean}
	df = df.append(data, ignore_index = True)

	"""
	final part of the scale
	"""
	data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
	'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
	'item_value': higher_side, 'text': final_part_clean}
	df = df.append(data, ignore_index = True)

	df = include_special_answer_category(survey_item_prefix, study, item_name,module, country_language, df)

	return df

def process_zero_to_x_scale(df,higher_side, answer, survey_item_prefix,study,module,item_name,country_language):
	answer = eliminate_dots(answer)
	

	if re.compile('(00)', re.IGNORECASE).findall(answer):
		first_part = answer.split('01')
		first_part_clean = re.sub("^00 ", "", first_part[0])
		
		if higher_side == '10':
			final_part = first_part[1].split('10')
		else:
			final_part = first_part[1].split('0'+higher_side)

		final_part_clean = re.sub("^\s", "", final_part[1])  
					
	else:
		final_part = answer.split(higher_side)
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('1')
		first_part_clean = re.sub("^0 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)
					
	"""
	first part of the scale
	"""
	data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
	'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
	'item_value': '0', 'text': first_part_clean}
	df = df.append(data, ignore_index = True)

	"""
	final part of the scale
	"""
	data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
	'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
	'item_value': higher_side, 'text': final_part_clean}
	df = df.append(data, ignore_index = True)

	df = include_special_answer_category(survey_item_prefix, study, item_name,module, country_language, df)

	return df

"""
Processes answer segments.

Args:
	param1 df (pandas dataframe): dataframe to store processed questionnaire data.
	param2 row (pandas dataframe row): row of dataframe with contents of the input 
	file being analyzed in outer loop.
	param3 survey_item_prefix (string): prefix of survey_item_ID.
	param4 item_name (string): item_name metadata parameter, retrieved in previous steps.
	param5 module (string): module metadata parameter, retrieved in previous steps.

Returns:
	a pandas dataframe with preprocessed answer segments.
"""
def process_answer(df, row, survey_item_prefix, item_name,module):
	study, country_language = get_country_language_and_study_info(survey_item_prefix)
	answer = row['Answer options text']
	
	if answer != '.' and isinstance(answer, str):
		# answer = remove_undesired_symbols(answer)
		answer = clean_text(answer)
		"""
		Regex matches 0-10 scales with words in item 5
		"""
		if zero_to_ten_with_value_in_five_pattern.match(unidecode.unidecode(answer)):
			return process_zero_to_ten_with_middle_text_scale(df, answer, survey_item_prefix,study,module,item_name,country_language)
		
		"""
		Regex matches 0-10 scales
		"""
		if zero_to_ten_pattern.match(unidecode.unidecode(answer)):
			return process_zero_to_x_scale(df,'10', answer, survey_item_prefix,study,module,item_name,country_language) 
			
		"""
		Regex matches 1-10 scales
		"""
		if one_to_ten_pattern.match(unidecode.unidecode(answer)):
			return process_one_to_x_scale(df,'10', answer, survey_item_prefix,study,module,item_name,country_language)		
			
		"""
		Regex matches 0-9 scales
		"""
		if zero_to_nine_pattern.match(unidecode.unidecode(answer)):
			return process_zero_to_x_scale(df,'9', answer, survey_item_prefix,study,module,item_name,country_language)
		

		"""
		Regex matches 0-5 scales
		"""
		if zero_to_five_pattern.match(unidecode.unidecode(answer)):
			return process_zero_to_x_scale(df,'5', answer, survey_item_prefix,study,module,item_name,country_language) 

		"""
		Regex matches 1-5 scales
		"""
		if one_to_five_pattern.match(unidecode.unidecode(answer)):
			return process_one_to_x_scale(df,'5', answer, survey_item_prefix,study,module,item_name,country_language)
		
		"""
		Regex matches 0-6 scales
		"""
		if zero_to_six_pattern.match(unidecode.unidecode(answer)):
			return process_zero_to_x_scale(df,'6', answer, survey_item_prefix,study,module,item_name,country_language) 


		"""
		Regex matches 1-7 scales
		"""
		if one_to_seven_pattern.match(unidecode.unidecode(answer)):
			return  process_one_to_x_scale(df,'7', answer, survey_item_prefix,study,module,item_name,country_language)
		

		"""
		Regex matches 0-4 scales
		"""
		if zero_to_four_pattern.match(unidecode.unidecode(answer)):
			return process_zero_to_x_scale(df,'4', answer, survey_item_prefix,study,module,item_name,country_language) 

		"""
		Regex matches 1-4 scales
		"""
		if one_to_four_pattern.match(unidecode.unidecode(answer)):
			return process_one_to_x_scale(df,'4', answer, survey_item_prefix,study,module,item_name,country_language)


		"""
		Regex matches 0-3 scales
		"""
		if zero_to_three_pattern.match(unidecode.unidecode(answer)):
			return  process_zero_to_x_scale(df,'3', answer, survey_item_prefix,study,module,item_name,country_language) 
			
		
		"""
		Regex matches 0-2 scales
		"""
		if zero_to_two_pattern.match(unidecode.unidecode(answer)):
			return process_zero_to_x_scale(df,'2', answer, survey_item_prefix,study,module,item_name,country_language)

			
		else:
			if len(answer.split(' ')) <= 3 or string_has_numbers(answer)==False:
				if string_has_numbers(answer)==False and len(answer.split(' ')) > 3:
					is_scale, scale_items = process_answer_without_numbers(answer)

					if is_scale ==  False:
						data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
						'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
						'item_value': None, 'text': answer}
						df = df.append(data, ignore_index = True)
						df = include_special_answer_category(survey_item_prefix, study, item_name,module, country_language, df)
						return df

					else:
						for i, scale_item in enumerate(scale_items):
							data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
							'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
							'item_value': i, 'text': scale_item}
							df = df.append(data, ignore_index = True)
						df = include_special_answer_category(survey_item_prefix, study, item_name,module, country_language, df)
						return df

			elif currency in answer:
				d = dict()
				d = recursive_split_income_question(answer, study, country_language)

				if d:
					for k, v in list(d.items()):
						if k == 'pre':
							data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
							'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
							'item_value': None, 'text': v}
							df = df.append(data, ignore_index = True)
						else:
							data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
							'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
							'item_value': k, 'text': v}
							df = df.append(data, ignore_index = True)
					df = include_special_answer_category(survey_item_prefix, study, item_name,module, country_language, df)
					return df

	
			else:
				d = dict()
				answer = eliminate_dots(answer)
				# flag_zero, flag_begins_with_zero, flag_parentheses, flag_begins_with_number
				if re.compile('(\s+)?(00\s+)', re.IGNORECASE).findall(answer):
					if re.compile('(^00\s+)', re.IGNORECASE).findall(answer):
						d = recursive_split(answer, True, True, False, True)
					else:
						d = recursive_split(answer, True, True, False, False)
				elif re.compile('(\s+)?(-1\s+)', re.IGNORECASE).findall(answer):
						d = recursive_split_plus_minus_scale(answer)
				elif re.compile('(\s+)?(01\s+)', re.IGNORECASE).findall(answer):
					if re.compile('(^01\s+)', re.IGNORECASE).findall(answer):
						d = recursive_split(answer, True, False, False, True)
					else:
						d = recursive_split(answer, True, False, False, False)
				elif re.compile('(\s+)?(0\s+)', re.IGNORECASE).findall(answer):
					if re.compile('(^0\s+)', re.IGNORECASE).findall(answer):
						d = recursive_split(answer, False, True, False, True)
					else:
						d = recursive_split(answer, False, True, False, False)
				elif re.compile('(\s+)?(1\)\s+)', re.IGNORECASE).findall(answer):
					if re.compile('(^1\)\s+)', re.IGNORECASE).findall(answer):
						d = recursive_split(answer, False, False, True, True)
					else:
						d = recursive_split(answer, False, False, True, False)
				elif re.compile('(\s+)?(1\s+)', re.IGNORECASE).findall(answer):
					if re.compile('(^1\s+)', re.IGNORECASE).findall(answer):
						d = recursive_split(answer, False, False, False, True)
					else:
						d = recursive_split(answer, False, False, False, False)
						
				else:
					if "(entre '0' et '10')" in answer:
						data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
						'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
						'item_value': None, 'text': answer}
						df = df.append(data, ignore_index = True)
						df = include_special_answer_category(survey_item_prefix, study, item_name,module, country_language, df)

					else:
						print('NO MATCHES', answer)


				if d:
					for k, v in list(d.items()):
						data = {'survey_item_ID':ut.update_survey_item_id(survey_item_prefix), 
						'Study':study,  'module': module, 'item_type': 'RESPONSE','item_name':item_name, 
						'item_value': k, 'text': v}
						df = df.append(data, ignore_index = True)
					df = include_special_answer_category(survey_item_prefix, study, item_name,module, country_language, df)
	return df

"""
Processes introduction segments.

Args:
	param1 df (pandas dataframe): dataframe to store processed questionnaire data.
	param2 row (pandas dataframe row): row of dataframe with contents of the input 
	file being analyzed in outer loop.
	param3 survey_item_prefix (string): prefix of survey_item_ID.
	param4 item_name (string): item_name metadata parameter, retrieved in previous steps.
	param5 module (string): module metadata parameter, retrieved in previous steps.
	param6 splitter (NLTK object): sentence segmentation from NLTK library.

Returns:
	a pandas dataframe with preprocessed introduction segments.
"""
def process_introduction(df, row, survey_item_prefix, item_name,module, splitter):
	introduction = row['Introduction text']
	study, country_language = get_country_language_and_study_info(survey_item_prefix)

	if introduction != '.' and isinstance(introduction, str):
		# introduction = remove_undesired_symbols(introduction)
		introduction = clean_text(introduction)
		sentences = splitter.tokenize(introduction)
		for sentence in sentences:
			if df.empty:
				survey_item_id = ut.get_survey_item_id(survey_item_prefix)
			else:
				survey_item_id = ut.update_survey_item_id(survey_item_prefix)

			data = {'survey_item_ID':survey_item_id, 'Study':study,  'module': module, 
			'item_type': 'INTRODUCTION','item_name':item_name, 'item_value': None, 'text': sentence}
			df = df.append(data, ignore_index = True)

	return df

"""
Processes request segments.

Args:
	param1 df (pandas dataframe): dataframe to store processed questionnaire data.
	param2 row (pandas dataframe row): row of dataframe with contents of the input 
	file being analyzed in outer loop.
	param3 survey_item_prefix (string): prefix of survey_item_ID.
	param4 item_name (string): item_name metadata parameter, retrieved in previous steps.
	param5 module (string): module metadata parameter, retrieved in previous steps.
	param6 splitter (NLTK object): sentence segmentation from NLTK library.

Returns:
	a pandas dataframe with preprocessed request segments.
"""
def process_request(df, row, survey_item_prefix, item_name,module, splitter):
	request = row['Request for answer text']
	study, country_language = get_country_language_and_study_info(survey_item_prefix)

	if request != '.' and isinstance(request, str):
		# request = remove_undesired_symbols(request)
		request = clean_text(request)
		sentences = splitter.tokenize(request)
		for sentence in sentences:
			if sentence != '...':
				if df.empty:
					survey_item_id = ut.get_survey_item_id(survey_item_prefix)
				else:
					survey_item_id = ut.update_survey_item_id(survey_item_prefix)

				if check_if_segment_is_instruction(sentence, country_language):
					item_type = 'INSTRUCTION'
				else:
					item_type = 'REQUEST'

				data = {'survey_item_ID':survey_item_id, 'Study':study,  'module': module, 
				'item_type': item_type,'item_name':item_name, 'item_value': None, 'text': sentence}
				df = df.append(data, ignore_index = True)

	return df

"""
Calls the appropriate methods to preprocess introduction, request and response segments
(there are no instruction segments in SQP by design).

Args:
	param1 df (pandas dataframe): dataframe with contents of the input file.
Returns:
	a pandas dataframe with preprocessed data.
"""
def preprocess_data_by_study(df, survey_item_prefix):
	"""
	A pandas dataframe to store questionnaire data.
	"""
	df_questionnaire = pd.DataFrame(columns=['survey_item_ID', 'Study', 'module', 'item_type', 
	'item_name', 'item_value', 'text'])

	"""
	Instantiate a NLTK sentence splitter based on language. 
	"""
	splitter = ut.get_sentence_splitter(survey_item_prefix)

	for i, row in df.iterrows():
		item_name = standardize_supplementary_item_name(row['Question admin'])
		module = retrieve_item_module(item_name, survey_item_prefix)
		df_questionnaire = process_introduction(df_questionnaire, row, survey_item_prefix, item_name,module, splitter)
		df_questionnaire = process_request(df_questionnaire, row, survey_item_prefix, item_name,module, splitter)
		df_questionnaire = process_answer(df_questionnaire, row, survey_item_prefix, item_name,module)

	return df_questionnaire


"""
Splits the dataframe with contents of the input file, which has all rounds in it,
in multiple dataframes divided by round (study). The splitted dataframes are stored
in a dictionary for futher preprocessing steps.

Args:
	param1 df (pandas dataframe): dataframe with contents of the input file.

Returns:
	dictionary containing the dataframes per study.
"""
def split_dataframe_by_study(df, filename):
	dataframes_by_study = dict()
	filename_without_extension = re.sub('\.csv', '', filename)

	unique_study = df['Study'].unique()
	for s in unique_study:
		a_round = df['Study'] == s
		df_round = df[a_round]
		study = standardize_study_metadata(s)
		survey_item_prefix = study+'_'+filename_without_extension+'_'
		dataframes_by_study[survey_item_prefix] = df_round


	return dataframes_by_study


"""
Deletes all questions that are not from supplementary modules in the input file.
Such input files come from the SQP database, and there are some questions from the
modules A, B, C, D and E. These questions are already included in the database 
trough the preprocessing of the plain text files. Therefore, it is necessary
to exclude them to not generate duplicates in the database.

Args:
	param1 df (pandas dataframe): input file contents stored in a pandas dataframe object.
Returns:
	pandas dataframe, without non supplementary modules.
"""
def drop_non_supplementary_modules(df):
	df = df.drop(df[(df['Question admin'].str.contains('^A')) | 
		(df['Question admin'].str.contains('^B')) | 
		(df['Question admin'].str.contains('^C')) | 
		(df['Question admin'].str.contains('^D')) |
		(df['Question admin'].str.contains('^F')) | 
		(df['Question admin'].str.contains('^E'))].index)

	return df

def define_currency(file):
	
	if 'CZE_CZ' in file:
		return 'Kč'
	elif 'NOR' in file:
		return 'NOK'
	elif 'GER_DE' in file or 'GER_AT' in file or 'FRE' in file or 'POR' in file or 'SPA' in file or 'CAT' in file or 'ENG_IE' in file or 'RUS' in file:
		return '€'
	elif 'GER_CH' in file:
		return 'CHF'
	elif 'ENG_GB' in file:
		return '£'
	elif 'ENG_SOURCE' in file:
		return 'individual income'

def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)

	for index, file in enumerate(files):
		if file.endswith(".csv") and 'SUPP' not in file:
			global currency
			currency =  define_currency(file)
			df_supplementary = pd.read_csv(file)

			df_supplementary = drop_non_supplementary_modules(df_supplementary)
			dataframes_by_study = split_dataframe_by_study(df_supplementary, file)

			for k,v in list(dataframes_by_study.items()):
				if v.empty==False:
					"""
					Reset the initial survey_id sufix.
					"""
					ut.reset_initial_sufix()

					df_supplementary = preprocess_data_by_study(v, k)

					df_supplementary.to_csv('SUPP_'+k[:-1]+'.csv', encoding='utf-8-sig', index=False)
	
	



if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)