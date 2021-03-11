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


def get_response_text_and_id_per_language(language):
	session = session_factory()

	result = session.execute("select r.responseid, r.text from response r, survey_item s where s.country_language ilike '"+language+"%' and r.responseid =  s.responseid")
	
	session.close()

	result_dictionary = dict()
	for i in result:
		responseid = i[0] 
		text = i[1]  
		result_dictionary[responseid] = text

	return result_dictionary

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


