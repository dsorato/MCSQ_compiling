import xml.etree.ElementTree as ET
import sys
import re
import string
import pandas as pd

def standartize_item_name(item_name):
	item_name = re.sub("\.", "", item_name)
	item_name = item_name.lower()
	item_name = re.sub("^q", "Q", item_name)
	item_name = re.sub("^f", "Q", item_name)
	# item_name = re.sub(")", "", item_name)

	if '_'  in item_name:
		item_name = item_name.split('_')
		item_name = item_name[0]+item_name[1].lower()

	if item_name[0].isdigit() or len(item_name)==1:
		item_name = 'Q'+item_name

	return item_name


def main(filename_xlsx,filename_xml):
	# parse an xml file by name
	file = str(filename_xml)
	tree = ET.parse(file)
	root = tree.getroot()

	xlsx_file = pd.read_excel(filename_xlsx)
	xlsx_file['v_item'] = xlsx_file['v_item'].str.lower()
	print(xlsx_file)
	items_xlsx = xlsx_file['v_item']

	parent_map = dict((c, p) for p in tree.getiterator() for c in p)
	evs_vars = root.findall('.//dataDscr/var')

	item_list = []

	for var in evs_vars:
		for node in var.getiterator():
			qstn = var.find('qstn')
			item_name = ''
			if node.tag=='txt' and 'level' in node.attrib:
				item_name = node.attrib['level']

			elif qstn is not None and 'seqNo' in qstn.attrib and 'level' not in node.attrib:
				item_name = qstn.attrib['seqNo'] 

			if item_name != '':
				item = [var.attrib['name'].lower(), item_name]
				if item not in item_list:
					item_list.append(item)

	print(item_list)

	df_evs_sample = pd.DataFrame(columns=['v_item', 'q_item'])
	for item_x in items_xlsx:
		for item_y in item_list:
			if item_x == item_y[0]:
				print(item_x, item_y[0], item_y[1].replace('.', ''))
				data = {'v_item':item_y[0], 'q_item': standartize_item_name(item_y[1])}
				df_evs_sample = df_evs_sample.append(data, ignore_index=True)

	df_evs_sample= df_evs_sample.drop_duplicates(subset='v_item', keep="last")
	result = pd.merge(df_evs_sample, xlsx_file, on='v_item')
	result.to_csv('evs_data/df_evs_sample_w4.csv', encoding='utf-8', index=False)






if __name__ == "__main__":
	#Call script using filename. 
	filename_xlsx = str(sys.argv[1])
	filename_xml = str(sys.argv[2])
	main(filename_xlsx,filename_xml)
