import re
import string
from ess_special_answer_categories import * 
from essmodules import * 
from evsmodules import * 



def remove_spaces_from_item_name(item_name):
	"""
	Removes spaces in item names such as A 1, because the MCSQ standard are item names without spaces (A1).

	Args:
		param1 item_name (string): item_name retrieved from the input file.
	Returns:
		item_name (string) withour spaces.
	"""
	return item_name.replace(" ", "")

def get_country_language_and_study_info(filename):
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
	if 'txt' in filename:
		filename_without_extension = re.sub('\.txt', '', filename)
		filename_split = filename_without_extension.split('_')
	else:
		filename_split = filename.split('_')

	study = filename_split[0]+'_'+filename_split[1]+'_'+filename_split[2]
	country_language = filename_split[3]+'_'+filename_split[4]

	return study, country_language


def standardize_study_metadata(study):
	"""
	Transforms study metadata present in the input file to the standard
	used in the MCSQ format.

	Args:
		param1 study (string): study metadata extracted from input file (Study column).

	Returns:
		Standardized study parameter (string).
	"""
	dict_year_round = {'ESS Round 1':'ESS_R01_2002', 'ESS Round 2':'ESS_R02_2004',
	'ESS Round 3':'ESS_R03_2006', 'ESS Round 4':'ESS_R04_2008', 'ESS Round 5':'ESS_R05_2010', 
	'ESS Round 6':'ESS_R06_2012', 'ESS Round 7':'ESS_R07_2014', 'ESS Round 8':'ESS_R08_2016',
	'ESS Round 9':'ESS_R09_2018'}

	for k,v in list(dict_year_round.items()):
		if study == k:
			return v



def standardize_supplementary_item_name(item_name):
	"""
	Standardizes the item name metadata of supplementary modules G, H and I

	Args:
		param1 item_name: item_name metadata, extracted from input file.

	Returns:
		Standardized item_name, when applicable.
	"""
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



def retrieve_supplementary_module(essmodules,item_name):
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
	for k,v in list(essmodules.modules.items()):
		if re.compile(k).match(item_name):
			return v


def retrieve_item_module(item_name, study):
	"""
	Retrieves the module of the survey_item, based on information from the ESSModulesRRR objects.
	This information comes from the source questionnaires.

	Args:
		param1 item_name (string): name of survey item, retrieved in previous steps.
		param2 study (string): study metadata, embedded in the file name.

	Returns: 
		module of survey_item (string).
	"""
	if 'ESS' in study:
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
	else:
		evsmodules = EVSModules1990()
		if item_name.lower() in evsmodules.perceptions_of_life:
				return 'Perceptions of Life'
		elif item_name.lower() in evsmodules.politics_and_society:
				return 'Politics and Society'
		elif item_name.lower() in evsmodules.environment:
				return 'Environment'
		elif item_name.lower() in evsmodules.family:
				return 'Family'
		elif item_name.lower() in evsmodules.work:
				return 'Work'
		elif item_name.lower() in evsmodules.religion_and_morale:
				return 'Religion and Morale'
		elif item_name.lower() in evsmodules.national_identity:
				return 'National Identity'
		elif item_name.lower() in evsmodules.socio_demographics:
				return 'Socio Demographics and Interview Characteristics'
		else:
			return None


def clean_text(text):
	"""
	Cleans Request, Introduction and Instruction text segments by removing
	undesired characters and standardizing some character representations.
	A string input is expected, if the input is not a string instance, 
	the method returns '', so the entry is ignored in the data extraction loop.

	Args:
		param1 text (string expected): text to be cleaned.

	Returns: 
		cleaned text (string).
	"""
	if isinstance(text, str):
		text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)
		text = re.sub('й','й', text)
		text = re.sub('Й','Й', text)
		text = re.sub('å','å', text)
		text = re.sub('ö','ö', text)
		text = re.sub('Ö','Ö', text)
		text = re.sub('ä','ä', text)
		text = re.sub('ů','ů', text)
		text = re.sub('ý','ý', text)
		text = re.sub('č','č', text)
		text = re.sub('Č','Č', text)
		text = re.sub('ě','ě', text)
		text = re.sub('Ě','Ě', text)
		text = re.sub('Ď','Ď', text)
		text = re.sub('ţ','ţ', text)
		text = re.sub('Ţ','Ţ', text)
		text = re.sub('Š','Š', text)
		text = re.sub('š', 'š', text)
		text = re.sub('ř', 'ř', text)
		text = re.sub('Ř', 'Ř', text)
		text = re.sub('Ä','Ä', text)
		text = re.sub('Á','Á', text)
		text = re.sub('Å','Å', text)
		text = re.sub('ü','ü', text)
		text = re.sub('ê','ê', text)
		text = re.sub('Ê','Ê', text)
		text = re.sub('è','è', text)
		text = re.sub('í','í', text)
		text = re.sub('î','î', text)
		text = re.sub('é','é', text)
		text = re.sub('ó','ó', text)
		text = re.sub('Í','Í', text)
		text = re.sub('ú','ú', text)
		text = re.sub('à','à', text)
		text = re.sub('Ó','Ó', text)
		text = re.sub('õ','õ', text)
		text = re.sub('ã','ã', text)
		text = re.sub('Ã','Ã', text)
		text = re.sub('ô','ô', text)
		text = re.sub('û','û', text)
		text = re.sub('ï','ï', text)
		text = re.sub('á','á', text)
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
		text = re.sub('Q[0-9]+\.', "",text)
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


def expand_interviewer_abbreviations(text, country_language):
	"""
	Switches abbreviations of the word interviewer for the full form.

	Args:
		param1 text (string): sentence being analyzed.
		param2 country_language (string): country_language metadata embedded in file name.

	Returns: 
		text (string) without abbreviations for the word interviewer, when applicable.
	"""
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


def instantiate_special_answer_category_object(country_language):
	"""
	Instantiates the SpecialAnswerCategories object that stores both the text
	and category values of the special answers (don't know, refusal, not applicable 
	and write down) in accordance to the country_language metadata parameter.

	Args:
		param1 country_language (string): country_language metadata parameter, embedded in file name.

	Returns: 
		instance of SpecialAnswerCategories object (Python object), in accordance to the country_language.
	"""
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


def check_if_answer_is_special_category(text, answer_value, ess_special_answer_categories):
	"""
	Verifies if a given answer segment is one of the special answer categories,
	by testing the answer text against the attributes of SpecialAnswerCategories object.
	This method serves the purpose of standardizing the special answer category values.

	Args:
		param1 text (string): answer segment currently being analyzed.
		param2 answer_value (string): answer category value, defined in clean_answer() method.
		param3 ess_special_answer_categories (Python object): instance of SpecialAnswerCategories object, in accordance to the country_language.

	Returns: 
		answer text (string) and its category value (string). When the answer is a special answer category, 
		the text and category values are the ones stored in the SpecialAnswerCategories object.
	"""
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
	"""
	Cleans the answer segment, by standardizing the text (when it is a special answer category),
	and attributing an category value to it. 

	Args:
		param1 text (string): answer segment currently being analyzed.
		param2 ess_special_answer_categories (Python object): instance of SpecialAnswerCategories object, in accordance to the country_language.

	Returns: 
		answer text (string) and its category value (string). When the answer is a special answer category, 
		the text and category values are the ones stored in the SpecialAnswerCategories object.
	"""
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
	elif re.compile(r'^012\s\w+').match(text):
		text = text.split('012', 1)
		answer_text = text[1].rstrip()
		answer_value = '12'
	elif re.compile(r'^02\s\w+').match(text):
		text = text.split('02', 1)
		answer_text = text[1].rstrip()
		answer_value = '2'
	elif re.compile(r'^03\s\w+').match(text):
		text = text.split('03', 1)
		answer_text = text[1].rstrip()
		answer_value = '3'
	elif re.compile(r'^04\s\w+').match(text):
		text = text.split('04', 1)
		answer_text = text[1].rstrip()
		answer_value = '4'
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
	elif re.compile(r'^09\s\w+').match(text):
		text = text.split('09', 1)
		answer_text = text[1].rstrip()
		answer_value = '9'
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
	elif re.compile(r'^G\s.+').match(text):
		text = text.split('G', 1)
		answer_text = text[1].rstrip()
		answer_value = 'G'
	elif re.compile(r'^N\s.+').match(text):
		text = text.split('N', 1)
		answer_text = text[1].rstrip()
		answer_value = 'N'
	elif re.compile(r'^Z\s.+').match(text):
		text = text.split('Z', 1)
		answer_text = text[1].rstrip()
		answer_value = 'Z'
	elif re.compile(r'^T\s.+').match(text):
		text = text.split('T', 1)
		answer_text = text[1].rstrip()
		answer_value = 'T'
	elif re.compile(r'^Y\s.+').match(text):
		text = text.split('Y', 1)
		answer_text = text[1].rstrip()
		answer_value = 'Y'
	elif re.compile(r'^Q\s.+').match(text):
		text = text.split('Q', 1)
		answer_text = text[1].rstrip()
		answer_value = 'Q'
	elif re.compile(r'^E\s.+').match(text):
		text = text.split('E', 1)
		answer_text = text[1].rstrip()
		answer_value = 'E'
	elif re.compile(r'^L\s.+').match(text):
		text = text.split('L', 1)
		answer_text = text[1].rstrip()
		answer_value = 'L'
	elif re.compile(r'^B\s.+').match(text):
		text = text.split('B', 1)
		answer_text = text[1].rstrip()
		answer_value = 'B'
	elif re.compile(r'^55\s.+').match(text):
		text = text.split('55', 1)
		answer_text = text[1].rstrip()
		answer_value = '55'
	elif re.compile(r'^\+4\s.+').match(text):
		text = text.split('+4', 1)
		answer_text = text[1].rstrip()
		answer_value = '+4'
	elif re.compile(r'^\+3\s.+').match(text):
		text = text.split('+3', 1)
		answer_text = text[1].rstrip()
		answer_value = '+3'
	elif re.compile(r'^\+2\s.+').match(text):
		text = text.split('+2', 1)
		answer_text = text[1].rstrip()
		answer_value = '+2'
	elif re.compile(r'^\+1\s.+').match(text):
		text = text.split('+1', 1)
		answer_text = text[1].rstrip()
		answer_value = '+1'
	elif re.compile(r'^\-4\s.+').match(text):
		text = text.split('-4', 1)
		answer_text = text[1].rstrip()
		answer_value = '-4'
	elif re.compile(r'^\-3\s.+').match(text):
		text = text.split('-3', 1)
		answer_text = text[1].rstrip()
		answer_value = '-3'
	elif re.compile(r'^\-2\s.+').match(text):
		text = text.split('-2', 1)
		answer_text = text[1].rstrip()
		answer_value = '-2'
	elif re.compile(r'^\-1\s.+').match(text):
		text = text.split('-1', 1)
		answer_text = text[1].rstrip()
		answer_value = '-1'
	else:
		answer_text = text.strip()
		answer_value = None

	answer_text = answer_text.strip()
	answer_text, answer_value = check_if_answer_is_special_category(answer_text, answer_value, ess_special_answer_categories)

	return answer_text, answer_value



def check_if_segment_is_instruction(sentence, country_language):
	"""
	Calls the appropriate instruction recognition method, according to the language.
	
	Args:
		param1 sentence (string): sentence being analyzed in outer loop of data extraction.
		param2 country_language (string): country_language metadata, embedded in file name.

	Returns: 
		bypass the return of instruction_recognition methods (boolean).
	"""
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


