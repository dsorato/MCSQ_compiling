import re
from itertools import groupby

def get_item_type(item_type_unique):
	item_types = []
	for item in item_type_unique:
		if type(item) is str:
			if len(item.split()) <= 2:
				item_types.append(item)

	return item_types

def get_module_name(module_unique):
	module_names = []
	for item in module_unique:
		if type(item) is str:
			name = re.findall("[A-Z] -", item)
			if name:
				module_names.append(item)

	return module_names

def get_module_enum(module_name, enum):
	module_name = module_name.strip()
	if module_name == "A - MEDIA USE":
		enum_number = enum.a
	elif module_name == "B - POLITICS":
		enum_number = enum.b
	elif module_name == "C - SUBJECTIVE WELLBEING":
		enum_number = enum.c
	elif module_name == "D - CLIMATE":
		enum_number = enum.d
	elif module_name == "E - WELFARE":
		enum_number = enum.e
	elif module_name == "F - SOCIO-DEMOGRAPHICS":
		enum_number = enum.f
	elif module_name == "H - HUMAN VALUES SCALE":
		enum_number = enum.h
	elif module_name == "I - TEST QUESTIONS":
		enum_number = enum.j
	else:
		enum_number = enum.no_module

	return enum_number


def get_code(a):
	first = a.split('_')[0]
	second = a.split('_')[1]

	return first+'_'+second

def group_by_prefix(translations_list):
	groups = [list(i) for j, i in groupby(translations_list, lambda a: get_code(a))]

	return groups

def get_id_column_name(columns):
	column_id = ''
	for c in columns:
		if 'id' in c.lower() and c != 'doc_id':
			column_id = c
	
	return column_id