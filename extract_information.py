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
	if module_name == "A - MEDIA USE" or module_name == 'A':
		enum_number = enum.a
	elif module_name == "B - POLITICS" or module_name == 'B':
		enum_number = enum.b
	elif module_name == "C - SUBJECTIVE WELLBEING" or module_name == 'C':
		enum_number = enum.c
	elif module_name == "D - CLIMATE" or module_name == 'D':
		enum_number = enum.d
	elif module_name == "E - WELFARE" or module_name == 'E':
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


def get_item_type_enum(item_type_name, enum):
	if type(item_type_name) is str:
		item_type_name = item_type_name.strip()
		if item_type_name == "Fill":
			enum_number = enum.fill
		elif item_type_name == "Question":
			enum_number = enum.question
		elif item_type_name == "QInstruction":
			enum_number = enum.qinstruction
		elif item_type_name == "QText":
			enum_number = enum.qtext
		elif item_type_name == "TranslatorNote":
			enum_number = enum.translatornote
		elif item_type_name == "Response":
			enum_number = enum.response
		elif item_type_name == "Response option":
			enum_number = enum.responseoption
		elif item_type_name == "IWER":
			enum_number = enum.iwer
		elif item_type_name == "Header":
			enum_number = enum.header
		elif item_type_name == "QCodingInstruction":
			enum_number = enum.qcodinginstruction
		else:
			enum_number = enum.notype
	else:
		enum_number = enum.notype

	return enum_number


def get_code(a):
	if 'CentERdatanese'.lower() in a.lower():
		return 'CentERdatanese'
	else:
		first = a.split('_')[0]
		second = a.split('_')[1]

	return first+'_'+second

def group_by_prefix(translations_list):
	groups = [list(i) for j, i in groupby(translations_list, lambda a: get_code(a))]

	return groups

def get_id_column_name(columns):
	column_id = ''
	for c in columns:
		if 'id' in c.lower() and c != 'doc_id' and c != 'generic description id':
			column_id = c
	
	return column_id


def get_generic_module_name(module_names):
	new_names = []
	for module in module_names:
		name = module.split('-')
		name[0] = name[0].strip()
		if len(name) == 3:
			aux = [name[1], name[2]]
			name[1] = ' '.join(aux)
			name[1].strip()
			name.remove(name[2])
		if len(name) == 2:
			name[1] = name[1].strip()
		new_names.append(name[0])

	return new_names