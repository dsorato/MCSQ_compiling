import re
from ess_special_answer_categories import * 
from essmodules import * 


"""
Removes spaces in item names such as A 1, because the MCSQ standard
are item names without spaces (A1).
Args:
	param1 item_name (string): item_name retrieved from the input file.
Returns:
	item_name (string) withour spaces.
"""
def remove_spaces_from_item_name(item_name):
	return item_name.replace(" ", "")
"""
Retrieves the country/language and study metadata based on the input filename,
or survey_item_ID prefix.
The filenames respect a nomenclature rule, as follows:
SSS_RRR_YYYY_CC_LLL
S = study name 
R = round or wave
Y = study year
C = Country (ISO code with two digits, except for SOURCE)
L = Language

Args:
	param1 filename (string): name of the input file.

Returns: 
	country/language (string) and study metadata (string).
"""
def get_country_language_and_study_info(filename):
	if 'txt' in filename:
		filename_without_extension = re.sub('\.txt', '', filename)
		filename_split = filename_without_extension.split('_')
	else:
		filename_split = filename.split('_')

	study = filename_split[0]+'_'+filename_split[1]+'_'+filename_split[2]
	country_language = filename_split[3]+'_'+filename_split[4]

	return study, country_language

"""
Transforms study metadata present in the input file to the standard
used in the MCSQ format.

Args:
	param1 study (string): study metadata extracted from input file (Study column).

Returns:
	Standardized study parameter (string).
"""
def standardize_study_metadata(study):
	dict_year_round = {'ESS Round 1':'ESS_R01_2002', 'ESS Round 2':'ESS_R02_2004',
	'ESS Round 3':'ESS_R03_2006', 'ESS Round 4':'ESS_R04_2008', 'ESS Round 5':'ESS_R05_2010', 
	'ESS Round 6':'ESS_R06_2012', 'ESS Round 7':'ESS_R07_2014', 'ESS Round 8':'ESS_R08_2016',
	'ESS Round 9':'ESS_R09_2018'}

	for k,v in list(dict_year_round.items()):
		if study == k:
			return v


"""
Standardizes the item name metadata of supplementary modules G, H and I

Args:
	param1 item_name: item_name metadata, extracted from input file.

Returns:
	Standardized item_name, when applicable.
"""
def standardize_supplementary_item_name(item_name):
	if 'GF' in item_name:
		return item_name.replace('GF', 'G')
	elif 'IF' in item_name:
		return item_name.replace('IF', 'I')
	elif 'HF' in item_name:
		return item_name.replace('HF', 'H')
	elif 'GS' in item_name:
		return item_name.replace('GS', 'G')
	elif 'IS' in item_name:
		return item_name.replace('IS', 'I')
	elif 'HS' in item_name:
		return item_name.replace('HS', 'H')
	else:
		return item_name


"""
Matches the item_name against the dictionary stored in the ESSModulesRRR objects.
Rotating/supplementary modules are defined by round because they may change from
round to round.
Args:
	param1 essmodules (Python object): ESSModulesRRR object, instantiated according to the round.
	param2 item_name (string): name of survey item, retrieved in previous steps.

Returns: 
	matching value for item name (string).
"""
def retrieve_supplementary_module(essmodules,item_name):
	for k,v in list(essmodules.modules.items()):
		if re.compile(k).match(item_name):
			return v

"""
Retrieves the module of the survey_item, based on information from the ESSModulesRRR objects.
This information comes from the source questionnaires.

Args:
	param1 item_name (string): name of survey item, retrieved in previous steps.
	param2 study (string): study metadata, embedded in the file name.

Returns: 
	module of survey_item (string).
"""
def retrieve_item_module(item_name, study):
	if re.compile(r'A').match(item_name):
		return 'A - Media; social trust'
	elif re.compile(r'B').match(item_name):
		return 'B - Politics, including: political interest, efficacy, trust, electoral and other forms of participation, party allegiance, socio-political evaluations/orientations, multi-level governance'
	elif re.compile(r'C').match(item_name):
		return 'C - Subjective well-being and social exclusion; religion; perceived discrimination; national and ethnic identity'
	elif re.compile(r'F').match(item_name):
		return 'F - Socio-demographic profile, including: Household composition, sex, age, type of area, Education & occupation details of respondent, partner, parents, union membership, household income, marital status'
	else:
		if 'R01' in study:
			essmodules = ESSSModulesR01()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R02' in study:
			essmodules = ESSSModulesR02()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R03' in study:
			essmodules = ESSSModulesR03()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R04' in study:
			essmodules = ESSSModulesR04()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R05' in study:
			essmodules = ESSSModulesR05()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R06' in study:
			essmodules = ESSSModulesR06()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R07' in study:
			essmodules = ESSSModulesR07()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R08' in study:
			essmodules = ESSSModulesR08()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

		elif 'R09' in study:
			essmodules = ESSSModulesR09()
			v = retrieve_supplementary_module(essmodules,item_name) 
			return v

"""
Cleans Request, Introduction and Instruction text segments by removing
undesired characters and standartizing some character representations.
A string input is expected, if the input is not a string instance, 
the method returns '', so the entry is ignored in the data extraction loop.

Args:
	param1 text (string expected): text to be cleaned.

Returns: 
	cleaned text (string).
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
		text = re.sub('´',"'", text)
		text = re.sub("…", "...", text)
		text = text.replace("... ...", "...")
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
		text = "".join(filter(lambda char: char != "»", text))
		text = "".join(filter(lambda char: char != "«", text))
		text = text.replace(" ?", "?")
		text = text.replace('\n',' ')
		text = text.rstrip()
	else:
		text = ''
		

	return text

"""
Switches abbreviations of the word interviewer for the full form.

