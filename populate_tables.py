from survey import *
from module import *
from itemtype import *
from itemname import *
from document import *
from documentitem import *
from base import *

def write_survey_table(survey, waveround, year):
	session = session_factory()
	item = Survey(survey, waveround, year)
	session.add(item)
	session.commit()
	session.close()


def write_module_table(module_names):
	session = session_factory()
	for module in module_names:
		item = Module(module)
		session.add(item)
		session.commit()

	session.close()


def write_itemtype_table(type_names):
	session = session_factory()
	for a_type in type_names:
		item = ItemType(a_type, False)
		session.add(item)
		session.commit()

	session.close()


def update_itemtype_table():
	session = session_factory()
	session.execute(update(ItemType, values={ItemType.itemtypeisresponse:True}).where(ItemType.itemtype.ilike('response%')))
	session.commit()
	session.close()

def write_document_table(parameters):
	session = session_factory()
	item = Document(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6])
	session.add(item)
	session.commit()

	session.close()

def write_document_item_table(parameters):
	session = session_factory()
	item = DocumentItem(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6], 
		parameters[7],parameters[8],parameters[9], parameters[10])
	session.add(item)
	session.commit()

	session.close()

def write_item_name_table(itemnames):
	session = session_factory()
	for item in itemnames:
		item = ItemName(item)
		session.add(item)
		session.commit()

	session.close()