def instruction_recognition_russian(text,country_language):
	"""
	Recognizes an instruction segment for texts written in Russian,
	based on regex named groups patterns.

	Args:
		param1 text (string): text (in Russian) currently being analyzed.
		param2 country_language (string): country_language metadata embedded in file name.

	Returns: 
		True if the segment is an instruction or False if it is not.
	"""
	text_aux = text
	text = text.translate(str.maketrans(' ', ' ', string.punctuation))

	regex= r"^(?P<interviewer>)(ИНТЕРВЬЮЕР|ИНТЕРВЬЮЕРА)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '№' not in text_aux:
		return True

	regex= r"^(?P<note>)ЗАМЕЧАНИЕ\s(?P<to>)ДЛЯ\s(?P<interviewer>)(ИНТЕРВЬЮЕР|ИНТЕРВЬЮЕРА|ИНТЕРЬВЬЮЕРА)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)ПРИМЕЧАНИЕ\b"
	matches = re.search(regex, text)
	if matches:
		return True
		

	regex= r"^(?P<readout>)(ЗАЧИТАТЬ|ЗАЧИТАЙТЕ|ЗАЧИТАЙТЕ|ЗАЧИТАЙТ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<listofinstitutions>)СПИСОК\sИНСТИТУЦИЙ\s(?P<read>)(ЗАЧИТАТЬ|ЗАЧИТАЙТЕ|ЗАЧИТАЙТЕ|ЗАЧИТАЙТ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<alternatives>)(АЛЬТЕРНАТИВЫ)?\s?(?P<dont>)НЕ\s(?P<read>)(ЗАЧИТЫВАТЬ|ЧИТАТЬ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)СПРОСИТЕ\s(?P<again>)ЕЩЕ\sРАЗ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)СПРOСИТЬ\s(?P<ifdoesnotlivewithspouse>)ЕСЛИ\sНЕ\sЖИВЕТ\sС\sСУПРУГОМ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<after>)ПОСЛЕ\sТОГО\s(?P<therespondent>)КАК\sРЕСПОНДЕНТ\s(?P<answers>)ДАСТ\sОТВЕТ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<possible>)ВОЗМОЖЕН\s(?P<oneanswer>)(ТОЛЬКО\sОДИН\sОТВЕТ|ОДИН\sВЫБОР)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<checkall>)(ОТМЕТЬТЕ|ВЫБЕРИТЕ|КОДИРУЕТЕ|Назовите)\sВСЕ\s(?P<thatapplies>)(ЧТО\sПОДХОДИТ|КОТОРЫЕ\sПОДХОДЯТ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<name>)НАЗЫВАЙТЕ\s(?P<groups>)ГРУППЫ\s(?P<peopleororganization>)ЛЮДЕЙ ИЛИ ОРГАНИЗАЦИИ "
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<options>)(ВАРИАНТЫ|УТВЕРЖДЕНИЯ)?\s?(?P<read>)(ПРОЧИТАТЬ|ЗАЧИТАЙТЕ)\s(?P<out>)ВСЛУХ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<write>)(ВПИШИТЕ|ЗАПИШИТЕ)\s(?P<duration>)(ПРОДОЛЖИТЕЛЬНОСТЬ|СКОЛЬКО\sВРЕМЕНИ|КОЛИЧЕСТВО\sВРЕМЕНИ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<read>)ПРОЧИТАЙТЕ\s(?P<each>)КАЖДОЕ\s(?P<utterance>)УТВЕРЖДЕНИЕ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
	    
	regex= r"^(?P<ask>)ОПРОСИТЕ\s(?P<respondent>)РЕСПОНДЕНТА\s?(?P<use>)(ОТКРЫТЬ)?\s?(?P<card>)(КАРТОЧКУ)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	
	regex= r"^(?P<read>)ЗАЧИТЫВАЙТЕ\s(?P<by>)ПО\s(?P<each>)КАЖДОЙ\s(?P<line>)СТРОКЕ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ifyouthink>)Если\s(Вы|вы)\sсчитаете\s(?P<thatthis>)(что)?\s?(эти|Ваш|Ваша|эта|этот|свой)\s(?P<income>)(неттодоход|доходы|разница|различия|доход|зарплата|заработок)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

 
	regex= r"^(?P<one>)ОДИН\s(?P<answer>)ОТВЕТ\s?(?P<in>)(В)?\s?(?P<each>)(КАЖДОЙ)?\s?(?P<line>)(СТРОКЕ)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
   
	regex= r"^(?P<canmark>)МОЖНО ОТМЕТИТЬ\s(?P<more>)БОЛЬШЕ\s(?P<than>)ЧЕМ\s(?P<one>)ОДИН\s(?P<answer>)(ОТВЕТ|ВАРИАНТ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<mark>)(ОТМЕТИТЬ|ОТМЕТЬТЕ)\s(?P<only>)ТОЛЬКО\s(?P<one>)ОДИН\s(?P<answer>)(ОТВЕТ|ВАРИАНТ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	 
	regex= r"^(?P<note>)(ПРИМЕЧАНИЕ|ПОЯСНЕНИЕ|ПРИМЕЧАНИЯ)\s(?P<interviewer>)(ИНТЕРВЬЮЕРУ|ОПРАШИВАЮЩЕМУ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)Пожалуйста\s(?P<choose>)выберите\s(?P<nomorethantwo>)не\sболее\sдвух"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<please>)Пожалуйста\s(?P<choose>)выберите\s(?P<optionclosesttoyourview>)мнение\sнаиболее\sблизкое\sвашим\sвзглядам"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"(?P<again>)(СНОВА|CHOBA)?\s?(?P<use>)(ИСПОЛЬЗУЙТЕ)?\s?(?P<card>)(КАРТОЧКА|КАРТОЧКУ|KAРTOЧКА)\s(?P<number>)(Nr|\d+|\w+)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<show>)ПОДАЙТЕ\s(?P<respondent>)РЕСПОНДЕНТУ\s(?P<card>)(КАРТОЧКА|КАРТОЧКУ|KAРTOЧКА)\s(?P<number>)(Nr|\d+|\w+)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<next>)ДАЛЕЕ\s(?P<ask>)ЗАДАЙТЕ\s(?P<question>)ВОПРОСЫ\s(?P<all>)ВСЕМ\s(?P<respondents>)РЕСПОНДЕНТАМ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<choose>)Выберите\s(?P<youranswer>)ответ\sпо\sследующей\sскале\s(?P<card>)карточке"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True
		  

	regex= r"^(?P<respondent>)(РЕСПОНДЕНТ|РЕСПОНДЕНТЫ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<for>)ДЛЯ\s(?P<respondent>)РЕСПОНДЕНТОВ\s(?P<male>)МУЖСКОГО ПОЛА"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<respondent>)Отвечают\s(?P<malefemale>)(женщины|мужчины)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

  
	regex= r"^(?P<mark>)ОТМЕТЬТЕ\s(?P<one>)ОДНО\s(?P<option>)ЧИСЛО"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<mark>)ОТМЕТЬТЕ\s(?P<answers>)ОТВЕТ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<possible>)ВОЗМОЖЕ(Н|Т)\s(?P<one>)ОДИН\s(?P<answer>)(ОТВЕТ|ВЫБОР)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<insist>)(УТОЧНИТЕ|Спросите|ВЫЯСНИТЕ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		  

	regex= r"^(?P<ask>)(СПАШИВАТЬ|СПРАШИВАТЬ|СПРОСИТЬ|СПРАШИВАЙТЕ|СПРОСИТЕ|СПРАШИВАИТE|ЗАДАВАТЬ)\s(?P<to>)(У)?\s?(?P<all>)(ВСЕХ|ВСЕМ)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

		 
	regex= r"^(?P<code>)КОДИРОВАТЬ\s(?P<all>)ВСЕ(Х)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)Пожалуйста\s(?P<selectyouranswer>)выберите\s(свой)?\s?ответ\s(?P<fromoptions>)(среди|из)\s(вариантовт|вариантов)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<ask>)(ОТМЕТЬТЕ|ВЫБЕРИТЕ)\s(?P<all>)ВСЕ\s?(?P<applicable>)(ПОДХОДЯЩИЕ)?"
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

	regex= r"^(?P<use>)Воспользуйтесь\s(?P<thesame>)той же\s(?P<card>)(карточкой|карточку)\s?(?P<toanswer>)(Для ответа|Для ответов)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<use>)Используйте\s(?P<please>)пожалуйста\s(?P<this>)эту\s(?P<card>)карточку\s(?P<toanswer>)(Для ответа|Для ответов)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux:
		return True


	regex= r"^(?P<please>)пожалуйста\s(?P<use>)Используйте\s(?P<this>)эту\s(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<toanswer>)(Для ответа|Для ответов)?\s?(?P<again>)(снова)?\s?(?P<use>)используйте\s(?P<please>)(пожалуйста)?\s?(?P<this>)эту\s(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<toanswer>)(Для ответа|Для ответов)\s(?P<again>)(снова)?\s?(?P<use>)(воспользуйтесь|пользуйтесь)\s(?P<please>)(пожалуйста)?\s?(?P<this>)(этой)?\s?(?P<thesame>)(той же)?\s?(?P<card>)(карточкой|карточку)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<toanswer>)(Для ответа|Для ответов)?\s?(?P<please>)(Пожалуйста)?\s?(?P<use>)(воспользуйтесь|пользуйтесь)\s(?P<this>)(этой|шкалой)\s(?P<on>)(на)?\s?(?P<card>)(карточки|карточкой|карты|карточке)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<please>)(Пожалуйста)?\s?(?P<select>)Выберите\s(?P<your>)(свой)?\s?(?P<one>)(один)?\s?(?P<answer>)ответ\s(?P<of>)из\s(?P<this>)этой\s(?P<card>)(карточки|карточкой|карты|карточке|карте)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<please>)(Пожалуйста)?\s?(?P<select>)Выберите\s(?P<your>)(свой)?\s?(?P<one>)(один)?\s?(?P<answer>)ответ\s(?P<this>)(этой)?\s?(?P<of>)(из)?\s?(?P<proposed>)(предложенных)?\s?(?P<on>)(на)?\s?(?P<card>)(карточки|карточкой|карты|карточке|карте)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<please>)(Пожалуйста)?\s?(?P<select>)Выберите\s(?P<answer>)ответ\s(?P<of>)из\s(?P<proposed>)предложенных\s(?P<on>)на\s(?P<this>)этой\s(?P<card>)карточке"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True
   


	regex= r"^(?P<select>)Выберите\s(?P<your>)свой\s(?P<answer>)ответ\s(?P<on>)на\s(?P<this>)этой\s(?P<card>)карте"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<please>)(Пожалуйста)?\s?(?P<select>)Выберите\s(?P<answer>)ответ\s(?P<of>)из\s(?P<proposedat>)(предложенных на)?\s?(?P<this>)этой\s(?P<card>)карточки"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<select>)Выберите\s(?P<please>)(пожалуйста)?\s?(?P<of>)из\s(?P<this>)этой\s(?P<card>)карточки"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<select>)Выберите\s(?P<please>)(пожалуйста)?\s?(?P<answer>)ответ\s(?P<of>)из\s(?P<card>)карточки"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<please>)(Пожалуйста)?\s?(?P<select>)(Выберите|выберите)\s(?P<your>)(свой)?\s?(?P<answer>)ответ\s(?P<of>)из\s(?P<options>)вариантов\s(?P<proposed>)(предложенных)?\s?(?P<on>)на\s(?P<tjis>)(этой)?\s?(?P<card>)(карточки|карточке)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<select>)(ОТМЕТЬТЕ|Выберите)\s(?P<all>)(ВСЕ|все)\s(?P<that>)(ПОХОДЯЩИЕ|которые)\s(?P<applies>)(ВАРИАНТЫ|подходят)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<select>)(Выберите|ОТМЕТЬЕ)\s(?P<please>)(Пожалуйста)?\s?(?P<answer>)ответ\s(?P<of>)из\s(?P<this>)этой\s(?P<card>)карточки"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<select>)(Выберите|ОТМЕТЬЕ)\s(?P<please>)(Пожалуйста)?\s?(?P<only>)(только)?\s?(?P<one>)один\s(?P<option>)(вариант)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<please>)(Пожалуйста)?\s?(?P<select>)(отметьте|выберите)\s(?P<only>)только\s(?P<one>)один\s(?P<option>)(вариант)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<select>)Отметить\s(?P<please>)(Пожалуйста)?\s?(?P<only>)(только)?\s?(?P<one>)один\s(?P<option>)вариант"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<please>)(Пожалуйста)?\s?(?P<select>)выберите\s(?P<all>)все\s(?P<options>)варианты\s(?P<answer>)ответа\s(?P<on>)на\s(?P<card>)(карточки|карточкой|карты|карточке)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<please>)(Пожалуйста)?\s?(?P<select>)Выберите\s(?P<on>)на\s(?P<card>)(карточки|карточкой|карты|карточке)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<please>)(Пожалуйста)?\s?(?P<use>)используйте\s(?P<toanswer>)(Для ответа|Для ответов)\s(?P<this>)эту\s(?P<card>)(карточки|карточкой|карточку|карточке)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<please>)(Пожалуйста)?\s?(?P<mark>)отметьте\s(?P<one>)один\s(?P<option>)квадрат"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<answer>)ОТВЕЧАЮТ\s(?P<all>)ВСЕ\s(?P<respondents>)РЕСПОНДЕНТЫ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<again>)(СНОВА)?\s?(?P<card>)(КАРТА|КАРТОЧКА)\s(?P<continue>)(ПРОДОЛЖАЕТСЯ)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<toanswer>)(Для ответа|Для ответов)?\s?(?P<please>)(Пожалуйста)?\s?(?P<now>)(Теперь)?\s?(?P<use>)используйте\s(?P<this>)эту\s(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True



	regex= r"^(?P<toanswer>)(Для ответа|Для ответов)?\s?(?P<please>)(пожалуйста)?\s?(?P<now>)(Теперь)?\s?(?P<use>)(Используйте|используйте|используйте)\s(?P<this>)(эту|ту)\s(?P<same>)(же)\s?(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<please>)(пожалуйста)?\s?(?P<now>)(Теперь)?\s?(?P<use>)(Используйте|используйте|используйте)\s(?P<toanswer>)(Для ответа|Для ответов)?\s?(?P<this>)(эту|ту)\s(?P<same>)(же)\s?(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<toanswer>)(Для ответа|Для ответов)\s(?P<use>)(используйте|пользуйтесь)\s(?P<please>)(пожалуйста)?\s?(?P<card>)(карточку|карточкой)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<check>)(Заполните|Отметьте)\s(?P<please>)(пожауйста|пожалуйста|пожалуйста)?\s?(?P<only>)(только)?\s?(?P<one>)(один|одну)\s(?P<box>)(ячейку|клетку|ответ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<please>)(пожалуйста)?\s?(?P<check>)отметьте\s(?P<one>)один\s(?P<box>)квадрат"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<use>)Используйте\s(?P<please>)(пожалуйста|пожалуйста)?\s?(?P<this>)(эту)?\s?(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<please>)(пожалуйста|пожалуйста)?\s?(?P<use>)Используйте\s(?P<toanswer>)(Для ответа|Для ответов)\s(?P<this>)эту\s(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

  
	regex= r"^(?P<check>)ОТМЕТЬТЕ\s(?P<all>)ВСЕ\s(?P<answers>)НАЗВАННЫЕ ОТВЕТЫ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<toanswer>)(Для ответа|Для ответов)\s(?P<please>)(пожалуйста)?\s?(?P<use>)используйте\s(?P<this>)(эту)?\s?(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<possible>)МОЖНО\s(?P<check>)ОТМЕТИТЬ\s(?P<more>)БОЛЬШЕ\s(?P<than>)ЧЕМ\s(?P<one>)ОДИН\s(?P<answer>)ОТВЕТ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<mark>)(Заполните|Отметьте)\s(?P<please>)(пожалуйста)?\s?(?P<one>)одну\s(?P<box>)клетку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<read>)(ПРОЧИТАЙТЕ|ЗАЧИТАТЬ)\s(?P<each>)КАЖДОЕ\s(?P<utterance>)УТВЕРЖДЕНИЕ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)ОТМЕТЬТЕ\s(?P<only>)(ТОЛЬКО)?\s?(?P<one>)ОДИН\s(?P<option>)(ВАРИАНТ|КОД|ЧИСЛО)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<write>)ВПИШИТЕ\s(?P<only>)ТОЛЬКО\s(?P<one>)ОДИН"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<readout>)ЗАЧИТЫВАЙТЕ\s(?P<by>)ПО\s(?P<each>)КАЖДОЙ\s(?P<line>)СТРОКЕ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<readout>)(ЗАЧИТЫВАЙТЕ|ЗАЧИТАЙТЕ)\s(?P<questions>)ВОПРОСЫ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<questions>)ВОПРОСЫ\s(?P<readout>)(ЗАЧИТЫВАЙТЕ|ЗАЧИТАЙТЕ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<readout>)(ЗАЧИТЫВАЙТЕ|ЗАЧИТАЙТЕ)\s(?P<statements>)УТВЕРЖДЕНИЯ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)Используйте\s(?P<the>)ту\s(?P<same>)(же|самую)\s(?P<card>)карту"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<check>)ОТМЕЧАТЬ\s(?P<all>)ВСЕ\s(?P<that>)КОТОРЫЕ\s(?P<apply>)ПОДХОДЯТ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<show>)ПОДАЙТЕ\s(?P<respondent>)РЕСПОНДЕНТУ\s(?P<card>)(КАРТОЧКУ|карточка)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<the>)ТА\s(?P<same>)ЖЕ\s(?P<card>)(КАРТОЧКУ|карточка)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True
  
	regex= r"^(?P<ask>)(ЗАДАЙТЕ|ЗАДАВАТЬ|ЗАДАВАЙТЕ)\s(?P<questions>)(ВОПРОСЫ|ВОПРОС)\s?(?P<everyone>)(ВСЕМ)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<readout>)(ЗАЧИТЫВАЙТЕ|ЗАЧИТАЙТЕ)\s(?P<questions>)(ВОПРОСЫ|ВОПРОС)\s(?P<mark>)(ОТМЕЧАЙТЕ)?\s?(?P<answer>)(ОТВЕТ)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<this>)ЭТОТ\s(?P<question>)ВОПРОС\s(?P<show>)ЗАДАЙТЕ\s(?P<all>)(ВСЕМ|ВСЕ|ВСЕX)\s(?P<respondent>)(РЕСПОНДЕНТА|РЕСПОНДЕНТУ|РЕСПОНДЕНТЫ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Пожалуйста)?\s?(?P<select>)выберите\s(?P<one>)один\s(?P<answer>)ответ\s(?P<on>)(на|из)\s(?P<this>)этой\s(?P<card>)(карточке|карточки)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<select>)(Выберите|Выбирите)?\s?(?P<your>)(Ваш)?\s?(?P<please>)(пожалуйста)?\s?(?P<answer>)ответ\s(?P<from>)из\s(?P<this>)этой\s(?P<card>)(карточке|карточки)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True


	regex= r"^(?P<use>)Используйте\s(?P<still>)(все еще)?\s?(?P<toanswer>)(Для ответа|Для ответов)?\s?(?P<this>)(эту)?\s?(?P<card>)(карточке|карточки|карточку)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<select>)Выберите\s(?P<your>)(Ваш|свой)\s(?P<answer>)ответ\s(?P<on>)на\s(?P<this>)(этой)?\s?(?P<card>)(карточке|карточки|карточку)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<select>)Выберите\s(?P<please>)пожалуйста\s(?P<one>)один\s(?P<answer>)ответ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<still>)Все еще\s(?P<use>)используйте\s(?P<card>)(карточке|карточки|карточку)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<toanswer>)(Для ответа|Для ответов)\s(?P<use>)используйте\s(?P<please>)(Пожалуйста)?\s?(?P<card>)(карточке|карточки|карточку)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<please>)Пожалуйста\s(?P<use>)используйте\s(?P<this>)(эту)?\s?(?P<card>)карточку"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

	regex= r"^(?P<please>)(Пожалуйста)?\s?(?P<use>)используйте\s(?P<thesame>)(ту же|ту же самую)?\s?(?P<card>)(карточку|карту)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'оцените' not in text and 'чтобы показать' not in text and 'где бы Вы поместили себя' not in text and 'которые я назову' not in text and 'скажите' not in text and 'ответьте' not in text and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
		return True

 
	regex= r"^(?P<note>)(ПРИМЕЧАНИЕ)?\s?(?P<to>)ДЛЯ\s(?P<interviewer>)ИНТЕРВЬЮЕРА"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<if>)ЕСЛИ\s(?P<not>)НЕ\s(?P<born>)(РОДИЛСЯ|РОДИЛАСЬ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<choose>)Выберите\s(?P<youranswer>)свой ответ\s(?P<fromcard>)на карте"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'поместили себя' not in text_aux:
		return True

  
	regex= r"^(?P<ask>)ПОПРОСИТЕ\s(?P<respondent>)РЕСПОНДЕНТА"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<giveascoreofn>)дайте\sоценку\s\d+"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'поместили себя' not in text_aux:
		return True

	regex= r"(?P<wherenmeans>)(если|где)?\s?\d\s(баллов)?\s?означает\s(?P<anything>).*\s(?P<andnmeans>)(а|и)\s\d+\s(означает)?"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'поместили себя' not in text_aux:
		return True

	regex= r"(?P<wherenmeans>)(если|где)?\s?\d\sзначит\s(?P<anything>).*\s(?P<andnmeans>)(а|и)\s\d+\s(значит)?"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'поместили себя' not in text_aux:
		return True

	regex= r"(?P<wherenmeans>)где\s\d\s(?P<anything>).*\s(?P<andnmeans>)(а|и)\s\d+"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'поместили себя' not in text_aux:
		return True


	regex= r"(?P<nmeans>)\d+\s(-\s?)?\s?означает\s(?P<anything>).*\s(?P<andnmeans>)(а|и)?\s?\d+\s(-\s?)?\s?означает"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'поместили себя' not in text_aux:
		return True

	regex= r"(?P<anynumber>)любую\sцифру\s(?P<fromnton>)от\s\d\sдо\s\d+(?P<whichbetterreflectsyouropinion>)образом\sотражает\sВаше\sмнение"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'поместили себя' not in text_aux:
		return True


	regex= r"(?P<probe>)РАССЛЕДОВАТE"
	matches = re.findall(regex, text)
	if matches:
		return True

	regex= r"(?P<insertnomorethannlanguages>)УКАЗАТЬ\sНЕ\sБОЛЕЕ\s\d\sЯЗЫКОВ"
	matches = re.findall(regex, text)
	if matches:
		return True


	regex= r"(?P<acceptestimations>)РЕСПОНДЕНТ МОЖЕТ УКАЗАТЬ ПРИБЛИЗИТЕЛЬНО"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True

	regex= r"(?P<roundup>)(ОКРУГЛИТЕ ДО|ОКРУГЛЯЙТЕ)"
	matches = re.findall(regex, text)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True

	regex= r"(?P<ifrespondent>)ЕСЛИ РЕСПОНДЕНТ"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True

	regex= r"(?P<askallrespondents>)ЗАДАЙТЕ\s(ЭТОТ)?\s?(ВОПРОС|ВОПРОСЫ)\s(ВСЕМ)?\s?РЕСПОНДЕНТАМ"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True

	regex= r"(?P<consideradoptions>)УСЫНОВЛЕНИЕ/УДОЧЕРЕНИЕ ТАК ЖЕ УЧИТЫВАЕТСЯ"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True

	regex= r"(?P<considerworkdays>)ПОЛНЫЙ И НЕПОЛНЫЙ РАБОЧИЙ ДЕНЬ СЧИТАЙТЕ ОДИНАКОВО"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True