Args:
	param1 text (string): sentence being analyzed.
	param2 country_language (string): country_language metadata embedded in file name.

Returns: 
	text (string) without abbreviations for the word interviewer, when applicable.
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
		text = text.replace('INT.', "Interviewer")
	elif 'NOR' in country_language:
		text = text.replace('Int.', "Intervjuer")

	return text

"""
Instantiates the SpecialAnswerCategories object that stores both the text
and category values of the special answers (don't know, refusal, not applicable 
and write down) in accordance to the country_language metadata parameter.

Args:
	param1 country_language (string): country_language metadata parameter, embedded in file name.

Returns: 
	instance of SpecialAnswerCategories object (Python object), in accordance to the country_language.
"""
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

"""
Verifies if a given answer segment is one of the special answer categories,
by testing the answer text against the attributes of SpecialAnswerCategories object.
This method serves the purpose of standartizing the special answer category values.

Args:
	param1 text (string): answer segment currently being analyzed.
	param2 answer_value (string): answer category value, defined in clean_answer() method.
	param3 ess_special_answer_categories (Python object): instance of SpecialAnswerCategories object, 
	in accordance to the country_language.

Returns: 
	answer text (string) and its category value (string). When the answer is a special answer category, 
	the text and category values are the ones stored in the SpecialAnswerCategories object.
"""
def check_if_answer_is_special_category(text, answer_value, ess_special_answer_categories):
	if text.lower() == ess_special_answer_categories.dont_know[0].lower():
		return ess_special_answer_categories.dont_know[0], ess_special_answer_categories.dont_know[1]
	elif text.lower() == ess_special_answer_categories.refuse[0].lower():
		return ess_special_answer_categories.refuse[0], ess_special_answer_categories.refuse[1]
	elif text.lower() == ess_special_answer_categories.dontapply[0].lower():
		return ess_special_answer_categories.dontapply[0], ess_special_answer_categories.dontapply[1]
	elif text.lower() == ess_special_answer_categories.write_down[0].lower():
		return ess_special_answer_categories.write_down[0], ess_special_answer_categories.write_down[1]

	return text, answer_value

"""
Cleans the answer segment, by standartizing the text (when it is a special answer category),
and attributing an category value to it. 

Args:
	param1 text (string): answer segment currently being analyzed.
	param2 ess_special_answer_categories (Python object): instance of SpecialAnswerCategories object, 
	in accordance to the country_language.

Returns: 
	answer text (string) and its category value (string). When the answer is a special answer category, 
	the text and category values are the ones stored in the SpecialAnswerCategories object.
"""
def clean_answer(text, ess_special_answer_categories):
	answer_value = None
	if isinstance(text, str) == False:
		return None, None

	text = text.replace('(No ho sap)','No ho sap')
	text = text.replace("(Don't know)","Don't know")

	if re.compile(r'^00\s\w+').match(text):
		text = text.split('00', 1)
		answer_text = text[1].rstrip()
		answer_value = '0'
	elif re.compile(r'^01\s\w+').match(text):
		text = text.split('01', 1)
		answer_text = text[1].rstrip()
		answer_value = '1'
	elif re.compile(r'^05\s\w+').match(text):
		text = text.split('05', 1)
		answer_text = text[1].rstrip()
		answer_value = '5'
	elif re.compile(r'^06\s\w+').match(text):
		text = text.split('06', 1)
		answer_text = text[1].rstrip()
		answer_value = '6'
	elif re.compile(r'^07\s\w+').match(text):
		text = text.split('07', 1)
		answer_text = text[1].rstrip()
		answer_value = '7'
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
		answer_value = '888'
	elif re.compile(r'^77\s\w+').match(text):
		text = text.split('77', 1)
		answer_text = text[1].rstrip()
		answer_value = '777'
	elif re.compile(r'^99\s\w+').match(text):
		text = text.split('99', 1)
		answer_text = text[1].rstrip()
		answer_value = '999'
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
	answer_text, answer_value = check_if_answer_is_special_category(answer_text, answer_value, ess_special_answer_categories)

	return answer_text, answer_value


"""
Calls the appropriate instruction recognition method, according to the language.
Args:
	param1 sentence (string): sentence being analyzed in outer loop of data extraction.
	param2 country_language (string): country_language metadata, embedded in file name.

Returns: 
	bypass the return of instruction_recognition methods (boolean).
"""
def check_if_segment_is_instruction(sentence, country_language):
	if 'CZE' in country_language:
		return instruction_recognition_czech(sentence,country_language)
	if 'ENG' in country_language:
		return instruction_recognition_english(sentence,country_language)
	if '_ES' in country_language:
		return instruction_recognition_catalan_spanish(sentence,country_language) 
	if 'FRE' in country_language:
		return instruction_recognition_french(sentence,country_language) 
	if 'GER' in country_language:
		return instruction_recognition_german(sentence,country_language) 
	if 'NOR' in country_language:
		return instruction_recognition_norwegian(sentence,country_language)
	if 'POR' in country_language:
		return instruction_recognition_portuguese(sentence,country_language)
	if 'RUS' in country_language:
		return instruction_recognition_russian(sentence,country_language)

