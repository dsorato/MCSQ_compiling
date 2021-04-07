"""
Python3 script for ESS dataset inclusion in the MCSQ database
Before running the script, install requirements: pandas, numpy, SQLAlchemy, psycopg2
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 
from DB.alignment import *
from DB.base import *
from DB.survey import *
from DB.survey_item import *
from DB.module import *
from DB.introduction import *
from DB.instruction import *
from DB.response import *
from DB.request import *

def tag_target_alignment_table(dictionary):
	"""
	Inserts the POS alignment annotation on the target text column.
	
	Args:
		param1 dictionary (dictionary): a dictionary where the keys are the target_survey_itemids and the values are the pos tagged text segments.

	"""	
	session = session_factory()

	for k, v in list(dictionary.items()):
		if "'" in v:
			v = v.replace("'", "''")

		result = session.execute("update alignment set target_pos_tagged_text = '"+v+"' where target_survey_itemid ilike '"+k+"';")
		print(v)
		session.commit()	

	session.close()

def tag_alignment_table(dictionary, id_list, column_name, source_or_target_id):
	"""
	Inserts the POS alignment annotation either on the target or the source text column.
	
	Args:

		param1 dictionary (dictionary): a dictionary where the keys are the survey_itemids and the values are the pos tagged text segments.
		param2 id_list (list of strings): list of the IDs that refers to the text to be annotated. 
		param3 column_name (string): defines if the column to be tagged is the source or the target
		param4 source_or_target_id (string): name of the ID (either target_survey_itemid or source_survey_itemid)

	"""	
	session = session_factory()

	for item in id_list:

		pos_tagged_text = dictionary[item]

		if "'" in pos_tagged_text:
			pos_tagged_text = pos_tagged_text.replace("'", "''")

		print(pos_tagged_text)
		result = session.execute("update alignment set "+column_name+" = '"+pos_tagged_text+"' where "+source_or_target_id+" ilike '"+item+"';")
		session.commit()	

	session.close()


def tag_item_type_table(dictionary, table_name, table_id_name):
	"""
	Inserts the POS alignment annotation in item type specific table.
	
	Args:

		param1 dictionary (dictionary): a dictionary where the keys are the survey_itemids and the values are the pos tagged text segments.
		param2 table_name (string): name of the table to be tagged (introduction, instruction, request or response).
		param3 table_id_name (string): name of the ID of the table.

	"""	
	session = session_factory()

	for k, v in list(dictionary.items()):

		if "'" in v:
			v = v.replace("'", "''")

		result = session.execute("update "+table_name+" set pos_tagged_text = '"+v+"' where "+table_id_name+"="+str(k)+";")
		session.commit()	

	session.close()


def tag_survey_item(dictionary, table_id_name):
	"""
	Inserts the POS alignment annotation in survey_item table.
	
	Args:

		param1 dictionary (dictionary): an item type specific dictionary where the keys are the IDs and the values are the pos tagged text segments.
		param2 table_id_name (string): name of the ID of item type specific the table.

	"""	
	session = session_factory()
	for k, v in list(dictionary.items()):

		if "'" in v:
			v = v.replace("'", "''")

		result = session.execute("update survey_item set pos_tagged_text = '"+v+"' where "+table_id_name+"="+str(k)+";")
		session.commit()

	session.close()



def write_module_table(modules):
	session = session_factory()
	for module in modules:
		exists = session.query(Module.module_name).filter_by(module_name=module).scalar() is not None
		if exists == False:
			item = Module(module)
			session.add(item)
			session.commit()

	session.close()

def write_survey_table(surveys):
	session = session_factory()
	for survey in surveys:
		surveyid = survey[0]
		study  = survey[1]
		wave_round  = survey[2]
		year  = survey[3]
		country_language  = survey[4]
		exists = session.query(Survey.surveyid).filter_by(surveyid=surveyid).scalar() is not None
		if exists == False:
			item = Survey(surveyid, study, wave_round, year, country_language)
			session.add(item)
			session.commit()
			session.close()

def write_introduction_table(introduction):
	session = session_factory()
	item = Introduction(introduction)
	session.add(item)
	session.commit()
	session.close()

def write_instruction_table(instruction):
	session = session_factory()
	item = Instruction(instruction)
	session.add(item)
	session.commit()
	session.close()


def write_request_table(request):
	session = session_factory()
	item = Request(request)
	session.add(item)
	session.commit()
	session.close()


def write_response_table(text, item_value):
	session = session_factory()
	item = Response(text, item_value)
	session.add(item)
	session.commit()
	session.close()



def write_alignment_table(source_text, target_text, source_survey_itemid,target_survey_itemid):
	session = session_factory()
	item = Alignment(source_text, target_text, source_survey_itemid,target_survey_itemid)
	session.add(item)
	session.commit()
	session.close()


def write_survey_item_table(survey_itemid, surveyid, text, item_value, moduleid, requestid, responseid, instructionid, introductionid, country_language, item_is_source, item_name, item_type):
	session = session_factory()
	item = Survey_item(survey_itemid, surveyid, text, item_value, moduleid, requestid, responseid, instructionid, introductionid, country_language, item_is_source, item_name, item_type)
	session.add(item)
	session.commit()
	session.close()




