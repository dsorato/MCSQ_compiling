import sys
from populate_tables import *
from retrieve_from_tables import *


def main():	
	# source_survey_itemid_list = get_ids_from_alignment_table('source_survey_itemid')
	# source_tagged_text_dict = get_tagged_text_from_survey_item_table()
	# tag_alignment_table(source_tagged_text_dict, source_survey_itemid_list, 'source_pos_tagged_text', 'source_survey_itemid')

	languages  = ['POR', 'NOR', 'SPA', 'CAT', 'GER', 'CZE', 'FRE', 'ENG', 'RUS']

	for l in languages:
		print(l)
		target_survey_itemid_list =  get_ids_from_alignment_table_per_language(l)
		target_tagged_text_dict = create_tagged_text_dict(target_survey_itemid_list)
		tag_target_alignment_table(target_tagged_text_dict)

	
	
	

if __name__ == "__main__":
	main()