"""
Recognizes an instruction segment for texts written in German,
based on regex named groups patterns.

Args:
	param1 text (string): text (in German) currently being analyzed.
	param2 country_language (string): country_language metadata embedded in file name.

Returns: 
	True if the segment is an instruction or False if it is not.
"""
def instruction_recognition_russian(text,country_language):
	regex= r"^(?P<interviewer>)ИНТЕРВЬЮЕР"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<readout>)(ЗАЧИТАТЬ|ЗАЧИТАЙТЕ|ЗАЧИТАЙТЕ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)ПРОЧИТАТЬ\s(?P<out>)ВСЛУХ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<canmark>)МОЖНО ОТМЕТИТЬ\s(?P<more>)БОЛЬШЕ\s(?P<than>)ЧЕМ\s(?P<one>)ОДИН\s(?P<answer>)ОТВЕТ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<use>)(ИСПОЛЬЗУЙТЕ)?\s?(?P<card>)(КАРТОЧКА|КАРТОЧКУ)\s(?P<number>)(Nr|\d+|\w+)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<respondent>)(РЕСПОНДЕНТ|РЕСПОНДЕНТЫ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<ask>)(СПАШИВАТЬ|СПРАШИВАТЬ|СПРОСИТЬ|СПРАШИВАЙТЕ|СПРОСИТЕ)\s(?P<to>)(У)?\s?(?P<all>)(ВСЕХ)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<ask>)ОТМЕТЬТЕ\s(?P<all>)ВСЕ\s(?P<applicable>)ПОДХОДЯЩИЕ\s(?P<answers>)ОТВЕТЫ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<for>)ДЛЯ\s(?P<interviewer>)ИНТЕРВЬЮЕРА"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)ИНТЕРВЬЮЕРА\s(?P<note>)ОТМЕЧАЕТ\s(?P<code>)КОД"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<toanswer>)Для ответа\s(?P<again>)(снова)?\s?(?P<use>)(воспользуйтесь|пользуйтесь)(,)?\s(?P<please>)(пожалуйста)?(,)?\s?(?P<this>)(этой)?\s?(?P<thesame>)(той же)?\s?(?P<card>)карточкой"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(Пожалуйста)?(,)?\s?(?P<select>)Выберите\s(?P<your>)(свой)?\s?(?P<one>)(один)?\s?(?P<answer>)ответ\s(?P<this>)(этой)?\s?(?P<of>)(из)?\s?(?P<proposed>)(предложенных)?\s?(?P<on>)(на)?\s?(?P<card>)(карточки|карточкой|карты|карточке)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(Пожалуйста)?(,)?\s?(?P<select>)выберите\s(?P<all>)все\s(?P<options>)варианты\s(?P<answer>)ответа\s(?P<on>)на\s(?P<card>)(карточки|карточкой|карты|карточке)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Пожалуйста)?(,)?\s?(?P<select>)Выберите\s(?P<on>)на\s(?P<card>)(карточки|карточкой|карты|карточке)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Пожалуйста)?(,)?\s?(?P<mark>)отметьте\s(?P<one>)один\s(?P<option>)квадрат"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<answer>)ОТВЕЧАЮТ\s(?P<all>)ВСЕ\s(?P<respondents>)РЕСПОНДЕНТЫ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<again>)(СНОВА)?\s?(?P<card>)КАРТА\s(?P<continue>)(ПРОДОЛЖАЕТСЯ)?\s?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<toanswer>)(Для ответа)?(,)?\s?(?P<please>)(пожалуйста)?(,)?\s?(?P<now>)(Теперь)?\s?(?P<use>)(Используйте|используйте|используйте)\s(?P<this>)эту\s(?P<same>)(же)\s?(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	
	regex= r"^(?P<check>)(Заполните|Отметьте)(,)?\s(?P<please>)(пожауйста|пожалуйста|пожалуйста)?(,)?\s?(?P<only>)(только)?\s?(?P<one>)(один|одну)\s(?P<box>)(ячейку|клетку|ответ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(пожалуйста)?(,)?\s?(?P<check>)отметьте\s(?P<one>)один\s(?P<box>)квадрат"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)Используйте(,)?\s(?P<please>)(пожалуйста)?(,)?\s?(?P<this>)эту\s(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<toanswer>)Для ответа(,)?\s(?P<please>)(пожалуйста)?(,)?\s?(?P<use>)используйте\s(?P<this>)(эту)?\s?(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)ПОПРОСИТЕ\s(?P<respondent>)РЕСПОНДЕНТА\s(?P<open>)ОТКРЫТЬ\s(?P<again>)СНОВА\s(?P<use>)ВОСПОЛЬЗОВАТЬСЯ\s(?P<card>)(КАРТОЧКОЙ|КАРТОЧКУ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<possible>)МОЖНО\s(?P<check>)ОТМЕТИТЬ\s(?P<more>)БОЛЬШЕ\s(?P<than>)ЧЕМ\s(?P<one>)ОДИН\s(?P<answer>)ОТВЕТ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<mark>)(Заполните|Отметьте)(,)?\s(?P<please>)(пожалуйста)?(,)?\s?(?P<one>)одну\s(?P<box>)клетку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)(ПРОЧИТАЙТЕ|ЗАЧИТАТЬ)\s(?P<each>)КАЖДОЕ\s(?P<utterance>)УТВЕРЖДЕНИЕ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)ОТМЕТЬТЕ\s(?P<only>)(ТОЛЬКО)?\s?(?P<one>)ОДИН\s(?P<option>)(ВАРИАНТ|КОД|ЧИСЛО)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<readout>)ЗАЧИТЫВАЙТЕ\s(?P<by>)ПО\s(?P<each>)КАЖДОЙ\s(?P<line>)СТРОКЕ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)Используйте\s(?P<the>)ту\s(?P<same>)(же|самую)\s(?P<card>)карту"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<check>)ОТМЕЧАТЬ\s(?P<all>)ВСЕ\s(?P<that>)КОТОРЫЕ\s(?P<apply>)ПОДХОДЯТ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<show>)ПОДАЙТЕ\s(?P<respondent>)РЕСПОНДЕНТУ\s(?P<card>)(КАРТОЧКУ|карточка)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<the>)ТА\s(?P<same>)ЖЕ\s(?P<card>)(КАРТОЧКУ|карточка)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
  
	regex= r"^(?P<ask>)(ЗАДАЙТЕ|ЗАДАВАТЬ|ЗАДАВАЙТЕ)\s(?P<questions>)(ВОПРОСЫ|ВОПРОС)\s?(?P<everyone>)(ВСЕМ)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<readout>)ЗАЧИТЫВАЙТЕ\s(?P<questions>)(ВОПРОСЫ|ВОПРОС)\s(?P<mark>)ОТМЕЧАЙТЕ\s(?P<answer>)ОТВЕТ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<this>)ЭТОТ\s(?P<question>)ВОПРОС\s(?P<show>)ЗАДАЙТЕ\s(?P<all>)(ВСЕМ|ВСЕ|ВСЕX)\s(?P<respondent>)(РЕСПОНДЕНТА|РЕСПОНДЕНТУ|РЕСПОНДЕНТЫ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Пожалуйста)?(,)?\s?(?P<select>)выберите\s(?P<one>)один\s(?P<answer>)ответ\s(?P<on>)(на|из)\s(?P<this>)этой\s(?P<card>)(карточке|карточки)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<select>)(Выберите)?\s?(?P<your>)Ваш\s(?P<answer>)ответ\s(?P<from>)из\s(?P<this>)этой\s(?P<card>)(карточке|карточки)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)Используйте\s(?P<still>)(все еще)?\s?(?P<toanswer>)(для ответа)?\s?(?P<this>)(эту)?\s?(?P<card>)(карточке|карточки|карточку)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<select>)Выберите\s(?P<your>)(Ваш|свой)\s(?P<answer>)ответ\s(?P<on>)на\s(?P<this>)(этой)?\s?(?P<card>)(карточке|карточки|карточку)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<select>)Выберите\s(?P<please>)пожалуйста\s(?P<one>)один\s(?P<answer>)ответ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<still>)Все еще\s(?P<use>)используйте\s(?P<card>)(карточке|карточки|карточку)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)Пожалуйста(,)?\s(?P<use>)используйте\s(?P<this>)(эту)?\s?(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Пожалуйста)?(,)?\s?(?P<use>)используйте\s(?P<thesame>)(ту же|ту же самую)?\s?(?P<card>)(карточку|карту)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True