def instruction_recognition_german(text,country_language):
	"""
	Recognizes an instruction segment for texts written in German,
	based on regex named groups patterns.

	Args:
		param1 text (string): text (in German) currently being analyzed.
		param2 country_language (string): country_language metadata embedded in file name.

	Returns: 
		True if the segment is an instruction or False if it is not.
	"""
	text_aux = text
	text = text.translate(str.maketrans(' ', ' ', string.punctuation))

	regex= r"^(?P<for>)(FÜR)?\s?(?P<interviewer>)(Befrager|Interviewer)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and "Interviewer ID" not in text:
		return True

	regex= r"^(?P<round>)Runden\b"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	
	regex= r"^(?P<informal>)INFORMELL:"
	matches = re.search(regex, text_aux)
	if matches:
		return True

	regex= r"^(?P<attention>)ACHTUNG:"
	matches = re.search(regex, text_aux)
	if matches:
		return True


	regex= r"^(?P<round>)ANM:"
	matches = re.search(regex, text_aux)
	if matches:
		return True

	regex= r"^(?P<estimation>)(Schätzung|SCHÄTZWERTE)\s?(?P<accept>)akzeptieren\b"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<checkeachapplicable>)Jeweils\sZutreffendes"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<all>)(Alles)?\s?(?P<each>)(Jeweils)?\s?(?P<circleabove>)Genannte(s)?\s(Stufe)?\s?einkreisen"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<againaccordingto>)Wieder\snach\sgrünem\sBildblatt"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<again>)(Immer noch|Weiterhin|Weiter|Und noch die|Noch einmal)?\s?(?P<card>)(karte\s(\d+|[a-z]+)|liste\s(\d+|[a-z]+))"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux:
		return True

	regex= r"^(?P<untilquestionx>)(bis\s\w\d+)?\s?(?P<card>)(karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<insist>)(NACHFRAGEN|NACHFASSEN)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<probeonce>)EINMAL\sNACHHAKEN"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<probe>)Zusatzfrage"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(bitte)?\s?(?P<readoutstatements>)JEDE(S)?\s(STATEMENT|AUSSAGE)\sVORLESEN"
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

	regex= r"^(?P<askall>)Alle\sfragen"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<codeduration>)(DAUER|ZEIT)\sEINTRAGEN"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<a>)(AN)?\s?(?P<male>)(MÄNNLICHE|Weibliche)\s(?P<respondent>)BEFRAGTE"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<questionsfor>)FRAGEVERSION\sFÜR\s(?P<malefemale>)(MÄNNER|FRAUEN)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<codeall>)ZUTREFFENDES\sBITTE\sKODIEREN"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
	  

	regex= r"(?P<givetwoanswers>)Geben\sSie\sbis\szu\szwei\sAntworten"
	matches = re.search(regex, text)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True


	regex= r"(?P<ifyouthink>)Wenn\sSie\s(glauben|finden)?\s?(?P<that>)(dass)?\s?(?P<these>)(Ihr|diese(s|r)?|Ihren)\s(Einkommen|Unterschiede|Verdienst)"
	matches = re.search(regex, text)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True


	regex= r"(?P<ifyouthink>)Wenn\sSie\s(?P<yourincome>)Ihren\sLohn"
	matches = re.search(regex, text)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True


	regex= r"^(?P<please>)(bitte)?\s?(?P<markall>)MARKIEREN\sSIE\sALLES"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(bitte)?\s?(?P<use>)(Verwenden|benutzen|nutzen)\sSie\s(?P<also>)(auch)?\s?(?P<to>)(dazu)?\s?(?P<forthis>)(dafür)?\s?(?P<the>)(die)?\s?(?P<this>)(diese)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(bitte)\s(?P<answer>)beantworten\sSie\s(?P<this>)diese\s(?P<question>)Frage"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(bitte)\s(?P<answer>)sagen\sSie\s(?P<tomeusing>)es mir anhand\s(?P<this>)dieser"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True
   
	regex= r"^(?P<please>)(bitte)?\s?(?P<use>)(Verwenden|benutzen|nutzen)\sSie\s(?P<again>)dazu\swieder\s(?P<the>)(die|diese)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<use>)(Verwenden|benutzen|nutzen)\sSie\s(?P<again>)dazu\s(?P<please>)(bitte)?\s?(?P<the>)(die)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<tellme>)(Sagen Sie es mir)?\s?(?P<please>)bitte\s(?P<answer>)(antworten sie)?\s?(?P<again>)(wieder)?\s?(?P<using>)anhand von\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<use>)(Verwenden|benutzen|Benützen|nutzen)\sSie\s(?P<now>)(jetzt|nun)?\s?(?P<please>)(bitte)?\s?(?P<the>)(die|diese)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(bitte)?\s?(?P<use>)(Verwenden|benutzen|nutzen)\s(Sie|Die)\s(?P<onceagain>)noch einmal\s(?P<this>)(diese)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(bitte)?\s?(?P<mark>)Nennen\s(Sie|Die)\s(?P<all>)alles"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True


	regex= r"^(?P<note>)Hinweis\s(?P<for>)für\s(?P<the>)(den)?\s?(?P<interviewer>)(Interviewer|Befrager)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<tick>)kreuzen\s(?P<a>)Sie ein\s(?P<box>)Kästchen an"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<tick>)kreuzen\s(?P<a>)Sie bitte ein\s(?P<box>)Kästchen an"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<use>)(Verwenden|benutzen|nutzen)\s(?P<this>)Sie\s(diese|die)?\s?(?P<same>)(selbe)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<use>)(Verwenden|benutzen|nutzen)\s(?P<this>)Sie dafür diese\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<use>)(Verwenden|benutzen|nutzen)\s(?P<again>)Sie nochmals\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<again>)nochmals\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<answer>)sagen Sie\s(?P<forme>)(es mir|es bitte)\s(?P<again>)(noch einmal|nochmals)?\s?(?P<withthis>)(anhand von dieser|anhand dieser|anhand von)\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True


	regex= r"^(?P<please>)(Bitte)?\s?(?P<use>)(Verwenden|benutzen|nutzen)\s(?P<this>)Sie\s(?P<again>)(wieder|wieder diese)\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<use>)(Verwenden|benutzen|nutzen)\s(?P<please>)Sie bitte\s(?P<again>)(wieder|wieder diese)\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<use>)(Verwenden|benutzen|nutzen)\s(?P<toanswer>)Sie für Ihre Antwort\s(?P<again>)(wieder|die gleiche|nochmals)?\s?(?P<the>)(die|diese|der|von)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True


	regex= r"^(?P<please>)(Bitte)?\s?(?P<this>)diese\s(?P<card>)(Karte|liste)\s(?P<use>)verwenden"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<use>)verwenden\s(?P<please>)Sie bitte\s(?P<this>)(diese)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<use>)verwenden\s(?P<this>)(die|diese)\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<use>)verwenden\s(?P<this>)Sie diese\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<mark>)ringeln\s(?P<a>)Sie eine\s(?P<answer>)Antwortzahl"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<only>)NUR\s(?P<one>)EINE\s(?P<answer>)(ANTWORT|NENNUNG|Angabe)\s?(?P<possible>)(MÖGLICH)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
	  
	regex= r"^(?P<multiple>)(Mehrere|MEHRFACHNENNUNGEN)\s(?P<answer>)(Antworten)?\s?(?P<possible>)möglich"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
 
	regex= r"^(?P<please>)BITTE\s(?P<choose>)VERSUCHEN SIE\s(?P<an>)EINE\s(?P<answer>)ANWORT\s(?P<fromthis>)VON DIESER\s(?P<card>)(KARTE|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<use>)(Verwenden|benutzen|nutzen)\s(?P<this>)Sie\s(diese|die)\s(?P<same>)(gleiche)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<choose>)wählen\s(?P<sie>)Sie\s(?P<one>)(eine|Ihre)?\s?(?P<answer>)Antwort\s(?P<fromthis>)(von|von dieser|von der|auf der|auf dieser|aus)\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<choose>)wählen\s(?P<sie>)Sie\s(?P<one>)(eine|Ihre|von)?\s?(?P<the>)(die|der|dieser)?\s?(?P<thecard>)(Karte|liste)?\s?(\d+)?\s?(die|der|dieser)?\s?(?P<answer>)(Antwortmöglichkeiten|Antwort|Antwortmöglichkeit)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True



	regex= r"^(?P<please>)(Bitte)?\s?(?P<just>)nur\s(?P<one>)eine\s(?P<answer>)Antwort\s(?P<select>)auswählen"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<choose>)(wählen)?\s?(?P<sie>)(Sie)?\s?(?P<one>)(eine|Ihre|von)?\s?(?P<answer>)Antwort\s(?P<on>)aus\s(?P<the>)(die|der|dieser)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"^(?P<please>)(Bitte)?\s?(?P<answer>)Antwort\s(?P<fromthis>)aus\s(dieser|die)\s(?P<card>)(Karte|liste)\s(?P<select>)auswählen"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True
		

	regex= r"^(?P<please>)(Bitte)?\s?(?P<use>)(Verwenden|benutzen|nutzen)\s(?P<continue>)Sie\s(weiterhin|wieder|wiederum)?\s?(?P<now>)(jetzt)?\s?(?P<this>)(diese|dieselbe)?\s?(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True


	regex= r"^(?P<please>)(Bitte)?\s?(?P<lookat>)betrachten Sie\s(?P<nowthis>)nun (diese|dieselbe)\s(?P<card>)(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True
	
	regex= r"^(?P<andnow>)Und nun\s(?P<use>)benutzen\s(?P<thecard>)Sie\s(Karte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux and 'sagen Sie es mir' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True


	regex= r"(?P<inascale>)einer\sSkala\s(?P<fromnton>)von\s\d\sbis\s\d+\s(?P<inwhich>)(wobei\s\d+\sbedeutet)?"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux and 'sagen Sie es mir' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True
	


	regex= r"(?P<usescalefromnton>)Verwenden\sSie\sdazu\sdiese\sSkala\svon\s\d\sbis\s\d+"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux and 'sagen Sie es mir' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"(?P<choosen>)wählen\sSie\d+(?P<anything>).*\s(?P<choosem>)wählen\sSie\d+"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux and 'sagen Sie es mir' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"(?P<wherenmeans>)\d+\ssteht\sfür(?P<anything>).*\s(?P<andnmeans>)\d+\sfür"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux and 'sagen Sie es mir' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True


	regex= r"(?P<wherenmeans>)\d+\sheißt\s(?P<anything>).*\s(?P<andnmeans>)\d+\sbedeutet"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux and 'sagen Sie es mir' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"(?P<wherenmeans>)wobei\s\d\s(?P<anything>).*\s(?P<andnmeans>)und\s\d+"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux and 'sagen Sie es mir' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"(?P<answerbasedon>)Antworten\sSie\sanhand\s(?P<list>)(dieser)?\s?(liste|karte)\s(\d+)?\s?(?P<nmeans>)\d\sbedeutet\s(?P<anything>).*\s(?P<andn>)und\s\d+"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux and 'sagen Sie es mir' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"(?P<nwouldmean>)\d+\swürde\sbedeuten"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'ablehnen' not in text_aux and 'sagen Sie mir' not in text_aux and 'sagen Sie es mir' not in text_aux and 'sagen Sie mir' not in text_aux:
		return True

	regex= r"(?P<nmeans>)\d+\sbedeutet"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True

	regex= r"(?P<nmeans>)\d+\sbedeutet\s(?P<anything>).*\s(?P<nstandsfor>)\d+\ssteht\sfür\s"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True


	regex= r"(?P<nmeans>)\d+\s(-\s?)?\s?heißt\s(?P<anything>).*\s(?P<andnmeans>)\d+\s(-\s?)?\s?bedeutet"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True

	regex= r"(?P<nstandsfor>)\d+\ssteht\shier\sfür\s(?P<anything>).*\s(?P<andnmeans>)und\s\d+\sfür"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True



