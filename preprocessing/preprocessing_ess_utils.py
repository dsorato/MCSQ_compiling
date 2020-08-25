import re
from ess_special_answer_categories import * 

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

"""
Switches abbreviations of the word interviewer for the full form.

:param text: sentence being analyzed.
:param country_language: country_language metadata embedded in file name.
:returns: text without abbreviations for the word interviewer, when applicable.
"""
def expand_interviewer_abbreviations(text, country_language):
	if 'CZE' in country_language:
		text = text.replace('Taz.', 'Tazatel')
	elif '_ES' in country_language or 'POR' in country_language:
		text = text.replace('Ent.', "Entrevistador")
	elif 'ENG_' in country_language:
		text = text.replace('Int.', "Interviewer")
	elif 'FRE_' in country_language:
		text = text.replace('Enq.', "Enquêteur")
	elif 'GER_' in country_language:
		text = text.replace('Befr.', "Befrager")
	elif 'NOR' in country_language:
		text = text.replace('Int.', "Intervjuer")

	return text

def instantiate_special_answer_category_object(country_language):
	if 'CAT' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesCAT()
	elif 'CZE' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesCZE()
	elif 'ENG_' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesENG()
	elif 'FRE_' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesFRE()
	elif 'GER_' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesGER()
	elif 'NOR' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesNOR()
	elif 'POR' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesPOR()
	elif 'SPA' in country_language:
		ess_special_answer_categories = SpecialAnswerCategoriesSPA()
	elif 'RUS' in country_language:
		if '_EE' in country_language:
			ess_special_answer_categories = SpecialAnswerCategoriesRUS_EE()
		elif '_IL' in country_language:
			ess_special_answer_categories = SpecialAnswerCategoriesRUS_IL()
		elif '_LV' in country_language:
			ess_special_answer_categories = SpecialAnswerCategoriesRUS_LV()
		elif '_LT' in country_language:
			ess_special_answer_categories = SpecialAnswerCategoriesRUS_LT()
		else:
			ess_special_answer_categories = SpecialAnswerCategoriesRUS_RU_UA()

	return ess_special_answer_categories

def check_if_answer_is_special_category(text, ess_special_answer_categories):
	answer_value = None

	if text.lower() == ess_special_answer_categories.dont_know[0].lower():
		return ess_special_answer_categories.dont_know[0], ess_special_answer_categories.dont_know[1]
	elif text.lower() == ess_special_answer_categories.refuse[0].lower():
		return ess_special_answer_categories.refuse[0], ess_special_answer_categories.refuse[1]
	elif text.lower() == ess_special_answer_categories.dontapply[0].lower():
		return ess_special_answer_categories.dontapply[0], ess_special_answer_categories.dontapply[1]
	elif text.lower() == ess_special_answer_categories.write_down[0].lower():
		return ess_special_answer_categories.write_down[0], ess_special_answer_categories.write_down[1]

	return text, answer_value

def clean_answer(text, ess_special_answer_categories):
	if isinstance(text, str) == False:
		return None, None

	text = text.replace('(No ho sap)','No ho sap')
	text = text.replace("(Don't know)","Don't know")

	if re.compile(r'^00\s\w+').match(text):
		text = text.split('00', 1)
		answer_text = text[1].rstrip()
		answer_value = '0'
	elif re.compile(r'^10\s\w+').match(text):
		text = text.split('10', 1)
		answer_text = text[1].rstrip()
		answer_value = '10'
	elif re.compile(r'^0\s\w+').match(text):
		text = text.split('0', 1)
		answer_text = text[1].rstrip()
		answer_value = '0'
	elif re.compile(r'^88\s\w+').match(text):
		text = text.split('88', 1)
		answer_text = text[1].rstrip()
		answer_value = '88'
	elif re.compile(r'^77\s\w+').match(text):
		text = text.split('77', 1)
		answer_text = text[1].rstrip()
		answer_value = '77'
	elif re.compile(r'^99\s\w+').match(text):
		text = text.split('99', 1)
		answer_text = text[1].rstrip()
		answer_value = '99'
	elif re.compile(r'^J\s.+').match(text):
		text = text.split('J', 1)
		answer_text = text[1].rstrip()
		answer_value = 'J'
	elif re.compile(r'^R\s.+').match(text):
		text = text.split('R', 1)
		answer_text = text[1].rstrip()
		answer_value = 'R'
	elif re.compile(r'^C\s.+').match(text):
		text = text.split('C', 1)
		answer_text = text[1].rstrip()
		answer_value = 'C'
	elif re.compile(r'^M\s.+').match(text):
		text = text.split('M', 1)
		answer_text = text[1].rstrip()
		answer_value = 'M'
	elif re.compile(r'^F\s.+').match(text):
		text = text.split('F', 1)
		answer_text = text[1].rstrip()
		answer_value = 'F'
	elif re.compile(r'^S\s.+').match(text):
		text = text.split('S', 1)
		answer_text = text[1].rstrip()
		answer_value = 'S'
	elif re.compile(r'^K\s.+').match(text):
		text = text.split('K', 1)
		answer_text = text[1].rstrip()
		answer_value = 'K'
	elif re.compile(r'^P\s.+').match(text):
		text = text.split('P', 1)
		answer_text = text[1].rstrip()
		answer_value = 'P'
	elif re.compile(r'^D\s.+').match(text):
		text = text.split('D', 1)
		answer_text = text[1].rstrip()
		answer_value = 'D'
	elif re.compile(r'^H\s.+').match(text):
		text = text.split('H', 1)
		answer_text = text[1].rstrip()
		answer_value = 'H'
	elif re.compile(r'^U\s.+').match(text):
		text = text.split('U', 1)
		answer_text = text[1].rstrip()
		answer_value = 'U'
	elif re.compile(r'^N\s.+').match(text):
		text = text.split('N', 1)
		answer_text = text[1].rstrip()
		answer_value = 'N'
	else:
		answer_text = text.strip()
		answer_value = None

	answer_text = answer_text.strip()
	answer_text, answer_value = check_if_answer_is_special_category(answer_text, ess_special_answer_categories)

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

		