"""
Recognizes an instruction segment for texts written in German,
based on regex named groups patterns.

Args:
	param1 text (string): text (in German) currently being analyzed.
	param2 country_language (string): country_language metadata embedded in file name.

Returns: 
	True if the segment is an instruction or False if it is not.
"""
def instruction_recognition_german(text,country_language):
	regex= r"^(?P<interviewer>)(Befrager|Interviewer)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<again>)(Weiterhin|Weiter|Und noch die)?\s?(?P<card>)(karte\s(\d+|[a-z]+)|liste\s(\d+|[a-z]+))"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<insist>)NACHFRAGEN"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(bitte)?\s?(?P<readout>)vorlesen"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<to>)an\s(?P<all>)alle"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(bitte)?(,)?\s?(?P<use>)(Verwenden|benutzen)\sSie\s(?P<also>)(auch)?\s?(?P<forthis>)(dafür)?\s?(?P<the>)(die)?\s?(?P<this>)(diese)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(bitte)?(,)?\s?(?P<use>)(Verwenden|benutzen)\sSie\s(?P<again>)dazu wieder\s(?P<the>)die\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<tellme>)(Sagen Sie es mir)?\s?(?P<please>)bitte\s(?P<answer>)(antworten sie)?\s?(?P<again>)(wieder)?\s?(?P<using>)anhand von\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)(Verwenden|benutzen|Benützen)\sSie\s(?P<now>)(jetzt|nun)?\s?(?P<please>)(bitte)?\s?(?P<the>)(die|diese)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(bitte)?(,)?\s?(?P<use>)(Verwenden|benutzen)\s(Sie|Die)\s(?P<onceagain>)noch einmal\s(?P<this>)(diese)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<note>)Hinweis\s(?P<for>)für\s(?P<the>)den\s(?P<interviewer>)(Interviewer|Befrager)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<tick>)kreuzen\s(?P<a>)Sie ein\s(?P<box>)Kästchen an"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<tick>)kreuzen\s(?P<a>)Sie bitte ein\s(?P<box>)Kästchen an"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<use>)(Verwenden|benutzen)\s(?P<this>)Sie\s(diese|die)?\s?(?P<same>)(selbe)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<use>)(Verwenden|benutzen)\s(?P<this>)Sie dafür diese\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<use>)(Verwenden|benutzen)\s(?P<again>)Sie nochmals\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<answer>)sagen Sie\s(?P<forme>)(es mir|es bitte)\s(?P<again>)(noch einmal|nochmals)?\s?(?P<withthis>)(anhand von dieser|anhand dieser|anhand von)\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<use>)benutzen\s(?P<this>)Sie\s(?P<again>)(wieder|wieder diese)\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)(Verwenden|benutzen)\s(?P<please>)Sie bitte\s(?P<again>)wieder diese\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<use>)(Verwenden|benutzen)\s(?P<toanswer>)Sie für Ihre Antwort\s(?P<this>)(diese|die gleiche)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<this>)diese\s(?P<card>)(Karte|liste)\s(?P<use>)verwenden"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)verwenden\s(?P<please>)Sie bitte\s(?P<this>)(diese)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<use>)verwenden\s(?P<this>)(die|diese)\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<use>)verwenden\s(?P<this>)Sie diese\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<mark>)ringeln\s(?P<a>)Sie eine\s(?P<answer>)Antwortzahl"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<only>)NUR\s(?P<one>)EINE\s(?P<answer>)ANTWORT\s(?P<possible>)(MÖGLICH)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<use>)(benutzen|verwenden)\s(?P<this>)Sie\s(diese|die)\s(?P<same>)(gleiche)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<choose>)wählen\s(?P<sie>)Sie\s(?P<one>)(eine|Ihre)?\s?(?P<answer>)Antwort\s(?P<fromthis>)(von|von dieser|von der|auf der)\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<just>)nur\s(?P<one>)eine\s(?P<answer>)Antwort\s(?P<select>)auswählen"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		

	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<use>)(benutzen|verwenden)\s(?P<continue>)Sie\s(weiterhin|wieder|wiederum)?\s?(?P<now>)(jetzt)?\s?(?P<this>)(diese|dieselbe)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(Bitte)?(,)?\s?(?P<lookat>)betrachten Sie\s(?P<nowthis>)nun (diese|dieselbe)\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
	

	