def instruction_recognition_norwegian(text,country_language):
	"""
	Recognizes an instruction segment for texts written in Norwegian,
	based on regex named groups patterns.

	Args:
		param1 text (string): text (in Norwegian) currently being analyzed.
		param2 country_language (string): country_language metadata embedded in file name.

	Returns: 
		True if the segment is an instruction or False if it is not.
	"""
	text_aux = text
	text = text.translate(str.maketrans(' ', ' ', string.punctuation))
	regex= r"^(?P<programmer>)programmerer:"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)Intervjuer"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'Intervjuer ID' not in text:
		return True

	regex= r"^(?P<malefemale>)(MANNLIGE|KVINNELIGE)\s(?P<respondent>)(IO|intervjuobjekter)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<respondent>)IO\s(?P<isman>)ER\sMANN"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<interviewer>)insistere"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<toall>)(SPØR)?\s?alle"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and 'land' not in text:
		return True

	regex= r"^(?P<typein>)SKRIV\sINN"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<probe>)(OPPFØLGING|FØLG\sOPP\sEN\sGANG)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		 

	regex= r"^(?P<read>)LES\s(?P<aloud>)(HØYT|OPP)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<codeall>)(REGISTRER|KOD)\s(ALT|ALLE)\s?(?P<answers>)(SVAR)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<codelowest>)(REGISTRER|KOD)\sdet\slaveste\skodetallet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<codeall>)(REGISTRER|KOD)\s(?P<onlyone>)BARE\sET(T)?\s(?P<answers>)(SVAR|alternativ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<codeall>)(REGISTRER|KOD)\s(ALT|ALLE)\s(?P<thatapplies>)SOM"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<codeall>)(REGISTRER|KOD)\s(?P<maximum>)MAKSIMALT"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<givetime>)GI\sIO\sTID\sTIL\s(?P<tolookcard>)Å\sSTUDERE\sSVARKORTET"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"(?P<tobeincluded>)FOR\sÅ\sREGNES\sMED"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"(?P<tobefilled>)FYLLES\sUT"
	matches = re.search(regex, text)
	if matches:
		return True
		 

	regex= r"(?P<donotinclude>)IKKE\sTA\sMED\s"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"(?P<tickfor>)KRYSS\sAV\sFOR\s"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"^(?P<includealso>)REGN\sOGSÅ\sMED"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<frozenfruit>)FROSSEN\sFRUKT\s(?P<mustbeincluded>)SKAL\sREGNES\sMED"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<forinstance>)FOR\sEKSEMPEL\s(?P<wheninterview>)HVI(S)?\sINTERVJUET"
	matches = re.search(regex, text)
	if matches:
		return True


	regex= r"(?P<referto>)VIS\sTIL\s(?P<samemonth>)SAMME\sMÅNED\s(?P<asinterview>)SOM\sINTERVJUET"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"(?P<ifyouthink>)Hvis\sdu\ssynes\s(?P<these>)(disse)?\s?(?P<different>)(inntektene|forskjellene|inntekten)"
	matches = re.search(regex, text)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'påstand' not in text_aux and 'fortell meg' not in text_aux and 'plasser deg selv' not in text_aux  and 'fortelle' not in text_aux:
		return True


	regex= r"^(?P<choose>)Velg\s(?P<youranswers>)svaret\sditt\s(?P<from>)fra\s(?P<this>)(dette)?\s?(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'påstand' not in text_aux and 'si' not in text_aux and 'fortell meg' not in text_aux and 'plasser deg selv' not in text_aux  and 'fortelle' not in text_aux:
		return True

		
	regex= r"^(?P<lookat>)Se\spå\s(?P<this>)(dette)?\s?(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'påstand' not in text_aux and 'si' not in text_aux and 'fortell meg' not in text_aux and 'plasser deg selv' not in text_aux  and 'fortelle' not in text_aux:
		return True

	regex= r"^(?P<takea>)Ta\sen\s(?P<lookat>)titt\spå\s(?P<this>)(dette)?\s?(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux:
		return True



	regex= r"^(?P<answer>)Svar\s(?P<based>)med utgangspunkt\s(?P<on>)i\s(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux:
		return True

	regex= r"^(?P<please>)Vær snill å\s(?P<use>)bruke\s(?P<this>)(dette)?\s?(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<read>)Les\s(?P<out>)opp\s(?P<the>)de\s(?P<different>)ulike\s(?P<organizations>)institusjonene"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
   
	regex= r"^(?P<choose>)Velg\s(?P<an>)et(t)?\s?(tall|av)?\s(?P<option>)(alternativene|svaralternativ|svaralternativene|alternativ|svar)?\s?(?P<from>)(nederst)?\s?(fra|på)\s(?P<this>)(dette)?\s?(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<no>)ikke\s(?P<card>)kort"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ifrespondent>)HVIS\sIO\s"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"^(?P<allkinds>)ALL\sSLAGS\s(?P<ofcontact>)KONTAKT\s(?P<mustbeincluded>)SKAL\sREGNES\sMED"
	matches = re.search(regex, text)
	if matches:
		return True


	regex= r"^(?P<again>)(vis|Forsatt|FORTSATT)?\s?(?P<card>)kort"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'påstand' not in text_aux and 'si' not in text_aux and 'fortell meg' not in text_aux and 'plasser deg selv' not in text_aux  and 'fortelle' not in text_aux:
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

	regex= r"^(?P<use>)Bruk\s(?P<still>)(fortsatt)?\s?(?P<this>)(det|dette)?\s?(?P<card>)kortet\s(?P<andtellwhichopinion>)og\ssi\shvilket\ssyn\s(?P<isclosesttoyours>)du\ser\smest\senig\si"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'påstand' not in text_aux and 'fortell meg' not in text_aux and 'plasser deg selv' not in text_aux  and 'fortelle' not in text_aux:
		return True


	regex= r"^(?P<lookat>)(Se\s?på)?\s?(?P<use>)Bruk\s(?P<still>)(fortsatt)?\s?(?P<this>)(det|dette)?\s?(?P<again>)(samme|fortsatt)?\s?(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'påstand' not in text_aux and 'si' not in text_aux and 'fortell meg' not in text_aux and 'plasser deg selv' not in text_aux  and 'fortelle' not in text_aux:
		return True


	regex= r"(?P<scalefrom>)skala\sfra\s(?P<nton>)\d\s?(-|til)\s?\d+"
	matches = re.findall(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'fortell meg' not in text_aux and 'plasser deg selv' not in text_aux and 'fortelle' not in text_aux:
		return True

	regex= r"(?P<numbersfrom>)tall\sfra\s(?P<nton>)\d\s?(-|til)\s?\d+"
	matches = re.findall(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'fortell meg' not in text_aux and 'plasser deg selv' not in text_aux and 'fortelle' not in text_aux:
		return True

	regex= r"(?P<nstandsfor>)\d\s(står|star)\sfor\s(?P<anything>).*\s(?P<andnstandsfor>)\d+\s(står|star)\sfor"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'fortell meg' not in text_aux and 'plasser deg selv' not in text_aux and 'fortelle' not in text_aux:
		return True

	regex= r"(?P<nstandsfor>)Null\s(står|star)\sfor\s(?P<anything>).*\s(?P<andnstandsfor>)ti\s(står|star)\sfor"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'fortell meg' not in text_aux and 'plasser deg selv' not in text_aux and 'fortelle' not in text_aux:
		return True

	regex= r"(?P<wherenmeans>)hvor\s\d\sbetyr\s(?P<anything>).*\s(?P<andnmeans>)og\s\d+\sbetyr"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'fortell meg' not in text_aux and 'plasser deg selv' not in text_aux and 'fortelle' not in text_aux:
		return True
 
	regex= r"^(?P<readout>)LES\sOPP\s(?P<options>)(ALTERNATIVENE|kategoriene)"
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

	regex= r"^(?P<select>)Velg\s(?P<one>)et(t)?\s(?P<option>)(svaralternativ|svaralternativene|alternativene|alternativ)\s(?P<from>)fra\s(?P<this>)(det|dette)\s(?P<card>)kortet"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<select>)Velg\s(?P<one>)et(t)?\s(?P<option>)(svaralternativ|svaralternativene|alternativene|alternativ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<newcard>)Her et nytt kort"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True



def instruction_recognition_french(text,country_language):
	"""
	Recognizes an instruction segment for texts written in French,
	based on regex named groups patterns.

	Args:
		param1 text (string): text (in French) currently being analyzed.
		param2 country_language (string): country_language metadata embedded in file name.

	Returns: 
		True if the segment is an instruction or False if it is not.
	"""
	text_aux = text
	text = text.translate(str.maketrans(' ', ' ', string.punctuation))

	regex= r"^(?P<programmer>)Programmeur"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)(Enquêteur|Enqueteur)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)(lisez|lire)\s?(?P<outloud>)(haute voix)?\s?(?P<each>)(chaque)?\s?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)(lisez|lire)\s?(?P<the>)(les)?\s?(?P<each>)(chaque)?\s?(?P<utterances>)PROPOSITION(S)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)CODER\s(?P<all>)TOUTES\s(?P<the>)(les)?\s?(?P<answers>)REPONSES"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)CODER\s(?P<fromthe>)A\sPARTIR\sDE\sLA"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)(CODAGE|CODER)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and text != 'CODER LE SEXE':
		return True

	regex= r"^(?P<code>)CITE(R|Z)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)NOTE(R|Z)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

		

	regex= r"^(?P<respondent>)REPONDANT\s(?P<malefemale>)(FEMININ|MASCULIN)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
	 

	regex= r"^(?P<ifnecessary>)AU\sBESOIN\s(?P<chooseaccording>)CHOISIR\sSELON\s(?P<thepriority>)LA\sPRIORITE"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)code(z|r)\s(?P<all>)tout(?P<thatapplies>)((ce)? qui s'applique)?"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)(demandez|poser)?\s?(?P<all>)(a|á)\stous"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<askifmainactivity>)POSER SI ACTIVITE PRINCIPALE"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		

	regex= r"^(?P<attention>)ATTENTION"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<show>)(montrer|montrez|LAISSER)\s(?P<again>)(encore|toujours|A NOUVEAU)?\s?(?P<the>)(la)?\s?(?P<card>)(carte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<show>)(montrer|montrez|LAISSER)?\s?(?P<again>)(encore|toujours|A NOUVEAU)?\s?(?P<the>)(la)?\s?(?P<card>)(carte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(S'il vous plaît|Veuillez|Veuillez s'il vous plaît)?(,)?\s?(?P<continue>)(Continuez)?\s?(à|a)?\s?(?P<use>)utiliser\s(?P<this>)cette\s(?P<card>)carte"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(S'il vous plaît|Veuillez|Je vous prie)?(,)?\s?(?P<use>)(d')?utilise(z|r)\s(?P<thesame>)la même\s(?P<card>)(carte|liste)"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(S'il vous plaît)?(,)?\s?(?P<iaskyouto>)(Je vous prie)?\s?(?P<use>)(d'utiliser|utilisez)\s(?P<this>)cette\s(?P<card>)(carte|liste)"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'dites-moi' not in text_aux and 'affirmations' not in text_aux:
		return True

	regex= r"^(?P<please>)(S'il vous plaît)?(,)?\s?(?P<iaskyouto>)(Je vous prie|Veuillez)?\s?(?P<use>)(d'utiliser|utilise(r|z))\s(?P<again>)(de nouveau|à nouveau|encore|toujours)?\s?(?P<this>)cette\s(?P<same>)(même)?\s?(?P<card>)(carte|liste)"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)Utilisez\s(?P<thesame>)toujours cette même\s(?P<card>)carte"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'dites-moi' not in text_aux and 'affirmations' not in text_aux:
		return True

	regex= r"^(?P<please>)(S'il vous plaît|Veuillez)(,)?\s(?P<answer>)répondre\s(?P<using>)(en utilisant|A L'AIDE)"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(S'il vous plaît|Veuillez)?(,)?\s?(?P<again>)(encore)?\s?(?P<use>)utiliser\s(?P<this>)(cette)?\s?(?P<the>)(la)?\s?(?P<card>)carte"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)note\s(?P<for>)(a|à)\s(?P<theinterviewer>)(l'enqueteur|l'enquetêur|l'enquêteur)"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<instruction>)(instruction|note)\s(?P<for>)pour\s(?P<theinterviewer>)(l'enqueteur|l'enquetêur|l'ENQUÊTEUR)"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<codeormark>)(code(r|z)|note(r|z))?\s?(?P<one>)UNE\s(?P<only>)SEULE\s(?P<answer>)(REPONSE|RÉPONSE)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<codeormark>)(code(r|z)|note(r|z))?\s?(?P<only>)SEULEMENT\s(?P<one>)(UNE)?\s?(?P<answer>)(REPONSE|RÉPONSE)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<one>)UNE\s(?P<answer>)(REPONSE|RÉPONSE)\s(?P<forline>)par\sligne"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<ask>)Demander\s(?P<thefive>)les\scinq\s(?P<mostimportant>)plus\simportantes"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<show>)Présenter\s(?P<optioncards>)la\scarte\sdes\sopinions"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'dites-moi' not in text_aux:
		return True
	  

	regex= r"(?P<nequals>)\d\s?=\s?(?P<anything>).*(?P<xequals>)\d+\s?="
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'dites-moi' not in text_aux:
		return True

	regex= r"(?P<choosetheoption>)vous\schoisissez\sle\s(chiffre|nombre)\s\d+"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'dites-moi' not in text_aux:
		return True

	regex= r"^(?P<choose>)choix\s(?P<multiple>)multiple\s?(?P<possible>)(possible)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
	  
	regex= r"^(?P<if>)Si\s(?P<the>)le\s(?P<respondent>)répondant"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(S'il vous plaît|Veuillez)?(,)?\s?(?P<choose>)(choisir|Choisissez)\s(?P<onlyone>)(une|une seule)?\s?(?P<your>)(votre)?\s?(?P<answer>)réponse(s)?\s"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(S'il vous plaît|Veuillez)?(,)?\s?(?P<choose>)(choisir|Choisissez)\s(?P<onlyone>)(une|une seule)?\s?(?P<answer>)(réponse(s)?)?\s?(?P<fromcard>)sur\scette\scarte"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'dites-moi' not in text_aux:
		return True


	regex= r"^(?P<choose>)choix\s(?P<multiple>)multiple\s(?P<possible>)possible"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<multiple>)(PLUSIEURS|Plusieures|cinq)\s(?P<answers>)(reponses|réponses)\s(?P<possible>)(possibles)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<answers>)(reponses|réponses)\s(?P<multiple>)multiples"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<respondent>)REPONDANT\s(?P<malefemale>)(MASCULIN|FEMININ)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewergiverespondent>)L'ENQUETEUR\sLAISSE\sAU\sREPONDANT"
	matches = re.search(regex, text_aux)
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

	regex= r"^(?P<withthehelp>)Toujours à l'aide\s(?P<of>)de\s(?P<this>)cette\s(?P<card>)carte"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and 'dites-moi' not in text_aux and 'affirmations' not in text_aux:
		return True

	regex= r"^(?P<continueto>)Continuez à\s(?P<use>)utiliser\s(?P<this>)cette\s(?P<card>)carte"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)Je vous prie de\s(?P<choose>)choisir\s(?P<youranswer>)votre réponse\s(?P<from>)sur\s(?P<this>)cette\s(?P<card>)carte."
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(S'il vous plaît|Veuillez)?(,)?\s?(?P<mark>)coche(z|r)\s(?P<theoption>)la case\s(?P<that>)(qui)?\s?(?P<represent>)(correspond|correspondante)\s?(?P<better>)(le mieux)?\s?(?P<your>)((à\s)?votre)?\s?(?P<answer>)(réponse(s)?)?"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)Veuillez\s(?P<choose>)choisir\s(?P<onlyone>)une seule des\s(?P<answer>)réponses\s(?P<from>)figurant sur\s(?P<this>)cette\s(?P<card>)(carte|liste)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Veuillez)?\s?(?P<answer>)(Répondez|répondre)\s(?P<using>)(à l'aide de|au moyen de)\s(?P<this>)cette\s(?P<card>)(carte|liste)"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(S'il vous plaît|Veuillez)?(,)?\s?(?P<mark>)Cerclez\s(?P<theoption>)le code\s(?P<correspondto>)correspondant à\s(?P<answer>)votre réponse\s"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)NOTE(R|Z)\s(?P<with>)AVEC\s(?P<asmany>)LE PLUS DE\s(?P<details>)DÉTAILS\s(?P<possible>)POSSIBLES"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<insist>)RELANCE(R|Z)?"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"^(?P<insist>)RELANCE(R|Z)\s(?P<interviewer>)(enquetêur|enqueteur|enquêteur)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"(?P<scalefrom>)échelle\sde\s(?P<nton>)\d\s?à\s?\d+\s(?P<wherenmeans>)où\s\d\ssignifie\sque"
	matches = re.findall(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True

	regex= r"^(?P<usea>)Utilisez\sune\s(?P<scalefrom>)échelle\sde\s(?P<nton>)\d\sà\s\d+(?P<wherenmeans>).*\(\d+\).*\(\d+\)"
	matches = re.findall(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True


	regex= r"(?P<nmeansthat>)\d\ssignifie\s(que|qu'il)?\s?(?P<anything>).*\s(?P<andnmeans>)(et)?\s?\d+\s(signifie)?\s?(que|qu'il)?"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True


	regex= r"(?P<nmeansthat>)\d\ssignifie\s(?P<anything>).*\s(?P<andnmeans>)\d+\ssignifie\s.*(?P<andthenotesinthemiddle>)et les notes intermédiaires permettent de nuancer votre jugement"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True

	regex= r"(?P<answerusingthiscard>)Répondez s'il vous plaît en utilisant cette carte(?P<anything>).*\s(?P<andnmeans>)et\s\d+\ssignifie"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True


	regex= r"^(?P<nmeansthat>)\d\ssignifie\sque"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True

	regex= r"(?P<giveascoreofn>)donnez\sun\sscore\sde\s\d+"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True


def instruction_recognition_english(text,country_language):
	"""
	Recognizes an instruction segment for texts written in English,
	based on regex named groups patterns.

	Args:
		param1 text (string): text (in English) currently being analyzed.
		param2 country_language (string): country_language metadata embedded in file name.

	Returns: 
		True if the segment is an instruction or False if it is not.
	"""
	text_aux = text
	text = text.translate(str.maketrans(' ', ' ', string.punctuation))

	regex= r"^(?P<programmer>)Programmer:"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)Interviewer"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and "Interviewer ID" not in text:
		return True

	regex= r"^(?P<computercode>)COMPUTER\sCODE"
	matches = re.search(regex, text)
	if matches:
		return True
  
	regex= r"^(?P<typeinduration>)TYPE\sIN\sDURATION"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<writeinnumber>)write\sIN\snumber"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"(?P<prespecifiedcodes>)(use|to\sbe\scoded\sinto)\s(pre\-specified)?\s?(codes|ISO)"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<tobeaskedascountryspecific>)(To|can)\sbe\sasked\sas\sa\scountry\-specific\squestion"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<tobeaskedascountryspecific>)Country\-specific\s(\(question\sand\))?\s?codes"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True


	
	regex= r"^(?P<chooseuptofive>)Please\schoose\sup\sto\sfive"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<toberecorded>)To\sbe\srecoded\sinto"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(Please)?\s?(?P<choosetheoption>)choose\sthe\soption.*(?P<closesttoyourview>)closest\sto\syour\sview"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"(?P<malefemalerespondents>)(ASK\sIF\sRESPONDENT\sIS\sFEMALE|FEMALE\sRESPONDENT(S)?|ASK\sIF\sRESPONDENT\sIS\sMALE|MALE\sRESPONDENT(S)?)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	

	regex= r"^(?P<probeifnecessary>)probe\sif\snecessary"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ifyouthink>)If\syou\sthink\s(?P<paymentcondition>)((this|your)\s(gross)?\s?pay|your\sincome\sfrom\s|these\sincomes|these\sdifferences)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)INTERVIEWER\s(?P<ifrespondent>)If\sthe\srespondent\s(?P<needadditionalinstructions>)needs\sadditional\sinstructions"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)NOTE\s(?P<numbermustbeexclusive>)THIS\sNUMBER\sMUST\sBE\sEXCLUSIVE\s(?P<toindividualinterviewers>)TO\sINDIVIDUAL\sINTERVIEWERS"
	matches = re.search(regex, text,  re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(please)?\s?(?P<answer>)answer\s(?P<using>)using\s(?P<this>)this\s(?P<card>)card\s(?P<where>)where\s(?P<zero>)0\s(?P<means>)means"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<nmeans>)\d\smeans\s(?P<anything>).*(?P<and>)(and)?\s?(?P<xmeans>)\d+\smeans"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True

	regex= r"(?P<nmeans>)\d\smeans\s(?P<anything>).*(?P<and>)(and)?\s?(?P<xmeans>)\d+\smeans"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True

	regex= r"(?P<nmeans>)\d\sis\s(?P<anything>).*(?P<and>)and\s(?P<xmeans>)\d+\sis"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True

	regex= r"(?P<nmeans>)WHERE\s\d\s?=\s?(?P<anything>).*(?P<and>)and\s(?P<xmeans>)\d+\s?=\s?"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True

	regex= r"(?P<nmeans>)On\sa\sscale\sfrom\s\d\sto\s\d+\s(?P<pleaseindicate>)please\sindicate"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True


	regex= r"(?P<nmeans>)WHERE\s\d\smeans\s(?P<anything>).*(?P<and>)and\s(?P<xmeans>)\d+"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True

	regex= r"(?P<give>)give\s(?P<ascoreof>)a\sscore\sof\s(?P<number>)\d+\b"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True

	regex= r"^(?P<please>)(please)?\s?(?P<use>)use\s(?P<this>)this\s(?P<card>)card\s?(?P<again>)(again)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?\s?(?P<tell>)tell\s(?P<me>)me\s(?P<on>)on\s(?P<a>)a\s(?P<score>)score"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
	
	regex= r"^(?P<again>)(again)?\s?(?P<still>)(still)?\s?(?P<card>)showcard"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<card>)card\s(?P<numberorletter>)(\d+|[a-z])"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<show>)(show|still)\s(?P<income>)(income)?\s?(?P<card>)card\s?(?P<again>)(again)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True

	regex= r"^(?P<ask>)ask\s(?P<all>)all"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<probe>)probe"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)code\s(?P<one>)(one|under|five)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<prompt>)prompt"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<insist>)insist"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)Please\s(?P<use>)use\s(?P<the>)the\s(?P<responses>)responses\s(?P<onthis>)on\sthis\s(?P<card>)card"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<look>)look\s(?P<atthis>)at\sthis\s(?P<card>)card"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True


	regex= r"^(?P<ingrid>)IN GRID\s(?P<collect>)collect\s(?P<details>)details\s(?P<of>)of\s(?P<respondent>)respondent"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<then>)then\s(?P<collect>)collect\s(?P<details>)details\s(?P<of>)of\s(?P<other>)other(s)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)code\s(?P<one>)one\s(?P<answer>)(answer)?\s?(?P<apply>)only"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)code\s(?P<ab>)AN\s(?P<answer>)(answer)?\s?(?P<foreach>)FOR\sEACH"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<codeorselect>)(code|select)\s(?P<all>)all\s(?P<that>)that\s(?P<apply>)(apply|applies)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)code\s(?P<all>)all"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<eng_gbcodes>)(Northern\sIreland|England\sScotland).*\scodes"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<enterdetails>)NOW\sENTER\sDETAILS\sFOR\sTHE\sOLDEST"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True



	regex= r"^(?P<read>)read\s(?P<out>)out\s?(?P<each>)(each)?\s?(?P<statement>)(statement)?\s?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?\s?(?P<still>)(still)?\s?(?P<use>)use\s(?P<this>)(this)?\s?(?P<the>)(the)?\s?(?P<same>)(same)?\s?(?P<card>)card"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?\s?(?P<choose>)choose\s(?P<oneor>)(one|your|an)\s(?P<answer>)answer\s(?P<infrom>)(in|from)\s(?P<this>)this\s(?P<same>)(same)?\s?(?P<card>)card"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<prompt>)prompt\s(?P<inrelation>)in relation\s(?P<to>)to\s(?P<precodes>)precodes"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?\s?(?P<select>)select\s(?P<only>)only\s(?P<one>)one"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?\s?(?P<tick>)tick\s(?P<oneorthe>)(one|the)?\s?(?P<box>)box"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(please)?\s?(?P<choose>)choose\s(?P<one>)(one)?\s?(?P<your>)(your)?\s?(?P<answer>)answer\s(?P<from>)from\s(?P<card>)(card|the options)"
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


