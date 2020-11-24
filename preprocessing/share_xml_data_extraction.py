"""
Python3 script (work in progress) to extract data from XML SHARE input files
Author: Danielly Sorato 
Author contact: danielly.sorato@gmail.com
""" 

import xml.etree.ElementTree as ET
import pandas as pd
import sys

ignore_elements = ['SampID', 'index', 'BPreload', 'B_SocialNetworkMember', 'B_Child', 'RespID']

"""
Clean answer text and attribute a value to answer category

:param text: text to be cleaned
:returns: cleaned answer text, along with its value
"""
def clean_answer_and_value(text):
	text = text.replace('<b>', '')
	text = text.replace('</b>', '')
	text = text.replace('\n', ' ').replace('\r', '')
	
	text = text.rstrip()

	text_and_value = text.split('.', 1)

	if text_and_value[0] != '':
		value = text_and_value[0]
		text = text_and_value[1].rstrip()
	else:
		value = None
		text = None


	return value, text


"""
Clean question text 
:param text: text to be cleaned
:returns: cleaned question text.
"""
def clean_question_text(text):
	text = text.replace('<b>', '')
	text = text.replace('</b>', '')
	text = text.replace('<br>', '')
	text = text.replace('<br />', '')
	text = text.replace('\n', ' ').replace('\r', '')
	
	text = text.rstrip()

	if text == '':
		text = None

	return text

"""
Extract answers text from XML node

:param name: name of the answer structure inside XML file
:param subnode: child node being analyzed in outer loop
:param df_answers: pandas dataframe containing answers extracted from XML file
:returns: answers dataframe, with new answer category retrieved (when appliable)
"""
def extract_answers(subnode, df_answers, name):
	for child in subnode.getiterator():
		if child.tag == 'answer_element':
			category_value = child.attrib['labelvalue']
			text_nodes = child.findall('text')
			for text_node in text_nodes:
				if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
					data = {'name': name, 'category_value':category_value, 'text': text_node.text}
					df_answers = df_answers.append(data, ignore_index = True)

	return df_answers


"""
Extract questions text from XML node

:param name: name of the answer structure inside XML file
:param subnode: child node being analyzed in outer loop
:param df_questions: pandas dataframe containing questions extracted from XML file
:returns: questions dataframe, with new question retrieved (when appliable)
"""
def extract_questions(subnode, df_questions, name):
	for child in subnode.getiterator():
		if child.tag == 'question_element' and 'type_name' in child.attrib:
			if child.attrib['type_name'] == 'QText':
				text_nodes = child.findall('text')
				for text_node in text_nodes:
					if text_node.attrib['translation_id'] != '1' and text_node.text is not None:
						data = {'name': name, 'text': text_node.text}
						df_questions = df_questions.append(data, ignore_index = True)

	return df_questions

def main(filename):
	"""
	Parse tree of input XML file.
	"""
	file = str(filename)
	tree = ET.parse(file)
	root = tree.getroot()

	"""
	Create a dictionary to map the information of node relations.
	"""
	parent_map = dict((c, p) for p in tree.getiterator() for c in p)

	questions = root.findall('.//questionnaire/questions')
	answers = root.findall('.//questionnaire/answers')

	df_answers = pd.DataFrame(columns=['name', 'category_value', 'text'])
	df_questions = pd.DataFrame(columns=['name', 'text'])

	dict_name_and_answer = dict()

	for node in questions:
		for subnode in node.getiterator():
			if subnode.tag == 'question':
				name = subnode.attrib['name']
				df_questions = extract_questions(subnode, df_questions, name)
					
	for node in answers:
		for subnode in node.getiterator():
			if subnode.tag == 'answer':
				name = subnode.attrib['name']
				df_answers = extract_answers(subnode, df_answers, name)				
							
	


	df_answers.to_csv('share_answers_por_pt.csv', encoding='utf-8', index=False)
	df_questions.to_csv('share_questions_por_pt.csv', encoding='utf-8', index=False)


"""
main method is executed for each file inside the given directory.
"""
if __name__ == "__main__":
	filename = str(sys.argv[1])
	print("Executing data extraction script for SHARE wave 8 (xml files)")
	main(filename)