"""
Recognizes an instruction segment for texts written in Norwegian,
based on regex named groups patterns.

Args:
	param1 text (string): text (in Norwegian) currently being analyzed.
	param2 country_language (string): country_language metadata embedded in file name.

Returns: 
	True if the segment is an instruction or False if it is not.
"""
def instruction_recognition_norwegian(text,country_language):
	regex= r"^(?P<programmer>)programmerer:"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)Intervjuer"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)insistere"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		 

	regex= r"^(?P<read>)LES\s(?P<aloud>)HØYT"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<lookat>)Se på\s(?P<this>)(dette)?\s?(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<takea>)Ta en\s(?P<lookat>)titt på\s(?P<this>)dette\s(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<answer>)Svar\s(?P<based>)med utgangspunkt\s(?P<on>)i\s(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)Vær snill å\s(?P<use>)bruke\s(?P<this>)dette\s(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<read>)Les\s(?P<out>)opp\s(?P<the>)de\s(?P<different>)ulike\s(?P<organizations>)institusjonene"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
   
	regex= r"^(?P<choose>)Velg\s(?P<an>)(et tall|et|ett av)\s(?P<option>)(alternativene|svaralternativ|svaralternativene)?\s?(?P<from>)(fra|på)\s(?P<this>)(dette)?\s?(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<again>)(vis|Forsatt|FORTSATT)?\s?(?P<card>)kort\s(?P<number>)\d+([a-z])*"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)notat\s(?P<for>)til\s(?P<interviewer>)intervjueren"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)les\s(?P<out>)høyt\s(?P<the>)(opp)?\s?(?P<options>)(alternativene)?\s?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)kod\s(?P<all>)alt\s(?P<that>)(som)?\s?(?P<apply>)(passer)?\s?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)stilles\s(?P<to>)til\s(?P<all>)alle"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<lookat>)(Se på)?\s?(?P<use>)Bruk\s(?P<this>)(det|dette)?\s?(?P<again>)(fortsatt)?\s?(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)Bruk\s(?P<answer>)kategoriene\s(?P<this>)(på)?\s?(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)Vennligst\s(?P<mark>)sett\s(?P<one>)ett\s(?P<case>)kryss"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)Vennligst\s(?P<mark>)sett\s(?P<case>)kryss\s(?P<closest>)i ruten nærmest\s(?P<youropinion>)din mening"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<answerby>)Svar ved å\s(?P<using>)bruke\s(?P<this>)dette\s(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)Bruk\s(?P<this>)det\s(?P<same>)samme\s(?P<card>)kortet\s(?P<to>)til\s(?P<answer>)å svare"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<select>)Velg\s(?P<one>)(et|ett)\s(?P<option>)(svaralternativ|svaralternativene|alternativene|)\s(?P<from>)fra\s(?P<this>)(det|dette)\s(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<newcard>)Her et nytt kort"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