def instruction_recognition_czech(text,country_language):
	"""
	Recognizes an instruction segment for texts written in Czech,
	based on regex named groups patterns.

	Args:
		param1 text (string): text (in Czech) currently being analyzed.
		param2 country_language (string): country_language metadata embedded in file name.

	Returns: 
		True if the segment is an instruction or False if it is not.
	"""
	text_aux = text
	text = text.translate(str.maketrans(' ', ' ', string.punctuation))


	regex= r"^(?P<code>)(KÓDUJE|KODUJE|zkontroluje)?\s?(?P<interviewer>)(tazatele|taz)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)(tazatele|taz)\s?(?P<code>)(KÓDUJE|KODUJE|zkontroluje)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<filter>)FILTR:"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<ask>)(PTEJTE SE)?\s?(?P<if>)(POKUD)?\s?(?P<the>)(JE)?\s?(?P<respondent>)(RESPONDENT(I)?|RESPONDENTKA|RESPONDENTŮ)"
	matches = re.search(regex, text)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True

	regex= r"^(?P<ifhasno>)POKUD NEMÁ ŽÁDNÉHO"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"^(?P<readout>)PŘEDČÍTEJTE"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"^(?P<codeall>)KODUJTE\sVŠECHNY"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"^(?P<chooseuptofive>)Vyznačte\spouze\spět"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"^(?P<selectuptofive>)Prosím\svyberte\snejvýše\spět"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"^(?P<registerestimations>)ZAZNAMENEJTE\sI\sODHADY"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"^(?P<roundup>)ZAOKROUHLETE"
	matches = re.search(regex, text)
	if matches:
		return True


	regex= r"^(?P<mainwork>)HLAVNÍ PRÁCE"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"^(?P<record>)ZAZNAMENEJTE"
	matches = re.search(regex, text)
	if matches and text != 'ZAZNAMENEJTE POHLAVÍ':
		return True

	regex= r"^(?P<askrespondent>)POŽÁDEJTE RESPONDENTA"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"^(?P<respondent>)RESPONDENT(I)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<roundtofullhour>)ZAOKROUHLETE NA CELÉ"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"(?P<includeadoptions>)ZAHRNUJTE\sADOPCE"
	matches = re.search(regex, text)
	if matches:
		return True

	regex= r"^(?P<ask>)PTEJTE\s(?P<all>)SE VŠECH\s(?P<employees>)ZAMĚSTANCŮ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
	
	regex= r"^(?P<markwiththiscard>)S\spomocí\stéto\skarty\sprosím\soznačte"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True

	regex= r"^(?P<now>)(A nyní|Nyní)?\s?(?P<use>)(Použijte|použijte)\s(?P<again>)(znovu)?\s?(?P<graduate>)(stupnici)?\s?(?P<this>)(tuto|této)?\s?(?P<card>)kart(u|a|y)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True

	regex= r"^(?P<toanswer>)(K odpovědi|Při odpovědích)\s(?P<use>)(použijte|pouţijte)\s(?P<please>)(prosím)?\s?(?P<this>)tuto\s(?P<card>)kart(u|a|y)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True

	regex= r"^(?P<please>)prosím\s(?P<use>)užijte\s(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True


	regex= r"^(?P<instruction>)Pokyn"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<prompt>)ZJIŠŤUJE"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

		

	regex= r"^(?P<show>)(PŘEDLOŽTE|PŘEDLOŢTE)?\s?(?P<still>)(STÁLE JEŠTĚ)?\s?(?P<again>)(OPĚT)?\s?(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<note>)poznámka\s(?P<for>)pro\s(?P<interviewer>)tazatele"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<respondent>)(RESPONDENKY|RESPONDENTI)\s(?P<malefemale>)(ŽENY|MUŽI)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"(?P<ineachline>)(V|NA)?\s?(KAŽDÉM ŘÁDKU)?\s?(?P<possible>)(MOŽNÁ|MOŢNÁ)\s(?P<only>)POUZE\s(?P<one>)JEDNA\s(?P<answer>)ODPOVĚĎ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<ineachline>)(V|NA)\sKAŽDÉM\sŘÁDKU\s(?P<choose>)VYBERTE\s(?P<one>)JEDNU\s(?P<answer>)ODPOVĚĎ"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<possible>)(MOŽNÁ|MOŢNÁ)?\s?(?P<only>)(POUZE|JE POUZE)\s(?P<one>)(JEDNA|JEDINÁ)\s(?P<answer>)ODPOVĚĎ"
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

	regex= r"^(?P<dontread>)NEČTĚTE\s(?P<only>)POUZE\s(?P<code>)ZAKÓDUJTE"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<look>)Prohlédněte\s(?P<at>)si\s(?P<this>)(tuto)?\s?(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True

	regex= r"^(?P<read>)přečtěte\s(?P<category>)varianty\s(?P<answers>)odpovědí"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<choose>)VYBERTE\s(?P<please>)(prosím)?\s?(?P<only>)(POUZE|jen)\s(?P<one>)JEDNU\s(?P<answer>)(ODPOVĚĎ)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)(ČTĚTE|ČTETE)\s(?P<out>)NAHLAS\s?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<prompt>)ZJIŠŤUJTE"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)(ČTĚTE|ČTETE|PŘEČTĚTE)\s(?P<out>)NAHLAS"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

 
	regex= r"^(?P<again>)(opět|STÁLE)\s(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(prosím)?\s?(?P<again>)(opět)?\s?(?P<use>)(Použijete|použijte|pouţijte)\s(?P<this>)(tuto)?\s?(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True

	regex= r"^(?P<use>)(Použijete|Použijte|Pouţijte)\s(?P<please>)(prosím)?\s?(?P<same>)(stejnou)?\s?(?P<this>)(tuto)?\s?\s(?P<card>)kart(u|a)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True


	regex= r"^(?P<chooseyour>)Vyberte svou\s(?P<answer>)odpověď\s(?P<accordingto>)podle této\s(?P<card>)karty"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<choose>)Vyberte(,)?\s(?P<please>)prosím(,)?\s(?P<youranswer>)svou\sodpověď\s(?P<accordingto>)(podle|z)\stéto\s(?P<card>)karty"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<choose>)Vyberte\s(?P<please>)(prosím)?\s?(?P<one>)(jen jednu|jednu)"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches  and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True

	regex= r"(?P<choose>)Pokud\ssi\smyslíte\s(?P<thatyourthis>)že\s(je|jsou)\s(vaše|váš|tyto)\s(?P<income>)(mzda|příjem|příjmy|rozdíly)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches  and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True


	regex= r"(?P<please>)(prosím)?\s?(?P<choose>)Vyberte\s(?P<one>)(jen jednu|jednu)?\s?(?P<answer>)odpověď\s(?P<fromthis>)(z|na)\smožností"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches  and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True


	regex= r"(?P<choose>)Vyberte\s(?P<please>)(prosím)?\s?(?P<one>)(jen jednu|jednu)?\s?(?P<answer>)odpověď\s(?P<fromthis>)(z|na)\stéto\s(?P<card>)(karty|kartě)"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches  and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True

	regex= r"(?P<youranswer>)Svou\sodpověď\s(?P<please>)(prosím)?\s?(?P<choose>)Vyberte\s(?P<fromthis>)(z|na)\stéto\s(?P<card>)(karty|kartě)"
	matches = re.search(regex, text_aux, re.IGNORECASE)
	if matches  and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True

	regex= r"(?P<choose>)Vyberte\s(?P<please>)prosím\s?(?P<one>)(jen jednu|jednu)\s(?P<answer>)odpověď\s?(?P<fromthis>)(z této)?\s?(?P<card>)(karty|kartě)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches  and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
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


	regex= r"(?P<wherenmeans>)\d+\sznamená\s(?P<anything>).*\s(?P<andnmeans>)(a)?\s?\d+\s(znamená)?"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE):
		return True

	regex= r"(?P<wherenmeans>)(kde)?\s?\d\sje\s(?P<anything>).*\s(?P<andnmeans>)(a)?\s?\d+\s(je)?"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE) and 'měsíčně' not in text:
		return True

	regex= r"(?P<wherenmeans>)(kde)?\s?\d\s(?P<anything>).*\s(?P<andnmeans>)(a)?\s?\d+\s(je)?"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux and not re.findall('řekněte', text_aux, re.IGNORECASE) and 'měsíčně' not in text:
		return True


	regex= r"(?P<givenscore>)dejte\sjí\s\d+\sbodů"
	matches = re.findall(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and ':' not in text_aux and '...' not in text_aux:
		return True

	return False



def instruction_recognition_portuguese(text,country_language):
	"""
	Recognizes an instruction segment for texts written in Portuguese,
	based on regex named groups patterns.

	Args:
		param1 text (string): text (in Portuguese) currently being analyzed.
		param2 country_language (string): country_language metadata embedded in file name.

	Returns: 
		True if the segment is an instruction or False if it is not.
	"""
	text_aux = text
	text = text.translate(str.maketrans(' ', ' ', string.punctuation))

	regex= r"^(?P<programador>)programador"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)entrevistador"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<card>)(cartão|lista)\s(?P<numberorletter>)(\d+|\w+)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)ler\b"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

   
	regex= r"^(?P<all>)TODOS\s(?P<except>)MENOS\sOS\s(?P<single>)SOLTEIROS"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<prompt>)APROFUNDAR"
	matches = re.search(regex, text)
	if matches:
		return True


	regex= r"^(?P<respondent>)INQUIRIDOS\s(?P<sex>)DO\sSEXO\s(?P<one>)(FEMININO|masculino)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<part>)parte\s(?P<lower>)inferior\sd(o|a)\s(?P<card>)(cartão|lista)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		  
 
	regex= r"^(?P<mark>)ASSINALAR\s(?P<only>)APENAS\s(?P<one>)UM(A)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<then>)DEPOIS\s(?P<repeat>)REPETIR\s(?P<forthe>)PARA\sA\s(?P<institution>)INSTITUIÇÃO"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)CODIFICAR\s(?P<only>)APENAS\s(?P<one>)UMA"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)CODIFICAR\s(?P<only>)TOD(O|A)S"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

  
	regex= r"^(?P<ifyouthink>)Se\s(considera|acha)\s(?P<thatyourthis>)que\s(o\sseu|ess(e|a)(s)?)\s(?P<income>)(rendimento|diferenças)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<answer>)Responda\s(?P<please>)(por favor)?\s?(?P<using>)(utilizando|com)\s(?P<theorthis>)(o|a|um|uma|esta|este)\s(?P<same>)(mesmo|mesma)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)utilize\s(?P<please>)(por favor)?\s?(?P<thesame>)(o\smesmo|a\smesma)\s(?P<card>)(cartão|lista)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(por favor)?\s?(?P<choose>)Escolha\s(?P<youranswer>)a sua resposta\s(?P<fromthe>)(a\spartir\sd(o|a))?\s?(?P<inthis>)(neste)?\s?(?P<following>)(seguinte)?\s?(?P<card>)(cartão|lista)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(por favor)?\s?(?P<use>)(utilize|use)\s(?P<youranswer>)as\srespostas\s(?P<fromthe>)dest(a|e)\s(?P<following>)(seguinte)?\s?(?P<card>)(cartão|lista)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<forthis>)Para\sisso\s(?P<youwilluse>)(utilizará|utilize)\s(?P<please>)(por favor)?\s?(?P<thefollowing>)(o|a)\sseguinte\s(?P<card>)(cartão|lista)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<show>)(mostrar|manter)\s(?P<again>)(novamente)?\s?(?P<the>)(a|o)?\s?(?P<card>)(cartão|lista)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<show>)(mostrando|utilizando)\s(?P<again>)ainda\s(?P<this>)este\s(?P<card>)(cartão|lista)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(por favor)?\s?(?P<use>)(utilize|mostrar|use)\s(?P<this>)(este|est(e|a)\smesmo|(o|a)\smesm(o|a))?\s?(?P<card>)(cartão|lista)\s?(?P<again>)(novamente)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(por favor)?\s?(?P<use>)utilize\s(?P<this>)es(te|ta|sa|se)\s(?P<card>)(cartão|lista)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<use>)(utilize\s|use\s)(?P<please>)(por\sfavor)?\s?(?P<this>)es(te|ta|sa|se)\s(?P<card>)(cartão|lista)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<use>)utilize\s(?P<thesame>)(o|a)\smesm(o|a)(?P<card>)(cartão|lista)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<please>)(por favor)?\s?(?P<continue>)continue\s(?P<show>)(mostrando|utilizando)\s(?P<this>)(este|este mesmo)?\s?(?P<card>)(cartão|lista)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		
	regex= r"^(?P<suggest>)sugerir\s(?P<categories>)categorias\s(?P<de>)de\s(?P<answer>)resposta"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		
	regex= r"^(?P<please>)(por favor)?\s?(?P<choose>)escolha\s(?P<the>)(a)?\s?(?P<youranswer>)resposta(s)?\s(?P<fromthis>)(a\spartir\s)?(deste|nest(e|a))\s(?P<card>)(cartão|lista)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<choose>)escolha\s(?P<please>)(por favor)?\s?(?P<youranswer>)a\ssua\sresposta\s(?P<fromthis>)(a\spartir\s)?deste\s(?P<card>)cartão"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<choose>)escolha\s(?P<please>)(por favor)?\s?(?P<amongoptions>)entre\sas\sopções"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<note>)(nota)?\s?(?P<for>)(para|ao)?\s?(?P<interviewer>)entrevistador\s?(?P<code>)(codifica(r)?)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<please>)(por favor)?\s?(?P<choose>)escolha\s(?P<option>)a afirmação\s(?P<closer>)que mais se aproxima da\s(?P<youropinion>)sua opinião"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)ler\s(?P<one>)uma\s(?P<organization>)organização\s(?P<ateachtime>)de cada vez"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<scalefrom>)escala\sde\s(?P<nton>)\d\sa\s\d+\b"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and '10,' not in text_aux:
		return True


	regex= r"(?P<thenmeans>)\d\ssignifica\s(que)?\s?(?P<anything>).*\s(?P<andthenmeans>)(de|e)\s(o)?\s?\d+"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True

	regex= r"(?P<thenmeans>)(em)?\s?que\d\ssignifica\s(?P<anything>).*\s(?P<andthenmeans>)(de|e)\s(o)?\s?\d+\s?(significa)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True

	regex= r"(?P<inascalewherenmeans>)Responda\spor\sfavor\snuma\sescala"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True

	regex= r"(?P<coose>)escolha\s(?P<please>)(por favor)?\s?(?P<amongoptions>)entre\sas\sopções"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
		return True

	regex= r"(?P<givenpoints>)dê\s\d+\spontos\b"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"(?P<notethenumber>)EXPLICITAR\sO\sNÚMERO\s(?P<ofhoursandminutes>)DE\sHORAS\sE\sMINUTOS\b"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<read>)ler\s(?P<slowly>)(pausadamente)?\s?(?P<outloud>)(em voz alta)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<choose>)Escolha\s(?P<oneofthe>)uma das\s(?P<following>)(seguintes)?\s?(?P<answers>)respostas"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux:
		return True

	regex= r"^(?P<choose>)Indique\s(?P<onlyone>)só\suma\s(?P<following>)hipótese"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux:
		return True

	regex= r"^(?P<askthe>)PEDIR AO\s(?P<respondent>)ENTREVISTADO\s(?P<adescription>)UMA DESCRIÇÃO"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<code>)(codificar|assinalar|registr(ar|e))\s(?P<all>)(todas|todos)\s?(?P<the>)(as)?\s?(?P<that>)(que\sse\s)?(?P<apply>)aplicam?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<codeormark>)(codificar|assinalar|registr(ar|e))\s(?P<only>)(só|apenas)?\s?(?P<one>)uma\s(?P<answer>)(resposta)?"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True


	regex= r"^(?P<use>)Use\s(?P<please>)por\sfavor(?P<thiscale>)esta\sescala\s(?P<toanswer>)para\sresponder\s"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux:
		return True

	regex= r"^(?P<describe>)descrever\s(?P<details>)detalhadamente"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<ask>)perguntar a\s(?P<all>)todos"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<mark>)REGISTR(E|AR)\s(?P<anything>)(UMA|CINCO|NA|TOD(O|A)S)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True
		 

	regex= r"^(?P<insist>)insistir"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	return False


