from survey import *
from module import *
from itemtype import *
from itemname import *
from document import *
from documentitem import *
from base import *
from sqlalchemy import MetaData

def get_document_item_id():
	documentitemid = 0
	session = session_factory()
	result = session.execute('SELECT last_value FROM document_item_id_seq;')
	for i in result:
		documentitemid = i[0]
	session.close()
	
	return documentitemid


def get_item_name_as_dict():
	dict_item_name = {}
	session = session_factory()
	results = session.query(ItemName).all()
	for item in results:
		dict_item_name[item.itemname] = item.itemnameid
	
	return dict_item_name



def find_additional_item_types(candidate_item_types):
	itemtypes_in_table = []
	session = session_factory()
	results = session.query(ItemType).all()
	for item in results:
		itemtypes_in_table.append(item.itemtype) 

	new_types = set(candidate_item_types) - set(itemtypes_in_table)
	session.close()

	return new_types


def find_additional_item_names(candidate_item_names):
	itemnames_in_table = []
	session = session_factory()
	m = Base.metadata
	tables = m.tables.keys()
	if 'itemname' in tables:
	#if 'itemname' in tables and session.query(ItemName.itemname) is not None:
		results = session.query(ItemName).all()
		for item in results:
			itemnames_in_table.append(item.itemname) 
	new_names = set(candidate_item_names) - set(itemnames_in_table)
	session.close()

	return new_names