"""
Recognizes an instruction segment for texts written in French,
based on regex named groups patterns.

Args:
	param1 text (string): text (in French) currently being analyzed.
	param2 country_language (string): country_language metadata embedded in file name.

Returns: 
	True if the segment is an instruction or False if it is not.
"""
def instruction_recognition_french(text,country_language):
	regex= r"^(?P<programmer>)Programmeur:"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)(Enquêteur|Enqueteur)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)(lisez|lire)(?P<outloud>)(haute voix)?\s?(?P<each>)(chaque)?\s?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)codez\s(?P<all>)tout(?P<thatapplies>)(qui s'applique)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)(demandez|poser)\s(?P<all>)a tous"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<show>)(montrer|montrez)?\s?(?P<again>)(encore|toujours)?\s?(?P<the>)(la)?\s?(?P<card>)carte"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(S'il vous plaît|Veuillez|Veuillez s'il vous plaît)?(,)?\s?(?P<continue>)(Continuez)?\s?(?P<use>)utiliser\s(?P<this>)cette\s(?P<card>)carte"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(S'il vous plaît|Veuillez|Je vous prie)?(,)?\s?(?P<use>)(d')?utilise(z|r)\s(?P<thesame>)la même\s(?P<card>)carte"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(S'il vous plaît)?(,)?\s?(?P<iaskyouto>)(Je vous prie)?\s?(?P<use>)(d'utiliser|utilisez)\s(?P<this>)cette\s(?P<card>)carte"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(S'il vous plaît)?(,)?\s?(?P<iaskyouto>)(Je vous prie|Veuillez)?\s?(?P<use>)(d'utiliser|utilise(r|z))\s(?P<again>)(de nouveau|à nouveau|encore)?\s?(?P<this>)cette\s(?P<same>)(même)?\s?(?P<card>)carte"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(S'il vous plaît|Veuillez)?(,)?\s?(?P<again>)(encore)?\s?(?P<use>)utiliser\s(?P<this>)cette\s(?P<card>)carte"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)note\s(?P<for>)a\s(?P<theinterviewer>)(l'enqueteur|l'enquetêur)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<instruction>)instruction\s(?P<for>)pour\s(?P<theinterviewer>)(l'enqueteur|l'enquetêur)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<choose>)choix\s(?P<multiple>)multiple\s?(?P<possible>)(possible)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(S'il vous plaît|Veuillez)?(,)?\s?(?P<choose>)(choisir|Choisissez)\s(?P<onlyone>)(une|une seule)?\s?(?P<your>)(votre)?\s?(?P<answer>)réponse(s)?\s"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<choose>)choix\s(?P<multiple>)multiple\s(?P<possible>)possible"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<multiple>)PLUSIEURS\s(?P<answers>)(reponses|réponses)\s(?P<possible>)possibles"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<enounce>)ENONCEZ\s(?P<one>)UNE\s(?P<organization>)ORGANISATION\s(?P<ata>)A LA\s(?P<time>)FOIS"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<you>)VOUS\s(?P<can>)POUVEZ\s(?P<mark>)COCHER\s(?P<multiple>)PLUSIEURS\s(?P<options>)CASES"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<withthehelp>)Toujours à l'aide\s(?P<of>)de\s(?P<this>)cette\s(?P<card>)carte."
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<continueto>)Continuez à\s(?P<use>)utiliser\s(?P<this>)cette\s(?P<card>)carte."
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)Je vous prie de\s(?P<choose>)choisir\s(?P<youranswer>)votre réponse\s(?P<from>)sur\s(?P<this>)cette\s(?P<card>)carte."
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(S'il vous plaît|Veuillez)?(,)?\s?(?P<mark>)coche(z|r)\s(?P<theoption>)la case\s(?P<that>)(qui)?\s?(?P<represent>)(correspond|correspondante)\s?(?P<better>)(le mieux)?\s?(?P<your>)((à\s)?votre)?\s?(?P<answer>)(réponse(s)?)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)Veuillez\s(?P<choose>)choisir\s(?P<onlyone>)une seule des\s(?P<answer>)réponses\s(?P<from>)figurant sur\s(?P<this>)cette\s(?P<card>)(carte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)Veuillez\s(?P<answer>)répondre\s(?P<using>)à l'aide de\s(?P<this>)cette\s(?P<card>)(carte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(S'il vous plaît|Veuillez)?(,)?\s?(?P<mark>)Cerclez\s(?P<theoption>)le code\s(?P<correspondto>)correspondant à\s(?P<answer>)votre réponse\s"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<insist>)RELANCER"
	matches = re.search(regex, text)
	if matches:
		return True



"""
Recognizes an instruction segment for texts written in English,
based on regex named groups patterns.

Args:
	param1 text (string): text (in English) currently being analyzed.
	param2 country_language (string): country_language metadata embedded in file name.

Returns: 
	True if the segment is an instruction or False if it is not.
"""
def instruction_recognition_english(text,country_language):
	regex= r"^(?P<programmer>)Programmer:"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)Interviewer"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?(,)?\s?(?P<use>)use\s(?P<this>)this\s(?P<card>)card\s?(?P<again>)(again)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?(,)?\s?(?P<use>)use\s(?P<the>)the\s(?P<same>)same\s(?P<card>)card"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
	
	regex= r"^(?P<card>)showcard"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<card>)card\s(?P<numberorletter>)(\d+|[a-z])"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<show>)(show|still)\s(?P<card>)card\s?(?P<again>)(again)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)ask\s(?P<all>)all"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<probe>)probe:"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<insist>)insist"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<codeorselect>)(code|select)\s(?P<all>)all\s(?P<that>)that\s(?P<apply>)(apply|applies)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)read\s(?P<out>)out\s?(?P<each>)(each)?\s?(?P<statement>)(statement)?\s?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?(,)?\s?(?P<still>)(still)?\s?(?P<use>)use\s(?P<this>)(this)?\s?(?P<same>)(same)?\s?(?P<card>)card"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?(,)?\s?(?P<choose>)choose\s(?P<oneor>)(one|your)\s(?P<answer>)answer\s(?P<infrom>)(in|from)\s(?P<this>)this\s(?P<same>)(same)?\s?(?P<card>)card"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<prompt>)prompt\s(?P<inrelation>)in relation\s(?P<to>)to\s(?P<precodes>)precodes"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?(,)?\s?(?P<select>)select\s(?P<only>)only\s(?P<one>)one"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?(,)?\s?(?P<tick>)tick\s(?P<oneorthe>)(one|the)?\s?(?P<box>)box"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?(,)?\s?(?P<choose>)choose\s(?P<one>)one\s(?P<answer>)answer\s(?P<from>)from\s(?P<card>)card"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)note\s(?P<forthe>)(for the)?\s?(?P<to>)(to)?\s?(?P<interviewer>)interviewer"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<if>)If\s(?P<respondent>)respondent"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)ASK\s(?P<if>)If\s(?P<partner>)PARTNER\s(?P<in>)in\s(?P<paid>)paid\s(?P<work>)work"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)ASK\s(?P<if>)If\s(?P<father>)father\s(?P<employed>)employed"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)ASK\s(?P<if>)If\s(?P<father>)father\s(?P<working>)working"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)ASK\s(?P<if>)If\s(?P<mother>)mother\s(?P<employed>)employed"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)ASK\s(?P<if>)If\s(?P<mother>)mother\s(?P<working>)working"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	return False