def instruction_recognition_catalan_spanish(text,country_language):
	"""
	Recognizes an instruction segment for texts written either in Spanish or Catalan,
	based on regex named groups patterns.

	Args:
		param1 text (string): text (in Spanish or Catalan) currently being analyzed.
		param2 country_language (string): country_language metadata embedded in file name.

	Returns: 
		True if the segment is an instruction or False if it is not.
	"""
	text_aux = text
	text = text.translate(str.maketrans(' ', ' ', string.punctuation))

	regex= r"^(?P<programador>)programador"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	regex= r"^(?P<interviewer>)(entrevistador|ENTREVISTADOR/A)"
	matches = re.search(regex, text, re.IGNORECASE)
	if matches:
		return True

	if 'CAT' in country_language:
		regex= r"^(?P<typeinduration>)ANOTAR\sDURADA"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<ask>)Preguntar:"
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<attentioninterviewer>)ATENCIÓ\sENTREVISTADOR(/A)?:"
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches:
			return True


		regex= r"^(?P<continue>)(continuï|continueu|continuar|seguir)?\s?(?P<show>)mostr(ar|eu|ant|ando)\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"(?P<malefemalerespondents>)(SOLO|SÓLO)\s(PARA|A)\sENTREVISTAD(A|O)S\s?(MUJERES|HOMBRES)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<spontaneousanswer>)RESPOSTA\s(ESPONTÁNIA|ESPONTÀNIA)\s(?P<dontread>)NO\sLLEGIR"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True


		regex= r"^(?P<multipleanswer>)RESPOSTA\sM(Ú|U)LTIPLE"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<still>)(encara)?\s?(?P<card>)targeta\s(\d+|\w+)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<continue>)seguir\s(?P<with>)amb\s(?P<the>)la\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<continue>)seguir\s(?P<showing>)MOSTRANT\s(?P<the>)(la)?\s?(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<use>)(Utilitzi)?\s?(?P<this>)aquesta\s(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
			return True

		regex= r"^(?P<ifyouthink>)Si\s(creu|pensa)\sque\s(?P<thispayis>)(la\sseva\sremuneració|els\sseus\singressos|aquests\singressos|aquestes\sdiferències)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<important>)IMPORTANT:\s(?P<interviewer>)Entrevistador(/a)?"
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<interviewer>)ENTREVISTADOR(/A)?:\s(?P<ifrespondent>)Si\sl'entrevistat\s(?P<needadditionalinstructions>)necessita\sinstruccions\saddicionals"
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches:
			return True 
   
		regex= r"^(?P<ask>)FER\s(?P<if>)SI\s(?P<interviewer>)L'ENTREVISTADOR\s(?P<codified>)HA CODIFICAT"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si\sus\splau)?\s?(?P<use>)(utili(tzi|zi|tzeu|zeu)|segueixi\sutilitzant|continu(ï|eu)\sutilitzant)\s(?P<this>)(aquesta)?\s?(?P<the>)(la)?\s?(?P<same>)(mateixa)?\s?(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
			return True

		regex= r"^(?P<please>)(si us plau)?\s?(?P<answer>)respongui\s(?P<using>)utilitzant\s(?P<this>)aquesta\s(?P<same>)(mateixa)?\s?(?P<card>)targeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
			return True
		
		regex= r"^(?P<suggest>)suggerir\s(?P<categories>)categories\s(?P<de>)de\s(?P<answer>)resposta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?(\,)?\s?(?P<choose>)encercli\s(?P<one>)una\s(?P<option>)opció"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(si us plau)?\s?(?P<choose>)encercli\s(?P<option>)l'opció\s(?P<closer>)més propera"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
			return True

		regex= r"(?P<scalefrom>)escala\s(del|de)\s(?P<nton>)\d\s(al|a)\s\d+\s"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'expressi' not in text:
			return True

		regex= r"(?P<scalefrom>)triï\sun\snúmero\sde\s(?P<nton>)\d\sa\s\d+\s(?P<where>)on\s(el)?\s?(?P<nmeans>)\d\sés"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'expressi' not in text:
			return True


		regex= r"(?P<thenmeans>)el\s\d\svol\sdir\s(?P<anything>).*\s(?P<andthenmeans>)i\s(el)?\s?\d+\s(vol\sdir)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'expressi' not in text:
			return True

		regex= r"(?P<thenmeans>)\d\ssignifica\s(que)?\s?(?P<anything>).*\s(?P<andthenmeans>)i\s(el)?\s?\d+\ssignifica\s(que)?\s?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'expressi' not in text:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<choose>)(esculli|elegeixi|Triï)\s(?P<the>)(la)?\s?(?P<your>)(seva)?\s?(?P<answer>)resposta\s(?P<fromthis>)(d'aquesta|en\saquesta)\s(?P<card>)targeta"
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
			return True

		regex= r"(?P<choose>)(esculli|elegeixi|Triï)\s(?P<theoption>)l'opció\s(?P<fromthis>)d'aquesta\s(?P<card>)targeta"
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<choose>)(esculli|elegeixi|Triï)\s(?P<the>)(la)?\s?(?P<your>)(seva)?\s?(?P<answer>)resposta\s(?P<amongoptions>)(entre|d'entre)\sles\sopcions"
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<choose>)(esculli|elegeixi|Triï)\s(?P<your>)(la seva)?\s?(?P<one>)(una|la)?\s?(?P<ofthe>)(de les)?\s?(?P<answer>)(resposta|respostes)\s(?P<thatappearin>)(que apareixen en)?\s?(?P<fromthis>)(aquesta|d'aquesta)\s(?P<card>)targeta"
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
			return True

		regex= r"^(?P<please>)(si us plau)?(,)?\s?(?P<choose>)(esculli|elegeixi|Triï)\s(?P<only>)només\s(?P<one>)una\s(?P<fromthis>)d'aquestes"
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
			return True

		regex= r"^(?P<please>)(si us plau)?\s?(?P<use>)Utilitzi\s(?P<thiscard>)aquesta\s(tarjeta|targeta)\s(?P<toguide>)com\sa\sguia\sper\sa\s(?P<youranswer>)la\sseva\sresposta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
			return True

		regex= r"^(?P<please>)(si us plau)?\s?(?P<note>)(anotar|codificar)\s(?P<only>)només\s(?P<one>)una\s(?P<answer>)resposta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux: 
			return True

		regex= r"^(?P<please>)(si us plau)?(,)\s?(?P<choose>)miri de triar\s(?P<the>)la\s(?P<answer>)resposta\s(?P<fromthis>)d'aquesta\s(?P<card>)targeta"
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux:
			return True

		regex= r"^(?P<dont>)(no)?\s?(?P<read>)llegi(r|u)\s?(?P<out>)(alta)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<noteallnecessarypeople>)Anoti\stotes\sles\spersones\sque\scalgui"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<noteallnecessarypeople>)MARCAR\sTOTES\sLES\sRESPOSTES\sQUE\sDONI"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<forall>)(OMPLIR\sPER\s)?A\sTOTES\sLES\sPERSONES"
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
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches:
			return True

		regex= r"(?P<markorcode>)(marqueu|marcar|codificar)\s(?P<all>)tot(s|es)\s(?P<thepeople>)(les persones)?\s?(?P<theanswers>)(les respostes)?\s?(?P<that>)(el|els)?\s?que\s(?P<apply>)(corresponguin|calgui)"
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

		regex= r"^(?P<insist>)insisti(u|r)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

	elif 'SPA' in country_language:
		regex= r"^(?P<card>)tarjeta\s(?P<numberorletter>)(\d+|\w+)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True


		regex= r"^(?P<continue>)(seguir|siga)\s(con la|mostrando|con)\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<writewith>)ESCRIBIR\sCON\s(?P<details>)DETALLE(s)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<mark>)(CIRCUNDAR|marcar|ANOTAR)\s(?P<all>)(SOLO|TODOS|UNA|BAJO|cinco)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<show>)preguntar:"
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches:
			return True


		regex= r"^(?P<show>)mostrar\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<attentioninterviewer>)ATENCIÓN\sENTREVISTADOR(/A)?:"
		matches = re.search(regex, text_aux, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<answer>)RESPUESTA\s(?P<multiple>)(MÚLTIPLE|MULTIPLE)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<choose>)ELEGIR\s(?P<only>)SOLO\s(?P<one>)UNA"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True
  
		regex= r"^(?P<answer>)RESPUESTA\s(?P<spontaneous>)(ESPONTÁNEA|ESPONTANEA)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<askall>)A\sTODAS\sLAS\sPERSONAS"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<fillforall>)RELLENAR\sPARA\sTODAS\sLAS\sPERSONAS\sENTREVISTADAS"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True


		regex= r"^(?P<if>)si\s(?P<the>)el\s(?P<respondent>)(encuestado|entrevistado)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True
     
		regex= r"^(?P<choose>)Elija\s(?P<an>)una\s(?P<answer>)respuesta\s(?P<fromthe>)de las que aparecen en esta\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux:
			return True

		regex= r"^(?P<please>)(por favor)?\s?(?P<answer>)responda\s(?P<using>)utilizando\s(?P<this>)esta\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<please>)(por favor)?\s?(?P<continueusing>)(siga utilizando|siga usando|use otra vez|use)\s(?P<same>)(la misma)?\s?(?P<this>)(esta)?\s?(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<ifyouthink>)Si\s(cree|piensa)\sque\s(?P<thispayis>)(su\sremuneración|sus\singresos|las\sdiferencias)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<now>)Ahora\s(?P<idlikeyouto>)querría\sque\s(?P<lookatthis>)examinase\sesta\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"^(?P<use>)(utilice|use)\s(?P<again>)(otra vez)?\s?(?P<please>)(por favor)?\s?(?P<theanswers>)las\srespuestas\s(?P<ofthis>)de\sesta\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"^(?P<use>)(utilice|use)\s(?P<again>)(otra vez)?\s?(?P<this>)esta\s(?P<card>)tarjeta(?P<please>)(por favor)?\s?(?P<toindicate>)para\sindicar(lo)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'afirmaciones' not in text_aux:
			return True


		regex= r"^(?P<use>)(utilice|use)\s(?P<toanswer>)para\scontestar"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"^(?P<please>)(por favor)?\s?(?P<use>)(utilice|use)\s(?P<again>)(otra vez)?\s?(?P<this>)(esta)?\s?(?P<thesame>)(la misma)?\s?(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"^(?P<use>)(utilice|use)\s(?P<again>)(otra vez)?\s?(?P<please>)(por favor)?\s?(?P<this>)(esta)?\s?(?P<thesame>)(la misma)?\s?(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"^(?P<please>)(por favor)?\s?(?P<choose>)elija\s(?P<oneofthe>)una de las\s(?P<answers>)respuestas\s(?P<that>)que\s(?P<appearinthis>)aparecen en esta\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"^(?P<suggest>)sugerir\s(?P<categories>)categorías\s(?P<de>)de\s(?P<answer>)respuesta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"(?P<look>)examinase(?P<this>)esta\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"(?P<answers>)respuestas\s(?P<thatshow>)que\saparecen\s(?P<inthis>)en\sesta\s(?P<card>)tarjeta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"^(?P<please>)(por favor)?\s?(?P<choose>)(escoja|elija)\s(?P<youranswer>)(su|una)\srespuesta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"^(?P<choose>)(escoja|elija)\s(?P<please>)(por favor)?\s?(?P<upto>)hasta"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True


		regex= r"^(?P<please>)(por favor)?\s?(?P<mark>)marque\s(?P<one>)una\s(?P<option>)casilla"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"(?P<scalefrom>)escala\sde\s(?P<nton>)\d\sa\s\d+\s(?P<where>)en\sla\sque\s(?P<nmeans>)\d\ssignifica"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"(?P<scalefrom>)número\sde\s(?P<nton>)\d\sa\s\d+\s(?P<where>)donde\s(?P<nmeans>)\d\ses"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"(?P<thenmeans>)\d\s(significa\sque|quiere\sdecir)\s(?P<anything>).*\s(?P<andthenmeans>)(y)?\s?(el)?\s?\d+\s(significa\sque|quiere\sdecir|és|es)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"(?P<thenmeans>)\d\ssignifica\s(?P<anything>).*\s(?P<andthenmeans>)y\s(el)?\s?\d+\s(significa)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"^(?P<note>)nota\s(?P<for>)(per|para)\s(?P<interviewer>)el entrevistador\s?(?P<code>)(codificar)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True


		regex= r"^(?P<please>)(por favor)?\s?(?P<mark>)marque\s(?P<option>)la casilla\s(?P<closer>)que mejor represente\s(?P<youropinion>)su opinión"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<readorcode>)(leer|codificar)\s(?P<each>)cada\s(?P<organization>)organización"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<note>)ANOT(AR|E)\s(?P<with>)CON\s(?P<all>)TODO\s(?P<details>)DETALLE"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True   


		regex= r"^(?P<note>)(ANOT(AR|E))?\s?(?P<onlyone>)(UNA\sSOLA|SÓLO\sUNA|SOLO\sUNA)\s(?P<answer>)RESPUESTA"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<dont>)(no)?\s?(?P<read>)leer\s?(?P<out>)(alto)?"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<read>)leer\s(?P<eachone>)una a una\s(?P<and>)(y)?\s?(?P<note>)anotar"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True

		regex= r"^(?P<read>)(leer|LEA)\s(?P<eachofthe>)CADA\sUNA\sDE\sLAS\s(?P<statements>)AFIRMACIONES"
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

		regex= r"^(?P<please>)(por favor)?\s?(?P<select>)elija\s(?P<onlyone>)sólo\suna"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"^(?P<please>)(por favor)?\s?(?P<select>)elija\s(?P<theoption>)la\sopción"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches and '?' not in text_aux and '...' not in text_aux and ':' not in text_aux and 'para indicar' not in text_aux and 'afirmaciones' not in text_aux:
			return True

		regex= r"^(?P<markorcode>)(Marcar|codificar)\s(?P<all>)tod(a|o)s\s(l(a|o)s)?\s?(RESPUESTAS)?\s?(?P<that>)que\s(se)?\s?(?P<apply>)(corresponda(n)?|MENCIONE(n)?)"
		matches = re.search(regex, text, re.IGNORECASE)
		if matches:
			return True



	return False

		