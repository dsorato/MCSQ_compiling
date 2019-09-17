from survey import *
from module import *
from itemtype import *
from document import *
from documentitem import *
from base import *

def get_document_item_id():
	documentitemid = 0
	session = session_factory()
	result = session.execute('SELECT last_value FROM document_item_id_seq;')
	for i in result:
		documentitemid = i[0]
	session.close()
	
	return documentitemid

def find_additional_item_types(evs_item_types):
	itemtypes_in_table = []
	session = session_factory()
	results = session.query(ItemType).all()
	for item in results:
		itemtypes_in_table.append(item.itemtype) 

	new_types = set(evs_item_types) - set(itemtypes_in_table)
	session.close()

	return new_types