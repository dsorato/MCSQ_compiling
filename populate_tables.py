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