"""
Recognizes an instruction segment for texts written in Czech,
based on regex named groups patterns.

Args:
	param1 text (string): text (in Czech) currently being analyzed.
	param2 country_language (string): country_language metadata embedded in file name.

Returns: 
	True if the segment is an instruction or False if it is not.
"""
def instruction_recognition_czech(text,country_language):
	regex= r"^(?P<interviewer>)tazatele"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<respondent>)RESPONDENTI"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)PTEJTE\s(?P<all>)SE VŠECH\s(?P<employees>)ZAMĚSTANCŮ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
  

	regex= r"^(?P<now>)(Nyní)?\s?(?P<use>)(Použijte|použijte)\s(?P<again>)(znovu)?\s?(?P<this>)(tuto)?\s?(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<toanswer>)K odpovědi\s(?P<use>)použijte\s(?P<please>)prosím\s(?P<this>)tuto\s(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<instruction>)Pokyn:"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<still>)(STÁLE JEŠTĚ)?\s?(?P<again>)(OPĚT)?\s?(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)poznámka\s(?P<for>)pro\s(?P<interviewer>)tazatele"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<probe>)SONDUJTE"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)(ptejte|Přejte)\s(?P<all>)se všech"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<look>)Prohlédněte\s(?P<at>)si\s(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)přečtěte\s(?P<category>)varianty\s(?P<answers>)odpovědí"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)ČTĚTE\s(?P<out>)NAHLAS"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)ČTĚTE\s(?P<out>)NAHLAS\s(?P<each>)KAŽDÝ\s(?P<utterance>)VÝROK"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
 
	regex= r"^(?P<again>)opět\s(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<again>)(opět)?\s?(?P<use>)(Použijete|použijte)\s(?P<this>)(tuto)?\s?(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)(Použijete|Použijte)\s(?P<please>)(prosím)?\s?(?P<same>)(stejnou)?\s?(?P<this>)(tuto)?\s?\s(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<chooseyour>)Vyberte svou\s(?P<answer>)odpověď\s(?P<accordingto>)podle této\s(?P<card>)karty"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<choose>)Vyberte\s(?P<please>)(prosím)?\s?(?P<one>)(jednu)?\s?(?P<answer>)odpověď\s(?P<fromthis>)z této\s(?P<card>)karty"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<choose>)Vyberte\s(?P<please>)(prosím)?\s?(?P<only>)jen\s(?P<one>)jednu\s(?P<option>)(možnost)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<choose>)Vyberte\s(?P<all>)všechny"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<toanswer>)Při odpovědích\s(?P<use>)použijte\s(?P<this>)tuto\s(?P<card>)kart(u|a|y)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	return False

"""
Recognizes an instruction segment for texts written in Portuguese,
based on regex named groups patterns.

Args:
	param1 text (string): text (in Portuguese) currently being analyzed.
	param2 country_language (string): country_language metadata embedded in file name.

Returns: 
	True if the segment is an instruction or False if it is not.
"""
def instruction_recognition_portuguese(text,country_language):
	regex= r"^(?P<programador>)programador"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)entrevistador"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<continue>)seguir con la\s(?P<card>)tarjeta"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<show>)(mostrar|manter)\s(?P<gain>)(novamente)?\s?(?P<card>)cartão"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<use>)(utilize|mostrar|use)\s(?P<this>)(este|este mesmo)?\s?(?P<card>)cartão\s(?P<again>)(novamente)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<use>)utilize\s(?P<this>)este\s(?P<card>)cartão\s"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)(utilize,|use,)\s(?P<please>)(por favor)?(,)?\s?(?P<this>)este\s(?P<card>)cartão\s"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)utilize\s(?P<thesame>)o mesmo\s(?P<card>)cartão"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<continue>)continue\s(?P<show>)(mostrando|utilizando)\s(?P<this>)(este|este mesmo)?\s?(?P<card>)cartão"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		
	regex= r"^(?P<suggest>)sugerir\s(?P<categories>)categorias\s(?P<de>)de\s(?P<answer>)resposta"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		
	regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<choose>)escolha\s(?P<youranswer>)respostas\s(?P<fromthis>)deste\s(?P<card>)cartão"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)(nota)?\s?(?P<for>)(para)?\s?(?P<interviewer>)entrevistador\s(?P<code>)codifica(r)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<choose>)escolha\s(?P<option>)a afirmação\s(?P<closer>)que mais se aproxima da\s(?P<youropinion>)sua opinião"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)ler\s(?P<one>)uma\s(?P<organization>)organização\s(?P<ateachtime>)de cada vez"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)ler\s(?P<slowly>)(pausadamente)?\s?(?P<outloud>)(em voz alta)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<choose>)Escolha\s(?P<oneofthe>)uma das\s(?P<following>)(seguintes)?\s?(?P<answers>)respostas"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<askthe>)PEDIR AO\s(?P<respondent>)ENTREVISTADO\s(?P<adescription>)UMA DESCRIÇÃO"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<code>)codificar\s(?P<only>)(só)?\s?(?P<one>)uma\s(?P<answer>)resposta"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<describe>)descrever\s(?P<details>)detalhadamente"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)perguntar a\s(?P<all>)todos"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<insist>)insistir"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	return False

