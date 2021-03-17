import sys
from populate_tables import *
from retrieve_from_tables import *


def main():	
	source_survey_itemid_list = get_ids_from_alignment_table('source_survey_itemid')
	source_tagged_text_dict = get_tagged_text_from_survey_item_table()
	tag_alignment_table(source_tagged_text_dict, source_survey_itemid_list, 'source_pos_tagged_text', 'source_survey_itemid')

	target_survey_itemid_list = get_ids_from_alignment_table('target_survey_itemid')
	target_tagged_text_dict = get_tagged_text_from_survey_item_table()
	tag_alignment_table(source_tagged_text_dict, target_survey_itemid_list, 'target_pos_tagged_text', 'target_survey_itemid')

if __name__ == "__main__":
	main()