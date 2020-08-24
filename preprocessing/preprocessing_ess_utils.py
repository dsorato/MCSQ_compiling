import re

"""
Retrieves the country/language and study metadata based on the input filename.
The filenames respect a nomenclature rule, as follows:
SSS_RRR_YYYY_CC_LLL
S = study name 
R = round or wave
Y = study year
C = Country (ISO code with two digits, except for SOURCE)
L = Language

:param filename: name of the input file.
:returns: country/language and study metadata.
"""
def get_country_language_and_study_info(filename):
	filename_without_extension = re.sub('\.txt', '', filename)
	filename_split = filename_without_extension.split('_')

	study = filename_split[0]+'_'+filename_split[1]+'_'+filename_split[2]
	country_language = filename_split[3]+'_'+filename_split[4]

	return study, country_language


def clean_text(text):
	if isinstance(text, str):
		text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)
		text = re.sub('å','å', text)
		text = re.sub('ö','ö', text)
		text = re.sub('ä','ä', text)
		text = re.sub('Ä','ä', text)
		text = re.sub('ü','ü', text)
		text = re.sub('–', '-', text)
		text = re.sub('’',"'", text)
		text = re.sub("…", "...", text)
		text = re.sub(" :", ":", text)
		text = re.sub("’", "'", text)
		text = re.sub("[.]{4,}", "", text)
		text = re.sub("[_]{2,}", "", text)
		text = re.sub('>', "",text)
		text = re.sub('<', "",text)
		text = re.sub('Q[0-9]*\.', "",text)
		text = re.sub('\[', "",text)
		text = re.sub('\]', "",text)
		text = re.sub('^[A-Z]\.\s', "",text)
		text = re.sub('S\.R\.', "SR",text)
		text = re.sub('S\.R', "SR",text)
		text = re.sub('SR\.', "SR",text)
		text = re.sub('s\.r', "SR",text)
		text = re.sub('s\.r\.', "SR",text)
		text = re.sub('S\.r', "SR",text)
		text = text.replace('\n',' ')
		text = text.rstrip()
	else:
		text = ''



	return text