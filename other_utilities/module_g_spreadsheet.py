"""
Python3 script for preprocessing raw module G ESS data to spreadsheet
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 

import pandas as pd
import csv
import re

initial_sufix = 0
item_name_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x']

def reset_item_name_sufix():
	global initial_sufix
	initial_sufix = 0


def update_item_name(prefix):
	global initial_sufix
	global item_name_list
	print(initial_sufix)
	item_name = prefix+item_name_list[initial_sufix]
	initial_sufix = initial_sufix + 1

	return item_name

def clean_item(item):
	item = item.replace('<BR>', '')
	item = item.rstrip()

	return item 

def append_df_answers(df_module_g_answers, df_module_g, item_name):
	for i, row in df_module_g_answers.iterrows():
		row['item_name'] = item_name
	
	df_module_g = df_module_g.append(df_module_g_answers, ignore_index = True)

	return df_module_g

def generate_spreadsheet(raw_items, study, language_country):
	df_module_g = pd.DataFrame(columns=['Study', 'Language', 'Country', 'q_name', 'q_concept', 'item_name',  'module', 'item_type', 'item_value', 'text'])

	language_country_split = language_country.split('_')
	language = language_country_split[0]
	country = language_country_split[1]
	for raw_item in raw_items:
		if '{MODULE}' in raw_item[0]:
			module = clean_item(raw_item[1])
			reset_item_name_sufix()

		if '{INSTRUCTION}' in raw_item[0]:
			for item in raw_item[1:]:
				item = clean_item(item)
				if item != '':
					data = {'Study': study, 'Language':language, 'Country':country, 'q_name':None, 'q_concept':None,'item_name':module, 
					'module':module, 'item_type': 'INSTRUCTION', 'item_value': None, 'text': item}
					df_module_g = df_module_g.append(data, ignore_index = True)
		if '{INTRODUCTION}' in raw_item[0]:
			for item in raw_item[1:]:
				item = clean_item(item)
				if item != '':
					data = {'Study': study, 'Language':language, 'Country':country, 'q_name':None, 'q_concept':None, 'item_name':module, 
					'module':module, 'item_type': 'INTRODUCTION', 'item_value': None, 'text': item}
					df_module_g = df_module_g.append(data, ignore_index = True)

		if '{ANSWERS}' in raw_item[0]:
			df_module_g_answers = pd.DataFrame(columns=['Study', 'Language', 'Country', 'q_name', 'q_concept', 'item_name',  'module', 'item_type', 'item_value', 'text'])
			for i, item in enumerate(raw_item[1:]):
				item = clean_item(item)
				if item != '':
					data = {'Study': study, 'Language':language, 'Country':country, 'q_name':None, 'q_concept':None, 'item_name':module, 
					'module':module, 'item_type': 'RESPONSE', 'item_value': i, 'text': item}
					df_module_g_answers = df_module_g_answers.append(data, ignore_index = True)

		if '{QUESTION}' in raw_item[0]:	
			for item in raw_item[1:]:
				item_without_letter = re.compile("^[A-Z]<BR>\s?", re.IGNORECASE).split(item)
				if item_without_letter != '':
					if len(item_without_letter) == 1:
						item = clean_item(item_without_letter[0])
					else:
						item = clean_item(item_without_letter[1])

					if item != '':
						if '.' in item:
							split_item = item.split('.')
							item_name = update_item_name(module)
							data = {'Study': study, 'Language':language, 'Country':country, 'q_name':None, 'q_concept':None,'item_name': item_name, 
							'module':module, 'item_type': 'REQUEST', 'item_value': None, 'text': item}
							df_module_g = df_module_g.append(data, ignore_index = True)
							for subitem in split_item[1:]:
								if subitem != '':
									data = {'Study': study, 'Language':language, 'Country':country, 'q_name':None, 'q_concept':None, 'item_name': item_name, 
									'module':module, 'item_type': 'REQUEST', 'item_value': None, 'text': subitem}
									df_module_g = df_module_g.append(data, ignore_index = True)

						else:
							item_name = update_item_name(module)
							data = {'Study': study, 'Language':language, 'Country':country, 'q_name':None, 'q_concept':None, 'item_name': item_name, 
							'module': module, 'item_type': 'REQUEST', 'item_value': None, 'text': item}
							df_module_g = df_module_g.append(data, ignore_index = True)
						df_module_g = append_df_answers(df_module_g_answers, df_module_g, item_name)
					

	return df_module_g

def split_raw_items_and_generate_spreadsheet(filename,language_country, study, raw_items):
	if 'FRE' in filename:
		dk = "Ne sait pas"
		refusal =  'Refus'
		dontapply = "Ne s'applique pas"
		write_down = "(Inscrivez)"

	df_module_g = pd.DataFrame(columns=['Study', 'Language', 'Country', 'q_name', 'q_concept', 'item_name',  'module', 'item_type', 'item_value', 'text'])

	language_country_split = language_country.split('_')
	language = language_country_split[0]
	country = language_country_split[1]

	for raw_item in raw_items:
		instruction = []
		introduction = []
		item_name = raw_item[0]
		print(item_name)

		index_response = raw_item.index('{ANSWERS}')+1
		index_request = raw_item.index('{QUESTION}')+1
		if '{INTRODUCTION}' in raw_item: 
			index_introduction = raw_item.index('{INTRODUCTION}')+1
			introduction = raw_item[index_introduction:index_request-1]
		
		request = raw_item[index_request:index_response-1]
		response = raw_item[index_response:]
		
		if '{INSTRUCTION}' in introduction:
			index_instruction = introduction.index('{INSTRUCTION}')+1
			instruction  = introduction[index_instruction:]
			introduction = introduction[:index_instruction-1]
			print(instruction)

		elif '{INSTRUCTION}' in request:
			index_instruction = request.index('{INSTRUCTION}')+1
			if index_instruction < index_request:
				instruction  = request[:index_request-1]
				request = request[index_request:]
			else:
				instruction  = request[index_instruction:]
				request = request[:index_instruction-1]
			print(instruction)

		if response == []:
			response.append(write_down)

		if introduction:
			for item in introduction:
				data = {'Study': study, 'Language':language, 'Country':country, 'q_name':None, 'q_concept':None, 'item_name': item_name, 
				'module': 'G', 'item_type': 'INTRODUCTION', 'item_value': None, 'text': item}
				df_module_g = df_module_g.append(data, ignore_index = True)
		if instruction:
			for item in instruction:
				data = {'Study': study, 'Language':language, 'Country':country, 'q_name':None, 'q_concept':None, 'item_name': item_name, 
				'module': 'G', 'item_type': 'INSTRUCTION', 'item_value': None, 'text': item}
				df_module_g = df_module_g.append(data, ignore_index = True)

		for item in request:
			data = {'Study': study, 'Language':language, 'Country':country, 'q_name':None, 'q_concept':None, 'item_name': item_name, 
			'module': 'G', 'item_type': 'REQUEST', 'item_value': None, 'text': item}
			df_module_g = df_module_g.append(data, ignore_index = True)

		for i, item in enumerate(response):
			if dk in item:
				item_value = 888
			elif refusal in item:
				item_value = 777
			elif dontapply in item:
				item_value = 999
			else:
				item_value = i

			data = {'Study': study, 'Language':language, 'Country':country, 'q_name':None, 'q_concept':None, 'item_name': item_name, 
			'module': 'G', 'item_type': 'RESPONSE', 'item_value': item_value, 'text': item}
			df_module_g = df_module_g.append(data, ignore_index = True)


	return df_module_g


def get_raw_items(lines, index_questions):
	raw_items = []
	for i, index in enumerate(index_questions):
		if index == index_questions[-1]:
				item = lines[index:]
		else:
			next_index_element = index_questions[i+1]
			item = lines[index:next_index_element]

		clean = []
		for i, it in enumerate(item):
			it = clean_item(it)
			if it != '':
				clean.append(it)

		raw_items.append(clean)

	return raw_items


def preprocess_r02_module_g(filename, lines, language_country, study):
	item_name_question_pattern = re.compile("(?:[A-Z][A-Z]?\s?[0-9]{1,3}[a-z]?)+")
	index_questions = []
	
	for i, line in enumerate(lines):
		if item_name_question_pattern.match(line):
			index_questions.append(i)
		
	
	raw_items = get_raw_items(lines, index_questions)
	df_module_g = split_raw_items_and_generate_spreadsheet(filename,language_country, study, raw_items)

	return df_module_g
		

def main(filename, language_country, study):
	tags = []
	with open(filename, 'r') as file:
		lines = file.readlines()
		last_line = len(lines) - 1

		if 'R02' in filename:
			df_module_g = preprocess_r02_module_g(filename,lines, language_country, study)

		else:
			index_tags = []
			for i, line in enumerate(lines):
				if '{MODULE}' in line:
					index_tags.append(i)

				if '{INSTRUCTION}' in line:
					index_tags.append(i)

				if '{INTRODUCTION}' in line:
					index_tags.append(i)

				if '{ANSWERS}' in line:
					index_tags.append(i)

				if '{QUESTION}' in line:
					index_tags.append(i)
			
	
			raw_items = []
			for i, index in enumerate(index_tags):
				if index == index_tags[-1]:
					item = lines[index:]
				else:
					next_index_element = index_tags[i+1]
					item = lines[index:next_index_element]
				raw_items.append(item)

			df_module_g = generate_spreadsheet(raw_items, study, language_country)

	file.close()

	

	return df_module_g


if __name__ == "__main__":
	#Call script using filename, language_country and study parameters. 
	filename = str(sys.argv[1])
	language_country = str(sys.argv[2])
	study = str(sys.argv[3])
	main(filename, language_country, study)