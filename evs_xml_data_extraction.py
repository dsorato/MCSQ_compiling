import xml.etree.ElementTree as ET



def main():
	# parse an xml file by name
	tree = ET.parse('data/evs_2008_fre_fr.xml')
	root = tree.getroot()

	labls = root.findall('.//dataDscr/var/labl')
	qstnLit = root.findall('.//dataDscr/var/qstn/qstnLit')
	evs_vars = root.findall('.//dataDscr/var')

	for var in evs_vars:
		for node in var.getiterator():
			if node.tag=='preQTxt':
				print(node.tag, node.attrib, node.text)
			if node.tag=='ivuInstr':
				print(node.tag, node.attrib, node.text)
			if node.tag=='qstnLit':
				print(node.tag, node.attrib, node.text)
			if node.tag=='catgry':
				for subnode in node.getiterator():
					if subnode.tag=='catValu':
						print('value', subnode.text)
					if subnode.tag=='txt':
						print('txt', subnode.text)
			# if node.tag=='txt':
			# 	print(node.tag, node.attrib, node.text)

		




if __name__ == "__main__":
	print("Executing data extraction script for EVS 2008 (xml files)")
	main()
