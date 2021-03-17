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
	session = session_factory()

	tagged_text_dict = dict()
	result = session.execute("select survey_itemid, pos_tagged_text from survey_item;")

	for i in result:
		if i[0] is not None:
			survey_itemid = i[0]
			tagged_text_dict[survey_itemid] = i[1]


	session.close()

	return tagged_text_dict

def get_ids_from_alignment_table(survey_itemid):
	session = session_factory()
	
	result = session.execute("select "+survey_itemid+" from alignment")
	
	session.close()

	survey_itemid_list = []
	for i in result:
		if i[0] is not None:
			survey_itemid_list.append(i[0])

	return survey_itemid_list



def build_id_dicts_per_language(language):
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
	session = session_factory()
	if "'" in text:
		text = text.replace("'", "''")

	result = session.execute("select introductionid from introduction where text='"+text+"'")
	
	session.close()

	for i in result:
		return i[0]

def get_instruction_id(text):
	session = session_factory()
	if "'" in text:
		text = text.replace("'", "''")

	result = session.execute("select instructionid from instruction where text='"+text+"'")
	
	session.close()

	for i in result:
		return i[0]


def get_request_id(text):
	session = session_factory()
	if "'" in text:
		text = text.replace("'", "''")

	result = session.execute("select requestid from request where text='"+text+"'")
	
	session.close()

	for i in result:
		return i[0]

def get_response_id(text, item_value):
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


