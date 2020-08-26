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
import utils as ut
from preprocessing_ess_utils import *


def eliminate_dots(sentence):
	return "".join(filter(lambda char: char != ".", sentence))

def remove_undesired_symbols(sentence):
	sentence = "".join(filter(lambda char: char != "»", sentence))
	sentence = "".join(filter(lambda char: char != "«", sentence))
	sentence = sentence.replace(" ?", "?")
	sentence = sentence.replace(" :", ":")

	return sentence
	

def string_is_uppercase(sentence):
	return [word for word in sentence if word.isupper()]

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
			# print(sentence)
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

def recursive_split_income_question(sentence, study, country):
	dict_answers = dict()
	categories = ['K','S','D','N','G','T', 'L', 'Q', 'F', 'J']


	if ('ESS Round 4' in study and 'Germany' in country) or ('ESS Round 9' in study and 'Switzerland' in country) or ('ESS Round 6' in study and 'United Kingdom' in country):
		categories = ['J','R','C','M','F','S', 'K', 'P', 'D', 'H']

	splits = re.compile("\s+[A-Z]\s+").split(sentence)

	dict_answers['pre'] = splits[0]
	for i, n in enumerate(splits[1:]):
		dict_answers[categories[i]] = n


	return dict_answers



def preprocess_one_to_ten_pattern(cleaned_df_round, analysed_item,row, module):
	sentence = eliminate_dots(analysed_item) 
	if re.compile('(01)', re.IGNORECASE).findall(sentence):
		first_part = sentence.split('02')
		first_part_clean = re.sub("^01 ", "", first_part[0])
		final_part = first_part[1].split('10')
		final_part_clean = re.sub("^10", "", final_part[1]) 
					
	else:
		final_part = sentence.split('10')
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('2')
		first_part_clean = re.sub("^1 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)
	
				
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
	'item_type': 'RESPONSE', 'item_value': 1, 'text': first_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	for n in range(2,10):
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': n, 'text': n}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
	'item_type': 'RESPONSE', 'item_value': 10, 'text': final_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	return cleaned_df_round

def preprocess_zero_to_ten_pattern(cleaned_df_round, analysed_item,row, module):
	sentence = sentence = eliminate_dots(analysed_item)
	if re.compile('(01)', re.IGNORECASE).findall(sentence):
		first_part = sentence.split('01')
		first_part_clean = re.sub("(^\s?00?\s?)*", "", first_part[0])
		final_part = first_part[1].split('10')
		final_part_clean = re.sub("^\s?10?\s?", "", final_part[1])
					
	else:
		final_part = sentence.split('10')
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('1')
		first_part_clean = re.sub("^0 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)
					

	#first part of the scale
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
	'item_type': 'RESPONSE', 'item_value': 0, 'text': first_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	#zero to ten values
	for n in range(1,10):
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': n, 'text': n}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	#last part of the scale
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
	'item_type': 'RESPONSE', 'item_value': 10, 'text': final_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	return cleaned_df_round


def preprocess_zero_to_nine_pattern(cleaned_df_round, analysed_item,row, module):
	sentence = eliminate_dots(analysed_item)
	if re.compile('(01)', re.IGNORECASE).findall(sentence):
		first_part = sentence.split('01')
		first_part_clean = re.sub("(^\s?00?\s?)*", "", first_part[0])
		final_part = first_part[1].split('09')
		final_part_clean = re.sub("^\s?09?\s?", "", final_part[1])
					
	else:
		final_part = sentence.split('9')
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('1')
		first_part_clean = re.sub("^0 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)
					

	#first part of the scale
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
	'item_type': 'RESPONSE', 'item_value': 0, 'text': first_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	#zero to ten values
	for n in range(1,9):
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': n, 'text': n}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	#last part of the scale
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
	'item_type': 'RESPONSE', 'item_value': 9, 'text': final_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	return cleaned_df_round


def preprocess_zero_to_six_pattern(cleaned_df_round, analysed_item,row, module):
	sentence = eliminate_dots(analysed_item)
	if re.compile('(00)', re.IGNORECASE).findall(sentence):
		first_part = sentence.split('01')
		first_part_clean = re.sub("^00 ", "", first_part[0])
		final_part = first_part[1].split('06')
		final_part_clean = re.sub("^06", "", final_part[1])
					
	else:
		final_part = sentence.split('6')
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('1')
		first_part_clean = re.sub("^0 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)
					

				
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
	'item_type': 'RESPONSE', 'item_value': 0, 'text': first_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	for n in range(1,6):
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': n, 'text': n}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
	'item_type': 'RESPONSE', 'item_value': 6, 'text': final_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)
	
	return cleaned_df_round
		
def preprocess_zero_to_five_pattern(cleaned_df_round, analysed_item,row, module):
	sentence = eliminate_dots(analysed_item)
	if re.compile('(00)', re.IGNORECASE).findall(sentence):
		first_part = sentence.split('01')
		first_part_clean = re.sub("^00 ", "", first_part[0])
		final_part = first_part[1].split('05')
		final_part_clean = re.sub("^05", "", final_part[1]) 
					
	else:
		final_part = sentence.split('5')
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('1')
		first_part_clean = re.sub("^0 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)
					
	#first part of the scale
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
	'item_type': 'RESPONSE', 'item_value': 0, 'text': first_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	for n in range(1,5):
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': n, 'text': n}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	#final part of the scale
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
	'item_type': 'RESPONSE', 'item_value': 5, 'text': final_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	return cleaned_df_round

def preprocess_one_to_seven_pattern(cleaned_df_round, analysed_item,row, module):
	sentence = eliminate_dots(analysed_item)
	if re.compile('(01)', re.IGNORECASE).findall(sentence):
		first_part = sentence.split('02')
		first_part_clean = re.sub("^01 ", "", first_part[0])
		final_part = first_part[1].split('07')
		final_part_clean = re.sub("^\s+", "", final_part[1]) 
					
	else:
		final_part = sentence.split('7')
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('2')
		first_part_clean = re.sub("^1 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)
	
	#first part of the scale			
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
	'item_type': 'RESPONSE', 'item_value': 1, 'text': first_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	#final part of the scale
	for n in range(2,7):
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': n, 'text': n}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
	'item_type': 'RESPONSE', 'item_value': 7, 'text': final_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	return cleaned_df_round

def preprocess_one_to_five_pattern(cleaned_df_round, analysed_item,row, module):
	sentence = eliminate_dots(analysed_item)
	if re.compile('(01)', re.IGNORECASE).findall(sentence):
		first_part = sentence.split('02')
		first_part_clean = re.sub("^01 ", "", first_part[0])
		final_part = first_part[1].split('05')
		final_part_clean = re.sub("^\s+", "", final_part[1]) 
					
	else:
		final_part = sentence.split('5')
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('2')
		first_part_clean = re.sub("^1 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)
	
	#first part of the scale			
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
	'item_type': 'RESPONSE', 'item_value': 1, 'text': first_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	#final part of the scale
	for n in range(2,5):
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': n, 'text': n}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
	'item_type': 'RESPONSE', 'item_value': 5, 'text': final_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	return cleaned_df_round

def preprocess_zero_to_four_pattern(cleaned_df_round, analysed_item,row, module):
	sentence = eliminate_dots(analysed_item)
	if re.compile('(00)', re.IGNORECASE).findall(sentence):
		first_part = sentence.split('01')
		first_part_clean = re.sub("^00 ", "", first_part[0])
		final_part = first_part[1].split('04')
		final_part_clean = re.sub("^04", "", final_part[1]) 
					
	else:
		final_part = sentence.split('4')
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('1')
		first_part_clean = re.sub("^0 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)

					
	#first part of the scale
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
	'item_type': 'RESPONSE', 'item_value': 0, 'text': first_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	for n in range(1,4):
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': n, 'text': n}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	#final part of the scale
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
	'item_type': 'RESPONSE', 'item_value': 4, 'text': final_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	return cleaned_df_round

def preprocess_one_to_four_pattern(cleaned_df_round, analysed_item,row, module):
	sentence = eliminate_dots(analysed_item)
	if re.compile('(01)', re.IGNORECASE).findall(sentence):
		first_part = sentence.split('02')
		first_part_clean = re.sub("^01 ", "", first_part[0])
		final_part = first_part[1].split('04')
		final_part_clean = re.sub("^4", "", final_part[1]) 
					
	else:
		final_part = sentence.split('4')
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('2')
		first_part_clean = re.sub("^1 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)
	
	#first part of the scale			
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
	'item_type': 'RESPONSE', 'item_value': 1, 'text': first_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	#final part of the scale
	for n in range(2,4):
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': n, 'text': n}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
	'item_type': 'RESPONSE', 'item_value': 4, 'text': final_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	return cleaned_df_round

def preprocess_zero_to_three_pattern(cleaned_df_round, analysed_item,row, module):
	sentence = eliminate_dots(analysed_item)
	if re.compile('(00)', re.IGNORECASE).findall(sentence):
		first_part = sentence.split('01')
		first_part_clean = re.sub("^00 ", "", first_part[0])
		final_part = first_part[1].split('03')
		final_part_clean = re.sub("^03", "", final_part[1]) 
					
	else:
		final_part = sentence.split('3')
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('1')
		first_part_clean = re.sub("^0 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)
					
	
	#first part of the scale
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
	'item_type': 'RESPONSE', 'item_value': 0, 'text': first_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	for n in range(1,3):
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': n, 'text': n}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	#final part of the scale
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
	'item_type': 'RESPONSE', 'item_value': 3, 'text': final_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	return cleaned_df_round

def preprocess_zero_to_two_pattern(cleaned_df_round, analysed_item,row, module):
	sentence = eliminate_dots(analysed_item)
	if re.compile('(00)', re.IGNORECASE).findall(sentence):
		first_part = sentence.split('01')
		first_part_clean = re.sub("^00 ", "", first_part[0])
		final_part = first_part[1].split('02')
		final_part_clean = re.sub("^\s+", "", final_part[1]) 
					
	else:
		final_part = sentence.split('2')
		final_part_clean = re.sub("^\s", "", final_part[1])
		first_part = final_part[0].split('1')
		first_part_clean = re.sub("^0 ", "", first_part[0])
		first_part_clean = re.sub("\s$", "", first_part_clean)
					
	
	#first part of the scale
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
	'item_type': 'RESPONSE', 'item_value': 0, 'text': first_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	for n in range(1,2):
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': n, 'text': n}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	#final part of the scale
	data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
	'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
	'item_type': 'RESPONSE', 'item_value': 2, 'text': final_part_clean}
	cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	return cleaned_df_round


def preprocess_zero_to_ten_with_value_in_five_pattern(cleaned_df_round, analysed_item,row, module):
	sentence = eliminate_dots(analysed_item)
	if re.compile('(00)', re.IGNORECASE).findall(sentence):
		first_part = sentence.split('01')
		first_part_clean = re.sub("^00 ", "", first_part[0])
		mid_part = first_part[1].split('05')
		mid_part_part = mid_part[1].split('06')
		mid_part_clean = re.sub("^\s+", "", mid_part_part[0]) 
		mid_part_clean = re.sub("\s+$", "", mid_part_clean) 
		final_part = mid_part_part[1]
		final_part = final_part.split('10')
		final_part_clean = re.sub("^\s+", "", final_part[1])
					
		#first part of the scale
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': 0, 'text': first_part_clean}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

		#one to four values
		for n in range(1,5):
			data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
			'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
			'item_type': 'RESPONSE', 'item_value': n, 'text': n}
			cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

		#mid part of the scale
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': 5, 'text': mid_part_clean}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

		#six to 10 values
		for n in range(6,10):
			data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'],"q_name": row['Question name'], 
			'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
			'item_type': 'RESPONSE', 'item_value': n, 'text': n}
			cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

		#final part of the scale
		data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
		'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
		'item_type': 'RESPONSE', 'item_value': 10, 'text': final_part_clean}
		cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

	return cleaned_df_round

def split_scale_without_numbers(sentence):
	is_scale = False
	scale_items = []
	index_uppercase = []

	for i, s in enumerate(sentence):
		if s.isupper():
			index_uppercase.append(i)

	
	if len(index_uppercase) > 1:
		is_scale = True
		for i, index in enumerate(index_uppercase):
			if index == index_uppercase[-1]:
				scale_items.append(sentence[index:])
			else:
				scale_items.append(sentence[index:(index_uppercase[i+1]-1)])


	return is_scale, scale_items





def clean_dataframe_by_round(df_round, sentence_splitter):
	# zero_to_ten_pattern = re.compile('(00?\s\w+(.)*\s0?1\s0?2\s0?3\s0?4\s0?5\s0?6\s0?7\s0?8\s0?9\s10\s\w+(.)*)', re.I)
	zero_to_ten_with_value_in_five_pattern = re.compile('(^00?\s+)(.)*(0?5\s[a-z]+)(.)*(10\s[a-z]+)', re.IGNORECASE)
	zero_to_ten_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?)\s+(0?6\.?)\s+(0?7\.?)\s+(0?8\.?)\s+(0?9\.?)\s+(10\.?\s+[a-z]+)', re.IGNORECASE)
	zero_to_nine_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?)\s+(0?6\.?)\s+(0?7\.?)\s+(0?8\.?)\s+(0?9\.?\s+[a-z]+)', re.IGNORECASE)
	one_to_ten_pattern = re.compile('(^0?1\.?\s+)(.)*\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?)\s+(0?6\.?)\s+(0?7\.?)\s+(0?8\.?)\s+(0?9\.?)\s+(10\.?\s+[a-z]+)', re.IGNORECASE)
	one_to_seven_pattern = re.compile('(^0?1\.?\s+)(.)*\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?)\s+(0?6\.?)\s+(0?7\.?\s+[a-z]+)', re.IGNORECASE)
	zero_to_five_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?\s+[a-z]+)', re.I)
	one_to_five_pattern = re.compile('(^0?1\.?\s+)(.)*\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?\s+[a-z]+)', re.IGNORECASE)
	zero_to_four_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?\s+[a-z]+)', re.I)
	one_to_four_pattern = re.compile('(^0?1\.?\s+)(.)*\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?\s+[a-z]+)', re.IGNORECASE)
	zero_to_three_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?)\s+(0?3\.?\s+[a-z]+)', re.I)
	zero_to_two_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?\s+[a-z]+)', re.I)
	zero_to_six_pattern = re.compile('(^00?\.?\s+)(.)*\s+(0?1\.?)\s+(0?2\.?)\s+(0?3\.?)\s+(0?4\.?)\s+(0?5\.?)\s+(0?6\.?\s+[a-z]+)', re.I)
	
	cleaned_df_round = pd.DataFrame(columns=['Study', 'Language', 'Country', 'q_name', 'q_concept', 'item_name', 'module', 'item_type', 'item_value', 'text'])
	
	for i, row in df_round.iterrows():
		module = re.match(r"([a-z]+)([0-9]+)", row['Question admin'], re.I)
		module = module.groups()[0]


		
		analysed_item = row['Answer options text']
		
		if analysed_item != '.' and isinstance(analysed_item, str):
			analysed_item = remove_undesired_symbols(analysed_item)
			######Regex matches 0-10 scales with words in item 5######
			if zero_to_ten_with_value_in_five_pattern.match(analysed_item):
				cleaned_df_round = preprocess_zero_to_ten_with_value_in_five_pattern(cleaned_df_round, analysed_item, row, module)
			#####################################
			######Regex matches 0-3 scales######
			elif zero_to_three_pattern.match(analysed_item):
				cleaned_df_round = preprocess_zero_to_three_pattern(cleaned_df_round, analysed_item,row, module)
			#####################################
			######Regex matches 0-2 scales######
			elif zero_to_two_pattern.match(analysed_item):
				cleaned_df_round = preprocess_zero_to_two_pattern(cleaned_df_round, analysed_item,row, module)
			#####################################
			######Regex matches 0-4 scales######
			elif zero_to_four_pattern.match(analysed_item):
				cleaned_df_round = preprocess_zero_to_four_pattern(cleaned_df_round, analysed_item,row, module)
			#####################################
			######Regex matches 1-4 scales######
			elif one_to_four_pattern.match(analysed_item):
				cleaned_df_round = preprocess_one_to_four_pattern(cleaned_df_round, analysed_item,row, module)
			#####################################
			######Regex matches 0-5 scales######
			elif zero_to_five_pattern.match(analysed_item):
				cleaned_df_round = preprocess_zero_to_five_pattern(cleaned_df_round, analysed_item,row, module)
			#####################################
			######Regex matches 0-5 scales######
			elif one_to_five_pattern.match(analysed_item):
				cleaned_df_round = preprocess_one_to_five_pattern(cleaned_df_round, analysed_item,row, module)
			#####################################
			######Regex matches 0-6 scales######
			elif zero_to_six_pattern.match(analysed_item):
				cleaned_df_round = preprocess_zero_to_six_pattern(cleaned_df_round, analysed_item,row, module)
			####################################
			######Regex matches 1-7 scales######
			elif one_to_seven_pattern.match(analysed_item):
				cleaned_df_round = preprocess_one_to_seven_pattern(cleaned_df_round, analysed_item,row, module)
			#####################################
			######Regex matches 0-10 scales######
			elif zero_to_ten_pattern.match(analysed_item):
				cleaned_df_round = preprocess_zero_to_ten_pattern(cleaned_df_round, analysed_item,row, module)
			#####################################
			######Regex matches 1-10 scales######
			elif one_to_ten_pattern.match(analysed_item):
				cleaned_df_round = preprocess_one_to_ten_pattern(cleaned_df_round, analysed_item,row, module)			
			#####################################
			######Regex matches 0-9 scales######
			elif zero_to_nine_pattern.match(analysed_item):
				cleaned_df_round = preprocess_zero_to_nine_pattern(cleaned_df_round, analysed_item,row, module)
			#####################################
			else:
				sentence = analysed_item
				if len(sentence.split(' ')) <= 3 or string_has_numbers(sentence)==False:
					if string_has_numbers(sentence)==False and len(sentence.split(' ')) > 3:
						is_scale, scale_items = split_scale_without_numbers(sentence)

						if is_scale ==  False:
							data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
							'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
							'item_type': 'RESPONSE', 'item_value': None, 'text': sentence}
							cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)
						else:
							for i, item in enumerate(scale_items):
								data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
								'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
								'item_type': 'RESPONSE', 'item_value': i, 'text': item}
								cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)


					else:
						data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
						'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
						'item_type': 'RESPONSE', 'item_value': None, 'text': sentence}
						cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

				elif currency in sentence:
					d = dict()
					d = recursive_split_income_question(sentence, row['Study'], row['Country'])

					if not d:
						pass
					else:
						for k, v in list(d.items()):
							if k == 'pre':
								data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
								'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
								'item_type': 'RESPONSE', 'item_value': None, 'text': v}
								cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)
							else:
								data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
								'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
								'item_type': 'RESPONSE', 'item_value': k, 'text': v}
								cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

				else:
					d = dict()
					sentence = eliminate_dots(analysed_item)
					# flag_zero, flag_begins_with_zero, flag_parentheses, flag_begins_with_number
					if re.compile('(\s+)?(00\s+)', re.IGNORECASE).findall(sentence):
						if re.compile('(^00\s+)', re.IGNORECASE).findall(sentence):
							d = recursive_split(sentence, True, True, False, True)
						else:
							d = recursive_split(sentence, True, True, False, False)
					elif re.compile('(\s+)?(-1\s+)', re.IGNORECASE).findall(sentence):
							d = recursive_split_plus_minus_scale(sentence)
					elif re.compile('(\s+)?(01\s+)', re.IGNORECASE).findall(sentence):
						if re.compile('(^01\s+)', re.IGNORECASE).findall(sentence):
							d = recursive_split(sentence, True, False, False, True)
						else:
							d = recursive_split(sentence, True, False, False, False)
					elif re.compile('(\s+)?(0\s+)', re.IGNORECASE).findall(sentence):
						if re.compile('(^0\s+)', re.IGNORECASE).findall(sentence):
							d = recursive_split(sentence, False, True, False, True)
						else:
							d = recursive_split(sentence, False, True, False, False)
					elif re.compile('(\s+)?(1\)\s+)', re.IGNORECASE).findall(sentence):
						if re.compile('(^1\)\s+)', re.IGNORECASE).findall(sentence):
							d = recursive_split(sentence, False, False, True, True)
						else:
							d = recursive_split(sentence, False, False, True, False)
					elif re.compile('(\s+)?(1\s+)', re.IGNORECASE).findall(sentence):
						if re.compile('(^1\s+)', re.IGNORECASE).findall(sentence):
							d = recursive_split(sentence, False, False, False, True)
						else:
							d = recursive_split(sentence, False, False, False, False)
						
					else:
						if "(entre '0' et '10')" in sentence:
							data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
							'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
							'item_type': 'RESPONSE', 'item_value': None, 'text': sentence}
							cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)
						else:
							print('NO MATCHES', sentence)


					if not d:
						pass
					else:
						for k, v in list(d.items()):
							data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
							'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
							'item_type': 'RESPONSE', 'item_value': k, 'text': v}
							cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)


	return cleaned_df_round

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
		introduction = remove_undesired_symbols(introduction)
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
		request = remove_undesired_symbols(request)
		sentences = splitter.tokenize(request)
		for sentence in sentences:
			if df.empty:
				survey_item_id = ut.get_survey_item_id(survey_item_prefix)
			else:
				survey_item_id = ut.update_survey_item_id(survey_item_prefix)

			if check_if_segment_is_instruction(sentence, country_language):
				item_type = 'INSTRUCTION'
			else:
				item_type = 'REQUEST'

			data = {'survey_item_ID':survey_item_id, 'Study':study,  'module': module, 
			'item_type': 'REQUEST','item_name':item_name, 'item_value': None, 'text': sentence}
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
		print(row['Question admin'], item_name)
		module = retrieve_item_module(item_name, survey_item_prefix)
		df_questionnaire = process_introduction(df_questionnaire, row, survey_item_prefix, item_name,module, splitter)
		df_questionnaire = process_request(df_questionnaire, row, survey_item_prefix, item_name,module, splitter)

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
		(df['Question admin'].str.contains('^E'))].index)

	return df


def main(folder_path):
	path = os.chdir(folder_path)
	files = os.listdir(path)

	for index, file in enumerate(files):
		if file.endswith(".csv") and 'SUPP' not in file:
			"""
			Reset the initial survey_id sufix, because main is called iterativelly for every file in folder.
			"""
			ut.reset_initial_sufix()
			df_supplementary = pd.read_csv(file)

			df_supplementary = drop_non_supplementary_modules(df_supplementary)
			dataframes_by_study = split_dataframe_by_study(df_supplementary, file)

			for k,v in list(dataframes_by_study.items()):
				if v.empty==False:
					df_supplementary = preprocess_data_by_study(v, k)

					df_supplementary.to_csv(k+'.csv', encoding='utf-8-sig', index=False)
	
	



if __name__ == "__main__":
	folder_path = str(sys.argv[1])
	main(folder_path)