"""
Recognizes an instruction segment for texts written either in Spanish or Catalan,
based on regex named groups patterns.

Args:
	param1 text (string): text (in Spanish or Catalan) currently being analyzed.
	param2 country_language (string): country_language metadata embedded in file name.

Returns: 
	True if the segment is an instruction or False if it is not.
"""
def instruction_recognition_catalan_spanish(text,country_language):
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

		regex= r"^(?P<card>)targeta\s(\d+|\w+)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<continue>)seguir\s(?P<with>)amb\s(?P<the>)la\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<use>)(Utilitzi)?\s?(?P<this>)aquesta\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

   
		regex= r"^(?P<ask>)FER\s(?P<if>)SI\s(?P<interviewer>)L'ENTREVISTADOR\s(?P<codified>)HA CODIFICAT"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<use>)(utilitzi la|segueixi utilitzant|continuï utilitzant)\s(?P<this>)(aquesta)?\s?(?P<the>)(la)?\s?(?P<same>)(mateixa)?\s?(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<use>)utilitzi\s(?P<this>)aquesta\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True
		
		regex= r"^(?P<suggest>)suggerir\s(?P<categories>)categories\s(?P<de>)de\s(?P<answer>)resposta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(\,)?\s?(?P<choose>)encercli\s(?P<one>)una\s(?P<option>)opció"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<choose>)encercli\s(?P<option>)l'opció\s(?P<closer>)més propera"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<choose>)Triï\s(?P<the>)(la)?\s?(?P<your>)(seva)?\s?(?P<answer>)resposta\s(?P<fromthis>)d'aquesta\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<choose>)esculli\s(?P<one>)una\s(?P<ofthe>)(de les)?\s?(?P<answer>)(resposta|respostes)\s(?P<thatappearin>)(que apareixen en)?\s?(?P<fromthis>)(aquesta|d'aquesta)\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<read>)llegi(r|u)\s?(?P<out>)(alta)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<read>)llegi(r|u)\s(?P<each>)cada\s(?P<utterance>)afirmació"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<readorcode>)(llegir|codificar)\s(?P<each>)cada\s(?P<organization>)organització"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<note>)nota\s(?P<for>)(per|per a)\s(?P<interviewer>)(l'entrevistador|entrevistador)\s?(?P<code>)(codificar)?"
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

		regex= r"^(?P<ask>)(preguntar)?\s?a\s(?P<all>)(tothom|tots)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<if>)si\s(?P<therespondent>)l'entrevistat"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<insist>)insistiu"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

	elif 'SPA' in country_language:
		regex= r"^(?P<continue>)seguir con la\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<show>)mostrar\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<continueusing>)(siga utilizando|siga usando|use otra vez|use)\s(?P<same>)(la misma)?\s?(?P<this>)(esta)?\s?(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True


		regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<use>)(utilice|use)\s(?P<again>)(otra vez)?\s?(?P<this>)(esta)?\s?(?P<thesame>)(la misma)?\s?(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<use>)(utilice|use)\s(?P<again>)(otra vez)?\s?(?P<please>)(por favor)?(,)?\s?(?P<this>)(esta)?\s?(?P<thesame>)(la misma)?\s?(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<choose>)elija\s(?P<oneofthe>)una de las\s(?P<answers>)respuestas\s(?P<that>)que\s(?P<appearinthis>)aparecen en esta\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<suggest>)sugerir\s(?P<categories>)categorías\s(?P<de>)de\s(?P<answer>)respuesta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True
		
		regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<choose>)(escoja|elija)\s(?P<youranswer>)su respuesta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<mark>)marque\s(?P<one>)una\s(?P<option>)casilla"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<note>)nota\s(?P<for>)per\s(?P<interviewer>)el entrevistador\s(?P<code>)codificar"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True


		regex= r"^(?P<please>)(por favor)?(,)?\s?(?P<mark>)marque\s(?P<option>)la casilla\s(?P<closer>)que mejor represente\s(?P<youropinion>)su opinión"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<readorcode>)(leer|codificar)\s(?P<each>)cada\s(?P<organization>)organización"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<read>)leer\s?(?P<out>)(alto)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<read>)leer\s(?P<eachone>)una a una\s(?P<and>)(y)?\s?(?P<note>)anotar"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<ask>)(preguntar)?\s?a\s(?P<all>)todos"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<insist>)insistir"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

	return False

		