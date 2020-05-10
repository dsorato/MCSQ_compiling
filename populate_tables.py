from DB.base import *
from DB.survey import *
from DB.survey_item import *
from DB.module import *
from DB.introduction import *
from DB.instruction import *
from DB.response import *
from DB.request import *


def write_survey_table(surveyid, study, wave_round, year, country_language):
	session = session_factory()
	item = Survey(surveyid, study, wave_round, year, country_language)
	session.add(item)
	session.commit()
	session.close()

def write_module_table(module_dict):
	session = session_factory()
	for k, v in list(module_dict.items()):
		exists = session.query(Module.module_name, Module.module_description).filter_by(module_name=k, module_description=v).scalar() is not None
		if exists == False:
			item = Module(k, v)
			session.add(item)
			session.commit()

	session.close()

def write_survey_item_table(survey_itemid, surveyid, moduleid, country_language, item_is_source, item_name, item_type):
	session = session_factory()
	item = Survey_item(survey_itemid, surveyid, moduleid, country_language, item_is_source, item_name, item_type)
	session.add(item)
	session.commit()
	session.close()

def get_survey_last_record():
	session = session_factory()
	last_survey_id = session.query(Survey).order_by(Survey.surveyid.desc()).first()
	session.close()

	return last_survey_id.surveyid


def get_module_table_as_dict():
	module_dict = dict()
	session = session_factory()
	for m in session.query(Module).all():
		module_dict[m.module_name] = m.moduleid
	
	return module_dict

def get_survey_item_last_record():
	session = session_factory()
	last_survey_item_id = session.query(Survey_item).order_by(Survey_item.survey_unique_itemid.desc()).first()
	session.close()

	return last_survey_item_id.survey_unique_itemid

def get_request_id(text):
	session = session_factory()
	request = session.query(Request).filter_by(text=text)
	session.close()

	return request.requestid

def write_request_table(unique_requests):
	session = session_factory()
	for request in unique_requests:
		exists = session.query(Request.text).filter_by(text=request).scalar() is not None
		if exists == False:
			item = Request(request)
			session.add(item)
			session.commit()

	session.close()

def write_introduction_table(unique_introductions):
	session = session_factory()
	for introduction in unique_introductions:
		exists = session.query(Introduction.text).filter_by(text=introduction).scalar() is not None
		if exists == False:
			item = Introduction(introduction)
			session.add(item)
			session.commit()

	session.close()

def write_instruction_table(unique_instructions):
	session = session_factory()
	for instruction in unique_instructions:
		exists = session.query(Instruction.text).filter_by(text=instruction).scalar() is not None
		if exists == False:
			item = Instruction(instruction)
			session.add(item)
			session.commit()

	session.close()



def write_response_table(response_id, text, item_value):
	session = session_factory()
	item = Response(response_id, text, item_value)
	session.add(item)
	session.commit()



