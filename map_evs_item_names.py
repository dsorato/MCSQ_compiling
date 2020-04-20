import xml.etree.ElementTree as ET
import sys
import re
import string


def main(filename_xlsx,filename_xml):
	# parse an xml file by name
	file = str(filename_xml)
	tree = ET.parse(file)
	root = tree.getroot()

	parent_map = dict((c, p) for p in tree.getiterator() for c in p)
	evs_vars = root.findall('.//dataDscr/var')

	for var in evs_vars:
		for node in var.getiterator():
			qstn = var.find('qstn')
			item_name = ''
			if node.tag=='txt' and 'level' in node.attrib:
				item_name = node.attrib['level']

			elif qstn is not None and 'seqNo' in qstn.attrib and 'level' not in node.attrib:
				item_name = qstn.attrib['seqNo'] 

			if item_name != '':
				print(var.attrib['name'], item_name)





if __name__ == "__main__":
	#Call script using filename. 
	filename_xlsx = str(sys.argv[1])
	filename_xml = str(sys.argv[2])
	main(filename_xlsx,filename_xml)
