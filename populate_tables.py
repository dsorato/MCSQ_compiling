from survey import *
from module import *
from itemtype import *
from base import *

def write_survey_table():
	session = session_factory()
	ess_r8 = Survey("ESS", 8, 2016, 'unknown')
	session.add(ess_r8)
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
