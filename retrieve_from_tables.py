"""
Python3 script for retrieving data from MCSQ database
Before running the script, install requirements: pandas, numpy, SQLAlchemy, psycopg2
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 

from DB.base import *
from DB.survey import *
from DB.survey_item import *
from DB.module import *
from DB.introduction import *
from DB.instruction import *
from DB.response import *
from DB.request import *
from sqlalchemy import MetaData
import pandas as pd
from sqlalchemy.sql import select


def get_tagged_text_from_survey_item_table():
	"""
	Gets the survey_itemid and the POS tagged text from the survey_item table and creates a dictionary.

	Returns: 
		A dictionary with survey_itemids as keys and POS tagged text as values.
	"""	
	session = session_factory()

	tagged_text_dict = dict()
	result = session.execute("select survey_itemid, pos_tagged_text from survey_item;")

	for i in result:
		if i[0] is not None:
			survey_itemid = i[0]
			tagged_text_dict[survey_itemid] = i[1]


	session.close()

	return tagged_text_dict

def create_tagged_text_dict(id_list):
	"""
	Gets the survey_itemid and the POS tagged text from the survey_item table and creates a dictionary.
	
	Args:
		param1 id_list (list of strings): a language specific list of the target segment IDs in the alignment table. 

	Returns: 
		A dictionary with target survey_itemids as keys and POS tagged text as values.
	"""	
	session = session_factory()

	tagged_text_dict = dict()
	result = session.execute("select survey_itemid, pos_tagged_text from survey_item;")

	for i in result:
		if i[0] is not None and i[0] in id_list:
			survey_itemid = i[0]
			tagged_text_dict[survey_itemid] = i[1]


	session.close()

	return tagged_text_dict

def get_ids_from_alignment_table(survey_itemid):
	"""
	Gets all IDs (either source or target) from the alignment table.
	
	Args:
		param1 survey_itemid (string): name of the column indicating if the desired IDs to be retrived are from source or from target.
		
	Returns: 
		A list of survey_itemids.
	"""	
	session = session_factory()
	
	result = session.execute("select "+survey_itemid+" from alignment")
	
	session.close()

	survey_itemid_list = []
	for i in result:
		if i[0] is not None:
			if i[0] not in survey_itemid_list:
				survey_itemid_list.append(i[0])

	return survey_itemid_list

def get_ids_from_alignment_table_per_language(language):
	"""
	Gets all target IDs from the alignment table based on the language.
	
	Args:
		param1 language (string): target language.
		
	Returns: 
		A list of all target_survey_itemids in the alignment table.
	"""	
	session = session_factory()
	
	result = session.execute("select target_survey_itemid from alignment where target_survey_itemid ilike '%"+language+"%' and target_pos_tagged_text is null")
	
	session.close()

	survey_itemid_list = []
	for i in result:
		if i[0] is not None:
			if i[0] not in survey_itemid_list:
				survey_itemid_list.append(i[0])

	return survey_itemid_list



def build_id_dicts_per_language(language):
	"""
	Gets all text segments and their IDs and builds a dictionary by item type.
	
	Args:
		param1 language (string): target language.
		
	Returns: 
		Four different dictionaries (one for each item type). The IDs are the keys and the text segments are the values.
	"""	
	session = session_factory()

	result = session.execute("select requestid, responseid, instructionid, introductionid, text from survey_item where country_language ilike '"+language+"%'")
	
	session.close()
	request = dict()
	response = dict()
	instruction = dict()
	introduction = dict()

	for i in result:
		requestid = i[0]  
		responseid = i[1] 
		instructionid = i[2] 
		introductionid = i[3] 
		text = i[4] 


		if requestid is not None and isinstance(requestid, int):
			request[requestid] = text
		elif responseid is not None and isinstance(responseid, int):
			response[responseid] = text
		elif instructionid is not None and isinstance(instructionid, int):
			instruction[instructionid] = text
		elif introductionid is not None and isinstance(introductionid, int):
			introduction[introductionid] = text

	return request, response, instruction, introduction

def get_introduction_id(text):
	"""
	Gets an introduction segment ID based on its text.
	
	Args:
		param1 text (string): the introduction segment text.
		
	Returns: 
		introduction segment ID (int).
	"""	
	session = session_factory()
	if "'" in text:
		text = text.replace("'", "''")

	result = session.execute("select introductionid from introduction where text='"+text+"'")
	
	session.close()

	for i in result:
		return i[0]

def get_instruction_id(text):
	"""
	Gets an instruction segment ID based on its text.
	
	Args:
		param1 text (string): the instruction segment text.
		
	Returns: 
		instruction segment ID (int).
	"""	
	session = session_factory()
	if "'" in text:
		text = text.replace("'", "''")

	result = session.execute("select instructionid from instruction where text='"+text+"'")
	
	session.close()

	for i in result:
		return i[0]


def get_request_id(text):
	"""
	Gets an request segment ID based on its text.
	
	Args:
		param1 text (string): the request segment text.
		
	Returns: 
		request segment ID (int).
	"""	
	session = session_factory()
	if "'" in text:
		text = text.replace("'", "''")

	result = session.execute("select requestid from request where text='"+text+"'")
	
	session.close()

	for i in result:
		return i[0]

def get_response_id(text, item_value):
	"""
	Gets an response segment ID based on its text.
	
	Args:
		param1 text (string): the response segment text.
		
	Returns: 
		response segment ID (int).
	"""	
	session = session_factory()
	if "'" in text:
		text = text.replace("'", "''")

	if isinstance(item_value, str):
		result = session.execute("select responseid from response where text='"+text+"' and item_value='"+item_value+"'")
	else:
		result = session.execute("select responseid from response where text='"+text+"' and item_value is null")
	
	session.close()

	for i in result:
		return i[0]

def get_module_id(module_name):
	"""
	Gets an module ID based on its name.
	
	Args:
		param1 module_name (string): the name of the module.
		
	Returns: 
		response module ID (int).
	"""	
	session = session_factory()
	if "'" in module_name:
		module_name = module_name.replace("'", "''")

	result = session.execute("select moduleid from module where module_name='"+module_name+"'")
	
	session.close()

	for i in result:
		return i[0]

def get_survey_id(surveyid):
	session = session_factory()
	if "'" in surveyid:
		surveyid = surveyid.replace("'", "''")

	result = session.execute("select surveyid from survey where surveyid='"+surveyid+"'")
	
	session.close()

	for i in result:
		return i[0]


