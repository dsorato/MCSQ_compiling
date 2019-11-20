from DB.base import *
from DB.survey import *
from DB.module import *



def write_survey_table(surveyid, study, wave_round, year, country_language):
	session = session_factory()
	item = Survey(surveyid, study, wave_round, year, country_language)
	session.add(item)
	session.commit()
	session.close()

def get_survey_last_record():
	session = session_factory()
	last_survey_id = session.query(Survey).order_by(Survey.surveyid.desc()).first()
	session.close()

	return last_survey_id


def write_module_table(module_names):
	session = session_factory()
	for module in module_names:
		exists = session.query(Module.module_name).filter_by(module_name=module).scalar() is not None
		if exists == False:
			item = Module(module)
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



