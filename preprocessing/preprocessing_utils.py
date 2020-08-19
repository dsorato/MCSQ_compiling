import re

"""
This function retrieves the country/language and study metadata based on the input filename.
:param filename: name of the input file.
:returns: country/language and study metadata.
"""
def get_country_language_and_study_info(filename):
	filename_without_extension = re.sub('\.xml', '', filename)
	filename_split = filename_without_extension.split('_')

	study = filename_split[0]+'_'+filename_split[1]+'_'+filename_split[2]
	country_language = filename_split[3]+'_'+filename_split[4]

	return study, country_language


def fix_variable_name_inconsistencies(name):
	if '_' in name:
		name = name.split('_')[0]

	return name