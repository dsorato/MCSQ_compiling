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

def write_request_table(survey_itemid, final_text, translation_1, translation_2, review, adjudication, item_name, item_type):
	session = session_factory()
	item = Request(survey_itemid, final_text, translation_1, translation_2, review, adjudication, item_name, item_type)
	session.add(item)
	session.commit()

def write_response_table(survey_itemid, final_text, translation_1, translation_2, review, adjudication, item_name, item_type, item_value):
	session = session_factory()
	item = Response(survey_itemid, final_text, translation_1, translation_2, review, adjudication, item_name, item_type, item_value)
	session.add(item)
	session.commit()

def write_introduction_table(survey_itemid, final_text, translation_1, translation_2, review, adjudication, item_name, item_type):
	session = session_factory()
	item = Introduction(survey_itemid, final_text, translation_1, translation_2, review, adjudication, item_name, item_type)
	session.add(item)
	session.commit()
	session.close()

def write_instruction_table(survey_itemid, final_text, translation_1, translation_2, review, adjudication, item_name, item_type):
	session = session_factory()
	item = Instruction(survey_itemid, final_text, translation_1, translation_2, review, adjudication, item_name, item_type)
	session.add(item)
	session.commit()
	session.close()





# def write_itemtype_table(type_names):
# 	session = session_factory()
# 	for a_type in type_names:
# 		item = ItemType(a_type, False)
# 		session.add(item)
# 		session.commit()

# 	session.close()


# def update_itemtype_table():
# 	session = session_factory()
# 	session.execute(update(ItemType, values={ItemType.itemtypeisresponse:True}).where(ItemType.itemtype.ilike('response%')))
# 	session.commit()
# 	session.close()

# def write_document_table(parameters):
# 	session = session_factory()
# 	item = Document(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6])
# 	session.add(item)
# 	session.commit()

# 	session.close()

# def write_document_item_table(parameters):
# 	session = session_factory()
# 	item = DocumentItem(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6], 
# 		parameters[7],parameters[8],parameters[9], parameters[10])
# 	session.add(item)
# 	session.commit()

# 	session.close()

# def write_item_name_table(itemnames):
# 	session = session_factory()
# 	for item in itemnames:
# 		item = ItemName(item)
# 		session.add(item)
# 		session.commit()

# 	session.close()



