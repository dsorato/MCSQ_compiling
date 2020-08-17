"""
Python3 script (work in progress) to extract data from XML SHARE input files
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 

import xml.etree.ElementTree as ET
import pandas as pd
import sys

def clean_answer_and_value(text):
	text = text.replace('<b>', '')
	text = text.replace('</b>', '')
	# text = text.replace('ex.', '')
	
	text = text.rstrip()

	text_and_value = text.split('.', 1)

	if text_and_value[0] != '':
		value = text_and_value[0]
		text = text_and_value[1].rstrip()
	else:
		value = None
		text = None


	return value, text


def main(filename):
	file = str(filename)
	tree = ET.parse(file)
	root = tree.getroot()

	parent_map = dict((c, p) for p in tree.getiterator() for c in p)
	share_metadefinitions = root.findall('.//MetaDefinitionCollection/MetaDefinition')

	df_answers = pd.DataFrame(columns=['response_table_name', 'category_value', 'categories'])

	dict_name_and_answer = dict()

	for node in share_metadefinitions:
		name = node.attrib['Name']
		for subnode in node.getiterator():
			if subnode.tag == 'RoleTexts':
				if subnode.attrib['Role'] == 'Category':
					text = subnode.find('Text')
					exp = text.find('Expression')
					if 'Text' in exp.attrib:
						value, text = clean_answer_and_value(exp.attrib['Text'])
						if text != None:
							data = {'response_table_name': name, 'category_value':value, 'categories': text}
							df_answers = df_answers.append(data, ignore_index = True)
							# print(exp.attrib['Text'])
		if node.attrib['DefinitionStructure'] == 'Block':
			if 'Section_' in node.attrib['Name']:
				for subnode in node.getiterator():
					if subnode.tag == 'Expression' and 'Text' in subnode.attrib:
						subnode_parent = parent_map[subnode]
						parent_of_parent = parent_map[subnode_parent]
						if 'Role' in parent_of_parent.attrib and parent_of_parent.attrib['Role'] != 'Category':
							print(subnode.tag, subnode.attrib)
						# for subsubnode in subnode.getiterator():
						# 	if subsubnode.tag == 'Text':


					

				# if subnode.attrib['Role'] == 'Question':
				# 	print(subnode.tag, subnode.attrib)
				# 	p = parent_map[subnode]
				# 	print(p.tag, p.attrib)
				# 	text = subnode.find('Text')
				# 	exp = text.find('Expression')
				# 	print(exp.attrib['Text'])



	# df_answers.to_csv('share_answers_por_pt.csv', encoding='utf-8', index=False)



if __name__ == "__main__":
	#Call script using filename. 
	filename = str(sys.argv[1])
	print("Executing data extraction script for SHARE wave 8 (xml files)")
	main(filename)
