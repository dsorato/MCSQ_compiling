import os
import sys
import pandas as pd
import nltk.data
import re

###############README###############
# This script read the contents of the raw spreadsheets of supplementary questions, 
# split the contents by round and preprocess the contents for each round.
# After the preprocessing, distinct spreadsheets are created with the cleaned contents.
###############README###############

#Determine which of the sentence segmentation modules will be loaded based on filename
def determine_sentence_tokenizer(filename):
	if 'ENG_' in filename:
		sentence_splitter_suffix = 'english.pickle'
	if 'FRE_' in filename:
		sentence_splitter_suffix = 'french.pickle'
	if 'GER_' in filename:
		sentence_splitter_suffix = 'german.pickle'
	if 'CZE_' in filename:
		sentence_splitter_suffix = 'czech.pickle'
	if 'POR_' in filename:
		sentence_splitter_suffix = 'portuguese.pickle'
	if 'ITA_' in filename:
		sentence_splitter_suffix = 'italian.pickle'
	if 'RUS_' in filename:
		sentence_splitter_suffix = 'russian.pickle'
	if 'SPA_' in filename or 'CAT_' in filename:
		sentence_splitter_suffix = 'spanish.pickle'
	if 'DAN_' in filename:
		sentence_splitter_suffix = 'danish.pickle'
	if 'DUT_' in filename:
		sentence_splitter_suffix = 'dutch.pickle'
	if 'SLO_' in filename:
		sentence_splitter_suffix = 'slovene.pickle'
	if 'EST_' in filename:
		sentence_splitter_suffix = 'estonian.pickle'
	if 'FIN_' in filename:
		sentence_splitter_suffix = 'finnish.pickle'
	if 'GRE_' in filename:
		sentence_splitter_suffix = 'greek.pickle'
	if 'POL_' in filename:
		sentence_splitter_suffix = 'polish.pickle'
	if 'NOR_' in filename:
		sentence_splitter_suffix = 'norwegian.pickle'
	if 'SWE_' in filename:
		sentence_splitter_suffix = 'swedish.pickle'
	if 'TUR_' in filename:
		sentence_splitter_suffix = 'turkish.pickle'
	if 'HUN_' in filename:
		sentence_splitter_suffix = 'hungarian.pickle'

	return sentence_splitter_suffix

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

		analysed_item = row['Introduction text']
		if analysed_item != '.' and isinstance(analysed_item, str):
			analysed_item = remove_undesired_symbols(analysed_item)
			split_into_sentences = sentence_splitter.tokenize(analysed_item)
			for sentence in split_into_sentences:
				data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
				'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module, 
				'item_type': 'INTRODUCTION', 'item_value': None, 'text': sentence}
				cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

		analysed_item = row['Request for answer text']
		if analysed_item != '.' and isinstance(analysed_item, str):
			analysed_item = remove_undesired_symbols(analysed_item)
			split_into_sentences = sentence_splitter.tokenize(analysed_item)
			for sentence in split_into_sentences:
				data = {'Study': row['Study'], 'Language': row['Language'], 'Country': row['Country'], "q_name": row['Question name'], 
				'q_concept': row['Question concept'], 'item_name': row['Question admin'], 'module': module,
				'item_type': 'REQUEST', 'item_value': None, 'text': sentence}
				cleaned_df_round = cleaned_df_round.append(data, ignore_index = True)

		
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




def split_dataframes(file, df_supp, sentence_splitter):
	global currency
	if 'CZE_CZ' in file:
		currency = 'Kč'
	elif 'NOR' in file:
		currency = 'NOK'
	elif 'GER_DE' in file or 'GER_AT' in file or 'FRE' in file or 'POR' in file or 'SPA' in file or 'CAT' in file or 'ENG_IE' in file or 'RUS' in file:
		currency = '€'
	elif 'GER_CH' in file:
		currency = 'CHF'
	elif 'ENG_GB' in file:
		currency = '£'
	elif 'ENG_SOURCE' in file:
		currency = 'individual income'
	dict_year_round = {'1':'2002', '2':'2004', '3':'2006', '4':'2008', '5':'2010', '6':'2012', '7':'2014', '8':'2016', '9':'2018'}

	filename_without_extension = re.sub('.csv', '', file)

	unique_values_study = df_supp['Study'].unique()
	for value in unique_values_study:
		a_round = df_supp['Study'] == value
		df_round = df_supp[a_round]
		df_round_unique = df_round['Study'].unique()
		df_round_unique = ''.join(df_round_unique)
		round_number =  [int(s) for s in df_round_unique.split() if s.isdigit()]
		round_number = str(round_number[0])
		cleaned_df_round = clean_dataframe_by_round(df_round, sentence_splitter)
		cleaned_df_round.to_csv('ESS_R0'+round_number+'_'+dict_year_round[round_number]+'_SUPP_'+filename_without_extension+'.csv', encoding='utf-8', index=False)

def main():
	path = os.getcwd()
	files = os.listdir(path)

	for index, file in enumerate(files):
		if file.endswith(".csv") and 'SUPP' not in file:
			print(file)
			#Punkt Sentence Tokenizer from NLTK	
			sentence_splitter_prefix = 'tokenizers/punkt/'
			sentence_splitter_suffix = determine_sentence_tokenizer(file)
			sentence_splitter_name = sentence_splitter_prefix+sentence_splitter_suffix
			sentence_splitter = nltk.data.load(sentence_splitter_name)
			df_supp = pd.read_csv(file)
			split_dataframes(file, df_supp, sentence_splitter)
		



if __name__ == "__main__":
	main()