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


