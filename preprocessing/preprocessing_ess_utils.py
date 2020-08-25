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


def extend_interviewer_abbreviations(text, country_language):
	if 'CZE' in country_language:
		text = text.replace('Taz.', 'Tazatel',text)
	elif '_ES' in country_language or 'POR' in country_language:
		text = text.replace('Ent.', "Entrevistador",text)
	elif 'ENG_' in country_language:
		text = text.replace('Int.', "Interviewer",text)
	elif 'FRE_' in country_language:
		text = text.replace('Enq.', "Enquêteur",text)
	elif 'GER_' in country_language:
		text = text.replace('Befr.', "Befrager",text)
	elif 'NOR':
		text = text.replace('Int.', "Intervjuer",text)



def clean_answer(text):
	if re.compile(r'^00\s\w+'):
		text = text.split('00', 1)
		answer_text = text[1].rstrip()
		answer_value = 0
	if re.compile(r'^10\s\w+'):
		text = text.split('10', 1)
		answer_text = text[1].rstrip()
		answer_value = 10
	if re.compile(r'^0\s\w+'):
		text = text.split('0', 1)
		answer_text = text[1].rstrip()
		answer_value = 0
	if re.compile(r'^88\s\w+'):
		text = text.split('88', 1)
		answer_text = text[1].rstrip()
		answer_value = 88
	if re.compile(r'^J\s.+'):
		text = text.split('J', 1)
		answer_text = text[1].rstrip()
		answer_value = 'J'
	if re.compile(r'^R\s.+'):
		text = text.split('R', 1)
		answer_text = text[1].rstrip()
		answer_value = 'R'
	if re.compile(r'^C\s.+'):
		text = text.split('C', 1)
		answer_text = text[1].rstrip()
		answer_value = 'C'
	if re.compile(r'^M\s.+'):
		text = text.split('M', 1)
		answer_text = text[1].rstrip()
		answer_value = 'M'
	if re.compile(r'^F\s.+'):
		text = text.split('F', 1)
		answer_text = text[1].rstrip()
		answer_value = 'F'
	if re.compile(r'^S\s.+'):
		text = text.split('S', 1)
		answer_text = text[1].rstrip()
		answer_value = 'S'
	if re.compile(r'^K\s.+'):
		text = text.split('K', 1)
		answer_text = text[1].rstrip()
		answer_value = 'K'
	if re.compile(r'^P\s.+'):
		text = text.split('P', 1)
		answer_text = text[1].rstrip()
		answer_value = 'P'
	if re.compile(r'^D\s.+'):
		text = text.split('D', 1)
		answer_text = text[1].rstrip()
		answer_value = 'D'
	if re.compile(r'^H\s.+'):
		text = text.split('H', 1)
		answer_text = text[1].rstrip()
		answer_value = 'H'
	if re.compile(r'^U\s.+'):
		text = text.split('U', 1)
		answer_text = text[1].rstrip()
		answer_value = 'U'
	if re.compile(r'^N\s.+'):
		text = text.split('N', 1)
		answer_text = text[1].rstrip()
		answer_value = 'N'
	else:
		answer_text = text[1].rstrip()
		answer_value = None

	answer_text = answer_text.replace('(No ho sap)','No ho sap')

	return answer_text, answer_value


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
		regex= r"^(?P<continue>)(continuï)?\s?(?P<show>)mostr(ar|eu|ant)\s(?P<card>)targeta"
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

		regex= r"^(?P<readorcode>)(llegir|codificar)\s(?P<each>)cada\s(?P<organization>)organització"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<markorcode>)(marqueu|codificar)\s(?P<all>)tot(s|es)\s(?P<that>)que\s(?P<apply>)(corresponguin|calgui)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<note>)anoteu\s(?P<with>)amb\s(?P<all>)tots\s(?P<details>)detalls"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<choose>)encercli\s(?P<option>)l'opció\s(?P<closer>)més propera"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True


	return False

		