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

"""
Cleans Request, Introduction and Instruction text segments by removing
undesired characters and standartizing some character representations.

:param text: text to be cleaned.
:returns: cleaned text.
"""
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


def instruction_recognition_spanish(text,country_language):
	regex= r"^(?P<programador>)programador"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)entrevistador"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	if 'CAT' in country_language:
		regex= r"^(?P<continue>(continuï)?\s?(?P<show>)mostr(ar|eu|ant)\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<ask>)(preguntar)?\s?a\s(?P<all>)tothom"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<insist>)insistiu"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<use>)(utilitzi la|segueixi utilitzant|continuï utilitzant)\s(?P<this>)(aquesta)?\s?(?P<same>)(mateixa)?\s?(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<use>)utilitzi\s(?P<this>)aquesta\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True


		regex= r"^(?P<read>)llegi(r|u)\s(?P<out>)(alta)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<suggest>)suggerir\s(?P<categories>)categories\s(?P<de>)de\s(?P<answer>)resposta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<choose>)encercli\s(?P<one>)una\s(?P<option>)opció"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<note>)nota\s(?P<for>)per\s(?P<interviewer>)entrevistador\s(?P<code>)codificar"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True


	# choose_answer_in_card_pattern = re.compile("(Triï|resposta|d'aquesta|targeta)", re.IGNORECASE)
	# note_for_interviewer_pattern = re.compile("(nota per entrevistador codificar)", re.IGNORECASE)
	# tick_box_or_choose_one_pattern = re.compile("(Si|us|plau|encercli|una|opció)", re.IGNORECASE)
	# choose_multiple_pattern = re.compile("(MARQUEU|TOTS|QUE|CORRESPONGUIN)", re.IGNORECASE)
	# choose_closest_to_opinion_pattern = re.compile("(Si|us|plau|encercli|l'opció|més|propera|seva|opinió)", re.IGNORECASE)
	# list_and_code_pattern = re.compile("(Codificar|totes|que|calgui)", re.IGNORECASE)
	# list_and_code_organization_pattern =  re.compile("(LLEGIR|CADA|ORGANITZACIÓ|PER|TORNS)", re.IGNORECASE)
	# note_with_details_pattern = re.compile("(ANOTEU|AMB|TOTS|DETALLS)", re.IGNORECASE)

	return False

		