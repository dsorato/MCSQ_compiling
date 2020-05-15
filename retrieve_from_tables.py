from DB.base import *
from DB.survey import *
from DB.survey_item import *
from DB.module import *
from DB.introduction import *
from DB.instruction import *
from DB.response import *
from DB.request import *
from sqlalchemy import MetaData

def retrieve_survey_last_record():
	session = session_factory()
	last_survey_id = session.query(Survey).order_by(Survey.surveyid.desc()).first()
	session.close()

	return last_survey_id.surveyid

def retrieve_module_id(name, description):
	session = session_factory()
	moduleid = session.query(Module.moduleid).filter_by(module_name=name,module_description=description)
	session.close()

	return moduleid

def retrieve_module_table_as_dict():
	module_dict = dict()
	session = session_factory()
	for m in session.query(Module).all():
		module_dict[m.module_name] = m.moduleid
	
	return module_dict

def retrieve_survey_item_last_record():
	session = session_factory()
	last_survey_item_id = session.query(Survey_item).order_by(Survey_item.survey_unique_itemid.desc()).first()
	session.close()

	return last_survey_item_id.survey_unique_itemid

def retrieve_request_id(text):
	session = session_factory()
	requestid = session.query(Request.requestid).filter_by(text=text)
	session.close()

	return requestid

def retrieve_instruction_id(text):
	session = session_factory()
	instructionid = session.query(Instruction.instructionid).filter_by(text=text)
	session.close()

	return instructionid

def retrieve_introduction_id(text):
	session = session_factory()
	introductionid = session.query(Introduction.introductionid).filter_by(text=text)
	session.close()

	return introductionid

# def get_document_item_id():
# 	documentitemid = 0
# 	session = session_factory()
# 	result = session.execute('SELECT last_value FROM document_item_id_seq;')
# 	for i in result:
# 		documentitemid = i[0]
# 	session.close()
	
# 	return documentitemid


